from os import mkdir, path

from baelfire.dependencies import PathsBasedFileDoesNotExists
from baelfire.task import Task
from baelfire.template import TemplateTask


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


class Inits(Task):
    hide = True
    name = 'Creating __init__ files'

    def get_paths(self):
        for dir_path in self._task_paths:
            yield dir_path

    def generate_dependencies(self):
        self._task_paths = []
        url = Directories
        for directory in self.task(url).directories:
            name = '%schild:initpy' % (directory,)
            self.recipe.set_path(name, directory, '__init__.py')
            if self.paths[name].startswith(self.paths['project:home']):
                self.add_dependecy(
                    PathsBasedFileDoesNotExists(self.paths, name))
                self._task_paths.append(self.paths[name])

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
