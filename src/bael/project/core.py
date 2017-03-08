from bael import project
from baelfire.core import Core
from baelfire.filedict import FileDict
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join


class ProjectCore(Core):

    def phase_settings(self):
        super().phase_settings()
        data = self.get_data_settings()

        self.settings['project_name'] = data['name']
        self.settings['package_name'] = data['package name']

        self.paths.set('cwd', dirname(self.find_pyproject_file()))
        self.paths.set('report', '.bael.yml', 'cwd')
        self.paths.set('pyproject', dirname(project.__file__))
        self.paths.set('pyptemplates', 'templates', 'pyproject')

        self.paths.set('package:src', 'src', 'cwd')
        self.paths.set_generator('package:main', lambda paths: self.settings['package_name'], 'package:src')
        self.paths.set(
            'template_setuppy',
            'setuppy.jinja2',
            'pyptemplates',
        )
        self.paths.set('setuppy', 'setup.py', 'cwd')

        self.paths.set_generator(
            'virtualenv:base',
            lambda paths: 'venv_{0}'.format(self.settings['package_name']),
            'cwd',
        )
        self.paths.set('virtualenv:bin', 'bin', 'virtualenv:base')
        self.paths.set('exe:python', 'python', 'virtualenv:bin')
        self.paths.set('exe:pip', 'pip', 'virtualenv:bin')

    def get_data_settings(self):
        path = self.find_pyproject_file()
        data = FileDict(path)
        data.load(True)
        data.ensure_key_exists('name', 'Project name')
        data.ensure_key_exists('package name', 'Package name')
        data.save()
        return data

    def find_pyproject_file(self, path=None):
        if not path:
            path = abspath('./')
        file_path = join(path, '.pyproject.yaml')
        if exists(file_path):
            return file_path
        else:
            toppath = dirname(path)
            if toppath == path:
                return '.pyproject.yaml'
            return self.find_pyproject_file(toppath)
