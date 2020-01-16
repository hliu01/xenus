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


#DATABASE SETUP
DB_FILE = "Info.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS USER(username TEXT, password TEXT);")
c.execute('DROP TABLE IF EXISTS TRIVIA;')
c.execute('CREATE TABLE IF NOT EXISTS TRIVIA (questions TEXT, one TEXT, two TEXT, three TEXT, four TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS answers (question TEXT, answer TEXT);')
c.execute('SELECT * FROM TRIVIA;')
exists = c.fetchall()
if (exists == []):
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
