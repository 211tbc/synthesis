*adapted from: http://wiki.pylonshq.com/display/pylonscommunity/Howto+install+Pylons+with+buildout

-Note: Synthesis currently runs only on unix platforms.  The hangup is Windows' lack of support for pyinotify.  
-There are workarounds, but nobody has requested this for Windows. 

-Install python > = 2.6.  In linux, the best way is to do this through your system's package manager.   Most linux distros already have it though.

-Install a postgres database.  Get it from your package manager, then configure it.  Here are notes for Debian: http://codeghar.wordpress.com/2009/01/24/postgresql-83-on-debian-lenny/

-Make sure you create a new database with your user.  It can have any name, like '$ createdb synthesis'.  
-To be able to run the createdb command, you'll probably first need to edit the pg_hba.conf and create a postgres user with postgres@localhost:$ createuser -s -P your_user_name
-Save the db password for later.

-also get gcc, python-dev, libpq-dev (for postgres connectivity), make, libxml2, libxml2-dev, libxslt1.1, libxslt1-dev, (all for lxml)  if you don't have those packages installed on your system already: run 'apt-get install gcc python-dev libpq' as root), if you don't already have that on your system.

-Create a directory to share all buildout files and your Pylons project: 
~$ cd ~
~$ mkdir myrestservice
~$ cd myrestservice

-Get the latest version of buildout's bootstrap script:
~/myrestservice$ wget "http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py"

-Get the buildout script: 
~/myrestservice$ wget "http://xsd.alexandriaconsulting.com/repos/trunk/synthesis/docs/buildout.cfg"

-Now we have a clean buildout config. Let's bootstrap the buildout and run it:

~/myrestservice$ mkdir downloads
~/myrestservice$ python bootstrap.py

-you should get "Generated script '~/myrestservice/bin/buildout'."
-Now run the generated script

~/myrestservice$ ./bin/buildout

-This will take a while.

-You now have two new binaries in the bin/ directory:

~/myrestservice$ ls bin
buildout*  nosetests* paster*

-All eggs can be found in eggs/:

~/myrestservice$ ls eggs
Beaker-1.2-py2.5.egg/         Pylons-0.9.7rc4-py2.5.egg/
FormAlchemy-1.1.1-py2.5.egg/  Routes-1.10.2-py2.5.egg/
...
-Make a synthesis development egg directory: 
~/myrestservice$ mkdir synthesis 

-Create a pylons project with the newly created paster binary:

$ ./bin/paster create -t pylons synthesis

-choose the 'mako' template engine, and say 'True' to sqlalchemy as well.

-go into this new project folder
~/myrestservice$ cd synthesis/synthesis

~/myrestservice/synthesis/synthesis$ wget --mirror --no-parent --no-host-directories --cut-dirs=4 http://xsd.alexandriaconsulting.com/repos/trunk/synthesis/src/
-Now, tell buildout.cfg about your development egg, by uncommenting two lines:

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

-run buildout again: 
~/myrestservice$ ./bin/buildout

-edit ~/myrestservice/synthesis/synthesis/conf/settings.py with the correct paths/db passwords, etc.

-set the mode to 'TEST' in conf/settings.py.  This creates/wipes the db.  Subsequent restarts should be in the 'PROD' mode. 

-start the server, but first move to the newly built location.  we have to do this because paster looks for the contents of the synthesis.egg-info dir to provide controller and serve command options
~/myrestservice$ cd synthesis
~/myrestservice/synthesis$ ../bin/python ../bin/paster serve ./development.ini start

-or make the paster server outside the console: ~/myrestservice/synthesis$ ../bin/python ../bin/paster serve --daemon --pid-file=./paster.pid --log-file=./paster.log ./development.ini start
-stop it with: ~/myrestservice/synthesis$ ../bin/python ../bin/paster --pid-file=./paster.pid serve ./development.ini stop

-Note, on first run, the wget operation above will drop index.html files into you input_files folder, but it'll just get moved to failed_files automatically, so not a problem.

-Now, test the installation by moving test_files xml files over to input_files.  Try the HUD_HMIS_3_0 XML files first, because those are most tested. 
 
-next, read the testing readme at: docs/synthesis_testing_read_me.txt


