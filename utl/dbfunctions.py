import sqlite3
import urllib.request as request
import simplejson as json

#DATABASE SETUP
DB_FILE = "Info.db"


def setup():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USER' ''')
    if c.fetchone()[0] < 1:
        c.execute("CREATE TABLE USER(username TEXT, password TEXT);")
        c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu00","hi"))
        c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu01","hi"))
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='TRIVIA' ''')
    if c.fetchone()[0] < 1:
        addQuestionsToDatabase();
    db.commit()
    c.close()
    return

def userExists(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE username = ?;",(user,))
    m = c.fetchall()
    if (m == []):
        return False
    db.commit()
    c.close()
    return True

def addUser(user, pswd, conf):
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        q = 'SELECT username, password FROM USER;'
        foo = cur.execute(q)
        userList = foo.fetchall()
    for row in userList:
        if user == row[0]:
            flash('Username already taken. Please try again.')
            return False
    if (pswd == conf):
        with sqlite3.connect(DB_FILE) as connection:
            cur = connection.cursor()
            q = "INSERT INTO USER VALUES('{}', '{}');".format(user, pswd) # Successfully registers new user
            cur.execute(q)
            connection.commit()
        return True
    else:
        flash('Passwords do not match. Please try again.')
        return False



def quest(list):
    q = request.urlopen("https://opentdb.com/api.php?amount=10&category=19&type=multiple").read()
    for i in range(10):
        count = json.loads(q)['results'][i]
        ans = [count['correct_answer']]
        list[count['question']] = [*ans,*count['incorrect_answers']]
    return list


def addQuestionsToDatabase():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DROP TABLE IF EXISTS TRIVIA')
    c.execute('CREATE TABLE IF NOT EXISTS TRIVIA (questions TEXT, one TEXT, two TEXT, three TEXT, four TEXT)')
    c.execute('DROP TABLE IF EXISTS answers')
    c.execute('CREATE TABLE IF NOT EXISTS answers (answer TEXT)')
    """Adds questions and choices into the database"""
    que = {}
    que = quest(que)
    for i in range(10):
        ques = list(que)[i]
        c.execute('INSERT INTO TRIVIA VALUES (?, ?, ?, ?, ?)', (str(ques), str(que[ques][0]), str(que[ques][1]), str(que[ques][2]), str(que[ques][3])))
    db.commit()
    db.close()
