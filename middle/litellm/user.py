import psycopg2

conn = psycopg2.connect(
    dbname="litellm",
    user="llmproxy",
    password="dbpassword9090",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Try both quoted and unquoted table names (Postgres is case-sensitive with quotes)
# if cur.execute('SELECT * FROM "LiteLLM_Users" LIMIT 5;'):
#     cur.execute('SELECT * FROM "LiteLLM_Users" LIMIT 5;')
# else:
print("No table found")
cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
""")

rows = cur.fetchall()
colnames = [desc[0] for desc in cur.description]

print("Sample data from LiteLLM_Users:")
print(colnames)
for row in rows:
    print(row)

cur.close()
conn.close()