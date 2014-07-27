from os import mkdir, path

from bael.project.datafile import DataFile
from baelfire.dependencies import PathsBasedFileDoesNotExists
from baelfire.task import Task
from baelfire.template import TemplateTask


class GatherData(Task):
    hide = True
    name = 'Gather data'

    def get_output_file(self):
        return self.paths['project:config']

    def make(self):
        self.ask_for_setting('name', 'Project name')
        datafile = DataFile('project:config', self.recipe)
        datafile.generate_settings()
        datafile.save({
            'name': self.settings['name'],
        })


class SetupPy(TemplateTask):
    hide = True
    name = 'Creating setup.py file'

    def __init__(self, *args, **kwargs):
        kwargs['check_template'] = False
        super().__init__(*args, **kwargs)

    def get_output_file(self):
        return self.paths['project:setuppy']

    def get_template_path(self):
        return 'setup.py'

    def pre_invoked_tasks(self):
        self.invoke_task(GatherData)


class Directories(Task):
    hide = True
    name = 'Creating directories'

    @property
    def directories(self):
        for name in self.settings['directories']:
            yield name

    def generate_dependencies(self):
        for directory in self.directories:
            self.add_dependecy(PathsBasedFileDoesNotExists(
                self.paths,
                directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(self.paths[directory]):
                mkdir(self.paths[directory])

    def generate_links(self):
        self.add_link(GatherData)


class Inits(Task):
    hide = True
    name = 'Creating __init__ files'

    def get_paths(self):
        url = Directories
        for directory in self.task(url).directories:
            name = '%s:initpy' % (directory,)
            yield self.paths[name]

    def generate_dependencies(self):
        url = Directories
        for directory in self.task(url).directories:
            name = '%s:initpy' % (directory,)
            self.recipe.set_path(name, directory, '__init__.py')
            self.add_dependecy(PathsBasedFileDoesNotExists(self.paths, name))

    def generate_links(self):
        self.add_link(Directories)

    def make(self):
        for file_path in self.get_paths():
            self.touch(file_path)


class Create(Task):

    help = 'Creates sample python repository'

    def generate_dependencies(self):
        pass

    def generate_links(self):
        self.add_link(SetupPy)
        self.add_link(Inits)
