import bcrypt
from flask import Flask, render_template, request
from sqlalchemy.orm import Session

from classes import User
from database import engine

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return render_template("home.html")

    elif request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password'].encode()

        with Session(engine) as session:
            dbInfo = session.query(User).filter(User.email == email).first()

            if dbInfo and bcrypt.checkpw(pwd, dbInfo.password.encode()):
                return 'OK'
            else:
                return 'Bad login'


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        with Session(engine) as session:
            salt = bcrypt.gensalt()
            newUser = User(firstName=request.form['fname'],
                lastName=request.form['lname'],
                email=request.form['email'],
                password=bcrypt.hashpw(request.form['password'].encode(), salt).decode(),
                isActive=True
            )
            # bcrypt.checkpw(userBytes, dbUser.hashed_password.encode()) to validate pwd for login

            session.add(newUser)
            session.commit()

            return f'<html>User registered! {newUser}</html>'
