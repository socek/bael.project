from bael import project
from baelfire.core import Core
from baelfire.filedict import FileDict
from os.path import abspath
from os.path import dirname
from os.path import exists
from os.path import join


class ProjectCore(Core):

    def before_dependencies(self):
        super().before_dependencies()
        data = self.get_data_settings()

        self.paths['cwd'] = dirname(self.find_pyproject_file())
        self.paths['pyproject'] = dirname(project.__file__)
        self.paths.set_path('pyptemplates', 'pyproject', 'templates')
        self.settings['project_name'] = data['name']
        self.settings['package_name'] = data['package name']

        self.paths.set_path('package:src', 'cwd', 'src')
        self.paths.set_path('package:main', 'src', '%(settings:package_name)s')

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
