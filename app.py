# xenus
# SoftDev1 PD 9
# Escape the World
# 1/13/2020

from flask import Flask, render_template, request, session, redirect, url_for, redirect
import sqlite3, random
import os
from flask import flash
import urllib.request
import json as simplejson
from os import urandom
import utl.dbfunctions as dbfunctions
import utl.blackjack as blackjack
import urllib.request as urlrequest
import random
import time
app = Flask(__name__)
app.secret_key = urandom(32)

#-----------------------------------------------------------------

#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor() #facilitate db operations
dbfunctions.setup()
db.commit()
db.close()
#-----------------------------------------------------------------

# DICTIONARY FOR IMPORTANT SEARCH DATA
searchdict = {}

@app.route("/")
def root():
    return render_template("play.html", sessionstatus = "user" in session)

@app.route("/level1")
def level1():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("level1.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)

@app.route("/level2")
def level2():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("level2.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)


@app.route("/level3")
def level3():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("level3.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)


@app.route("/login")
def login():
    # if user already logged in, redirects back to discover
    if 'user' in session:
        return redirect(url_for('root'))
    # checking to see if things were submitted
    if (request.args):
        if (bool(request.args["username"]) and bool(request.args["password"])):
            # setting request.args to variables to make life easier
            inpUser = request.args["username"]
            inpPass = request.args["password"]
            with sqlite3.connect(DB_FILE) as connection:
                cur = connection.cursor()
                q = 'SELECT username, password FROM USER;'
                foo = cur.execute(q)
                userList = foo.fetchall()
                for row in userList:
                    if inpUser == row[0] and inpPass == row[1]:
                        session['user'] = inpUser
                        return(redirect(url_for("root")))
                flash('Username not found or login credentials incorrect.')
                return(redirect(url_for("login")))
        else:
            flash('Login unsuccessful')
            return(redirect(url_for("login")))
    return render_template("login.html")

@app.route("/register")
def register():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('root'))

  # checking to see if things were submitted
  if (request.args):
    if (bool(request.args["username"]) and bool(request.args["password"])):
      # setting request.args to variables to make life easier
      inpUser = request.args["username"]
      inpPass = request.args["password"]
      inpConf = request.args["confirmPass"]

      if(addUser(inpUser, inpPass, inpConf)):
        flash('Success! Please login.')
        return redirect(url_for("login"))
      else:
        return(redirect(url_for("register")))
    else:
      flash('Please make sure to fill all fields!')
  return render_template("register.html")


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop('user')
    return redirect(url_for("root"))

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

@app.route("/play")
def play():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("play.html",
    title = "Play - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)

@app.route("/indexxx")
def index():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("indexxx.html",
    title = "Play - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)


# Dispalys user's personal blog page and loads HTML with blog writing form
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("profile.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)

#https://gist.github.com/straker/ff00b4b49669ad3dec890306d348adc4
@app.route("/snake")
def snake():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("snake.html", heading = session["user"],sessionstatus = "user" in session)

@app.route("/blackjack")
def startBlackJack():
    if "user" not in session:
        return redirect(url_for('root'))
    if 'blackjackwins' not in session:
        session['blackjackwins'] = 0
    blackjack.newGame()
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
    req = urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    req = urlrequest.urlopen(req)
    res = req.read()
    deck = simplejson.loads(res)
    session['deckid'] = deck["deck_id"]
    shuffle()
    users = blackjack.getusercards()
    ours =  blackjack.getourcards()
    return render_template('blackjack.html',gameOver = False,gameStarted = False)

def shuffle():
    if "user" not in session:
        return redirect(url_for('root'))
    if not ('deckid' in session):
        return url_for('startBlackJack')
    url = "https://deckofcardsapi.com/api/deck/" + session['deckid'] + "/shuffle/?deck_count=6"
    req = urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    req = urlrequest.urlopen(req)
    res = req.read()
    deck = simplejson.loads(res)
    return True

@app.route("/draw")
def drawCard():
    if "user" not in session:
        return redirect(url_for('root'))
    if not ('deckid' in session):
        return redirect(url_for('startBlackJack'))
    url = "https://deckofcardsapi.com/api/deck/" + session['deckid'] +"/draw/?count=1"
    req = urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    req = urlrequest.urlopen(req)
    res = req.read()
    card = simplejson.loads(res)['cards'][0]
    print(card)
    blackjack.userdraw(card['image'],card['value'])
    return redirect(url_for('playBlackJack'))

def housedrawCard():
    if "user" not in session:
        return redirect(url_for('root'))
    if not ('deckid' in session):
        return redirect(url_for('startBlackJack'))
    url = "https://deckofcardsapi.com/api/deck/" + session['deckid'] +"/draw/?count=1"
    req = urlrequest.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    req = urlrequest.urlopen(req)
    res = req.read()
    card = simplejson.loads(res)['cards'][0]
    print(card)
    blackjack.wedraw(card['image'],card['value'])
    return

@app.route("/playblackjack")
def playBlackJack():
    if "user" not in session:
        return redirect(url_for('root'))
    users = blackjack.getusercards()
    ours =  blackjack.getourcards()
    uscore = blackjack.getUserScore()
    oscore = "?"
    if (ours == []):
        housedrawCard()
        housedrawCard()
        ours =  blackjack.getourcards()
    if (uscore > 21):
        uscore = blackjack.getUserScore()
        oscore = blackjack.getOurScore()
        session.pop('deckid')
        return render_template('blackjack.html',gameOver = True, userWin = False,ourcards=ours,ourscore = oscore,usercards = users,yourscore =uscore)
    print(users)
    print(ours)
    return render_template('blackjack.html',gameOver = False ,gameStarted =True,userMove = True,ourcards = ours,ourscore = oscore,usercards = users,userscore =uscore)

@app.route("/houseblackjack")
def houseBlackJack():
    if "user" not in session:
        return redirect(url_for('root'))
    users = blackjack.getusercards()
    ours =  blackjack.getourcards()
    uscore = blackjack.getUserScore()
    oscore = blackjack.getOurScore()
    if (oscore > 21):
        uscore = blackjack.getUserScore()
        oscore = blackjack.getOurScore()
        session.pop('deckid')
        if 'blackjackwins' in session
            session['blackjackwins'] = session['blackjackwins'] + 1
        return render_template('blackjack.html',gameOver = True, userWin = True,ourcards=ours,ourscore = oscore,usercards = users,yourscore =uscore)
    if (oscore > uscore):
        uscore = blackjack.getUserScore()
        oscore = blackjack.getOurScore()
        session.pop('deckid')
        return render_template('blackjack.html',gameOver = True, userWin = False,ourcards=ours,ourscore = oscore,usercards = users,yourscore =uscore)
    if (uscore >= oscore):
        housedrawCard()
        ours =  blackjack.getourcards()
        oscore = blackjack.getOurScore()
    return render_template('blackjack.html',gameOver = False ,gameStarted =True,userMove = False,ourcards = ours,ourscore = oscore,usercards = users,userscore = uscore)

@app.route("/typeracer")
def typeracer():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("typeracer.html", heading = session["user"],sessionstatus = "user" in session)

@app.route('/checktyperacer', methods=['POST'])
def checktyperacer():
    if "user" not in session:
        return redirect(url_for('root'))
    comment = request.form['comment']
    if comment == "I need a landing sight":
        return render_template("checktyperacer.html", heading = session["user"],sessionstatus = "user" in session)
    else:
        return render_template("typeracer.html", heading = session["user"],sessionstatus = "user" in session)

@app.route("/typeracer2")
def typeracer2():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("typeracer2.html", heading = session["user"],sessionstatus = "user" in session)

@app.route('/checktyperacer2', methods=['POST'])
def checktyperacer2():
    if "user" not in session:
        return redirect(url_for('root'))
    comment = request.form['comment']
    if comment == "I am here":
        return render_template("checktyperacer2.html", heading = session["user"],sessionstatus = "user" in session)
    else:
        return render_template("typeracer2.html", heading = session["user"],sessionstatus = "user" in session)

@app.route('/playclo')
def playclo():
    dice = ["http://roll.diceapi.com/images/poorly-drawn/d6/1.png","http://roll.diceapi.com/images/poorly-drawn/d6/2.png","http://roll.diceapi.com/images/poorly-drawn/d6/3.png","http://roll.diceapi.com/images/poorly-drawn/d6/4.png","http://roll.diceapi.com/images/poorly-drawn/d6/5.png","http://roll.diceapi.com/images/poorly-drawn/d6/6.png"]
    ourroll = rolldice()
    while ((ourroll[0] != ourroll[1]) and (ourroll[1] != ourroll[2]) and (ourroll[0] != ourroll[2])):
        ourroll = rolldice()
    ourdie1 = dice[ourroll[0]-1]
    ourdie2 = dice[ourroll[1]-1]
    ourdie3 = dice[ourroll[2]-1]
    session['ourdie1'] = ourdie1
    session['ourdie2'] = ourdie2
    session['ourdie3'] = ourdie3
    yourroll = rolldice()
    yourdie1 = dice[yourroll[0]-1]
    yourdie2 = dice[yourroll[1]-1]
    yourdie3 = dice[yourroll[2]-1]
    validroll = True
    if ((yourroll[0] != yourroll[1]) and (yourroll[1] != yourroll[2]) and (yourroll[0] != yourroll[2])):
            validroll = False
    return render_template('clo.html',die1 = ourdie1,die2=ourdie2,die3=ourdie3,die4=yourdie1,die5=yourdie2,die6=yourdie3,validRoll = validroll)

@app.route('/reroll')
def reroll():
    dice = ["http://roll.diceapi.com/images/poorly-drawn/d6/1.png","http://roll.diceapi.com/images/poorly-drawn/d6/2.png","http://roll.diceapi.com/images/poorly-drawn/d6/3.png","http://roll.diceapi.com/images/poorly-drawn/d6/4.png","http://roll.diceapi.com/images/poorly-drawn/d6/5.png","http://roll.diceapi.com/images/poorly-drawn/d6/6.png"]
    yourroll = rolldice()
    ourdie1 = session['ourdie1']
    ourdie2 = session['ourdie2']
    ourdie3 = session['ourdie3']
    yourdie1 = dice[yourroll[0]-1]
    yourdie2 = dice[yourroll[1]-1]
    yourdie3 = dice[yourroll[2]-1]
    validroll = True
    if ((yourroll[0] != yourroll[1]) and (yourroll[1] != yourroll[2]) and (yourroll[0] != yourroll[2])):
        validroll = False
    return render_template('clo.html',die1 = ourdie1,die2=ourdie2,die3=ourdie3,die4=yourdie1,die5=yourdie2,die6=yourdie3)

def rolldice():
    die1 = random.randint(0,6)
    die2 = random.randint(0,6)
    die3 = random.randint(0,6)
    ans = [die1,die2,die3]
    return ans



@app.route("/computation")
def computation():
    if "user" not in session:
        return redirect(url_for('root'))
    with sqlite3.connect(DB_FILE) as connection:
        c = connection.cursor()
        dbfunctions.addQuestionsToDatabase()
        q = 'SELECT questions, one, two , three, four FROM TRIVIA;'
        foo = c.execute(q)
        List = foo.fetchall()
        connection.commit()
    return render_template('computation.html',q = List, heading = session["user"],sessionstatus = "user" in session)


@app.route("/computationchecker",methods=["POST"])
def computationchecker():
    if "user" not in session:
        return redirect(url_for('root'))
    dict = request.form
    #list of list answers
    #for each in list answers check if the anser is equal to dict[question]
    return "woo"

if __name__ == "__main__":
    app.debug = True
    app.run()
