from os import mkdir, path

from baelfire.task import Task
from baelfire.template import TemplateTask
from baelfire.dependencys import (
    AlwaysRebuild,
    FileDoesNotExists,
    ParentFileChanged,
)


class Ignore(TemplateTask):
    hide = True
    name = 'Creating .gitignore file'
    path = '/git/ignore'

    def get_output_file(self):
        return '.gitignore'

    def get_template_path(self):
        return '.gitignore.tpl'


class Init(Task):
    hide = True
    name = 'Initializing git repository'
    path = '/git/init'

    def get_output_file(self):
        return '.git'

    def generate_dependencys(self):
        self.add_dependecy(
            ParentFileChanged(self.recipe.get_task('/git/ignore')))

    def make(self):
        self.command(['git init'])


class Commit(Task):
    name = 'Git initial commit'
    path = '/git'
    help = 'Creates sample python repository with git'

    def get_output_file(self):
        return '.git.flag'

    def generate_dependencys(self):
        self.add_dependecy(FileDoesNotExists(self.get_output_file()))
        self.add_dependecy(
            FileDoesNotExists(
                self.recipe.get_task('/git/init').get_output_file()))

    def generate_links(self):
        self.add_link('/create')
        self.add_link('/git/init')

    def make(self):
        self.command(['git add .'])
        self.command(['git commit -a -m "Initial commit."'])
        self.touch(self.get_output_file())
