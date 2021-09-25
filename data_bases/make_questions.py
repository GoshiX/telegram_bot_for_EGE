import sqlite3
from requests import *
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import sys, threading
import os



class task:
    def __init__(self):
        self.condition = ""
        self.answer = []
        self.explanation = ""
        self.num = 0
        self.theme_num = 0
    def new_ans(self, x):
        self.answer.append(x)
    def make_condition(self, x):
        self.condition = x
    def ret_condition(self):
        return self.condition
    def ret_ans(self):
        return self.answer

#----------соединение с бд-------------
conn = sqlite3.connect('tasks.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
   taskid INT PRIMARY KEY,
   tasktheme INT,
   condition TEXT,
   text TEXT,
   explanation TEXT, 
   ans1 TEXT, 
   ans2 TEXT, 
   ans3 TEXT, 
   ans4 TEXT, 
   ans5 TEXT, 
   ans6 TEXT, 
   ans7 TEXT, 
   ans8 TEXT, 
   ans9 TEXT, 
   ans10 TEXT);
""")
conn.commit()
#-------------------

base = [['https://rus-ege.sdamgia.ru/test?filter=all&category_id=228&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=311&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=281&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=339&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=349&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=213&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=296&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=266&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=254&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=202&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=285&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=203&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=286&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=256&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=337&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=204&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=287&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=257&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=205&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=206&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=333&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=352&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=344&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=348&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=343&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=351&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=346&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=350&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=219&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=302&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=272&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=220&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=303&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=273&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=214&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=297&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=267&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=325&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=307&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=277&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=222&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=305&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=275&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=223&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=306&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=276&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=226&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=309&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=279&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=227&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=310&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=280&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=338&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=229&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=312&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=282&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=230&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=313&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=283&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=231&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=314&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=284&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=252&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=321&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=253&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=255&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=322&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=239&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=331&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=332&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=240&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=323&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=330&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=208&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=291&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=261&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=210&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=293&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=263&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=211&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=294&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=264&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=295&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=265&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=212&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=304&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=221&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=274&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=225&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=308&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=278&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=207&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=241&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=232&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=242&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=243&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=244&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=233&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=245&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=246&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=234&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=247&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=324&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=235&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=319&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=249&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=248&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=236&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=320&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=251&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=250&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=237&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=326&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=345&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=347&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=209&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=292&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=262&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=328&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=288&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=215&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=298&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=268&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=216&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=299&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=269&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=218&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=301&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=271&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=217&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=300&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=270&print=true'], ['https://rus-ege.sdamgia.ru/test?filter=all&category_id=336&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=335&print=true', 'https://rus-ege.sdamgia.ru/test?filter=all&category_id=334&print=true']]

id = 1
for i2 in range(26):
    for j2 in range(len(base[i2])):
        id1 = 1
        r = get(base[i2][j2])
        r.encoding = 'utf8'
        html = BS(r.content, 'html.parser')

        for task in html.select(".prob_maindiv"):
            new_task = task()
            # задание
            task_ti_write = ""
            task_txt = task.select(".pbody")[0]
            find_txt = str(task_txt)
            open_br = 0
            for i in range(len(find_txt)):
                if (find_txt[i] == ">"):
                    open_br = i
                if (find_txt[i] == "<"):
                    if (i != open_br + 1):
                        task_ti_write += find_txt[open_br + 1:i] + "\n"
            # текст
            text_txt = task.find_all("tr")
            if text_txt != []:
                text_txt = text_txt[0].find_all("td")
                text_txt = text_txt[0].find_all("i")
                if (text_txt != []):
                    text_txt = str(text_txt[0].text)
                    text_txt.replace("&lt", "<")
                    text_txt.replace("&gt", ">")
                else:
                    text_txt = ""
            else:
                text_txt = ""
            # ответ
            answer = task.select(".answer")
            raw_ans = answer[0].text
            raw_ans = raw_ans[7:]
            ans_list = raw_ans.split("|")
            print(id, id1)
            print(ans_list)
            for i in range(10):
                ans_list.append("точно_неправильный_ответ")
            new_task.answer = ans_list

            # пояснение
            exp_ti_write = ""
            expl_txt = task.select(".pbody")[1]
            find1_txt = str(expl_txt)
            open_br = 0
            for i in range(len(find1_txt)):
                if (find1_txt[i] == ">"):
                    open_br = i
                if (find1_txt[i] == "<"):
                    if (i != open_br + 1):
                        exp_ti_write += find1_txt[open_br + 1:i] + "\n"
            add_to_base = (id, i2, task_ti_write, text_txt, exp_ti_write, ans_list[0], ans_list[1], ans_list[2], ans_list[3], ans_list[4], ans_list[5], ans_list[6], ans_list[7], ans_list[8], ans_list[9])
            print(add_to_base)
            cur.execute("INSERT INTO tasks VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", add_to_base)
            conn.commit()
            id1 += 1
            id += 1