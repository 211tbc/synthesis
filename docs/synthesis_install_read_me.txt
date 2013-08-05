-Note: Synthesis currently runs only on unix platforms.  The hangup is Windows' lack of support for pyinotify.  
-There are workarounds, but nobody has requested this for Windows. 

-Install python > = 2.6.  In linux, the best way is to do this through your system's package manager.   Most linux distros already have it though.

-Install a postgres database.  Get it from your package manager, then configure it.  Here are notes for Debian: http://codeghar.wordpress.com/2009/01/24/postgresql-83-on-debian-lenny/

-Make sure you create a new database with your user.  It can have any name, like '$ createdb synthesis'.  
-To be able to run the createdb command, you'll probably first need to edit the pg_hba.conf and create a postgres user with postgres@localhost:$ createuser -s -P your_user_name
-Save the db password for later.

-Install python-setuptools like '$ apt-get install python-setuptools'

-Install python-virtualenv like '$ apt-get install python-virtualenv'

-also get gcc, python-dev, libpq-dev (for postgres connectivity), make, unzip, libxml2, libxml2-dev, libxslt1.1, libxslt1-dev, (all for lxml)  if you don't have those packages installed on your system already: run 'apt-get install gcc python-dev libpq' as root), if you don't already have that on your system.

-Create the virtual environment for the Pyramid project
~$ cd ~
~$ virtualenv --distribute --no-site-packages myrestservice
~$ cd myrestservice

-Retrieve the installation scripts

~$ wget "https://raw.github.com/211tbc/synthesis/synthesis-pyramid/docs/dependencies.sh"
~$ wget "https://raw.github.com/211tbc/synthesis/synthesis-pyramid/docs/deploy-synthesis.sh"

-Install dependencies

~$ sh dependencies.sh

-Deploy Synthesis within the virtual environment

~$ sh deploy-synthesis.sh

-edit ~/myrestservice/synthesis/synthesis/conf/settings.py with the correct paths/db passwords, etc..  
BASE_PATH = "/home/your_username_here_ie_$USERNAME/myrestservice/synthesis/synthesis"
-if you get logging errors on the first start, it's probably because your base base isn't configured correctly
-Incoming file decryption by the web service is turned off by default.  If you want it it on, uncomment  "USE_ENCRYPTION = True" within ~/myrestservice/synthesis/synthesis/conf/inputConfiguration.py (and comment the statement containing the opposite value) NOTE: Only PGP and 3DES incoming decryption is supported at this time.  Outgoing supports PGP.   
 if you get "XMLSyntaxError: Document is empty, line 1, column 1" errors from the server, this may be something to look at.

-If you enable 3DES decryption, make sure to also set the paths within inputConfiguration.py for the corresponding 3DES key and IV: 
KEY_PATH = '/home/myrestservice/occ/synthesis/synthesis/conf/3des3.txt' # full directory path to the 3DES key file
IV_PATH = '/home/myrestservice/occ/synthesis/synthesis/conf/IV3.txt' # full directory path to the 3DES IV file
Make sure those files exist in those places.   

-ensure the mode is set to 'TEST' in conf/settings.py.  This creates/wipes the db upon each restart.  Subsequent restarts should be in the 'PROD' mode, if you don't want data to be wiped each restart. 
-also in conf/inputConfiguration.py, make sure all the paths in are real.  Mainly, put the actual username in, SMTPRECIPIENTS = {    
        "/home/username/myrestservice/synthesis/synthesis/input_files":
  Do not use "~" in the path.  It will cause errors.

edit ~/myrestservice/bin/python to add the path:
'/home/your_username_here_ie_$USERNAME/myrestservice/synthesis/synthesis',
as an additional entry into the sys.path[0:0] =  section.

-start the server, but first move to the newly built location.  we have to do this because paster looks for the contents of the synthesis.egg-info dir to provide controller and serve command options
~/myrestservice$ cd synthesis
~/myrestservice/synthesis$ ../bin/pserve development.ini start

The above starts the server in daemon mode where all outout is written to a file call pyramid.log

-stop it with: ~/myrestservice/synthesis$ ../bin/pserve ./development.ini stop
-run it foregrounded in the console with: ~/myrestservice/synthesis$ ../bin/pserve ./development.ini

-Now, test the installation by moving test_files xml files over to input_files.  Try the HUD_HMIS_3_0 XML files first, because those are most tested.
 
-To generate XML output after you have shredded some test XML.  

First, set up the database, so the IDs to be configured are present.  This doc explains that:

http://xsd.alexandriaconsulting.com/trac/browser/trunk/synthesis/docs/output_configurations.readme

#http://xsd.alexandriaconsulting.com/trac/browser/trunk/synthesis/docs/generating_output_manually.readme

You can also test the pyramid web service by sending HTTP POST messages with sample XML payload.  Use the HUD HMIS XML for best results.
