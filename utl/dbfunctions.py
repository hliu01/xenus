import sqlite3

#DATABASE SETUP
DB_FILE = "Info.db"

def setup():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT,
        points INTEGER);""")
    db.commit()
    c.close()
    return

def adduser():
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USER' ''')
    if c.fetchone()[0] < 1:
        c.execute("CREATE TABLE USER(username TEXT, password TEXT);")
    # TESTS
        c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu00","hi"))
        c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu01","hi"))
    db.commit()
    c.close()
    return
