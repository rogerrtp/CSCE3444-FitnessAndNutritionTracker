import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import Session
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import engine
from classes import User, MealLogEntry, WeightLogEntry, ExerciseLogEntry

from datetime import datetime
import os

from graphing import graph


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
    with Session(engine) as session:
        thisUser = session.query(User).filter(User.email == current_user.email).first()
        totalCaloriesInDay = thisUser.getCaloriesInToday()
        totalExerciseDurationDay = thisUser.getExerciseDurationToday()
        latestWeightDay = thisUser.getWeightToday()

        totalCaloriesInWeek = thisUser.getCaloriesInWeek()
        totalExerciseDurationWeek = thisUser.getExerciseDurationWeek()
        latestWeightWeek = thisUser.getWeightWeek()
        return render_template('user-home.html',
                               email=current_user.email,
                               firstName=current_user.firstName,
                               totalCaloriesInDay=totalCaloriesInDay,
                               totalExerciseDurationDay=totalExerciseDurationDay,
                               latestWeightDay=latestWeightDay,
                               totalCaloriesInWeek=totalCaloriesInWeek,
                               totalExerciseDurationWeek=totalExerciseDurationWeek,
                               latestWeightWeek=latestWeightWeek
                               )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('root'))


@app.route("/meals", methods=['GET'])
@login_required
def meals():
    if request.method == 'GET':
        with Session(engine) as session:
            meals = session.query(MealLogEntry).filter(MealLogEntry.userID==current_user.userID).order_by(MealLogEntry.entryDt.asc()).all()
            headers = ["Date", "Time", "Calories"]

            graphLabels = '[' + ', '.join(["'" + str(m.entryDt) + "'" for m in meals]) + ']'
            graphData = '[' + ', '.join([str(m.calories) for m in meals]) + ']'
            rows = [
                [str(datetime.date(m.entryDt)), str(datetime.time(m.entryDt)), m.calories] for m in meals
            ]
        return render_template("meals.html", headers=headers, rows=rows,
                               graphLabels=graphLabels, graphData=graphData)
    else:
        raise Exception("Invalid request method")

# @app.route("/meal/<int:mealLogID>", methods=['DELETE'])
# @login_required
# def meal(mealLogID: int):
#     if request.method == 'DELETE':
#         with Session(engine) as session:
#             meal = session.query(MealLogEntry).get(mealLogID)
#             session.delete(meal)
#             session.commit()
#
#
#
#         return redirect(url_for('meals'))
#     else:
#         raise Exception("Invalid request method")

@app.route("/add_meal", methods=['GET', "POST"])
@login_required
def add_meal():
    if request.method == 'GET':
        return render_template('add_meal.html')
    if request.method == 'POST':
        with Session(engine) as session:
            newMeal = MealLogEntry(
                entryDt=datetime.strptime(request.form['date'] + ' ' + request.form['time'], "%Y-%m-%d %H:%M"),
                calories=int(request.form['calories']),
                proteinGrams=int(request.form['proteinGrams']),
                carbsGrams=int(request.form['carbsGrams']),
                fatsGrams=int(request.form['fatsGrams']),
                userID=current_user.userID
                           )

            session.add(newMeal)
            session.commit()
            return redirect(url_for('meals'))
    else:
        raise Exception("Invalid request method")


@app.route("/weights", methods=['GET'])
@login_required
def weights():
    if request.method == 'GET':
        with Session(engine) as session:
            weights = session.query(WeightLogEntry).filter(WeightLogEntry.userID==current_user.userID).order_by(WeightLogEntry.entryDt.asc()).all()
            headers = ["Date", "Time", "Weight"]

            graphLabels = '[' + ', '.join(["'" + str(m.entryDt) + "'" for m in weights]) + ']'
            graphData = '[' + ', '.join([str(m.weightLbs) for m in weights]) + ']'
            rows = [
                [str(datetime.date(m.entryDt)),
                 str(datetime.time(m.entryDt)),
                 m.weightLbs] for m in weights
            ]
        return render_template("weights.html", headers=headers, rows=rows,
                               graphLabels=graphLabels, graphData=graphData)
    else:
        raise Exception("Invalid request method")



# @app.route("/weight/<int:weightLogID>", methods=['DELETE'])
# @login_required
# def weight(weightLogID: int):
#     if request.method == 'DELETE':
#         with Session(engine) as session:
#             weight = session.query(WeightLogEntry).get(weightLogID)
#             session.delete(weight)
#             session.commit()
#         return redirect(url_for('weights'))
#     else:
#         raise Exception("Invalid request method")

@app.route("/add_weight", methods=['GET', "POST"])
@login_required
def add_weight():
    if request.method == 'GET':
        return render_template('add_weight.html')
    if request.method == 'POST':
        with Session(engine) as session:
            newweight = WeightLogEntry(
                entryDt=datetime.strptime(request.form['date'] + ' ' + request.form['time'], "%Y-%m-%d %H:%M"),
                weightLbs=int(request.form['weightLbs']),
                userID=current_user.userID
                           )

            session.add(newweight)
            session.commit()
            return redirect(url_for('weights'))
    else:
        raise Exception("Invalid request method")


@app.route("/exercises", methods=['GET'])
@login_required
def exercises():
    if request.method == 'GET':
        with Session(engine) as session:
            exercises = session.query(ExerciseLogEntry).filter(ExerciseLogEntry.userID==current_user.userID).order_by(ExerciseLogEntry.entryDt.asc()).all()
            headers = ["Date", "Time", "Duration"]

            graphLabels = '[' + ', '.join(["'" + str(m.entryDt) + "'" for m in exercises]) + ']'
            graphData = '[' + ', '.join([str(m.durationSeconds) for m in exercises]) + ']'
            rows = [
                [str(datetime.date(m.entryDt)), str(datetime.time(m.entryDt)), m.durationSeconds] for m in exercises
            ]
        return render_template("exercises.html", headers=headers, rows=rows,
                               graphLabels=graphLabels, graphData=graphData)
    else:
        raise Exception("Invalid request method")

# @app.route("/exercise/<int:exerciseLogID>", methods=['DELETE'])
# @login_required
# def exercise(exerciseLogID: int):
#     if request.method == 'DELETE':
#         with Session(engine) as session:
#             exercise = session.query(ExerciseLogEntry).get(exerciseLogID)
#             session.delete(exercise)
#             session.commit()
#         return redirect(url_for('exercises'))
#     else:
#         raise Exception("Invalid request method")

@app.route("/add_exercise", methods=['GET', "POST"])
@login_required
def add_exercise():
    if request.method == 'GET':
        return render_template('add_exercise.html')
    if request.method == 'POST':
        with Session(engine) as session:
            newexercise = ExerciseLogEntry(
                entryDt=datetime.strptime(request.form['date'] + ' ' + request.form['time'], "%Y-%m-%d %H:%M"),
                durationSeconds=int(request.form['durationSeconds']),
                avgHeartRateBpm=int(request.form['avgHeartRateBpm']),
                cardioOrStrength=request.form['cardioOrStrength'],
                userID=current_user.userID
                           )

            session.add(newexercise)
            session.commit()
            return redirect(url_for('exercises'))
    else:
        raise Exception("Invalid request method")
