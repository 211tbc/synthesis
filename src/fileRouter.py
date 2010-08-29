#!/usr/bin/env python
from fileutils import FileUtilities
from conf import settings

class router:
    def __init__(self):
        self.FILEUTIL = FileUtilities(settings.DEBUG)
    
    def moveFile(self, sourceFile, destinationLocation):
        self.FILEUTIL.moveFile(sourceFile, destinationLocation)
    
    def moveUsed(self, fileName):
        self.moveFile(fileName, settings.USEDFILES_PATH)

    def moveFailed(self, fileName):
        self.moveFile(fileName, settings.FAILEDFILES_PATH)

