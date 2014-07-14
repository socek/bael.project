# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    'baelfire==0.2',
    'virtualenv',
]

if __name__ == '__main__':
    setup(name='bael.project',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          namespace_packages=['bael'],
          install_requires=install_requires,
          include_package_data=True,
          zip_safe=False,
          package_data={
              '': ['.gitignore.tpl'],
          },
          entry_points="""\
              [console_scripts]
                  pyproject = bael.project.recipe:run
          """,
          )
