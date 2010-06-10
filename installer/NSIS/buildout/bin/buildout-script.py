#!"C:\Synthesis\Python25\python.exe"

import sys
sys.path[0:0] = [
  'c:\\joe\\installer\\buildout\\eggs\\setuptools-0.6c11-py2.5.egg',
  'c:\\joe\\installer\\buildout\\eggs\\zc.buildout-1.5.0b2-py2.5.egg',
  ]

import zc.buildout.buildout

if __name__ == '__main__':
    zc.buildout.buildout.main()
