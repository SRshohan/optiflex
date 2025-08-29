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
try:
    cur.execute('SELECT * FROM "LiteLLM_VerificationToken" LIMIT 5;')
except psycopg2.errors.UndefinedTable:
    cur.execute('SELECT * FROM last30dmodelsbyspend LIMIT 5;')

rows = cur.fetchall()
colnames = [desc[0] for desc in cur.description]

print("Sample data from Last30dModelsBySpend:")
print(colnames)
for row in rows:
    print(row)

cur.close()
conn.close()