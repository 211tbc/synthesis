echo
echo "####################"
echo "Initiating setup ..."
echo "####################"
echo
./bin/pcreate -s alchemy synthesis
cd synthesis
echo "Edit setup.py"
sed -i "s/'pyramid_tm/#'pyramid_tm/g" setup.py
echo "Edit development.ini"
sed -i "s/    pyramid_tm/#    pyramid_tm/g" development.ini
../bin/python setup.py develop
echo
echo "#######################"
echo "Deploying synthesis source code ..."
echo "#######################"
echo
cd ..
mv synthesis synthesis_old
git clone https://github.com/211tbc/synthesis.git
cd synthesis
CURRENT_PATH="$( cd "$(dirname "$0")" ; pwd -P )"
SRC_PATH="$CURRENT_PATH/src"
ln -s $SRC_PATH synthesis
echo
echo "###############"
echo "Cleaning up ..."
echo "###############"
echo
cd ..
rm -rf synthesis_old/synthesis
cp -vR synthesis_old/* synthesis/
rm -rf synthesis_old
echo
echo "Done!"
echo
