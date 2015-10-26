from .base import ProjectBase
from .project import SetupPy
from .folders import FillWithInitsTask
from baelfire.dependencies import FileChanged
from baelfire.dependencies import FileDoesNotExists
from baelfire.dependencies import RunBefore
from baelfire.dependencies import TaskDependency
from baelfire.task import SubprocessTask


class BaseVirtualenv(SubprocessTask):

    def create_dependecies(self):
        self.add_dependency(RunBefore(ProjectBase()))

    def phase_settings(self):
        super().phase_settings()

        self.paths.set_path('virtualenv:base', 'cwd', 'venv_%(settings:package_name)s')
        self.paths.set_path('virtualenv:bin', 'virtualenv:base', 'bin')
        self.paths.set_path('exe:python', 'virtualenv:bin', 'python')
        self.paths.set_path('exe:pip', 'virtualenv:bin', 'pip')

    def python(self, command, *args, **kwargs):
        command = self.paths['exe:python'] + ' ' + command
        return self.popen([command], *args, **kwargs)

    def pip(self, command, *args, **kwargs):
        command = self.paths['exe:pip'] + ' ' + command
        return self.popen([command], *args, **kwargs)


class VirtualenvTask(BaseVirtualenv):

    def create_dependecies(self):
        super().create_dependecies()
        self.add_dependency(FileDoesNotExists('virtualenv:base'))

    def build(self):
        cmd = 'virtualenv ' + self.paths['virtualenv:base']
        self.popen([cmd])


class Develop(BaseVirtualenv):
    output_name = 'exe:python'

    @property
    def output(self):
        return self.paths[self.output_name]

    def create_dependecies(self):
        super().create_dependecies()
        self.add_dependency(TaskDependency(VirtualenvTask()))
        self.add_dependency(TaskDependency(SetupPy()))
        self.add_dependency(RunBefore(FillWithInitsTask()))
        self.add_dependency(FileChanged('setuppy'))

    def build(self):
        cmd = '%(setuppy)s develop' % self.paths
        self.python(cmd)
        self.popen(['touch %(exe:python)s' % self.paths])
