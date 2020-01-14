import sqlite3
import urllib.request as request
import simplejson as json
import random

#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()


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
