from baelfire.dependencies import FileChanged
from baelfire.dependencies import RunBefore
from baelfire.dependencies import TaskDependency
from baelfire.task import Task

from .folders import FillWithInitsTask
from .project import SetupPy
from .virtualenv import BaseVirtualenv
from .virtualenv import VirtualenvTask


class Create(Task):

    def create_dependecies(self):
        self.add_dependency(TaskDependency(VirtualenvTask()))
        self.add_dependency(TaskDependency(SetupPy()))
        self.add_dependency(RunBefore(FillWithInitsTask()))

    def build(self):
        pass


class Develop(BaseVirtualenv):
    output_name = 'exe:python'

    @property
    def output(self):
        return self.paths[self.output_name]

    def create_dependecies(self):
        self.add_dependency(TaskDependency(Create()))
        self.add_dependency(FileChanged('setuppy'))

    def build(self):
        cmd = '%(setuppy)s develop' % self.paths
        self.python(cmd)
        self.popen(['touch %(exe:python)s' % self.paths])
