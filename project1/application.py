import os
import time
import requests
import json
from test import bookreview
from booktable import *
from flask import Flask, session, render_template, request, redirect, url_for,jsonify
from register import *
from userReview import *
from sqlalchemy import or_


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
        return render_template('Search.html', user=user)
    return redirect(url_for('index'))


@app.route("/admin/<user>")
def allusers(user):
    if user in session:
        users = User.query.all()
        return render_template("admin.html", users=users)
    return render_template('registration.html', message="Please login!!")


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
                return render_template("user.html",  username=userName, message="Successfully Registered", name=firstName+" "+lastName)

            except:
                return render_template("registration.html", message="Fill all the details!")
    return "<h1>Please Register</h1>"


@app.route("/search/<user>", methods=["POST", "GET"])
def search(user):

    if request.method == "GET":
        # return render_template("Search.html", user = user)
        return redirect(url_for('index'))

    else:
        res = request.form.get("find")
        res = '%'+res+'%'
        result = books.query.filter(or_(books.title.ilike(
            res), books.author.ilike(res), books.isbn.ilike(res))).all()
        return render_template("Search.html", result=result, user=user)


@app.route("/bookpage/<username>/<isbn>", methods=["POST", "GET"])
def bookpage(username, isbn):

    user1 = username
    bookisbn = isbn
    # allow the user only if he in session
    if user1 in session:
        # # Creating book object for testing purpose
        # book = bookreview("1439152802", "The Secret Keeper",
        #                   "Kate Morton", 2012)
        # Get book details using goodreads api
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": bookisbn})

        book = books.query.filter_by(isbn=bookisbn).first()
        # Parsing the data
        data = res.text
        parsed = json.loads(data)
        print(parsed)
        res = {}
        for i in parsed:
            for j in (parsed[i]):
                res = j

        # # Variables for testing
        # bookisbn = book.isbn

        # Get all the reviews for the given book.
        allreviews = review.query.filter_by(isbn=bookisbn).all()

        if request.method == "POST":
            print(res)
            rating = request.form.get("rating")
            reviews = request.form.get("review")
            isbn = bookisbn
            timestamp = time.ctime(time.time())
            title = book.title
            username = user1
            user = review(isbn=isbn, review=reviews, rating=rating,
                          time_stamp=timestamp, title=title, username=username)
            db.session.add(user)
            db.session.commit()

            # Get all the reviews for the given book.
            allreviews = review.query.filter_by(isbn=bookisbn).all()
            return render_template("books.html", res=res, book=book, review=allreviews, property="none", message="You reviewed this book!!", username=username)
        else:
            # database query to check if the user had given review to that paticular book.
            rev = review.query.filter(review.isbn.like(
                bookisbn), review.username.like(user1)).first()
            # print(rev)

            # Get all the reviews for the given book.
            allreviews = review.query.filter_by(isbn=bookisbn).all()

            # if review was not given then dispaly the book page with review button
            if rev is None:
                return render_template("books.html", book=book, res=res, review=allreviews, username=user1)
            return render_template("books.html", book=book, message="You reviewed this book!!", review=allreviews, res=res, property="none", username=user1)
    else:
        return redirect(url_for('index'))
@app.route("/api/submit_review/", methods=["POST"])
def review_api():
    if request.method == "POST":

        var = request.json
        print("-------------------", var)
        isbn = var["isbn"]
        username = var["username"]
        rating = var["rating"]
        reviews = var["reviews"]
        print(isbn, username, rating, reviews)

        # if "username" and "isbn" in request.args:
        #     username = request.args["username"]
        #     isbn = request.args["isbn"]
        #     rating = request.args["rating"]
        #     reviews = request.args["review"]
        # else:
        #     return "Error: no isbn/username/rating/review/ field provided"

        # check if the paticular user given review before
        rev_From_db = review.query.filter(
            review.isbn.like(isbn), review.username.like(username)
        ).first()
        print("first", str(rev_From_db))

        # if the user doesnt give the review for that book
        if rev_From_db is None:

            try:
                # bring the book details
                book = books.query.filter_by(isbn=isbn).first()
                print("book", str(book))
            except:
                message = "Enter valid ISBN"
                return jsonify(message), 404

            timestamp = time.ctime(time.time())
            title = book.title
            user = review(
                isbn=isbn,
                review=reviews,
                rating=rating,
                time_stamp=timestamp,
                title=title,
                username=username,
            )
            db.session.add(user)
            db.session.commit()

            allreviews = review.query.filter_by(isbn=isbn).all()
            rew = []
            timeStamp = []
            usr = []
            for rev in allreviews:
                rew.append(rev.review)
                timeStamp.append(rev.time_stamp)
                usr.append(rev.username)

            dict = {
                "isbn": isbn,
                "review": rew,
                "time_stamp": timeStamp,
                "username": usr,
                "message": "You reviewed this book.",
            }

            return jsonify(dict), 200
        else:
            dict = {"message": "You already reviewed this book."}
            return jsonify(dict), 200