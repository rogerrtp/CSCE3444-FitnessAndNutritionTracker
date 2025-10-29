from datetime import datetime

from sqlalchemy import (ForeignKey, String, Integer, DateTime, func)
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, relationship, declared_attr)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    firstName: Mapped[str] = mapped_column(String(255))
    lastName: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))  # TODO: hash password
    isActive: Mapped[bool] = mapped_column(default=True)
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    lastLoginDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    def __repr__(self):
        return f"<User(userID={self.userID}, id={self.userID}, username={self.username})>"


class LogEntryBase:
    createDt: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    entryDt: Mapped[datetime] = mapped_column(DateTime)
    modifiedDt: Mapped[datetime] = mapped_column(DateTime)
    userID: Mapped[int] = mapped_column(ForeignKey("users.userID"))

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User")


class MealLogEntry(LogEntryBase, Base):
    __tablename__ = "meal_log_entries"
    mealLogID: Mapped[int] = mapped_column(primary_key=True)
    calories: Mapped[int] = mapped_column(String(255))
    proteinGrams: Mapped[int] = mapped_column(Integer)
    carbsGrams: Mapped[int] = mapped_column(Integer)
    fatsGrams: Mapped[int] = mapped_column(Integer)
