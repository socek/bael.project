from os import fwalk
from os import mkdir
from os import path

from baelfire.dependencies import FileDoesNotExists
from baelfire.dependencies import RunBefore
from baelfire.dependencies.file import FileDependency
from baelfire.task import Task


class MissingInitFiles(FileDependency):

    def should_build(self):
        try:
            for root, dirs, files, rootfd in fwalk(self.path):
                make = True
                for dirname in self.settings['ignore_inits_dirs']:
                    if dirname in root:
                        make = False
                        break
                if make and '__init__.py' not in files:
                    return True
        except FileNotFoundError:
            return True
        return False


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
        mkdir(self.paths['package:main'])


class FillWithInitsTask(Task):

    output_name = 'package:main'

    def create_dependecies(self):
        self.add_dependency(RunBefore(MainFolderTask()))
        self.add_dependency(MissingInitFiles(self.output_name))

    def phase_settings(self):
        super().phase_settings()
        self.settings['ignore_inits_dirs'] = [
            '__pycache__',
        ]

    def build(self):
        for root, dirs, files, rootfd in fwalk(self.paths[self.output_name]):
            make = True
            for dirname in self.settings['ignore_inits_dirs']:
                if dirname in root:
                    make = False
                    break
            if make and '__init__.py' not in files:
                open(path.join(root, '__init__.py'), 'w').close()
