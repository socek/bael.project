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
        self.paths['virtualenv_path'] = 'venv'
        self.paths['setuppy'] = 'setup.py'
        self.paths['src'] = 'src'
        self.paths['project_home'] = ['%(src)s']
        self.paths['flags'] = 'flags'
        self.paths['develop_flag'] = ['%(flags)s', 'develop.flag']

        self.paths['VEbin'] = ['%(virtualenv_path)s', 'bin']
        self.paths['VEpython'] = ['%(VEbin)s', 'python']
        self.paths['VEpip'] = ['%(VEbin)s', 'pip']

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
