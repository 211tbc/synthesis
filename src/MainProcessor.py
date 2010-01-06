#!/usr/bin/env python
import selector
from conf import settings
from fileUtils import fileUtilities
from selector import FileHandler
import traceback

# run forever
processFiles = 1

###################################################################################
# Looping construct
# After that is done, we can enter our wait state for the arrival of new files.
###################################################################################

# Display banner if in TEST Mode
if settings.MODE == 'TEST':
    FU = fileUtilities(settings.DEBUG, None)
    warningTxt = 'CAUTION: TEST MODE - This wipes DB Clean'
    FU.makeBlock(warningTxt)
    warningTxt = 'CTRL-C or CTRL-Break to Stop - (waiting 30 seconds to startup)'
    FU.makeBlock(warningTxt)
    # sleep for 10 seconds
    FU.sleep(10)
        
# test if we are in debug and TEST Mode.  If so we clear out the DB every processing run, PROD mode need should never do this.
if settings.DEBUG and settings.MODE == 'TEST':								# Only reset the DB in Test mode
    import postgresutils
    UTILS = postgresutils.Utils()
    UTILS.blank_database()    

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
