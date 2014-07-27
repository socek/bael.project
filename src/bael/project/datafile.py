import json
from os import path


class DataFile(object):

    def __init__(self, path, recipe):
        self.recipe = recipe
        self.settings = recipe.settings
        self.paths = recipe.paths
        self.path = path

    def run(self):
        if self.is_data_saved():
            data = self.load()
            self.settings['name'] = data['name']
            self.generate_settings()

    def is_data_saved(self):
        return path.exists(self.get_filepath())

    def get_filepath(self):
        return self.paths[self.path]

    def generate_settings(self):
        self.settings['package:name'] = self.settings['name'].lower()
        self.paths['project:home'] = [
            '%(src)s',
            self.settings['package:name']]

    def save(self, data):
        datafile = open(self.get_filepath(), 'w')
        json.dump(data, datafile)
        datafile.close()

    def load(self):
        with open(self.get_filepath(), 'r') as datafile:
            return json.load(datafile)
