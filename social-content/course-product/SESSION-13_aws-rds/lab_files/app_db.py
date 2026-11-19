import os
import psycopg2

conn = psycopg2.connect(host=os.environ["DB_HOST"], dbname="postgres", user="atithi_admin",
                        password=os.environ["DB_PASSWORD"], connect_timeout=5)
cur = conn.cursor()

# the right way: the driver passes the value separately (%s), it is never glued into the SQL text
cur.execute("INSERT INTO guests(name) VALUES (%s) RETURNING id", ("Meera",))
print("inserted guest id", cur.fetchone()[0])

name = "x' OR '1'='1"                        # what a hostile guest might type into a form
cur.execute("SELECT count(*) FROM guests WHERE name = %s", (name,))
print("safe query, hostile text matches:", cur.fetchone()[0], "guests")

bad = "SELECT count(*) FROM guests WHERE name = '" + name + "'"     # the wrong way: text glued in
cur.execute(bad)
print("glued query:", bad)
print("glued query matches:", cur.fetchone()[0], "guests (all of them)")
conn.commit()
conn.close()
