from os import getcwd
from os.path import dirname

from baelfire.task import Task

from bael import project


class ProjectBase(Task):

    def phase_settings(self):
        super().phase_settings()
        self.paths['cwd'] = getcwd()
        self.paths['project'] = dirname(project.__file__)
        self.paths.set_path('templates', 'project', 'templates')

    def create_dependecies(self):
        pass

    def build(self):
        pass
