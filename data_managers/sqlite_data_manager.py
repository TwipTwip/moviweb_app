from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from moviweb_app.data_managers.data_manager_interface import DataManagerInterface
from moviweb_app.data_managers.models import User, Movie

Base = declarative_base()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name, app):
        self.db = SQLAlchemy(app)
        self.app = app
        engine = create_engine(db_file_name)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_users(self):
        with self.app.app_context():
            users = self.session.query(User).all()
        return users

    def get_user_movies(self, user_id):
        with self.app.app_context():
            user_movies = self.session.query(Movie).filter(Movie.user_id == user_id).all()
        return user_movies

    def add_user(self, username):
        with self.app.app_context():
            user = User(
                username=username
            )

            self.session.add(user)
            self.session.commit()

        return "User has been successfully been added"

    def get_username_by_id(self, user_id):
        with self.app.app_context():
            user = self.session.query(User).filter(User.id == user_id).one()
        return user

    def add_movie(self, movie_info, user_id):
        with self.app.app_context():
            movie = Movie(
                title=movie_info['Title'],
                director=movie_info['Director'],
                year=movie_info['Year'],
                rating=movie_info['imdbRating'],
                poster=movie_info['Poster'],
                user_id=user_id
            )

            self.session.add(movie)
            self.session.commit()

        return "Movie has been successfully added"

    def update_movie(self, movie_id, new_title, new_rating):
        with self.app.app_context():
            movie_to_update = self.session.query(Movie).filter(Movie.id == movie_id).one()
            movie_to_update.title = new_title
            movie_to_update.rating = new_rating
            self.session.commit()

        return "Movie has been successfully updated"

    def get_movie_info(self, movie_id):
        with self.app.app_context():
            movie_info = self.session.query(Movie).filter(Movie.id == movie_id).one()
        return movie_info

    def delete_movie(self, movie_id):
        with self.app.app_context():
            self.session.query(Movie).filter(Movie.id == movie_id).delete()
            self.session.commit()
        return "Movie has successfully been deleted"
