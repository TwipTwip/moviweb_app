import json
from moviweb_app.data_managers.data_manager_interface import DataManagerInterface


# data = [
#     {1: {"name": "Alice", "movies": {"id": 4,
#                                      "director": "somebody",
#                                      "title": "movie title",
#                                      "year": 2004}}},
#     {2: {"name": "Bob", "movies": {"id": 4,
#                                    "director": "somebody",
#                                    "title": "movie title",
#                                    "year": 2004}}}
# ]
# with open("users.json", "w") as rewrite:
#     json.dump(data, rewrite)


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    # noinspection PyTypeChecker
    def get_all_users(self):
        # Return a list of all users
        with open(self.filename, "r") as user_info:
            users = json.loads(user_info.read())
        all_movie_info = []
        counter = -1
        id_counter = 0
        str_counter = 0
        for user in users:
            # id_counter += 1
            # counter += 1
            # str_counter = int(str_counter)
            # str_counter += 1
            # str_counter = str(str_counter)
            # movie_data = {"id": id_counter, "name": users[counter][str_counter]['name']}
            all_movie_info.append(user)
        return all_movie_info

    def get_user_movies(self, user_id):
        # Return a list of all movies for a given user
        with open(self.filename, "r") as user_info:
            users = json.loads(user_info.read())
        counter = -1
        for user in users:
            for key in user.keys():
                counter += 1
                if str(user_id) == str(key):
                    user_movies = users[counter][key]['movies']
                    # for movie in user_movies:
                    #     print(f"{movie['title']}({movie['year']}), "
                    #           f"Director: {movie['director']}, Movie ID: {movie['id']}")
        return user_movies

    def add_user(self):
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
        return None

    def get_username_by_id(self, user_id):
        with open(self.filename, "r") as user_info:
            users = json.loads(user_info.read())
        for user in users:
            for id in user:
                if str(user_id) == str(id):
                    user_name = user[id]['name']
                    return user_name
        return None

    """These function don't technically work, I just moved them in here so I still have the code
    for the json files"""
    # def add_movie(self):
    #     # This entire section of code is here for if a new user is added and their list is empty
    #     if len(user_movies) == 0:
    #         user_movies = []
    #         movie_data = {"id": 1,
    #                       "title": returned_movie_info["Title"],
    #                       "director": returned_movie_info["Director"],
    #                       "year": int(returned_movie_info["Year"]),
    #                       "poster": returned_movie_info["Poster"],
    #                       "rating": float(returned_movie_info["imdbRating"])}
    #         user_movies.append(movie_data)
    #         with open("storage/users.json", "r") as new_movie:
    #             users = json.loads(new_movie.read())
    #             users = list(users)
    #             for user in users:
    #                 for user_info in user:
    #                     if user[user_info]['name'] == user_name:
    #                         user[user_info]['movies'] = user_movies
    #                         user_id = user_info
    #                         other_id = user_info
    #         with open("storage/users.json", "w") as new_data:
    #             new_data.write(json.dumps(users))
    #         return redirect(url_for('list_user_movies', user_id=user_id))
    #     user_movies = list(user_movies)
    #
    #     # This is where the 'regular' code returns if the user has movies in their list
    #     movie_ids = []
    #     for movie in user_movies:
    #         movie_ids.append(movie['id'])
    #     new_movie_id = max(movie_ids) + 1
    #     movie_data = {"id": new_movie_id,
    #                   "title": returned_movie_info["Title"],
    #                   "director": returned_movie_info["Director"],
    #                   "year": int(returned_movie_info["Year"]),
    #                   "poster": returned_movie_info["Poster"],
    #                   "rating": float(returned_movie_info["imdbRating"])}
    #     user_movies.append(movie_data)
    #     with open("storage/users.json", "r") as new_movie:
    #         users = json.loads(new_movie.read())
    #         users = list(users)
    #         for user in users:
    #             for user_info in user:
    #                 if user[user_info]['name'] == user_name:
    #                     user[user_info]['movies'] = user_movies
    #                     user_id = user_info
    #                     other_id = user_info
    #     with open("storage/users.json", "w") as new_data:
    #         new_data.write(json.dumps(users))
    #
    # def update_movie(self):
    #     movies = data_manager.get_user_movies(user_id)
    #     movies_to_keep = []
    #     for movie in movies:
    #         movies_to_keep.append(movie)
    #         for movie in movies_to_keep:
    #             if int(movie['id']) == int(movie_id):
    #                 movie['title'] = title
    #                 movie['rating'] = rating
    #         with open("storage/users.json", "r") as user_data:
    #             users = json.loads(user_data.read())
    #             for user in users:
    #                 for user_info in user:
    #                     if int(user_info) == int(user_id):
    #                         user[user_info]['movies'] = movies_to_keep
    #         with open("storage/users.json", "w") as new_info:
    #             new_info.write(json.dumps(users))
    #             for movie in movies:
    #                 if int(movie['id']) == int(movie_id):
    #                     movie_info = movie
    #             print(movie_info)
    #
    # def delete_movie(self):
    #     movies = data_manager.get_user_movies(user_id)
    #     user_name = data_manager.get_username_by_id(user_id)
    #     counter = -1
    #     for movie in movies:
    #         counter += 1
    #         if int(movie['id']) == int(movie_id):
    #             del movies[counter]
    #     with open("storage/users.json", "r") as info:
    #         users = json.loads(info.read())
    #         for user in users:
    #             for user_info in user:
    #                 if user_name == user[user_info]['name']:
    #                     user[user_info]['movies'] = movies
    #     with open("storage/users.json", "w") as new_data:
    #         new_data.write(json.dumps(users))

# JSONDataManager("users.json").get_all_users()
# JSONDataManager("../storage/users.json").get_user_movies(1)
