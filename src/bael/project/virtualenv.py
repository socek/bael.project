from baelfire.dependencies import FileDoesNotExists
from baelfire.task import SubprocessTask


class BaseVirtualenv(SubprocessTask):

    def python(self, command, *args, **kwargs):
        command = self.paths.get('exe:python') + ' ' + command
        return self.popen([command], *args, **kwargs)

    def pip(self, command, *args, **kwargs):
        command = self.paths.get('exe:pip') + ' ' + command
        return self.popen([command], *args, **kwargs)


class VirtualenvTask(BaseVirtualenv):

    def create_dependecies(self):
        self.add_dependency(FileDoesNotExists('virtualenv:base'))

    def build(self):
        cmd = 'virtualenv ' + self.paths.get('virtualenv:base')
        self.popen([cmd])
