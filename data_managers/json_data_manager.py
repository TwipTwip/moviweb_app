import json
from moviweb_app.data_managers.data_manager_interface import DataManagerInterface


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
        return user_movies

    def get_username_by_id(self, user_id):
        with open(self.filename, "r") as user_info:
            users = json.loads(user_info.read())
        for user in users:
            for id in user:
                if str(user_id) == str(id):
                    user_name = user[id]['name']
                    return user_name
        return None

