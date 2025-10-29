from flask import Flask, render_template, request
from database import engine
from classes import User
from sqlalchemy.orm import Session
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        with Session(engine) as session:
            newUser = User(
                firstName=request.form['fname'],
                lastName=request.form['lname'],
                username=request.form['email'],
                password=request.form['password'],
                isActive=True
            )

            session.add(newUser)
            session.commit()

            return f'<html>User registered! {newUser}</html>'
