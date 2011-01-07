*adapted from: http://wiki.pylonshq.com/display/pylonscommunity/Howto+install+Pylons+with+buildout

Note: Synthesis currently runs only on unix platforms.  The hangup is Windows' lack of support for pyinotify.  
There are workarounds, but nobody has requested this for Windows. 

-Install python > = 2.6.  In linux, the best way is to do this through your system's package manager.   Most linux distros already have it though.

-Install a postgres database.  Get it from your package manager, then configure it.  Here are notes for Debian: http://codeghar.wordpress.com/2009/01/24/postgresql-83-on-debian-lenny/

-Make sure you create a new database with your user.  It can have any name, like '$ createdb synthesis'.  Save the db password for later.

2.1 also get gcc, python-dev, libpq-dev (for postgres connectivity), make, libxml2, libxml2-dev, libxslt1.1, libxslt1-dev, (all for lxml)  if you don't have those packages installed on your system already: run 'apt-get install gcc python-dev libpq' as root), if you don't already have that on your system.

-Create a directory to share all buildout files and your Pylons project: 
~$ cd ~
~$ mkdir synthesis
~$ cd synthesis

-Get the latest version of buildout's bootstrap script:
~/synthesis$ wget "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"

-Get the buildout script: 
~/synthesis$ wget "http://xsd.alexandriaconsulting.com/repos/trunk/synthesis/docs/buildout.cfg"

-Now we have a clean buildout config. Let's bootstrap the buildout and run it:

~/synthesis$ mkdir downloads
~/synthesis$ python bootstrap.py
~/synthesis$ ./bin/buildout

This will take a while.

You now have two new binaries in the bin/ directory:

~/synthesis$ ls bin
buildout*  nosetests* paster*

All eggs can be found in eggs/:

~/synthesis$ ls eggs
Beaker-1.2-py2.5.egg/         Pylons-0.9.7rc4-py2.5.egg/
FormAlchemy-1.1.1-py2.5.egg/  Routes-1.10.2-py2.5.egg/
...
Make a synthesis directory: 
~/synthesis$ mkdir synthesis 

Create a pylons project with the newly created paster binary:

$ ./bin/paster create -t pylons synthesis

-choose the 'mako' template engine, and say 'True' to sqlalchemy as well.

-go into this new project folder
~/synthesis$ cd synthesis/synthesis

-grab the synthesis project sources:
#note these wget options aren't working correctly as many of the files in the subdirectories are not obtained, also all the index.html files are annoying
~/synthesis/synthesis/synthesis$ wget -r --no-parent --no-host-directories --cut-dirs=4 http://xsd.alexandriaconsulting.com/repos/trunk/synthesis/src/
-if you want to develop, tell buildout.cfg about your development egg, by uncommenting:

[buildout]
...
#uncomment this line after initial buildout install, if you want to start to develop, then re-run buildout 
#develop = synthesis
...
[synthesis]
eggs=
...
#uncomment this to develop
#   synthesis

-edit ~/synthesis/synthesis/synthesis/fileconverter.ini with the correct path to the logging file

args=('/home/yourusername/synthesis/synthesis/synthesis/logs/synthesis.log', 'a')

-start the server:
~/synthesis$ ./bin/paster serve ./synthesis/development.ini start

-Note, the wget operation will drop index.html files into you input_files folder, but it'l just get moved to failed_files.

Now, test the installation by moving test_files xml files over to input_files.  Try the HUD_HMIS_3_0 XML files first, because those are most tested. 
 



