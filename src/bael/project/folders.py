from os import mkdir

from baelfire.dependencies import FileDoesNotExists
from baelfire.dependencies import RunBefore
from baelfire.task import Task


class SrcFolderTask(Task):

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists('package:src'))

    def build(self):
        mkdir(self.paths['package:src'])


class MainFolderTask(Task):

    def create_dependecies(self):
        self.add_dependency(RunBefore(SrcFolderTask()))
        self.add_dependency(FileDoesNotExists('package:main'))

    def build(self):
        mkdir(self.paths.get('package:main'))
