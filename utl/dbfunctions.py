#DATABASE SETUP
DB_FILE = "Info.db"

def setup():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(
        text username,
        text password,

        integer points,
    )
#Creates USER
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USER' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE USER(username TEXT, password TEXT);")
    # TESTS
    c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu00","hi"))
    c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu01","hi"))


#Creates
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='STORIES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE STORIES(storyid INTEGER, title TEXT, text BLOB);")
    # TESTS
    c.execute("INSERT INTO STORIES VALUES ('{}', '{}', '{}')".format(0, "DD", "0dswdwdw"))
    c.execute("INSERT INTO STORIES VALUES ('{}', '{}', '{}')".format(1, "DD", "1dswdwdw"))
    db.commit()
    db.close()
