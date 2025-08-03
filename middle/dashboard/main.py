import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="LiteLLM Usage Dashboard",
    page_icon="",
    layout="wide"
)

# Load users from JSON file
def load_users():
    try:
        with open('user.json', 'r') as f:
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
        host="db",
        port=5432
    )

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