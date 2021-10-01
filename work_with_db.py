from sqlite3 import *
import random

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

cur.execute("""SELECT taskid FROM tasks""")

QUESTION_NUM = len(cur.fetchmany(10000000))

def random_condition():
    num = random.randint(1, QUESTION_NUM)
    sql = "SELECT condition FROM tasks WHERE taskid == '" + str(num) + "'"
    cur.execute(sql)
    return cur.fetchmany(100000)[0][0]