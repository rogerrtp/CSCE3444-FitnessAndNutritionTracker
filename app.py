import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import Session
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import engine
from classes import User

from datetime import datetime
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userID):
    with Session(engine) as session:
        return session.query(User).get(int(userID))

@app.route("/", methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return render_template("home.html")

    elif request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        with Session(engine) as session:
            dbInfo = session.query(User).filter(User.email == email).first()
            dbInfo.lastLoginDt = datetime.now()

            if dbInfo and check_password_hash(dbInfo.password, pwd):
                print("Login successful")
                login_user(dbInfo)
                return redirect(url_for('user_home'))
            else:
                print("Login failed")
                return render_template("home.html")


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':

        email = request.form['email']
        with Session(engine) as session:
            if session.query(User).filter(User.email == email).first():
                return render_template("home.html",
                                       error="User with that email address already exists")

            newUser = User(firstName=request.form['fname'],
                lastName=request.form['lname'],
                email=request.form['email'],
                password=generate_password_hash(request.form['password']),
                is_active=True
            )

            session.add(newUser)
            session.commit()

            return redirect(url_for('root'))

@app.route("/userhome", methods=['GET', 'POST'])
@login_required
def user_home():
    return render_template('user-home.html', email=current_user.email, firstName=current_user.firstName)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('root'))


@app.route("/weight", methods=['GET', 'POST', 'DELETE'])
@login_required
def weight():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        raise Exception("Invalid request method")


@app.route("/exercises", methods=['GET', 'POST', 'DELETE'])
@login_required
def exercises():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        raise Exception("Invalid request method")


@app.route("/meals", methods=['GET', 'POST', 'DELETE'])
@login_required
def meals():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        raise Exception("Invalid request method")
