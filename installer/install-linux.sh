#/bin/bash

## supports: debian, ubuntu, rhel, centos
## should run on most *nix platforms

## Accept args ( -d database_type -i install_directory )

usage() {
cat << EOF
usage: $0 options

This script installs Synthesis and required dependencies

OPTIONS:
   -h      These instructions
   -d      Database preference
                    ignore - Use an existing Postgres server
                    os - Install a new Postgres server using your os package management system
                    build - Compile and install a new Postgres server from source 
                    binary - Install a new Postgres server using the binary installer
   -f      Directory to install Syntheis (ie. /opt/synthesis)
   -s      Operating system (debian,redhat)
EOF
}

DBTYPE=
INSTALL_DIR=
OSTYPE=
while getopts “hd:f:s:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         d)
             DBTYPE=$OPTARG
             ;;
         f)
             INSTALL_DIR=$OPTARG
             ;;
         s)
             OSTYPE=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $DBTYPE ]] || [[ -z $INSTALL_DIR ]];
    then
         usage
         exit 1
fi;

echo "Installing Synthesis ..."

## check os flavor
if [ "$OSTYPE" == '' ];
    then    
        debian='/etc/debian_version'
        if [ -e "$debian" ];
            then
                flavor='debian'
        fi;
        redhat='/etc/redhat-release'
        if [ -e "$redhat" ]; then
            flavor='redhat'
        fi;
    else
        flavor=$OSTYPE
fi;
        
if [ -n $flavor ];
    then
        echo "Operating system: ${flavor}"
    else
        echo "Operating system: unknown -- trying to install anyway"
fi;

## install any missing os packages
if [ "$flavor" == 'debian' ];
    then
        apt-get -y install python python-dev python-setuptools zlib1g-dev libreadline5 libreadline-dev readline-common ledit libpq-dev
fi;

if [ "$flavor" == 'redhat' ];
    then
        yum -y install python python-devel python-setuptools
fi;

## prep directory structure
mkdir ${INSTALL_DIR}
mkdir ${INSTALL_DIR}/OutputFiles
mkdir ${INSTALL_DIR}/UsedFiles
mkdir ${INSTALL_DIR}/FailedFiles
mkdir ${INSTALL_DIR}/logs
mkdir ${INSTALL_DIR}/InputFiles
mkdir ${INSTALL_DIR}/InputFiles/1
mkdir ${INSTALL_DIR}/InputFiles/2
mkdir ${INSTALL_DIR}/InputFiles/3

## database installers (currently built from source with Buildout)

## os package system
if [ "$DBTYPE" == 'build' ];
    then
        BUILDOUTCFG='buildout_pg.cfg'    
fi;

if [ "$DBTYPE" == 'binary' ];
    then
        BUILDOUTCFG='buildout.cfg'
        chmod a+x buildout/packages/postgresql-8.4.3-1-linux.bin
        buildout/packages/postgresql-8.4.3-1-linux.bin --prefix ${INSTALL_DIR}/postgresql-server --datadir ${INSTALL_DIR}/postgresql-data --servicename synthesispg --serviceaccount synthesispg --superaccount postgres --superpassword SynT49pgDBpw --serverport 5433 --mode unattended
fi;

if [ "$DBTYPE" == 'ignore' ];
    then
        BUILDOUTCFG='buildout.cfg'
fi;

if [ "$DBTYPE" == 'os' ];
    then
        BUILDOUTCFG='buildout.cfg'
        if [ "$flavor" == 'debian' ];
            then
                apt-get -y install postgresql
        fi;

        if [ "$flavor" == 'redhat' ];
            then
                yum -y install postgresql
        fi;    
fi;

## bootstrap and buildout
cd buildout/
python bootstrap.py -c $BUILDOUTCFG
./bin/buildout

## tidy up
cp -rp src/synthesis/* ${INSTALL_DIR}
cd $INSTALL_DIR

exit 1