import sqlite3

conn = sqlite3.connect('users.db')
cur = conn.cursor()
try:
    cur.execute("""INSERT INTO users (user_id) VALUES(1221928197)""")
except sqlite3.IntegrityError:
    pass
conn.commit()
cur.execute("""SELECT * FROM users""")

tmp_q = cur.fetchmany(10000000)
print(tmp_q)