import sqlite3

with open('./sql/create_table.sql') as f:
    query = f.read()

conn = sqlite3.connect('fib_log.db')
c = conn.cursor()
c.execute(query)
c.execute("DELETE FROM fib_log")
conn.commit()
conn.close()
