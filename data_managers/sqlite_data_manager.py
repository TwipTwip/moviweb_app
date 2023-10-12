from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from moviweb_app.data_managers.data_manager_interface import DataManagerInterface
from moviweb_app.data_managers.models import User, Movie, Review

Base = declarative_base()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name, app):
        self.db = SQLAlchemy(app)
        self.app = app
        engine = create_engine(db_file_name)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_users(self):
        """Returns all the users in the database"""
        with self.app.app_context():
            users = self.session.query(User).all()
        return users

    def get_user_movies(self, user_id):
        """Gets all the movies that the selected user has added"""
        with self.app.app_context():
            user_movies = self.session.query(Movie).filter(Movie.user_id == user_id).all()
        return user_movies

    def add_user(self, username):
        """Adds a new user to the database"""
        with self.app.app_context():
            user = User(
                username=username
            )

            self.session.add(user)
            self.session.commit()

        return "User has been successfully been added"

    def get_username_by_id(self, user_id):
        """Returns user based on their ID"""
        with self.app.app_context():
            user = self.session.query(User).filter(User.id == user_id).one()
        return user

    def add_movie(self, movie_info, user_id):
        """Adds a movie to the database"""
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
        """Updates selected movie with a new title(nickname if the user has a nickname for the movie) and
        the rating can be altered if the user has a rating for the movie that they want to change it to"""
        with self.app.app_context():
            movie_to_update = self.session.query(Movie).filter(Movie.id == movie_id).one()
            movie_to_update.title = new_title
            movie_to_update.rating = new_rating
            self.session.commit()

        return "Movie has been successfully updated"

    def get_movie_info(self, movie_id):
        """Gets all the info for the selected movie"""
        with self.app.app_context():
            movie_info = self.session.query(Movie).filter(Movie.id == movie_id).one()
        return movie_info

    def delete_movie(self, movie_id):
        """Deletes selected movie"""
        with self.app.app_context():
            self.session.query(Movie).filter(Movie.id == movie_id).delete()
            self.session.query(Review).filter(Review.movie_id == movie_id).delete()
            self.session.commit()
        return "Movie has successfully been deleted"

    def get_all_movies(self):
        """Gets all the movies in the database"""
        with self.app.app_context():
            movies = self.session.query(Movie).all()
        return movies

    def list_reviews(self, movie_id):
        """Lists all the reviews for the selected movie"""
        with self.app.app_context():
            reviews = self.session.query(Review).filter(Review.movie_id == movie_id).all()
        return reviews

    def add_review(self, user_id, movie_id, rating, review_text):
        """Adds a review for the selected movie"""
        with self.app.app_context():
            review = Review(
                movie_id=movie_id,
                user_id=user_id,
                rating=rating,
                review_text=review_text
            )
            self.session.add(review)
            self.session.commit()

        return "Review has been successfully added"

    def update_review(self, review_id, new_rating, new_text_review):
        """Updates the selected review witha new rating(if it is changed) and a new review(if the review was changed)"""
        with self.app.app_context():
            review_to_update = self.session.query(Review).filter(Review.id == review_id).one()
            review_to_update.rating = new_rating
            review_to_update.review_text = new_text_review
            self.session.commit()

        return "Review has successfully been updated"

    def delete_review(self, review_id):
        """Deletes selected review"""
        with self.app.app_context():
            self.session.query(Review).filter(Review.id == review_id).delete()
            self.session.commit()
        return "Review has successfully been deleted"

    def get_review(self, review_id):
        """Returns the selected review"""
        with self.app.app_context():
            review = self.session.query(Review).filter(Review.id == review_id).one()
            return review

    def delete_user(self, user_id):
        """Deletes selected user"""
        with self.app.app_context():
            self.session.query(User).filter(User.id == user_id).delete()
            self.session.query(Movie).filter(Movie.user_id == user_id).delete()
            self.session.query(Review).filter(Review.user_id == user_id).delete()
            self.session.commit()
        return "User has successfully been defeated"
