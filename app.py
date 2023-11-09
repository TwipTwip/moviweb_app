from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_
from data_managers.sqlite_data_manager import SQLiteDataManager, Base
import requests
import sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/user_movies.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Blueprint('api', __name__)
app.register_blueprint(api, url_prefix='/api')
data_manager = SQLiteDataManager('sqlite:///data/user_movies.sqlite', app)
MOVIE_API = "http://www.omdbapi.com/?apikey=a27c1668&t="


# data_manager.db.create_all()


@app.route('/')
def home():
    """Simple home page"""
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def list_users():
    """Lists all the users"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/user/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    """Deletes selected user"""
    data_manager.delete_user(user_id)
    return redirect(url_for('list_users'))


@app.route('/movies', methods=['GET'])
def list_movies():
    """Lists all the added movies"""
    movies = data_manager.get_all_movies()
    users = data_manager.get_all_users()
    return render_template('movies.html', movies=movies, users=users)


@app.route('/movies/<movie_id>')
def list_reviews(movie_id):
    """Lists all the reviews for the selected"""
    reviews = data_manager.list_reviews(movie_id)
    movie = data_manager.get_movie_info(movie_id)
    return render_template('list_reviews.html', reviews=reviews, movie=movie)


@app.route('/movies/<movie_id>/add_review', methods=['GET', 'POST'])
def add_review(movie_id):
    """Adds a review to the selected movie"""
    if request.method == 'POST':
        user_id = request.form.get("user_id")
        rating = request.form.get("rating")
        review_text = request.form.get("review_text")

        data_manager.add_review(user_id, movie_id, rating, review_text)

        movies = data_manager.get_all_movies()
        users = data_manager.get_all_users()
        return redirect(url_for('list_movies', movies=movies, users=users))

    users = data_manager.get_all_users()
    return render_template('add_review.html', movie_id=movie_id, users=users)


@app.route('/movies/<movie_id>/delete_review/<review_id>', methods=['POST'])
def delete_review(movie_id, review_id):
    """Deletes a specified review"""
    data_manager.delete_review(review_id)

    reviews = data_manager.list_reviews(movie_id)
    movie = data_manager.get_movie_info(movie_id)
    return redirect(url_for('list_reviews', reviews=reviews, movie_id=movie.id))


@app.route('/movies/<movie_id>/update_review/<review_id>', methods=['GET', 'POST'])
def update_review(movie_id, review_id):
    """Updates selected review"""
    if request.method == 'POST':
        new_rating = request.form.get('rating')
        new_text = request.form.get('review_text')
        data_manager.update_review(review_id, new_rating, new_text)
        reviews = data_manager.list_reviews(movie_id)
        movie = data_manager.get_movie_info(movie_id)
        return redirect(url_for('list_reviews', reviews=reviews, movie_id=movie.id))
    review = data_manager.get_review(review_id)
    rating = review.rating
    return render_template('update_review.html', review=review, movie_id=movie_id, review_id=review_id)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    """Lists all the users"""
    user_movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_username_by_id(user_id)
    user_name = user.username + "'" + "s"
    return render_template('user_movies.html', user_movies=user_movies, user_name=user_name, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Opens a form to add a new user to the list of users"""
    if request.method == 'POST':
        username = request.form.get("username")
        data_manager.add_user(username=username)
        return redirect(url_for("list_users"))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """This is found inside the users favorite movies, but it opens a form that allows you to enter
    the title and year of the movie to add it to the user's list of movies.Also, the year for the movie
    is there to help with movies with the same title but released in different years but the year
    is NOT required, just a suggestion if you know the year that the movie was released.There is also the code
    to check if a movie is in the list already, this is because the user can update the name of a movie if they
    choose to do so"""
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        SEARCH_URL = "http://www.omdbapi.com/?t="
        API_KEY = "a27c1668"
        if year is not None:
            movie_to_be_added = f"{title}&y={year}&apikey={API_KEY}"
        else:
            movie_to_be_added = f"{title}&apikey={API_KEY}"
        url = f"{SEARCH_URL}{movie_to_be_added}"
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            returned_movie_info = res.json()
            if "Error" in returned_movie_info.keys():
                return "The movie entered does not exist or could not be found"
        user_movies = data_manager.get_user_movies(user_id)
        user_name = data_manager.get_username_by_id(user_id)
        try:
            data_manager.add_movie(returned_movie_info, user_id)
        except sqlalchemy.exc.IntegrityError:
            return "Another user already has this movie in their list, please try adding a different movie"
        return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)


#
#
@app.route('/users/<user_id>/update_movie/<movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """This updates the title and rating of a movie and makes sure that the rating is a number.
    Also, I included the title becuase an entire html page that is used to only update the rating would
    look empty and redundant.The title is also there because maybe the user has a nickname for the movie
    or want to change the name of the movie for some reason."""
    if request.method == "POST":
        title = request.form.get('title')
        rating = request.form.get('rating')
        try:
            rating = float(rating)
        except ValueError:
            return "The wrong type of data was entered, the rating MUST be a number"
        data_manager.update_movie(movie_id, title, rating)
        return redirect(url_for('list_user_movies', user_id=user_id))
    movie_info = data_manager.get_movie_info(movie_id)
    movie_data = {'title': movie_info.title,
                  'rating': movie_info.rating
                  }
    return render_template('update_movie.html', movie_id=movie_id, user_id=user_id, movie=movie_data)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    """Deletes a specified movie"""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Returns a very simple template to show that the page couldn't be found"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
