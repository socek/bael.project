from os import mkdir, path

from baelfire.task import Task
from baelfire.template import TemplateTask
from baelfire.dependencies import (
    AlwaysRebuild,
    FileDoesNotExists,
)


class GatherData(Task):
    hide = True
    name = 'Gather data'

    def make(self):
        self.ask_for_setting('project_name', 'Project name')
        self.settings['package_name'] = self.settings['project_name'].lower()
        self.paths['project_home'] = [
            '%(src)s',
            self.settings['package_name']]

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())


class SetupPy(TemplateTask):
    hide = True
    name = 'Creating setup.py file'

    def __init__(self, *args, **kwargs):
        kwargs['check_template'] = False
        super().__init__(*args, **kwargs)

    def get_output_file(self):
        return self.paths['setuppy']

    def get_template_path(self):
        return self.paths['setuppy']

    def pre_invoked_tasks(self):
        self.invoke_task(GatherData)


class Directories(Task):
    hide = True
    name = 'Creating directories'

    directorie_names = [
        'src',
        'flags',
        'project_home',
    ]

    @property
    def directories(self):
        for name in self.directorie_names:
            yield self.paths[name]

    def generate_dependencies(self):
        for directory in self.directories:
            self.add_dependecy(FileDoesNotExists(directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(directory):
                mkdir(directory)

    def pre_invoked_tasks(self):
        self.invoke_task(GatherData)


class Inits(Task):
    hide = True
    name = 'Creating __init__ files'

    def paths(self):
        url = Directories
        for directory in self.task(url).directories:
            yield path.join(directory, '__init__.py')

    def generate_dependencies(self):
        for file_path in self.paths():
            self.add_dependecy(FileDoesNotExists(file_path))

    def generate_links(self):
        self.add_link(Directories)

    def make(self):
        for file_path in self.paths():
            self.touch(file_path)


class Create(Task):

    help = 'Creates sample python repository'

    def generate_dependencies(self):
        pass

    def generate_links(self):
        self.add_link(SetupPy)
        self.add_link(Inits)
