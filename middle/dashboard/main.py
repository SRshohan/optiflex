import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

HOST_NAME = os.getenv("HOST_NAME", "localhost")

# Page config
st.set_page_config(
    page_title="LiteLLM Usage Dashboard",
    page_icon="",
    layout="wide"
)

# Load users from JSON file
def load_users():
    try:
        with open('./user.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Simple authentication
def check_auth(email, password):
    users = load_users()
    return email in users and users[email]["password"] == password

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="litellm",
        user="llmproxy", 
        password="dbpassword9090",
        host=HOST_NAME,
        port=5432
    )

# Get budget information for users
def get_user_budget_info():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get budget table info with model_max_budget
        cur.execute("""
            SELECT 
                budget_id,
                max_budget,
                soft_budget,
                budget_duration,
                model_max_budget,
                created_at
            FROM "LiteLLM_BudgetTable"
            ORDER BY created_at DESC
        """)
        budgets = cur.fetchall()
        
        # Get user usage from SpendLogs
        cur.execute("""
            SELECT 
                u.user_email,
                s.model,
                SUM(s.spend) as total_spend,
                COUNT(*) as request_count,
                MAX(s."startTime") as last_request
            FROM "LiteLLM_SpendLogs" s
            JOIN "LiteLLM_UserTable" u ON s."user" = u.user_id
            WHERE s."user" IS NOT NULL AND s."user" != ''
            GROUP BY u.user_email, s.model
            ORDER BY u.user_email, total_spend DESC
        """)
        user_usage = cur.fetchall()
        
        # Get recent spend data for budget tracking
        cur.execute("""
            SELECT 
                u.user_email,
                s.model,
                s.spend,
                s."startTime",
                s."status"
            FROM "LiteLLM_SpendLogs" s
            JOIN "LiteLLM_UserTable" u ON s."user" = u.user_id
            WHERE s."user" IS NOT NULL AND s."user" != ''
            ORDER BY s."startTime" DESC
            LIMIT 100
        """)
        recent_spend = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return budgets, user_usage, recent_spend
        
    except Exception as e:
        st.error(f"Error getting budget info: {e}")
        return [], [], []

# Calculate budget alerts for users with model-specific budgets
def calculate_budget_alerts(budgets, user_usage, recent_spend):
    alerts = []
    
    if not budgets:
        return alerts  # No budgets configured
    
    # Process each budget
    for budget in budgets:
        budget_id, max_budget, soft_budget, duration, model_max_budget, created = budget
        
        # Handle NULL values
        max_budget = max_budget if max_budget is not None else 0
        soft_budget = soft_budget if soft_budget is not None else 0
        
        # Parse model_max_budget (it's stored as JSON)
        model_budgets = {}
        if model_max_budget:
            try:
                if isinstance(model_max_budget, str):
                    import json
                    model_budgets = json.loads(model_max_budget)
                else:
                    model_budgets = model_max_budget
            except:
                model_budgets = {}
        
        # Check each user's usage against both global and model-specific budgets
        for usage in user_usage:
            user_email, model, total_spend, request_count, last_request = usage
            
            # Handle NULL values in usage
            total_spend = total_spend if total_spend is not None else 0
            request_count = request_count if request_count is not None else 0
            
            # Check global budget
            global_alert_level = "none"
            global_percentage = 0
            
            if max_budget > 0:
                global_percentage = (total_spend / max_budget) * 100
                if total_spend >= max_budget:
                    global_alert_level = "exceeded"
                elif soft_budget > 0 and total_spend >= soft_budget:
                    global_alert_level = "warning"
                elif global_percentage >= 80:
                    global_alert_level = "high"
                elif global_percentage >= 60:
                    global_alert_level = "medium"
            
            # Check model-specific budget
            model_alert_level = "none"
            model_percentage = 0
            model_max = 0
            model_soft = 0
            
            if model in model_budgets:
                model_config = model_budgets[model]
                model_max = model_config.get('max_budget', 0)
                model_soft = model_config.get('soft_budget', 0)
                
                if model_max > 0:
                    model_percentage = (total_spend / model_max) * 100
                    if total_spend >= model_max:
                        model_alert_level = "exceeded"
                    elif model_soft > 0 and total_spend >= model_soft:
                        model_alert_level = "warning"
                    elif model_percentage >= 80:
                        model_alert_level = "high"
                    elif model_percentage >= 60:
                        model_alert_level = "medium"
            
            # Use the higher alert level (model-specific takes precedence)
            final_alert_level = model_alert_level if model_alert_level != "none" else global_alert_level
            final_percentage = model_percentage if model_alert_level != "none" else global_percentage
            final_max_budget = model_max if model_alert_level != "none" else max_budget
            final_soft_budget = model_soft if model_alert_level != "none" else soft_budget
            
            if final_alert_level != "none":
                alerts.append({
                    'user_email': user_email,
                    'model': model,
                    'total_spend': total_spend,
                    'max_budget': final_max_budget,
                    'soft_budget': final_soft_budget,
                    'percentage_used': final_percentage,
                    'alert_level': final_alert_level,
                    'request_count': request_count,
                    'last_request': last_request,
                    'budget_id': budget_id,
                    'is_model_specific': model_alert_level != "none",
                    'global_percentage': global_percentage,
                    'model_percentage': model_percentage
                })
    
    return alerts

# Display budget alerts
def show_budget_alerts(alerts):
    if not alerts:
        st.success("✅ All users are within budget limits")
        return
    
    st.subheader("🚨 Budget Alerts")
    
    # Group alerts by level
    exceeded = [a for a in alerts if a['alert_level'] == 'exceeded']
    warnings = [a for a in alerts if a['alert_level'] == 'warning']
    high = [a for a in alerts if a['alert_level'] == 'high']
    medium = [a for a in alerts if a['alert_level'] == 'medium']
    
    # Show exceeded budgets first
    if exceeded:
        st.error(" BUDGET EXCEEDED")
        for alert in exceeded:
            budget_type = "Model-Specific" if alert['is_model_specific'] else "Global"
            with st.expander(f"❌ {alert['user_email']} - {alert['model']} (${alert['total_spend']:.2f}/{alert['max_budget']:.2f}) - {budget_type}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spent", f"${alert['total_spend']:.2f}")
                    st.metric("Budget", f"${alert['max_budget']:.2f}")
                    st.metric("Budget Type", budget_type)
                with col2:
                    st.metric("Requests", alert['request_count'])
                    st.metric("Last Request", alert['last_request'].strftime('%Y-%m-%d %H:%M') if alert['last_request'] else 'N/A')
                    st.metric("Usage %", f"{alert['percentage_used']:.1f}%")
                
                # Progress bar showing overage
                overage = alert['total_spend'] - alert['max_budget']
                st.progress(1.0)
                st.error(f"💰 ${overage:.2f} OVER BUDGET")
                
                # Show both global and model percentages if applicable
                if alert['is_model_specific'] and alert['global_percentage'] > 0:
                    st.info(f"Global budget usage: {alert['global_percentage']:.1f}%")
    
    # Show warning budgets
    if warnings:
        st.warning("⚠️ SOFT BUDGET WARNING")
        for alert in warnings:
            budget_type = "Model-Specific" if alert['is_model_specific'] else "Global"
            with st.expander(f"⚠️ {alert['user_email']} - {alert['model']} (${alert['total_spend']:.2f}/{alert['max_budget']:.2f}) - {budget_type}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spent", f"${alert['total_spend']:.2f}")
                    st.metric("Soft Limit", f"${alert['soft_budget']:.2f}")
                    st.metric("Budget Type", budget_type)
                with col2:
                    st.metric("Remaining", f"${alert['max_budget'] - alert['total_spend']:.2f}")
                    st.metric("Usage %", f"{alert['percentage_used']:.1f}%")
                
                # Progress bar
                progress = min(alert['total_spend'] / alert['max_budget'], 1.0)
                st.progress(progress)
    
    # Show high usage
    if high:
        st.info("📈 HIGH USAGE (80%+)")
        for alert in high:
            budget_type = "Model-Specific" if alert['is_model_specific'] else "Global"
            with st.expander(f" {alert['user_email']} - {alert['model']} ({alert['percentage_used']:.1f}%) - {budget_type}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spent", f"${alert['total_spend']:.2f}")
                    st.metric("Remaining", f"${alert['max_budget'] - alert['total_spend']:.2f}")
                    st.metric("Budget Type", budget_type)
                with col2:
                    st.metric("Usage %", f"{alert['percentage_used']:.1f}%")
                    st.metric("Requests", alert['request_count'])
                
                # Progress bar
                progress = alert['total_spend'] / alert['max_budget']
                st.progress(progress)
    
    # Show medium usage
    if medium:
        st.info("📊 MEDIUM USAGE (60%+)")
        for alert in medium:
            budget_type = "Model-Specific" if alert['is_model_specific'] else "Global"
            with st.expander(f" {alert['user_email']} - {alert['model']} ({alert['percentage_used']:.1f}%) - {budget_type}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spent", f"${alert['total_spend']:.2f}")
                    st.metric("Remaining", f"${alert['max_budget'] - alert['total_spend']:.2f}")
                    st.metric("Budget Type", budget_type)
                with col2:
                    st.metric("Usage %", f"{alert['percentage_used']:.1f}%")
                    st.metric("Requests", alert['request_count'])
                
                # Progress bar
                progress = alert['total_spend'] / alert['max_budget']
                st.progress(progress)

# Show budget configuration
def show_budget_config(budgets):
    if not budgets:
        st.info("💰 No budgets configured yet")
        st.write("To set up budgets, use the LiteLLM API or admin interface")
        return
    
    st.subheader("💰 Budget Configuration")
    
    for budget in budgets:
        budget_id, max_budget, soft_budget, duration, model_max_budget, created = budget
        
        # Handle NULL values
        max_budget = max_budget if max_budget is not None else 0
        soft_budget = soft_budget if soft_budget is not None else 0
        
        # Parse model_max_budget
        model_budgets = {}
        if model_max_budget:
            try:
                if isinstance(model_max_budget, str):
                    import json
                    model_budgets = json.loads(model_max_budget)
                else:
                    model_budgets = model_max_budget
            except:
                model_budgets = {}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Budget ID", budget_id)
            st.metric("Global Max Budget", f"${max_budget:.2f}" if max_budget else "Not set")
        
        with col2:
            st.metric("Global Soft Budget", f"${soft_budget:.2f}" if soft_budget else "Not set")
            st.metric("Duration", duration if duration else "Not set")
        
        with col3:
            st.metric("Created", created.strftime('%Y-%m-%d') if created else "Unknown")
            st.metric("Model Budgets", len(model_budgets))
        
        # Show model-specific budgets
        if model_budgets:
            st.subheader("🤖 Model-Specific Budgets")
            for model, config in model_budgets.items():
                model_max = config.get('max_budget', 0)
                model_soft = config.get('soft_budget', 0)
                model_duration = config.get('budget_duration', 'Not set')
                tpm_limit = config.get('tpm_limit', 'Not set')
                rpm_limit = config.get('rpm_limit', 'Not set')
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{model}**")
                    st.write(f"Max: ${model_max:.2f}")
                with col2:
                    st.write(f"Soft: ${model_soft:.2f}")
                with col3:
                    st.write(f"Duration: {model_duration}")
                with col4:
                    st.write(f"TPM: {tpm_limit}")
                    st.write(f"RPM: {rpm_limit}")

# Sign-in page
def login():
    st.title("🔐 LiteLLM Dashboard")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")
            
            if submit:
                if check_auth(email, password):
                    st.session_state.logged_in = True
                    st.session_state.user = email
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# Main dashboard
def dashboard():
    # Header with logout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📊 LiteLLM Usage Dashboard")
    
    with col2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown("---")
    
    # Auto-refresh
    refresh = st.sidebar.selectbox("Auto-refresh", ["Off", "30s", "1m", "5m"], index=1)
    
    if refresh != "Off":
        refresh_map = {"30s": 30, "1m": 60, "5m": 300}
        st.sidebar.info(f"Refreshing every {refresh}")
        st.markdown(f"""
        <script>
            setTimeout(function(){{
                window.location.reload();
            }}, {refresh_map[refresh] * 1000});
        </script>
        """, unsafe_allow_html=True)
    
    try:
        # Get budget information
        budgets, user_usage, recent_spend = get_user_budget_info()
        
        # Show budget configuration
        show_budget_config(budgets)
        
        # Calculate alerts
        alerts = calculate_budget_alerts(budgets, user_usage, recent_spend)
        
        # Show budget alerts
        show_budget_alerts(alerts)
        
        st.markdown("---")
        
        conn = get_db_connection()
        
        # Get users and models for filters
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT u.user_email 
            FROM "LiteLLM_UserTable" u
            JOIN "LiteLLM_SpendLogs" s ON u.user_id = s."user"
            WHERE s."user" IS NOT NULL AND s."user" != ''
            ORDER BY u.user_email
        """)
        all_users = [row[0] for row in cur.fetchall()]
        
        cur.execute("""
            SELECT DISTINCT model 
            FROM "LiteLLM_SpendLogs"
            WHERE model IS NOT NULL AND model != ''
            ORDER BY model
        """)
        all_models = [row[0] for row in cur.fetchall()]
        
        # Filters
        st.sidebar.subheader("Filters")
        
        selected_users = st.sidebar.multiselect("Users", all_users)
        selected_models = st.sidebar.multiselect("Models", all_models)
        
        date_filter = st.sidebar.selectbox("Date Range", ["All Time", "24h", "7d", "30d"])
        
        # Build query
        where_conditions = ['s."user" IS NOT NULL AND s."user" != \'\'']
        
        if selected_users:
            user_placeholders = ','.join(['%s'] * len(selected_users))
            where_conditions.append(f'u.user_email IN ({user_placeholders})')
        
        if selected_models:
            model_placeholders = ','.join(['%s'] * len(selected_models))
            where_conditions.append(f's.model IN ({model_placeholders})')
        
        if date_filter == "24h":
            where_conditions.append('s."startTime" >= NOW() - INTERVAL \'24 hours\'')
        elif date_filter == "7d":
            where_conditions.append('s."startTime" >= NOW() - INTERVAL \'7 days\'')
        elif date_filter == "30d":
            where_conditions.append('s."startTime" >= NOW() - INTERVAL \'30 days\'')
        
        where_clause = ' AND '.join(where_conditions)
        
        # Get data
        query = f"""
        SELECT
            u.user_email,
            s.model,
            SUM(s.spend) AS total_spend,
            SUM(s.prompt_tokens) AS total_prompt_tokens,
            SUM(s.completion_tokens) AS total_completion_tokens,
            SUM(s.total_tokens) AS total_tokens,
            COUNT(*) as request_count
        FROM "LiteLLM_SpendLogs" s
        JOIN "LiteLLM_UserTable" u ON s."user" = u.user_id
        WHERE {where_clause}
        GROUP BY u.user_email, s.model
        ORDER BY total_spend DESC;
        """
        
        if selected_users and selected_models:
            cur.execute(query, selected_users + selected_models)
        elif selected_users:
            cur.execute(query, selected_users)
        elif selected_models:
            cur.execute(query, selected_models)
        else:
            cur.execute(query)
        
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df_usage = pd.DataFrame(rows, columns=columns)
        
        # Recent activity
        recent_query = f"""
        SELECT 
            u.user_email,
            s."completion_tokens", 
            s."model", 
            s."spend", 
            s."startTime"
        FROM "LiteLLM_SpendLogs" s
        JOIN "LiteLLM_UserTable" u ON s."user" = u.user_id
        WHERE s."status" = 'success' AND {where_clause}
        ORDER BY s."startTime" DESC
        LIMIT 50;
        """
        
        if selected_users and selected_models:
            cur.execute(recent_query, selected_users + selected_models)
        elif selected_users:
            cur.execute(recent_query, selected_users)
        elif selected_models:
            cur.execute(recent_query, selected_models)
        else:
            cur.execute(recent_query)
        
        recent_rows = cur.fetchall()
        recent_columns = [desc[0] for desc in cur.description]
        df_recent = pd.DataFrame(recent_rows, columns=recent_columns)
        
        cur.close()
        conn.close()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Users", len(df_usage['user_email'].unique()) if not df_usage.empty else 0)
        
        with col2:
            st.metric("Models", len(df_usage['model'].unique()) if not df_usage.empty else 0)
        
        with col3:
            total_spend = df_usage['total_spend'].sum() if not df_usage.empty else 0
            st.metric("Total Spend", f"${total_spend:.2f}")
        
        with col4:
            total_requests = df_usage['request_count'].sum() if not df_usage.empty else 0
            st.metric("Requests", total_requests)
        
        # Charts
        if not df_usage.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Spend by Model")
                fig_spend = px.pie(df_usage, values='total_spend', names='model')
                st.plotly_chart(fig_spend, use_container_width=True)
            
            with col2:
                st.subheader("Requests by Model")
                fig_requests = px.bar(df_usage, x='model', y='request_count')
                st.plotly_chart(fig_requests, use_container_width=True)
            
            # Tables
            st.subheader("Usage Summary")
            st.dataframe(df_usage, use_container_width=True)
            
            st.subheader("Recent Activity")
            st.dataframe(df_recent, use_container_width=True)
        else:
            st.info("No data found")
        
    except Exception as e:
        st.error(f"Database error: {e}")

# Main app
def main():
    if not st.session_state.get('logged_in', False):
        login()
    else:
        dashboard()

if __name__ == "__main__":
    main()