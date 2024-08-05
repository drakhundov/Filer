import os
import pickle
import config


class Paths:
    def __init__(self):
        if os.path.exists(config.PATHS) and open(config.PATHS, "r").read():
            with open(config.PATHS, "rb") as paths_file:
                self.__data = pickle.load(paths_file)
        else:
            open(config.PATHS, "w").close()
            self.reset()

    def get_locations(self):
        return self.__data["locations"]

    def add_location(self, location):
        self.__data["locations"].add(location)

    def get_backup(self):
        return self.__data["backup"]

    def set_backup(self, backup):
        self.__data["backup"] = backup

    def reset(self):
        self.__data = {"locations": set(), "backup": None}

    def save_changes(self):
        if self.__data:
            with open(config.PATHS, "wb") as paths_file:
                pickle.dump(self.__data, paths_file)
