# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, session, redirect, url_for, redirect
import sqlite3, random
import os
from flask import flash
import urllib.request, json
from os import urandom
import utl.dbfunctions as dbfunctions
import urllib.request as urlrequest
app = Flask(__name__)
app.secret_key = urandom(32)

#-----------------------------------------------------------------

#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor() #facilitate db operations
dbfunctions.setup()
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

@app.route("/computation")
def computation():
    if "user" not in session:
        return redirect(url_for('root'))
    with sqlite3.connect(DB_FILE) as connection:
        c = connection.cursor()
        q = 'SELECT questions, one, two , three, four FROM TRIVIA;'
        foo = c.execute(q)
        List = foo.fetchall()
        connection.commit()
    return render_template('computation.html',q = List, heading = session["user"],sessionstatus = "user" in session)

if __name__ == "__main__":
    app.debug = True
    app.run()
