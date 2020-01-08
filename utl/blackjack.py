import sqlite3, random

DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()

def newGame()
    c.execute("DROP TABLE IF EXISTS currentgame")
    c.execute("CREATE TABLE currentgame ")
