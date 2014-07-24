from baelfire.task import Task
from baelfire.template import TemplateTask


class Ignore(TemplateTask):
    hide = True
    name = 'Creating .gitignore file'
    path = '/git/ignore'

    def get_output_file(self):
        return '.gitignore'

    def get_template_path(self):
        return 'gitignore.tpl'


class Init(Task):
    hide = True
    name = 'Initializing git repository'
    path = '/git/init'

    def get_output_file(self):
        return '.git'

    def generate_links(self):
        self.add_link('bael.project.git:Ignore')

    def make(self):
        self.command(['git init'])


class Commit(Task):
    name = 'Git initial commit'
    path = '/git'
    help = 'Creates sample python repository with git'

    def get_output_file(self):
        return self.paths['flags:git']

    def generate_links(self):
        self.add_link('bael.project.tasks:Create')
        self.add_link('bael.project.git:Init')

    def make(self):
        self.command(['git add .'])
        self.command(['git commit -a -m "Initial commit by PyProject."'])
        self.touchme()


class Develop(Task):
    name = 'Develop with git'
    path = '/develop/git'
    help = 'Run setup.py develop with virtualenv with git repository'

    def generate_links(self):
        self.add_link('bael.project.virtualenv:Develop')
        self.add_link(Commit)

    def make(self):
        pass
