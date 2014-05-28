from baelfire.task import Task
from baelfire.dependencies import ParentFileChanged


class Virtualenv(Task):
    name = 'Create virtualenv'
    help = 'Generates virtual envoritment'

    def get_output_file(self):
        return self.paths['virtualenv_path']

    def make(self):
        self.command(['virtualenv -p python%s %s' % (
            self.python_version(),
            self.paths['virtualenv_path'])]
        )

    def python_version(self):
        if self.kwargs.get('python_version', False):
            return self.kwargs['python_version'][0]
        else:
            return self.settings['python_version']


class VirtualenvTask(Task):

    def python(self, command, *args, **kwargs):
        command = self.paths['VEpython'] + ' ' + command
        return self.command([command], *args, **kwargs)

    def pip(self, command, *args, **kwargs):
        command = self.paths['VEpip'] + ' ' + command
        return self.command([command], *args, **kwargs)


class Develop(VirtualenvTask):
    name = 'Setup develop'
    help = 'Run setup.py develop with virtualenv'

    def get_output_file(self):
        return self.paths['develop_flag']

    def generate_dependencies(self):
        self.add_dependecy(
            ParentFileChanged(
                self.task(
                    'bael.project.tasks:SetupPy')))

    def generate_links(self):
        self.add_link('bael.project.tasks:Create')
        self.add_link('bael.project.virtualenv:Virtualenv')

    def make(self):
        self.python('%(setuppy)s develop' % self.paths)
        self.touchme()
