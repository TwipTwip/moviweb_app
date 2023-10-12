import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = sqlalchemy.orm.declarative_base()
engine = create_engine("sqlite:///data/user_movies.sqlite")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    director = Column(String)
    year = Column(String)
    rating = Column(Integer)
    poster = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    movie_id = Column(Integer, ForeignKey('movies.id'))
    review_text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)


Base.metadata.create_all(engine)
