from baelfire.recipe import Recipe
from baelfire.application.application import Application

from .tasks import (
    Create,
    SetupPy,
    Directories,
    Inits,
)

from .git import (
    Ignore,
    Init,
    Commit,
    Develop as GitDevelop,
)

from .datafile import DataFile

from .virtualenv import Virtualenv, Develop


class ProjectRecipe(Recipe):

    prefix = '/pyproject'

    def __init__(self, is_parent=True, python_version='3.4'):
        self.python_version = python_version
        super().__init__(is_parent=is_parent)

    def final_settings(self):
        self.settings['python_version'] = self.python_version

    def create_settings(self):
        self.set_path('virtualenvdir', 'cwd', 'venv')
        self.set_path('src', 'cwd', 'src')
        self.set_path('flagsdir', 'cwd', 'flags')

        self.set_path('project:setuppy', 'cwd', 'setup.py')
        self.set_path('project:config', 'cwd', '.pyproject.json')

        self.set_path('flags:develop', 'flagsdir', 'develop.flag')
        self.set_path('flags:git', 'flagsdir', '.git.flag')

        self.set_path('virtualenv:bin', 'virtualenvdir', 'bin')
        self.set_path('exe:python', 'virtualenv:bin', 'python')
        self.set_path('exe:pip', 'virtualenv:bin', 'pip')

        self.settings['packages'] = []
        self.settings['dependency_links'] = []
        self.settings['directories'] = [
            'src',
            'flagsdir',
            'project:home',
        ]
        self.settings['entry_points'] = ''

        self.datafile = DataFile('project:config', self)
        self.datafile.run()

        self.paths['project:home'] = ['%(src)s', '%(package:name)s']
        self.paths.set_path('virtualenvdir', 'cwd', 'venv_%(package:name)s')
        self.set_path('exe:python', 'virtualenv:bin', 'python')
        self.set_path('exe:pip', 'virtualenv:bin', 'pip')

    def gather_tasks(self):
        self.add_task(Create)
        self.add_task(SetupPy)
        self.add_task(Directories)
        self.add_task(Inits)
        self.add_task(Ignore)
        self.add_task(Init)
        self.add_task(Commit)
        self.add_task(Virtualenv)
        self.add_task(Develop)
        self.add_task(GitDevelop)


def run():
    Application(recipe=ProjectRecipe())()
