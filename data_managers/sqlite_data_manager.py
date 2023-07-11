from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from moviweb_app.data_managers.data_manager_interface import DataManagerInterface

Base = declarative_base()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        users = self.db.query(User).all()
        return users

    def get_user_movies(self, user_id):
        user_movies = self.db.query(Movie).filter(Movie.user_id).all()
        return user_movies


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    movies = relationship("Movie", back_populates="user")


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
