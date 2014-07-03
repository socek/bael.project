1. bael.project
===============
bael.project is simple example for Baelfire framework. This project provide simple
command line tool for auto-creation Python projects.

2. Command line tool
====================
pyproject is a script using bael.project recipe
::
    $ pyproject -l
     Name                 Path           Help
     ----                 ----           ----
     Create virtualenv    /virtualenv    Generates virtual envoritment
     Create               /create        Creates sample python repository
     Git initial commit   /git           Creates sample python repository with git
     Develop with git     /develop/git   Run setup.py develop with virtualenv with git repository
     Setup develop        /develop       Run setup.py develop with virtualenv

3. Creating bare project
========================
bael.project asume that Python project needs to have setu.py and src directory.
When creating new project, pyproject will ask for project name, ane write it into
setup.py file
::
    $ pyproject /create
    * Gather data
    Project name: myproject
    * Creating setup.py file
    * Creating directories
    * Creating __init__ files

or you can provide project name in command line like this:
::
    $ pyproject /create /gatherdata?project_name=myproject
    * Gather data
    * Creating setup.py file
    * Creating directories
    * Creating __init__ files

/gatherdata is another task, which is here only to ask for project name

4. Creating project with virtualenv
===================================
Often we need to have project with virtualenv. /virtualenv task will create it
for us. /develop will run "setup.py develop" for us. It will be runned every time
when we change the setup.py (where we can change package dependencies).
::
    $ pyproject /develop /gatherdata?project_name=myproject
    * Gather data
    * Creating setup.py file
    * Creating directories
    * Creating __init__ files
    * Create virtualenv
    Running virtualenv with interpreter /usr/bin/python3.4
    Using base prefix '/usr'
    New python executable in venv/bin/python3.4
    Also creating executable in venv/bin/python
    Installing setuptools, pip...done.
    * Setup develop
    running develop
    running egg_info
    creating src/myproject.egg-info
    writing dependency_links to src/myproject.egg-info/dependency_links.txt
    writing top-level names to src/myproject.egg-info/top_level.txt
    writing src/myproject.egg-info/PKG-INFO
    writing manifest file 'src/myproject.egg-info/SOURCES.txt'
    reading manifest file 'src/myproject.egg-info/SOURCES.txt'
    writing manifest file 'src/myproject.egg-info/SOURCES.txt'
    running build_ext
    Creating /tmp/red/venv/lib/python3.4/site-packages/myproject.egg-link (link to src)
    Adding myproject 0.1 to easy-install.pth file

    Installed /tmp/red/src
    Processing dependencies for myproject==0.1
    Finished processing dependencies for myproject==0.1
    $ pyproject /develop /gatherdata?project_name=myproject
    * Gather data
    $ touch setup.py
    $ pyproject /develop /gatherdata?project_name=myproject
    * Setup develop
    running develop
    running egg_info
    writing src/myproject.egg-info/PKG-INFO
    writing dependency_links to src/myproject.egg-info/dependency_links.txt
    writing top-level names to src/myproject.egg-info/top_level.txt
    reading manifest file 'src/myproject.egg-info/SOURCES.txt'
    writing manifest file 'src/myproject.egg-info/SOURCES.txt'
    running build_ext
    Creating /tmp/red/venv/lib/python3.4/site-packages/myproject.egg-link (link to src)
    myproject 0.1 is already the active version in easy-install.pth

    Installed /tmp/red/src
    Processing dependencies for myproject==0.1
    Finished processing dependencies for myproject==0.1
    * Gather data

5. Drawning graphs
==================
We can draw a task graph of actual (or last) command.
::
    $ pyproject -g
    $ ls .baelfire.lastlog.png
    .baelfire.lastlog.png
