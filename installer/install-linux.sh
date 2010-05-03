#!/bin/sh
INSTALL_DIR='/opt/synthesis'
echo "Synthesis is being installed in /opt/synthesis"

## check os flavor
debian='/etc/debian_version'
if [ -e "$debian" ]
    then
        flavor='debian'
        pycheck=`which python`
        pycheckdev=`dpkg --get-selections | grep python-dev`
        zlcheck=`dpkg --get-selections | grep zlibg1-dev`
fi

redhat='/etc/redhat-release'
if [ -e "$redhat" ]
    then
        flavor='redhat'
        pycheckdev=`rpm -qa | grep python-devel`
        pycheck=`which python`
fi

if [ -n $flavor ]
    then
        echo "Detected OS: ${flavor}"
fi

## check for existing python
if [ -z $pycheck ]
    then
        echo "Python not found.  Attempting to install Python now."
        if [ $flavor == 'debian' ]
            then
                apt-get -y install python
        fi
        if [ $flavor == 'redhat' ]
            then
                yum -y install python
        fi
fi

## check for existing python-dev
if [ "$pycheckdev" == "" ]
    then
        echo "python-dev not found.  Attempting to install Python now."
        if [ $flavor == 'debian' ]
            then
                apt-get -y install python-dev
        fi
        if [ $flavor == 'redhat' ]
            then
                yum -y install python
        fi
fi

## check for existing zlib1g-dev
if [ "$zlcheck" == "" ]
    then
        echo "zlibg1-dev not found.  Attempting to install Python now."
        if [ $flavor == 'debian' ]
            then
                apt-get -y install zlib1g-dev
        fi
        if [ $flavor == 'redhat' ]
            then
                yum -y install python-devel
        fi
fi

## build a clean python binary with zlib
tar -C buildout/packages/ -xzf buildout/packages/zlib-1.2.5.tar.gz
cd buildout/packages/zlib-1.2.5
./configure --shared --prefix=${INSTALL_DIR}/zlib
make
make install prefix=${INSTALL_DIR}/zlib
cd ../../..

mkdir ${INSTALL_DIR}

## prep directories for input files
mkdir ${INSTALL_DIR}/InputFiles
mkdir ${INSTALL_DIR}/InputFiles/1
mkdir ${INSTALL_DIR}/InputFiles/2
mkdir ${INSTALL_DIR}/InputFiles/3

## install independent postgresql binary
chmod a+x buildout/packages/postgresql-8.4.3-1-linux.bin
buildout/packages/postgresql-8.4.3-1-linux.bin --prefix ${INSTALL_DIR}/postgresql-server --datadir ${INSTALL_DIR}/postgresql-data --servicename synthesispg --serviceaccount synthesispg --superaccount postgres --superpassword SynT49pgDBpw --serverport 5433 --mode unattended

## bootstrap
cd buildout/
python bootstrap.py
./bin/buildout
