from datetime import datetime

from sqlalchemy import (ForeignKey, String, Integer, DateTime, func)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, declared_attr)

import bcrypt

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, immutable=True)
    firstName: Mapped[str] = mapped_column(String(255))
    lastName: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))  # TODO: hash password
    isActive: Mapped[bool] = mapped_column(default=True)
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    lastLoginDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    def __repr__(self):
        return f"<User(userID={self.userID}, id={self.userID}, email={self.email})>"


    def getUserID(self):
        return self.userID

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

    def getIsActive(self):
        return self.isActive

    def setIsActive(self, isActive):
        self.isActive = isActive
        return self.getIsActive()

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


class LogEntryBase:
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    entryDt: Mapped[datetime] = mapped_column(DateTime)
    modifiedDt: Mapped[datetime] = mapped_column(DateTime)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User")


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


class MealLogEntry(LogEntryBase, Base):
    __tablename__ = "meal_log_entries"
    mealLogID: Mapped[int] = mapped_column(primary_key=True)
    calories: Mapped[int] = mapped_column(String(255))
    proteinGrams: Mapped[int] = mapped_column(Integer)
    carbsGrams: Mapped[int] = mapped_column(Integer)
    fatsGrams: Mapped[int] = mapped_column(Integer)

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


class ExerciseLogEntry(LogEntryBase, Base):
    exerciseLogID: Mapped[int] = mapped_column(primary_key=True)
    durationSeconds: Mapped[int] = mapped_column(Integer)
    cardioOrStrength: Mapped[str] = mapped_column(String(1))  # C = cardio, S = strength

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


class WeightLogEntry(LogEntryBase, Base):
    weightLogID: Mapped[int] = mapped_column(primary_key=True)
    weightLbs: Mapped[int] = mapped_column(Integer)

    def getWeightLogId(self):
        return self.weightLogID

    def getWeightLbs(self):
        return self.weightLbs

    def setWeightLbs(self, weightLbs):
        self.weightLbs = weightLbs
        return self.getWeightLbs()
