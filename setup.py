# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'baelfire>=0.4.1',
    'virtualenv',
]

if __name__ == '__main__':
    setup(
        name='bael.project',
        version='0.2.6',
        description='Simple project generator.',
        license='Apache License 2.0',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        namespace_packages=['bael'],
        install_requires=install_requires,
        zip_safe=False,
        package_data={
            '': ['project/templates/*.jinja2'],
        },
        entry_points="""\
              [console_scripts]
                  pyproject = bael.project.cmd:run
          """,
    )
