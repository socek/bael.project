from os import getcwd
from os.path import dirname

from baelfire.task import Task
from baelfire.filedict import FileDict

from bael import project


class ProjectBase(Task):

    def phase_settings(self):
        super().phase_settings()
        data = self.get_data_settings()

        self.paths['cwd'] = getcwd()
        self.paths['project'] = dirname(project.__file__)
        self.paths.set_path('templates', 'project', 'templates')
        self.settings['project_name'] = data['name']
        self.settings['package_name'] = data['package name']

        self.paths.set_path('package:src', 'cwd', 'src')
        self.paths.set_path('package:main', 'src', '%(settings:package_name)s')

    def get_data_settings(self):
        data = FileDict('.pyproject.yaml')
        data.load(True)
        data.ensure_key_exists('name', 'Project name')
        data.ensure_key_exists('package name', 'Package name')
        data.save()
        return data

    def create_dependecies(self):
        pass

    def build(self):
        pass
