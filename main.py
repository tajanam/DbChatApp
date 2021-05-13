import os
from flask import Flask, render_template, request, redirect, url_for
from sqla_wrapper import SQLAlchemy

app = Flask(__name__)

# db = SQLAlchemy("sqlite:///db.sqlite") # konekcija na bazu podataka

db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primarni kljuc
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)

db.create_all()

@app.route("/", methods=["GET"])
def index():

    messages = db.query(Message).all()

    return render_template("index.html", messages=messages)

@app.route("/add-message", methods=["POST"])
def add_message():

    username = request.form.get("username")
    text = request.form.get("text")

    print("{0}: {1}".format(username, text))

    message = Message(author=username, text=text)
    message.save()

    return redirect("/")

if __name__== "__main__":
    app.run()
