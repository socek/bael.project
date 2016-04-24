from baelfire.task.template import FirstTemplateTask


class SetupPy(FirstTemplateTask):
    source_name = 'template_setuppy'
    output_name = 'setuppy'

    def phase_settings(self):
        super().phase_settings()
        self.paths.set_path(
            'template_setuppy',
            'pyptemplates',
            'setuppy.jinja2',
        )
        self.paths.set_path('setuppy', 'cwd', 'setup.py')
