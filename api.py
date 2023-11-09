from flask import Blueprint, jsonify, render_template, request, redirect, url_for
import requests
import sqlalchemy
from moviweb_app.app import data_manager, api


"""Quick litte disclaimer, this file doesn't work and I can't figure out why, it's some weird problem
where none of the api urls don't work or load anything they just return a 404 error"""


@api.route('/api/users', methods=['GET'])
def get_users():
    """Lists all the users"""
    users = data_manager.get_all_users()
    return jsonify(users)


@api.route('/api/users/<user_id>')
def list_user_movies(user_id):
    """Lists all the users"""
    user_movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_username_by_id(user_id)
    user_name = user.username + "'" + "s"
    return jsonify(user_movies)


@api.route('/api/users/<user_id>/add_movie', methods=['GET', 'POST'])
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
        return jsonify(user_movies)
    return render_template('add_movie.html', user_id=user_id)
