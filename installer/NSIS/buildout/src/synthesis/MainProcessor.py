#!/usr/bin/env python
import selector
from conf import settings
from fileUtils import fileUtilities
from selector import FileHandler
import traceback
import os
import sys
from clsLogger import clsLogger

# run forever
processFiles = 1

###################################################################################
# Looping construct
# After that is done, we can enter our wait state for the arrival of new files.
###################################################################################

# Display banner if in TEST Mode
if settings.MODE == 'TEST':
    FILEUTIL = fileUtilities(settings.DEBUG, None)
    warningTxt = 'CAUTION: TEST MODE - This wipes DB Clean'
    FILEUTIL.makeBlock(warningTxt)
    warningTxt = 'CTRL-C or CTRL-Break to Stop - (waiting 30 seconds to startup)'
    FILEUTIL.makeBlock(warningTxt)
    # sleep for 10 seconds
    FILEUTIL.sleep(10)
        
# test if we are in debug and TEST Mode.  If so we clear out the DB every processing run, PROD mode need should never do this.
if settings.DEBUG and settings.MODE == 'TEST':								# Only reset the DB in Test mode
    import postgresutils
    UTILS = postgresutils.Utils()
    UTILS.blank_database()    

# setup logging
if not os.path.exists(settings.LOGS):
    os.mkdir(settings.LOGS)
else:
    if settings.DEBUG:
        print "Logs Dir exists:"
iniFile = 'logging.ini'

# command argument set's log level or Settings.py
if len(sys.argv) > 1:
    level = sys.argv[1]
else:
    level = 0

debugMessages = clsLogger(iniFile, level)
if settings.DEBUG:
    debugMessages.log("Logging System Online", 0)

# first try to process existing files, then start the loop for ongoing processing            
FILEHANDLER = FileHandler()
FILEHANDLER.processExisting()

try:
    while processFiles:
            
        try:
        
        # This will wait till files arrive, once processed, it will loop and start over (unless we get ctrl-C or break
            RESULTS = FILEHANDLER.run()
        except:
            excString = traceback.format_exc()
            print excString
            continue
        # logging?
        
        
except KeyboardInterrupt:
	print 'Stopping'

# need to shutdown the logging system prior to program termination.  This is to flush buffers, send messages etc.	
debugMessages.__quit__()
