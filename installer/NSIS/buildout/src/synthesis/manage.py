#!/usr/bin/env python
from migrate.versioning.shell import main
from conf import settings

main(url='postgres://%s:%s@%s:%s/coastaldb_test' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT),repository='Synthesis_Repository') 
