#!/usr/bin/env python
import logging
import logging.config
import sys
from borg import Borg

_defaultConfig = {}

class clsLogger(Borg):
    def __init__(self, configFile='logging.ini', loglevel=1):
        # make our class a singleton
        Borg.__init__(self)
        
        self.LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
        
        try:
            logging.config.fileConfig(configFile, _defaultConfig)
        except IOError:
            raise
        
        self.logger = logging.getLogger("synthesis.engine")
        self.logger.setLevel(loglevel)
        # test if logging dir exists, if not create it
        
    def getLogger(self, loggerName):
        return logging.getLogger(loggerName)
        
    def __quit__(self):
        print 'Shutting down logging system...'
        logging.shutdown()
    
    def log(self, message, loglevel=0):
        
        if loglevel == 0:
            self.logger.info(message)
        elif loglevel == 1:
            self.logger.debug(message)    
        elif loglevel == 2:
            self.logger.warning(message)    
        elif loglevel == 3:
            self.logger.error(message)
        elif loglevel == 4:
            self.logger.critical(message)
            
if __name__ == "__main__":
    
    
    # get the log level from the command line (args)
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
        #level = LEVELS.get(level_name, logging.NOTSET)
    else:
        level = logging.NOTSET
        
    iniFile = 'logging.ini'
    myLog = clsLogger(iniFile, level)
    
    #myLog._setConfig(level)
    myLog.log("user's Log Message", 0)
    myLog.log("user's Log Message", 1)
    myLog.log("user's Log Message", 2)
    myLog.log("user's Log Message", 3)
    myLog.log("user's Log Message", 4)
    myLog.logger.critical("Test Debug")
    
    myLog2 = clsLogger()
    myLog2.log("user's Log2 Message", 4)
    # Shutdown the logger
    myLog.__quit__()
        

