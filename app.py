from flask import Flask, render_template
from data_managers.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('storage/users.json')


@app.route('/')
def home():
    return "Welcome to Movie App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_username_by_id(user_id)
    user_name = user_name + "'" + "s"
    return render_template('user_movies.html', user_movies=user_movies, user_name=user_name)


# @app.route('/users/<user_id>/add_movie')
# def add_movie(user_id):
#     pass
#
#
# @app.route('/users/<user_id>/update_movie/<movie_id>')
# def update_movie(user_id, movie_id):
#     pass
#
#
# @app.route('/users/<user_id>/delete_movie/<movie_id')
# def delete_movie(user_id, movie_id):
#     pass


if __name__ == '__main__':
    app.run(debug=True)
