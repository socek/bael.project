from baelfire.dependencies.task import RunBefore
from baelfire.task.template import FirstTemplateTask

from .base import ProjectBase


class SetupPy(FirstTemplateTask):
    source_name = 'template_setuppy'
    output_name = 'setuppy'

    def create_dependecies(self):
        super().create_dependecies()
        self.add_dependency(RunBefore(ProjectBase()))

    def phase_settings(self):
        super().phase_settings()
        self.paths.set_path('template_setuppy', 'pyptemplates', 'setuppy.jinja2')
        self.paths.set_path('setuppy', 'cwd', 'setup.py')
