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
wget https://github.com/211tbc/synthesis/archive/synthesis-pyramid.zip
unzip synthesis-pyramid.zip -d unzipfolder
cp -R --force unzipfolder/synthesis-synthesis-pyramid/src/* synthesis/synthesis
echo
echo "###############"
echo "Cleaning up ..."
echo "###############"
echo
rm synthesis-pyramid.zip
rm -rf unzipfolder
echo
echo "Done!"
echo
