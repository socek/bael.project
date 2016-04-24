from baelfire.dependencies import FileDoesNotExists
from baelfire.task import SubprocessTask


class BaseVirtualenv(SubprocessTask):

    def phase_settings(self):
        super().phase_settings()

        self.paths.set_path(
            'virtualenv:base',
            'cwd',
            'venv_%(settings:package_name)s',
        )
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
        self.add_dependency(FileDoesNotExists('virtualenv:base'))

    def build(self):
        cmd = 'virtualenv ' + self.paths['virtualenv:base']
        self.popen([cmd])
