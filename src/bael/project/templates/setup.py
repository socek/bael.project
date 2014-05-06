# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
]

if __name__ == '__main__':
    setup(name='{{settings["project_name"]}}',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'{{settings["package_name"]}}': 'src'},
          namespace_packages=['{{settings["package_name"]}}'],
          install_requires=install_requires,
          include_package_data=True,
          )
