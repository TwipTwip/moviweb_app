from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data/usermovies.sqlite"
MOVIE_API = "http://www.omdbapi.com/?apikey=a27c1668&t="


@app.route('/')
def home():
    """Simple home page. Also, this code ONLY works with json right now but the person using the
    website wouldn't be able to tell, this is just a little note. Another little side note is that if
    you want to see what the webpage looks like with 7 or more movies navigate to the user 'Dylan'(Me)
    and there are 8 movies in that user's favorite movies."""
    return render_template('home.html')


@app.route('/users', methods=['GET'])
def list_users():
    """Lists all the users"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    """Lists all the users"""
    user_movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_username_by_id(user_id)
    user_name = user_name + "'" + "s"
    return render_template('user_movies.html', user_movies=user_movies, user_name=user_name, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Opens a form to add a new user to the list of users"""
    if request.method == 'POST':
        with open("storage/users.json", "r") as user_info:
            users = json.loads(user_info.read())
            users = list(users)
            counter = 0
            for user in users:
                counter += 1
        new_id = counter + 1
        name = request.form.get('name')
        movies = []
        new_user = {new_id: {'name': name, 'movies': movies}}
        users.append(new_user)
        with open("storage/users.json", "w") as add:
            add.write(json.dumps(users))
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
        user_movies = list(user_movies)

        # This entire section of code is here for if a new user is added and their list is empty
        if len(user_movies) == 0:
            user_movies = []
            movie_data = {"id": 1,
                          "title": returned_movie_info["Title"],
                          "director": returned_movie_info["Director"],
                          "year": int(returned_movie_info["Year"]),
                          "poster": returned_movie_info["Poster"],
                          "rating": float(returned_movie_info["imdbRating"])}
            user_movies.append(movie_data)
            with open("storage/users.json", "r") as new_movie:
                users = json.loads(new_movie.read())
                users = list(users)
                for user in users:
                    for user_info in user:
                        if user[user_info]['name'] == user_name:
                            user[user_info]['movies'] = user_movies
                            user_id = user_info
                            other_id = user_info
            with open("storage/users.json", "w") as new_data:
                new_data.write(json.dumps(users))
            return redirect(url_for('list_user_movies', user_id=user_id))

        # This is where the 'regular' code returns if the user has movies in their list
        movie_ids = []
        for movie in user_movies:
            movie_ids.append(movie['id'])
        new_movie_id = max(movie_ids) + 1
        movie_data = {"id": new_movie_id,
                      "title": returned_movie_info["Title"],
                      "director": returned_movie_info["Director"],
                      "year": int(returned_movie_info["Year"]),
                      "poster": returned_movie_info["Poster"],
                      "rating": float(returned_movie_info["imdbRating"])}
        user_movies.append(movie_data)
        with open("storage/users.json", "r") as new_movie:
            users = json.loads(new_movie.read())
            users = list(users)
            for user in users:
                for user_info in user:
                    if user[user_info]['name'] == user_name:
                        user[user_info]['movies'] = user_movies
                        user_id = user_info
                        other_id = user_info
        with open("storage/users.json", "w") as new_data:
            new_data.write(json.dumps(users))
        return redirect(url_for('list_user_movies', user_id=other_id))
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
        movies = data_manager.get_user_movies(user_id)
        movies_to_keep = []
        for movie in movies:
            movies_to_keep.append(movie)
        title = request.form.get('title')
        rating = request.form.get('rating')
        try:
            rating = float(rating)
        except ValueError:
            return "The wrong type of data was entered, the rating MUST be a number"
        for movie in movies_to_keep:
            if int(movie['id']) == int(movie_id):
                movie['title'] = title
                movie['rating'] = rating
        with open("storage/users.json", "r") as user_data:
            users = json.loads(user_data.read())
            for user in users:
                for user_info in user:
                    if int(user_info) == int(user_id):
                        user[user_info]['movies'] = movies_to_keep
        with open("storage/users.json", "w") as new_info:
            new_info.write(json.dumps(users))
        return redirect(url_for('list_user_movies', user_id=user_id))
    movies = data_manager.get_user_movies(user_id)
    for movie in movies:
        if int(movie['id']) == int(movie_id):
            movie_info = movie
    print(movie_info)
    return render_template('update_movie.html', movie_id=movie_id, user_id=user_id, movie=movie_info)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    """Deletes a specified movie"""
    movies = data_manager.get_user_movies(user_id)
    user_name = data_manager.get_username_by_id(user_id)
    counter = -1
    for movie in movies:
        counter += 1
        if int(movie['id']) == int(movie_id):
            del movies[counter]
    with open("storage/users.json", "r") as info:
        users = json.loads(info.read())
        for user in users:
            for user_info in user:
                if user_name == user[user_info]['name']:
                    user[user_info]['movies'] = movies
    with open("storage/users.json", "w") as new_data:
        new_data.write(json.dumps(users))
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Returns a very simple template to show that the page couldn't be found"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
