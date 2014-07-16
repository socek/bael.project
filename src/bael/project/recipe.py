from baelfire.recipe import Recipe
from baelfire.application.application import Application

from .tasks import (
    Create,
    SetupPy,
    GatherData,
    Directories,
    Inits,
)

from .git import (
    Ignore,
    Init,
    Commit,
    Develop as GitDevelop,
)

from .virtualenv import Virtualenv, Develop


class ProjectRecipe(Recipe):

    def __init__(self, python_version='3.4'):
        self.python_version = python_version
        super().__init__()

    def final_settings(self):
        self.settings['python_version'] = self.python_version

    def create_settings(self):
        self.set_path('virtualenv', 'cwd', 'venv')
        self.set_path('src', 'cwd', 'src')
        self.set_path('flags', 'cwd', 'flags')

        self.set_path('project:setuppy', 'cwd', 'setup.py')

        self.set_path('flags:develop', 'flags', 'develop.flag')
        self.set_path('flags:git', 'flags', '.git.flag')

        self.set_path('virtualenv:bin', 'virtualenv', 'bin')
        self.set_path('exe:python', 'virtualenv:bin', 'python')
        self.set_path('exe:pip', 'virtualenv:bin', 'pip')

    def gather_recipes(self):
        self.add_task(Create)
        self.add_task(SetupPy)
        self.add_task(GatherData)
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
