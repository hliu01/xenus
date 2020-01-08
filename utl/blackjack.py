import sqlite3, random

DB_FILE = "Info.db"

cardvalues = {"ACE":1,"2": 2, "3": 3, "4": 4, "5", 5, "6": 6, "7": 7, "8": 8, "9": 9, "JACK": 10, "QUEEN": 10, "KING":10}

def newGame():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS userGame")
    c.execute("""CREATE TABLE currentgame(
        text cards,
        Integer score,
    )""")
    c.execute("DROP TABLE IF EXISTS ourGame")
    c.execute("""CREATE TABLE currentgame(
        text cards,
        Integer score,
    )""")
    db.commit()
    c.close()
    return

def wedraw(cardImg,cardVal):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    score = cardvalues[cardVal]
    if (cardVal == "ACE"):
        if (getOurScore()) > 11):
            score = 1
    c.execute("INSERT INTO ourGame VALUES(?,?);",(cardImg,score))
    db.commit()
    c.close()
    return

def userdraw(cardImg,score):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    score = cardvalues[cardVal]
    if (cardVal == "ACE"):
        if (getUserScore()) > 11):
            score = 1
    c.execute("INSERT INTO userGame VALUES(?,?);",(cardImg,score))
    db.commit()
    c.close()
    return

def getUserScore():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT score FROM userGame VALUES")
    data = c.fetchall()
    int totalscore;
    for (score in data):
        totalscore += score[0];
    return totalscore

def getOurScore():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT score FROM ourGame VALUES")
    data = c.fetchall()
    int totalscore;
    for (score in data):
        totalscore += score[0];
    return totalscore

def replaceAce():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
