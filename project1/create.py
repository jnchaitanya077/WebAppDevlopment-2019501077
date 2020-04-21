import csv
import os
from flask import Flask, render_template, request
from booktable import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def main():
    db.create_all()
    f = open("books.csv")
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        book = books(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print(
            f"added{book.title} with number {book.isbn} written by {book.author} published in the year {book.year}")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
