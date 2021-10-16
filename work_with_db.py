from sqlite3 import *
import random

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

conn1 = connect("users.db")
cur1 = conn1.cursor()

class ques:
    id = 0
    tasktheme = 0
    condition = ""
    text = ""
    explanation = ""
    ans1, ans2, ans3, ans4, ans5, ans6, ans7, ans8, ans9, ans10 = "$", "$", "$", "$", "$", "$", "$", "$", "$", "$"
cur.execute("""SELECT * FROM tasks""")

tmp_q = cur.fetchmany(10000000)
QUESTION = list()
QUESTION_NUM = len(tmp_q)
THEME_NUM = 26
THEME_QUESTIONS = [[] for i in range(THEME_NUM)]
THEME_QUESTIONS_NUM = []
tp = list()
#rewrite
for i in range(QUESTION_NUM):
    QUESTION.append(ques())
    QUESTION[i].id = tmp_q[i][0]
    QUESTION[i].tasktheme = tmp_q[i][1]
    QUESTION[i].condition = tmp_q[i][2]
    QUESTION[i].text = tmp_q[i][3]
    QUESTION[i].explanation = tmp_q[i][4]
    if (tmp_q[i][5] != "точно_неправильный_ответ"):
        QUESTION[i].ans1 = tmp_q[i][5]
    if (tmp_q[i][6] != "точно_неправильный_ответ"):
        QUESTION[i].ans2 = tmp_q[i][6]
    if (tmp_q[i][7] != "точно_неправильный_ответ"):
        QUESTION[i].ans3 = tmp_q[i][7]
    if (tmp_q[i][8] != "точно_неправильный_ответ"):
        QUESTION[i].ans4 = tmp_q[i][8]
    if (tmp_q[i][9] != "точно_неправильный_ответ"):
        QUESTION[i].ans5 = tmp_q[i][9]
    if (tmp_q[i][10] != "точно_неправильный_ответ"):
        QUESTION[i].ans6 = tmp_q[i][10]
    if (tmp_q[i][11] != "точно_неправильный_ответ"):
        QUESTION[i].ans7 = tmp_q[i][11]
    if (tmp_q[i][12] != "точно_неправильный_ответ"):
        QUESTION[i].ans8 = tmp_q[i][12]
    if (tmp_q[i][13] != "точно_неправильный_ответ"):
        QUESTION[i].ans9 = tmp_q[i][13]
    if (tmp_q[i][14] != "точно_неправильный_ответ"):
        QUESTION[i].ans10 = tmp_q[i][14]

for i in range(QUESTION_NUM):
    THEME_QUESTIONS[QUESTION[i].tasktheme].append(i)

for i in THEME_QUESTIONS:
    THEME_QUESTIONS_NUM.append(len(i))

def text_to_list(text):
    p = 4000
    ret = list()
    while (len(text) > 4000):
        p+=1
        if (text[p] == ' '):
            ret.append(text[0:p])
            text = text[p + 1:]
            p = 4000
    ret.append(text)
    return ret

def random_condition(id):
    ret = list()
    num = random.randint(0, QUESTION_NUM - 1)
    #db
    sql = "UPDATE users SET check_ans = 1, last_question = " + str(num) + " WHERE user_id = " + id
    cur1.execute(sql)
    conn1.commit()

    ret.append(QUESTION[num].condition)
    if (QUESTION[num].text != ""):
        ret.append("Текст:")
        add = text_to_list(QUESTION[num].text)
        for i in add:
            ret.append(i)
    ret.append("---\nВопрос №" + str(QUESTION[num].id))
    return ret

def theme_condition(theme_num, id):
    ret = list()
    num = random.randint(0, THEME_QUESTIONS_NUM[theme_num] - 1)
    quest = QUESTION[THEME_QUESTIONS[theme_num][num]]
    ret.append(quest.condition)
    # db
    sql = "UPDATE users SET check_ans = 1, last_question = " + str(quest.id - 1) + " WHERE user_id = " + id
    cur1.execute(sql)
    conn1.commit()

    if (quest.text != ""):
        ret.append("Текст:")
        add = text_to_list(quest.text)
        for i in add:
            ret.append(i)
    ret.append("---\nВопрос №" + str(quest.id))
    return ret

def get_explain(id):
    sql = "SELECT last_question FROM users WHERE user_id == " + id
    cur1.execute(sql)
    txt = cur1.fetchone()[0]
    return text_to_list(QUESTION[txt].explanation)

def login(id):
    try:
        sql = "INSERT INTO users (user_id) VALUES(" + str(id) + ")"
        cur1.execute(sql)
    except IntegrityError:
        pass
    conn1.commit()

def if_ans(id):
    sql = "SELECT check_ans FROM users WHERE user_id == " + id
    cur1.execute(sql)
    txt = cur1.fetchone()[0]
    return txt

def check_ans(id, ans):
    sql = "UPDATE users SET check_ans = 0 WHERE user_id == " + id
    cur1.execute(sql)
    conn1.commit()
    ans = ans.lower()
    sql = "SELECT last_question FROM users WHERE user_id == " + id
    cur1.execute(sql)
    txt = cur1.fetchone()[0]
    correct = [QUESTION[int(txt)].ans1, QUESTION[int(txt)].ans2, QUESTION[int(txt)].ans3, QUESTION[int(txt)].ans4, QUESTION[int(txt)].ans5, QUESTION[int(txt)].ans6, QUESTION[int(txt)].ans7, QUESTION[int(txt)].ans8, QUESTION[int(txt)].ans9, QUESTION[int(txt)].ans10]
    ret = False
    for i in correct:
        if (ans == i):
            ret = True
    return ret

def give_admin(id):
    sql = "UPDATE "