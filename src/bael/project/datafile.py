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
        else:
            data = {}
        self.make_settings(data)
        self.generate_settings()
        self.save()

    def is_data_saved(self):
        return path.exists(self.get_filepath())

    def get_filepath(self):
        return self.paths[self.path]

    def _raw_save(self, data):
        datafile = open(self.get_filepath(), 'w')
        json.dump(data, datafile)
        datafile.close()

    def load(self):
        with open(self.get_filepath(), 'r') as datafile:
            return json.load(datafile)

    def ask_for(self, key, label):
        return input(label + ': ')

    def ask_for_setting(self, data, key, label):
        if key in data:
            self.settings[key] = data[key]
        else:
            self.settings[key] = self.ask_for(key, label)

    def generate_settings(self):
        self.settings['package:name'] = self.settings['name'].lower()
        self.paths['package:name'] = self.settings['package:name']

    def make_settings(self, data):
        self.ask_for_setting(data, 'name', 'Project name')

    def save(self):
        data = self.generate_data()
        self._raw_save(data)

    def generate_data(self):
        return {
            'name': self.settings['name'],
        }
