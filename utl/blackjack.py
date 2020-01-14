import sqlite3, random

DB_FILE = "Info.db"

cardvalues = {"ACE":11,"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,"10" : 10, "JACK": 10, "QUEEN": 10, "KING":10}

def newGame():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS userGame;")
    c.execute("""CREATE TABLE userGame(
        cards TEXT,
        score INTEGER
    );""")
    c.execute("DROP TABLE IF EXISTS ourGame;")
    c.execute("""CREATE TABLE ourGame(
        cards TEXT,
        score INTEGER
    );""")
    db.commit()
    c.close()
    return

def wedraw(cardImg,cardVal):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    score = cardvalues[cardVal]
    if (cardVal == "ACE"):
        if (getOurScore() > 21):
            score = 1
    c.execute("INSERT INTO ourGame VALUES(?,?);",(cardImg,score,))
    db.commit()
    c.close()
    return

def userdraw(cardImg,cardVal):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    score = cardvalues[cardVal]
    if (cardVal == "ACE"):
        if (getUserScore() > 21):
            score = 1
    c.execute("INSERT INTO userGame VALUES(?,?);",(cardImg,score,))
    db.commit()
    c.close()
    return

def getUserScore():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT score FROM userGame;")
    data = c.fetchall()
    totalscore = 0
    for score in data:
        totalscore += score[0]
    db.commit()
    c.close()
    return totalscore

def getOurScore():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT score FROM ourGame;")
    data = c.fetchall()
    totalscore = 0
    for score in data:
        totalscore += score[0]
    db.commit()
    c.close()
    return totalscore

def getusercards():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT cards FROM userGame;")
    cards = c.fetchall();
    db.commit()
    c.close()
    return cards

def getourcards():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT cards FROM ourGame;")
    cards = c.fetchall();
    db.commit()
    c.close()
    return cards
