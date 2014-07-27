# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

install_requires = [
    {% for package in settings["packages"] -%}
        '{{package}}',
    {% endfor %}
]
dependency_links = [
    {% for link in settings["dependency_links"] -%}
        '{{link}}',
    {% endfor %}
]

if __name__ == '__main__':
    setup(name='{{settings["name"]}}',
          version='0.1',
          packages=find_packages('src'),
          package_dir={'': 'src'},
          install_requires=install_requires,
          dependency_links=dependency_links,
          include_package_data=True,
          entry_points="""\
          {{settings["entry_points"]}}
          """,
          )
