import os
import time

from flask import Flask, session, render_template, request, redirect, url_for, escape, request
from register import *


app = Flask(__name__)
app.secret_key = 'any random string'

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('register'))


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/home")
def home():
    if 'username' in session:
        username = session['username']
        return render_template("user.html", username=username, message="Successfully logged in.", heading="Welcome back")

    return redirect(url_for('index'))


@app.route("/admin")
def allusers():
    users = User.query.all()

    return render_template("admin.html", users=users)


@app.route("/auth", methods=["POST"])
def auth():
    if request.method == "POST":
        username = request.form.get('username')
        usr_pas = request.form.get('password')

        # check if user existed or not
        userData = User.query.filter_by(username=username).first()

        # if user is present, validate username and password
        if userData is not None:
            if userData.username == username and userData.password == usr_pas:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
            # user verification failed
            else:
                return render_template("registration.html", message="username/password is incorrect!!")
        # if user doesn't exists.
        else:
            return redirect(url_for('index'))
    # if try access directly
    else:
        return "<h1>Please login/register instead.</h1>"


@app.route("/userDetails", methods=["POST"])
def userDetails():
    firstName = request.form.get("fname")
    lastName = request.form.get("lname")
    userName = request.form.get("username")
    password = request.form.get("password")
    gender = request.form.get("gender")

    user = User(firstname=firstName, lastname=lastName,
                username=userName, password=password, gender=gender, time_registered=time.ctime(time.time()))
    try:
        db.session.add(user)
        db.session.commit()
        session['username'] = request.form['username']
        return render_template("user.html",  user=userName, message="Successfully Registered", name=firstName+" "+lastName)

    except:
        return render_template("registration.html", message="Fill all the details!")
