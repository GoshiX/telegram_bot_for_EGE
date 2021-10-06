from sqlite3 import *
import random

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

class ques:
    id = 0
    tasktheme = 0
    condition = ""
    test = ""
    explanation = ""
    ans = []
    def __init__(self):
        pass
cur.execute("""SELECT * FROM tasks""")

tmp_q = cur.fetchmany(10000000)
QUESTION = list()
QUESTION_NUM = len(tmp_q)
THEME_NUM = 26
THEME_QUESTIONS = [[] for i in range(THEME_NUM)]
THEME_QUESTIONS_NUM = []
tp = list()
for i in range(QUESTION_NUM):
    tmp = ques()
    tmp.id = tmp_q[i][0]
    tmp.tasktheme = tmp_q[i][1]
    tmp.condition = tmp_q[i][2]
    tmp.text = tmp_q[i][3]
    tmp.explanation = tmp_q[i][4]
    tmp.ans.clear()
    for j in range(5, 15):
        if (tmp_q[i][j] != "точно_неправильный_ответ"):
            tmp.ans.append(tmp_q[i][j])
    QUESTION.append(tmp)

for i in range(QUESTION_NUM):
    THEME_QUESTIONS[QUESTION[i].tasktheme].append(i)

for i in THEME_QUESTIONS:
    THEME_QUESTIONS_NUM.append(len(i))

def random_condition():
    ret = list()
    num = random.randint(0, QUESTION_NUM - 1)
    ret.append(QUESTION[num].condition)
    if (QUESTION[num].text != ""):
        ret.append("Текст:")
        ret.append(QUESTION[num].text)
    ret.append("---\nВопрос №" + str(QUESTION[num].id))
    return ret

def theme_condition(theme_num):
    ret = list()
    num = random.randint(0, THEME_QUESTIONS_NUM[theme_num] - 1)
    quest = QUESTION[THEME_QUESTIONS[theme_num][num]]
    ret.append(quest.condition)
    if (quest.text != ""):
        ret.append("Текст:")
        ret.append(quest.text)
    ret.append("---\nВопрос №" + str(quest.id))
    return ret