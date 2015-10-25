from .base import ProjectBase
from .project import SetupPy
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
        self.paths.set_path('virtualenv:base', 'cwd', 'venv')
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
        self.add_dependency(FileChanged('setuppy'))

    def build(self):
        cmd = '%(setuppy)s develop' % self.paths
        self.python(cmd)
        self.popen(['touch %(exe:python)s' % self.paths])

#     name = 'Setup develop'
#     help = 'Run setup.py develop with virtualenv'

#     def get_output_file(self):
#         return self.paths['flags:develop']

#     def generate_dependencies(self):
#         self.add_dependecy(
#             ParentFileChanged(
#                 self.task(
#                     'bael.project.tasks:SetupPy')))

#     def generate_links(self):
#         self.add_link('bael.project.tasks:Create')
#         self.add_link('bael.project.virtualenv:Virtualenv')

#     def make(self):
#         self.python('%(project:setuppy)s develop' % self.paths)
#         self.touchme()
