import sqlite3

with open('./sql/create_table.sql') as f:
    query = f.read()

conn = sqlite3.connect('fib_log.db')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS fib_log")
c.execute(query)
conn.commit()
conn.close()
