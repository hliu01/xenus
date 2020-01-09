# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, session, redirect, url_for, redirect
import sqlite3, random
import os
from flask import flash
import urllib.request, json
import utl.dbfunctions
from os import urandom
app = Flask(__name__)
app.secret_key = urandom(32)

utl.dbfunctions.setup()
DB_FILE = "Info.db"

# DICTIONARY FOR IMPORTANT SEARCH DATA
searchdict = {}

def checkAuth(): #checks if the user is logged in
    if "userID" in session:
        return True
    else:
        return False

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
    # if already logged in, don't display login page
    if checkAuth():
        return redirect(url_for('play'))
    else:
        return render_template('login.html')


@app.route("/auth", methods=["POST"])
def auth():
    username = request.form['username']
    password = request.form['password']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT username,password FROM users WHERE username = ?", (username, ))
    a = c.fetchone()
    db.commit()
    c.close()
    if a == None: #checks login username and password
        flash("No user found with given username") #no given username in database
        return redirect(url_for('login'))
    elif password != a[1]:
        flash("Incorrect password") #password is incorrect for given username
        return redirect(url_for('login'))
    else: #successfully pass the tests
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.")
        return redirect(url_for('root'))

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
    if (utl.dbfunctions.userExists(user)):
        flash('Username already taken. Please try again.')
        return False
    if (pswd == conf):
        utl.dbfunctions.adduser(user,pswd)
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


# Dispalys user's personal blog page and loads HTML with blog writing form
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("profile.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],sessionstatus = "user" in session)

@app.route("/blackjack")
def playBlackJack():
    req = urllib.request.urlopen(
        "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6"
        )
    res = req.read()
    deck = json.loads(res)
    session['deckid'] = deck["deckid"]
    shuffle()
    users = utl.dbfunctions.getusercards()
    ours =  utl.dbfunctions.getourcards()
    return render_template('blackjack.html',ourcards = ours,usercards = users)

def shuffle():
    if not ('deckid' in session):
        return url_for('playBlackJack')
    req = urllib.request.urlopen(
        "https://deckofcardsapi.com/api/deck/" + session['deckid'] + "/shuffle/?deck_count=6"
        )
    return True

@app.route("/draw")
def drawCard():
    if not ('deckid' in session):
        return url_for('playBlackJack')
    req = urllib.request.urlopen(
        "https://deckofcardsapi.com/api/deck/" + session['deckid'] +"/draw/?count=1"
        )
    res = req.read()
    card = json.loads(res)
    utl.dbfunctions.userdraw(card[image],card[value])
    return redirect(url_for('playBlackJack'))


@app.route("/snake")
def snake():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("snake.html", heading = session["user"],sessionstatus = "user" in session)

@app.route("/indexx")
def indexx():
    if "user" not in session:
        return redirect(url_for('root'))
    return render_template("indexx.html", heading = session["user"],sessionstatus = "user" in session)

if __name__ == "__main__":
    app.debug = True
    app.run()
