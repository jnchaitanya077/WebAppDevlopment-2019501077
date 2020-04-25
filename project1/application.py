import os
import time
import requests
import json
from test import bookreview


from flask import Flask, session, render_template, request, redirect, url_for
from register import *
from userReview import *


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


@app.route("/logout/<username>")
def logout(username):
    session.pop(username, None)
    return redirect(url_for('index'))


@app.route("/home/<user>")
def userHome(user):
    if user in session:
        return render_template("user.html", username=user, message="Successfully logged in.", heading="Welcome back")
    return redirect(url_for('index'))


@app.route("/admin")
def allusers():

    users = User.query.all()
    # details = {}
    # accountDetails = []

    # for eachuser in range(len(users)):
    #     accountDetails.append({"username": users[eachuser].username, "password":
    #                            users[eachuser].password, "time_registered": users[eachuser].time_registered})
    # details["Users"] = accountDetails
    # print(str(details))
    return render_template("admin.html", users=users)


@app.route("/auth", methods=["POST", "GET"])
def auth():
    if request.method == "POST":
        username = request.form.get('username')
        usr_pas = request.form.get('password')

        # check if user existed or not
        userData = User.query.filter_by(username=username).first()

        # if user is present, validate username and password
        if userData is not None:
            if userData.username == username and userData.password == usr_pas:
                session[username] = username
                return redirect(url_for('userHome', user=username))
            # user verification failed
            else:
                return render_template("registration.html", message="username/password is incorrect!!")
        # if user doesn't exists.
        else:
            return render_template("registration.html", message="Account doesn't exists, Please register!")
    # if try to access directly
    else:
        return "<h1>Please login/register instead.</h1>"


@app.route("/userDetails", methods=["POST", "GET"])
def userDetails():
    if request.method == "POST":
        firstName = request.form.get("fname")
        lastName = request.form.get("lname")
        userName = request.form.get("username")
        password = request.form.get("password")
        gender = request.form.get("gender")
        email = request.form.get("email")

        # check if user existed or not
        userData = User.query.filter_by(email=email).first()

        if userData is not None:
            return render_template("registration.html", message="email already exists, Please login.")
        else:
            user = User(firstname=firstName, lastname=lastName,
                        username=userName, password=password, gender=gender, time_registered=time.ctime(time.time()), email=email)

            # check if all details were given for registration.
            try:
                db.session.add(user)
                db.session.commit()
                session[userName] = request.form['username']
                return render_template("user.html",  username=userName, message="Successfully Registered", name=firstName+" "+lastName)

            except:
                return render_template("registration.html", message="Fill all the details!")
    return "<h1>Please Register</h1>"

@app.route("/homepage", methods=["GET", "POST"])
def saibabaMethod():
    book = bookreview("1439152802", "The Secret Keeper","Kate Morton", 2012)
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                    params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": book.isbn})
    data = res.text
    parsed = json.loads(data)
    print(parsed)
    res = {}
    for i in parsed:
        for j in (parsed[i]):
            res = j
    # Variables for testing
    bookisbn = book.isbn
    user = "Akhil.alla2"
    # Get all the reviews for the given book.
    allreviews = review.query.filter_by(isbn=bookisbn).all()
    if request.method == "POST":
        rating = request.form.get("rating")
        reviews = request.form.get("review")
        isbn = book.isbn
        timestamp = time.ctime(time.time())
        title = book.title
        username = "srinivas"
        user = review(isbn=isbn, review=reviews, rating=rating, time_stamp=timestamp, title=title, username=username)
        db.session.add(user)
        db.session.commit()
         # Get all the reviews for the given book.
        allreviews = review.query.filter_by(isbn=bookisbn).all()
        return render_template("review.html", res=res, book=book, review=allreviews)
    else:
        # database query to check if the user had given review to that paticular book.
        rev = review.query.filter(review.isbn==bookisbn, review.username==user)
        # print(json.parse(allreviews))
        # for i in allreviews:
        #     print(i.review)
        # if review was not given then dispaly the book page with review button
        if rev is None:
            return render_template("review.html", book=book, review=allreviews, res=res) 
        else:
            return render_template("review.html", book=book, message="You reviewed this book!!", review=allreviews, res=res,property="none")
