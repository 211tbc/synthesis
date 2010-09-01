#!/usr/bin/env python

from conf import settings
from fileutils import FileUtilities
from selector import FileHandler
import traceback
import os
import sys
from clsLogger import clsLogger

fileutilities = FileUtilities()


###################################################################################
# Looping construct
# After that is done, we can enter our wait state for the arrival of new files.
###################################################################################

# Display banner if in TEST Mode
if settings.MODE == 'TEST':
    warningTxt = 'CAUTION: TEST MODE - This wipes DB Clean'
    fileutilities.makeBlock(warningTxt)
    warningTxt = "CTRL-C or CTRL-Break to Stop - (waiting before startup, in case you don't want to wipe your existing db)"
    fileutilities.makeBlock(warningTxt)
    # sleep for 10 seconds
    fileutilities.sleep(1)
        
# test if we are in debug and TEST Mode.  If so we clear out the DB every processing run, PROD mode need should never do this.
if settings.DEBUG and settings.MODE == 'TEST':								# Only reset the DB in Test mode
    import postgresutils
    utils = postgresutils.Utils()
    utils.blank_database()    

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
    
try:
    if settings.DEBUG:
        print "Now instantiating FileHandler"
    filehandler = FileHandler() 
    print "calling sys.exit"
    sys.exit

except KeyboardInterrupt:
    print 'Stopping: KeyboardInterrupt at MainProcessor.py'
    # need to shutdown the logging system prior to program termination.  This is to flush buffers, send messages etc.	
    debugMessages.__quit__()
    sys.exit()