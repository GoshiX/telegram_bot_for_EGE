from sqlite3 import *
import random

conn = connect("data_bases/tasks.db")
cur = conn.cursor()

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

def random_condition():
    ret = list()
    num = random.randint(0, QUESTION_NUM - 1)
    ret.append(QUESTION[num].condition)
    if (QUESTION[num].text != ""):
        ret.append("Текст:")
        ret.append(QUESTION[num].text)
    ret.append("---\nВопрос №" + str(QUESTION[num].id))
    return [ret, [QUESTION[num].ans1, QUESTION[num].ans2, QUESTION[num].ans3, QUESTION[num].ans4, QUESTION[num].ans5, QUESTION[num].ans6, QUESTION[num].ans7, QUESTION[num].ans8, QUESTION[num].ans9, QUESTION[num].ans10], QUESTION[num].explanation]

def theme_condition(theme_num):
    ret = list()
    num = random.randint(0, THEME_QUESTIONS_NUM[theme_num] - 1)
    quest = QUESTION[THEME_QUESTIONS[theme_num][num]]
    ret.append(quest.condition)
    if (quest.text != ""):
        ret.append("Текст:")
        ret.append(quest.text)
    ret.append("---\nВопрос №" + str(quest.id))
    return [ret, [quest.ans1, quest.ans2, quest.ans3, quest.ans4, quest.ans5, quest.ans6, quest.ans7, quest.ans8, quest.ans9, quest.ans10], quest.explanation]