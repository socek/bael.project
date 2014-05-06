from os import mkdir, path

from baelfire.task import Task
from baelfire.template import TemplateTask
from baelfire.dependencys import (
    AlwaysRebuild,
    FileDoesNotExists,
    ParentFileChanged,
)


class GatherData(Task):
    hide = True
    name = 'Gather data'

    def make(self):
        self.settings['project_name'] = input('Project name: ')
        self.settings['package_name'] = self.settings['project_name'].lower()

    def generate_dependencys(self):
        self.add_dependecy(AlwaysRebuild())


class SetupPy(TemplateTask):
    hide = True
    name = 'Creating setup.py file'

    def get_output_file(self):
        return 'setup.py'

    def get_template_path(self):
        return 'setup.py'

    def generate_links(self):
        self.add_link('/gatherdata')


class Directories(Task):
    hide = True
    name = 'Creating directories'

    directories = [
        'src'
    ]

    def generate_dependencys(self):
        for directory in self.directories:
            self.add_dependecy(FileDoesNotExists(directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(directory):
                mkdir(directory)


class Inits(Task):
    hide = True
    name = 'Creating __init__ files'

    def paths(self):
        for directory in Directories.directories:
            yield path.join(directory, '__init__.py')

    def generate_dependencys(self):
        for file_path in self.paths():
            self.add_dependecy(FileDoesNotExists(file_path))

    def generate_links(self):
        self.add_link('/directories')

    def make(self):
        for file_path in self.paths():
            self.touch(file_path)


class Create(Task):

    help = 'Creates sample python repository'

    def generate_dependencys(self):
        pass

    def generate_links(self):
        self.add_link('/setuppy')
        self.add_link('/inits')


class GitIgnore(TemplateTask):
    hide = True
    name = 'Creating .gitignore file'

    def get_output_file(self):
        return '.gitignore'

    def get_template_path(self):
        return '.gitignore.tpl'


class GitInit(Task):
    hide = True
    name = 'Initializing git repository'

    def get_output_file(self):
        return '.git'

    def generate_dependencys(self):
        self.add_dependecy(
            ParentFileChanged(self.recipe.get_task('/gitignore')))

    def make(self):
        self.command(['git init'])


class GitCommit(Task):
    name = 'Git initial commit'
    path = '/git'
    help = 'Creates sample python repository with git'

    def get_output_file(self):
        return '.git.flag'

    def generate_dependencys(self):
        self.add_dependecy(FileDoesNotExists(self.get_output_file()))
        self.add_dependecy(ParentFileChanged(self.recipe.get_task('/gitinit')))

    def generate_links(self):
        self.add_link('/create')

    def make(self):
        self.command(['git add .'])
        self.command(['git commit -a -m "Initial commit."'])
