#!"C:\Synthesis\Python25\python.exe"

import sys
sys.path[0:0] = [
  'c:\\joe\\installer\\buildout\\eggs\\sqlalchemy-0.4.7p1-py2.5.egg',
  'c:\\joe\\installer\\buildout\\eggs\\sqlalchemy_migrate-0.4.5-py2.5.egg',
  'c:\\joe\\installer\\buildout\\eggs\\python_dateutil-1.5-py2.5.egg',
  'c:\\joe\\installer\\buildout\\{buildout:directory}\\src\\synthesis',
  ]

import migrate.versioning.shell

if __name__ == '__main__':
    migrate.versioning.shell.main()
