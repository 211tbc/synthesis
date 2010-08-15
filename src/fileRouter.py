#!/usr/bin/env python
from fileUtils import fileUtilities
from conf import settings

class router:
    def __init__(self):
        self.FILEUTIL = fileUtilities(settings.DEBUG)
    
    def moveFile(self, sourceFile, destinationLocation):
        self.FILEUTIL.moveFile(sourceFile, destinationLocation)
    
    def moveUsed(self, fileName):
        self.moveFile(fileName, settings.USEDFILES)

    def moveFailed(self, fileName):
        self.moveFile(fileName, settings.FAILEDFILES)

