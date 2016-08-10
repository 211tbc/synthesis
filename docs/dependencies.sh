./bin/pip install lxml==2.2.8
./bin/pip install markerlib
./bin/pip install pycrypto
#./bin/pip install SQLAlchemy==0.6.8
./bin/pip install SQLAlchemy==0.8.2
./bin/pip install python-dateutil==1.5
./bin/pip install nose
./bin/pip install pyinotify
./bin/pip install zope.interface
./bin/pip install psycopg2
./bin/pip install python-gnupg
./bin/pip install sqlalchemy-migrate
./bin/pip install paramiko
./bin/pip install pyramid==1.4.5
./bin/pip install pyramid_controllers==0.3.11

#
# very dumb success|fail test
#
echo "##############################################"
echo "##############################################"
echo "                   SUMMARY                    "
echo "##############################################"
echo "##############################################"

for python_version in "python2.6" "python2.7"
do
    # test site-packages folder for location of dependencies
    if [ -n "$(find lib -maxdepth 1 -name $python_version -print -quit)" ]
    then
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'lxml*' -print -quit)"
        then
            echo "lxml install ... failed!"
        else
            echo "lxml install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'markerlib' -print -quit)"
        then
            echo "markerlib installed ... failed!"
        else
            echo "markerlib installed ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'Crypto' -print -quit)"
        then
            echo "pycrypto installed ... failed!"
        else
            echo "pycrypto installed ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'sqlalchemy' -print -quit)"
        then
            echo "SQLAlchemy install ... failed!"
        else
            echo "SQLAlchemy install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'dateutil' -print -quit)"
        then
            echo "python-dateutil install ... failed!"
        else
            echo "python-dateutil install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'nose' -print -quit)"
        then
            echo "nose installed ... failed!"
        else
            echo "nose installed ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'pyinotify*' -print -quit)"
        then
            echo "pyinotify install ... failed!"
        else
            echo "pyinotify install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'zope.interface*' -print -quit)"
        then
            echo "zope.interface install ... failed!"
        else
            echo "zope.interface install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'psycopg2*' -print -quit)"
        then
            echo "psycopg2 install ... failed!"
        else
            echo "psycopg2 install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'python_gnupg*' -print -quit)"
        then
            echo "python-gnupg install ... failed!"
        else
            echo "python-gnupg install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'sqlalchemy_migrate*' -print -quit)"
        then
            echo "sqlalchemy-migrate install ... failed!"
        else
            echo "sqlalchemy-migrate install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'paramiko*' -print -quit)"
        then
            echo "paramiko install ... failed!"
        else
            echo "paramiko install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'pyramid' -print -quit)"
        then
            echo "pyramid install ... failed!"
        else
            echo "pyramid install ... ok."
        fi
        if test -z "$(find ./lib/$python_version/site-packages -maxdepth 1 -name 'pyramid_controllers' -print -quit)"
        then
            echo "pyramid-controllers install ... failed!"
        else
            echo "pyramid-controllers install ... ok."
        fi
    fi
done
