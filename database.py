from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///finance.db', echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    category = Column(String)
    date = Column(String, primary_key=True)
    value = Column(Float)


class Expense(Operation):
    __tablename__ = 'expenses'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    category = Column(String, primary_key=True)


class Revenue(Operation):
    __tablename__ = 'revenues'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    category = Column(String, primary_key=True)


Base.metadata.create_all(engine)
