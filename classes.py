from datetime import datetime

import bcrypt
from flask_login import UserMixin
from sqlalchemy import (ForeignKey, String, Integer, DateTime, func, select)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, declared_attr, Session)
from typing import List
from datetime import datetime, timedelta

from sqlalchemy.util.concurrency import have_greenlet

from database import engine
from statistics import mean

class Base(DeclarativeBase):
    pass


#  Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class User(UserMixin, Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    firstName: Mapped[str] = mapped_column(String(255))
    lastName: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))  # TODO: hash password
    is_active: Mapped[bool] = mapped_column(default=True)  # For Flask-Login
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    lastLoginDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    meals: Mapped[List["MealLogEntry"]] = relationship(back_populates="user")
    exercises: Mapped[List["ExerciseLogEntry"]] = relationship(back_populates="user")
    weights: Mapped[List["WeightLogEntry"]] = relationship(back_populates="user")


    def __repr__(self):
        return f"<User(userID={self.userID}, id={self.userID}, email={self.email})>"

    def getUserID(self):
        return self.userID

    def get_id(self):
        return self.getUserID()

    def getEmail(self):
        return self.email

    def getFirstName(self):
        return self.firstName

    def setFirstName(self, firstName):
        self.firstName = firstName
        return self.getFirstName()

    def getLastName(self):
        return self.lastName

    def setLastName(self, lastName):
        self.lastName = lastName
        return self.getLastName()

    def getis_active(self):
        return self.is_active

    def setis_active(self, is_active):
        self.is_active = is_active
        return self.getis_active()

    def getCreateDt(self):
        return self.createDt

    def getLastLoginDt(self):
        return self.lastLoginDt

    def setLastLoginDt(self, lastLoginDt):
        self.lastLoginDt = lastLoginDt
        return self.getLastLoginDt()

    def setPassword(self, password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode(), salt).decode()
        return True

    def getCaloriesInToday(self):
        calories = sum(
            [meal.calories for meal in self.meals if meal.entryDt.date() == datetime.today().date()]
        )
        return calories

    def getCaloriesInWeek(self):
        calories = sum(
            [meal.calories for meal in self.meals if
             datetime.today().date() - timedelta(days=7) <= meal.entryDt.date() <= datetime.today().date()]
        )
        return calories


    def getExerciseDurationToday(self):
        duration = sum(
            [exercise.durationSeconds for exercise in self.exercises if exercise.entryDt.date() == datetime.today().date()]
        )
        return duration

    def getExerciseDurationWeek(self):
        duration = sum(
            [exercise.durationSeconds for exercise in self.exercises if
             datetime.today().date() - timedelta(days=7) <= exercise.entryDt.date() <= datetime.today().date()]
        )
        return duration

    def getWeightToday(self):
        weight = mean(
            [weight.weightLbs for weight in self.weights if weight.entryDt.date() == datetime.today().date()]
        ) if len(self.weights) > 0 else 0
        return weight

    def getWeightWeek(self):
        weight = mean(
            [weight.weightLbs for weight in self.weights if
             datetime.today().date() - timedelta(days=7) <= weight.entryDt.date() <= datetime.today().date()]
        ) if len(self.weights) > 0 else 0
        return weight



# class LogEntryBase(Base):
#     # logEntryID: Mapped[int] = mapped_column(primary_key=True)
#     createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
#     entryDt: Mapped[datetime] = mapped_column(DateTime)
#     modifiedDt: Mapped[datetime] = mapped_column(DateTime)
#     userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
#     user: Mapped[User] = relationship(back_populates="users")
#
#     __tablename__ = "log_entries"
#
#
#     # @declared_attr
#     # def User(cls):
#     #     return relationship("User", back_populates=cls.__name__.lower())
#
#     def getEntryDt(self):
#         return self.entryDt
#
#     def setEntryDt(self, entryDt):
#         self.entryDt = entryDt
#         return self.getEntryDt()
#
#     def getCreateDt(self):
#         return self.createDt
#
#     def getModifiedDt(self):
#         return self.modifiedDt
#
#     def setModifiedDt(self, modifiedDt):
#         self.modifiedDt = modifiedDt
#         return self.getModifiedDt()
#
#     # These will need to be implemented by subclasses
#     def hasNextEntry(self):
#         pass
#
#     def getNextEntry(self):
#         pass
#
#     def getPreviousEntry(self):
#         pass


class MealLogEntry(Base):
    __tablename__ = "meal_log_entries"
    mealLogID: Mapped[int] = mapped_column(primary_key=True)
    calories: Mapped[int] = mapped_column(String(255))
    proteinGrams: Mapped[int] = mapped_column(Integer)
    carbsGrams: Mapped[int] = mapped_column(Integer)
    fatsGrams: Mapped[int] = mapped_column(Integer)
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    entryDt: Mapped[datetime] = mapped_column(DateTime)
    modifiedDt: Mapped[datetime] = mapped_column(DateTime)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    user: Mapped["User"] = relationship(back_populates="meals")


    # @declared_attr
    # def User(cls):
    #     return relationship("User", back_populates=cls.__name__.lower())

    def getEntryDt(self):
        return self.entryDt

    def setEntryDt(self, entryDt):
        self.entryDt = entryDt
        return self.getEntryDt()

    def getCreateDt(self):
        return self.createDt

    def getModifiedDt(self):
        return self.modifiedDt

    def setModifiedDt(self, modifiedDt):
        self.modifiedDt = modifiedDt
        return self.getModifiedDt()

    # These will need to be implemented by subclasses
    def hasNextEntry(self):
        pass

    def getNextEntry(self):
        pass

    def getPreviousEntry(self):
        pass

    def getMealLogId(self):
        return self.mealLogID

    def getCalories(self):
        return self.calories

    def setCalories(self, calories):
        self.calories = calories
        return self.getCalories()

    def getProteinGrams(self):
        return self.proteinGrams

    def setProteinGrams(self, proteinGrams):
        self.proteinGrams = proteinGrams
        return self.getProteinGrams()

    def getCarbsGrams(self):
        return self.carbsGrams

    def setCarbsGrams(self, carbsGrams):
        self.carbsGrams = carbsGrams
        return self.getCarbsGrams()

    def getFatsGrams(self):
        return self.fatsGrams

    def setFatsGrams(self, fatsGrams):
        self.fatsGrams = fatsGrams
        return self.getFatsGrams()


class ExerciseLogEntry(Base):
    __tablename__ = "exercise_log_entries"
    exerciseLogID: Mapped[int] = mapped_column(primary_key=True)
    durationSeconds: Mapped[int] = mapped_column(Integer)
    cardioOrStrength: Mapped[str] = mapped_column(String(1))  # C = cardio, S = strength
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    entryDt: Mapped[datetime] = mapped_column(DateTime)
    modifiedDt: Mapped[datetime] = mapped_column(DateTime)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    user: Mapped["User"] = relationship(back_populates="exercises")


    # @declared_attr
    # def User(cls):
    #     return relationship("User", back_populates=cls.__name__.lower())

    def getEntryDt(self):
        return self.entryDt

    def setEntryDt(self, entryDt):
        self.entryDt = entryDt
        return self.getEntryDt()

    def getCreateDt(self):
        return self.createDt

    def getModifiedDt(self):
        return self.modifiedDt

    def setModifiedDt(self, modifiedDt):
        self.modifiedDt = modifiedDt
        return self.getModifiedDt()

    # These will need to be implemented by subclasses
    def hasNextEntry(self):
        pass

    def getNextEntry(self):
        pass

    def getPreviousEntry(self):
        pass

    def getExerciseLogId(self):
        return self.exerciseLogID

    def getDurationSeconds(self):
        return self.durationSeconds

    def setDurationSeconds(self, durationSeconds):
        self.durationSeconds = durationSeconds
        return self.getDurationSeconds()

    def getCardioOrStrength(self):
        return self.cardioOrStrength

    def setCardioOrStrength(self, cardioOrStrength):
        self.cardioOrStrength = cardioOrStrength
        return self.getCardioOrStrength()


class WeightLogEntry(Base):
    __tablename__ = "weight_log_entries"
    weightLogID: Mapped[int] = mapped_column(primary_key=True)
    weightLbs: Mapped[int] = mapped_column(Integer)
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    entryDt: Mapped[datetime] = mapped_column(DateTime)
    modifiedDt: Mapped[datetime] = mapped_column(DateTime)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))
    user: Mapped["User"] = relationship(back_populates="weights")


    # @declared_attr
    # def User(cls):
    #     return relationship("User", back_populates=cls.__name__.lower())

    def getEntryDt(self):
        return self.entryDt

    def setEntryDt(self, entryDt):
        self.entryDt = entryDt
        return self.getEntryDt()

    def getCreateDt(self):
        return self.createDt

    def getModifiedDt(self):
        return self.modifiedDt

    def setModifiedDt(self, modifiedDt):
        self.modifiedDt = modifiedDt
        return self.getModifiedDt()

    # These will need to be implemented by subclasses
    def hasNextEntry(self):
        pass

    def getNextEntry(self):
        pass

    def getPreviousEntry(self):
        pass

    def getWeightLogId(self):
        return self.weightLogID

    def getWeightLbs(self):
        return self.weightLbs

    def setWeightLbs(self, weightLbs):
        self.weightLbs = weightLbs
        return self.getWeightLbs()
