import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="db-postgresql-sustainability-group-do-user-14262231-0.b.db.ondigitalocean.com",
    port=25060,
    database="defaultdb",
    user="doadmin",
    password="AVNS_xJlGYQTQBtMI5V_xcj1",
    sslmode="require"
)

# Execute SQL statements or queries
cur = conn.cursor()

# Query the "Company" table
cur.execute("SELECT * FROM company")
company_rows = cur.fetchall()
print("Company:")
for row in company_rows:
    print(row)

# Query the "csrd" table
cur.execute("SELECT * FROM csrd")
csrd_rows = cur.fetchall()
print("csrd:")
for row in csrd_rows:
    print(row)

# Query the "directives" table
cur.execute("SELECT * FROM directives")
directives_rows = cur.fetchall()
print("directives:")
for row in directives_rows:
    print(row)

# Query the "nfrd" table
cur.execute("SELECT * FROM nfrd")
nfrd_rows = cur.fetchall()
print("nfrd:")
for row in nfrd_rows:
    print(row)

# Query the "sfdr" table
cur.execute("SELECT * FROM sfdr")
sfdr_rows = cur.fetchall()
print("sfdr:")
for row in sfdr_rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()
