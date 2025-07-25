import streamlit as st
import pandas as pd 


df = pd.read_csv("user_model_usage.csv")

st.title("User Model Usage Analytics")

if df.empty:
    st.warning("No data found.")
else:
    users = df['user_email'].unique()
    selected_user = st.selectbox("Select User Email", users)
    user_df = df[df['user_email'] == selected_user]

    st.write(f"### Usage for {selected_user}")
    st.dataframe(user_df)

    st.bar_chart(user_df.set_index('model')[['total_spend', 'total_tokens']])