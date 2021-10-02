from sqlite3 import *
import random

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

cur.execute("""SELECT taskid FROM tasks""")

QUESTION_NUM = len(cur.fetchmany(10000000))

def random_condition():
    ret = list()
    num = random.randint(1, QUESTION_NUM)
    sql = "SELECT condition FROM tasks WHERE taskid == '" + str(num) + "'"
    cur.execute(sql)
    ret.append(cur.fetchmany(1)[0][0])
    sql1 = "SELECT text FROM tasks WHERE taskid == '" + str(num) + "'"
    cur.execute(sql1)
    txt = cur.fetchmany(1)[0][0]
    if (txt != ""):
        ret.append(txt)
    return ret