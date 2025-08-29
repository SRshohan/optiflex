import psycopg2
import pandas as pd
import csv  


def get_user_model_usage():
    """
    Get the user model usage from the database.
    """
    conn = psycopg2.connect(
        dbname="litellm",
        user="llmproxy",
        password="dbpassword9090",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT
            u.user_email,
            s.model,
            SUM(s.spend) AS total_spend,
            SUM(s.prompt_tokens) AS total_prompt_tokens,
            SUM(s.completion_tokens) AS total_completion_tokens,
            SUM(s.total_tokens) AS total_tokens
        FROM "LiteLLM_SpendLogs" s
        JOIN "LiteLLM_UserTable" u ON s."user" = u.user_id
        WHERE s."user" IS NOT NULL AND s."user" != ''
        GROUP BY u.user_email, s.model
        ORDER BY u.user_email, total_spend DESC;
    """)

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    with open("user_model_usage.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
  
    cur.close()
    conn.close()
    return 


if __name__ == "__main__":
    get_user_model_usage()
    



