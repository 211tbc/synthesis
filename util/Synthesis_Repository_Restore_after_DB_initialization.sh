# Repository name = Synthesis_Repository

# move existing repo out of the way
mv Synthesis_Repository/ Synthesis_Repository_orig/

# run the Repo setup command
migrate create Synthesis_Repository "Synthesis Project"

# push the version control system into the DB
python Synthesis_Repository/manage.py version_control postgres://scottben:nx9353@localhost/synthesis

# This is for Crusty
#python Synthesis_Repository/manage.py version_control postgres://scottben:openM3rc@localhost/synthesis

# remove the new Repo Directory
rm -rf Synthesis_Repository/

# now move the correct repo back into it's place
mv  Synthesis_Repository_orig/ Synthesis_Repository/

# Now tell user to go into db and set the last version in the version_control table

# downgrade the DB to prior version (currently 6 -> 5)
# python src/manage.py downgrade postgres://[username]:[password]@localhost/coastaldb_test  "Synthesis_Repository" 5
