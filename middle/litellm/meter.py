import psycopg2
import csv

conn = psycopg2.connect(
    dbname="litellm",
    user="llmproxy",
    password="dbpassword9090",
    host="localhost",
    port=5432
)
cur = conn.cursor()

cur.execute("""
    SELECT "user", "end_user", "completion_tokens", "model", "spend"
    FROM "LiteLLM_SpendLogs"
    WHERE "status" = 'success'
    ORDER BY "startTime" DESC
    LIMIT 100;
""")

rows = cur.fetchall()
header = [desc[0] for desc in cur.description]

with open("successful_usage.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print("Exported to successful_usage.csv")

cur.close()
conn.close()