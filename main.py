# završni projekt

import requests
import uuid
import hashlib
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User,Contact, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    session_token = request.cookies.get("session_token")

    if session_token:
        user = db.query(User).filter_by(session_token=session_token, deleted=False).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")
    password = request.form.get("user-password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # provjera postoji li user
    user = db.query(User).filter_by(email=email).first()

    if not user:
        # stvaranje novog usera
        user = User(name=name, email=email, password=hashed_password)
        db.add(user)
        db.commit()

    if hashed_password != user.password:
        return render_template("wrong.html")
    elif hashed_password == user.password:
        session_token = str(uuid.uuid4())

        user.session_token = session_token
        db.add(user)
        db.commit()

        response = make_response(redirect(url_for('index')))
        response.set_cookie("session_token", session_token, httponly=True, samesite="Strict")

    return response

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", expires=0)

    return response

@app.route("/profile", methods=["GET"])
def profile():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token, deleted=False).first()

    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("index"))

@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token, deleted=False).first()

    if request.method == "GET":
        if user:
            return render_template("profile_edit.html", user=user)
        else:
            return redirect(url_for("index"))
    elif request.method == "POST":
        name = request.form.get("profile-name")
        email = request.form.get("profile-email")

        user.name = name
        user.email = email
        db.add(user)
        db.commit()

        return redirect(url_for("profile"))

@app.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token, deleted=False).first()

    if request.method == "GET":
        if user:
            return render_template("profile_delete.html", user=user)
        else:
            return redirect(url_for("index"))
    elif request.method == "POST":
        user.deleted = True
        db.add(user)
        db.commit()

        return redirect(url_for("index"))

@app.route("/add", methods=["POST"])
def add_contact():
    name = request.form.get("contact-name")
    surname = request.form.get("contact-surname")
    email = request.form.get("contact-email")
    phone = request.form.get("contact-phone")
    city = request.form.get("contact-city")

    contact = Contact(name=name, surname=surname, email=email, phone=phone, city=city)
    db.add(contact)
    db.commit()

    response = make_response(redirect(url_for("index")))

    return response

@app.route("/contacts", methods=["GET"])
def contacts():

    contacts = db.query(Contact).all()

    return render_template("contacts.html", contacts=contacts)

@app.route("/joke", methods=["GET"])
def joke():
    url = "https://api.chucknorris.io/jokes/random"

    data = requests.get(url=url)

    return render_template("joke.html", data=data.json())

if __name__ == "__main__":
    app.run()