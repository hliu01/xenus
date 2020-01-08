import sqlite3

#DATABASE SETUP
DB_FILE = "Info.db"

def setup():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        username text,
        password text,
        points Integer);""")
    db.commit()
    c.close()
    return

def userExists(user):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print("username")
    c.execute("SELECT username FROM users WHERE username = ?;",(user,))
    m = c.fetchall()
    if (m == []):
        return False
    db.commit()
    c.close()
    return True

def adduser(user,pswd):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES (?,?,0);",(user,pswd,))
    db.commit()
    c.close()
    return
