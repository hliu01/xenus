import sqlite3
import urllib.request as request
import simplejson as json
import random


def quest(list):
    q = request.urlopen("https://opentdb.com/api.php?amount=10&category=19&type=multiple").read()
    for i in range(10):
        count = json.loads(q)['results'][i]
        ans = [count['correct_answer']]
        list[count['question']] = [*ans,*count['incorrect_answers']]
    return list


def realquest(list):
    q = request.urlopen("https://opentdb.com/api.php?amount=10&category=22&type=multiple").read()
    for i in range(10):
        count = json.loads(q)['results'][i]
        ans = [count['correct_answer']]
        list[count['question']] = [*ans,*count['incorrect_answers']]
    return list

#DATABASE SETUP
DB_FILE = "Info.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("CREATE TABLE USER(username TEXT, password TEXT);")
c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu00","hi"))
c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu01","hi"))
c.execute('CREATE TABLE TRIVIA (questions TEXT, one TEXT, two TEXT, three TEXT, four TEXT)')
c.execute('CREATE TABLE answers (question TEXT, answer TEXT)')
"""Adds questions and choices into the database"""
que = {}
que = quest(que)
for i in range(10):
    ques = list(que)[i]
    c.execute('INSERT INTO answers VALUES (?, ?)', (str(ques), str(que[ques][0])))
    randolist = [0,1,2,3]
    random.shuffle(randolist)
    c.execute('INSERT INTO TRIVIA VALUES (?, ?, ?, ?, ?)', (str(ques), str(que[ques][randolist[0]]), str(que[ques][randolist[1]]), str(que[ques][randolist[2]]), str(que[ques][randolist[3]])))
db.commit()
c.close()
