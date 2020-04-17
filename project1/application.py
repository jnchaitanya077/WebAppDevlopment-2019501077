import os
import sys
import time

from flask import Flask, session, render_template, request
from register import *
seconds = time.time()


app = Flask(__name__)


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
    return "<h1>Register</h1>"


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/userDetails", methods=["POST"])
def userDetails():
    firstName = request.form.get("fname")
    lastName = request.form.get("lname")
    userName = request.form.get("username")
    password = request.form.get("password")
    gender = request.form.get("gender")

    try:
        user = User(firstname=firstName, lastname=lastName,
                    username=userName, password=password, gender=gender, time_registered=time.ctime(seconds))
        db.session.add(user)
        db.session.commit()

    except ValueError:
        return render_template("error.html", message="New user creation failed.")

    print(firstName, file=sys.stderr)
    print(lastName, file=sys.stderr)
    print(userName, file=sys.stderr)

    return render_template("user.html",  user=userName, name=firstName+" "+lastName)


@app.route("/admin")
def allusers():
    users = User.query.all()

    return render_template("admin.html", users=users, count=1)
