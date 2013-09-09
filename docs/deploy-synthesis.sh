echo
echo "####################"
echo "Initiating setup ..."
echo "####################"
echo
./bin/pcreate -s alchemy synthesis
cd synthesis
../bin/python setup.py develop
cd ..
echo
echo "#######################"
echo "Deploying Synthesis ..."
echo "#######################"
echo
wget https://github.com/211tbc/synthesis/archive/master.zip
unzip master.zip -d unzipfolder
cp -R --force unzipfolder/synthesis-master/src/* synthesis/synthesis
echo
echo "###############"
echo "Cleaning up ..."
echo "###############"
echo
rm master.zip
rm -rf unzipfolder
echo
echo "Done!"
echo
