# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
]

if __name__ == '__main__':
    setup(name='{{settings["project_name"]}}',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          include_package_data=True,
          )
