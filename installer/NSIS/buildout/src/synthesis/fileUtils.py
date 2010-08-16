#import sys
import os
# The MIT License
# 
# Copyright (c) 2007 Suncoast Partnership 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

import glob
import string
import copy
import shutil
import csv
from time import sleep

class fileUtilities:
    
        
    def __init__(self, debug=False, debugMessages=None):
        print "fileUtilities initialized..."
        self.failedDictAdd = {'daily census':0, 'intakes':0, 'outcomes':0}
        self.debug = debug
        
    def sleep(self, sleepTime):
        print 'Sleeping for %s' % sleepTime
        sleep(sleepTime)
        
    def getSmartPath(self, baseDir, filePath):
        # 1st Try to open the filePath as a normal file path, if that works it should take precedence
        # 2nd if that doesn't work, try to open the path as a subdirectory of the basepath
        # 3rd if that doesn't work try to create the path
        # lastly, if that doens't work, raise a hard error
            if os.path.exists(filePath):
                return filePath
            else:
                newPath = os.path.join(baseDir, filePath)
                if os.path.exists(newPath):
                    return newPath
                else:
                    try:
                        os.makedirs(newPath)
                    except OSError:
                        raise OSError
                
    def checkPath(self, filePath):
        # first check if the path exists
        if os.path.exists(filePath):
            # nothing to do return 0
            return 0
        # if it doesn't exist, try to create it
        else:
            try:
                os.makedirs(filePath)
                if os.path.exists(filePath):
                    return 0
                else:
                    raise pathCreationError
            except:
                raise

    def keyToDict(self, listVals):
        dict={}
        for key in range(0,len(listVals)):
            dict.setdefault(listVals[key],key)
        return dict
        
    def stripData(self, record, delimiter='\n'):
        #print "ready to strip bad data"
        record = record.split(delimiter)
        record = record[0]
        #record = self.unquoteString(record, findChar='"')
        return record
    
    def unquoteList(self, parts=[], findChar='"'):
        newList = []
        for item in parts:
            item = self.unquoteField(item, findChar='"')
            newList.append(item)
        return newList
        
    def unquoteField(self, field, findChar='"'):
        newField = ''
        newField = field.replace(findChar, '')
        newField = newField.replace(findChar, '')
        x = copy.deepcopy(newField)
        return x
                
    def unquoteString(self, record="", findChar='"'):
        posFind = record.find(findChar)
        while not posFind == -1:
            record = record.replace(findChar, '')
            posFind = record.find(findChar)
        return record
        
    def cleanRecord(self, record, delimitter, findChar, replaceChar, startPos=0):
        ''' this function takes the input record (csv record) and 
        searches for a delimiter (") at the extremes of the record
        and replaces the findChar with a replaceChar in the substring
        between the delimited chars.'''
        #print "Before Cleaning Record is: " + record
        pos1Find = record.find(delimitter, startPos)
        if pos1Find == -1: # quick out, not found exit out with original record
            return record
        pos2Find = record.find(delimitter, pos1Find + 1)
        if pos2Find == -1: # quick out, not found exit out with original record
            return record
        badChars = record[pos1Find:pos2Find + 1]
        
        goodChars = badChars.replace(findChar, replaceChar)
        
        newRecord = record[0:pos1Find] + goodChars + record[pos2Find+1:len(record)]
        
        # recursive call to ourself maybe there is more data that's fd up.
        pos3Find = newRecord.find(delimitter, pos2Find)
        if pos3Find == -1: # quick out, not found exit out with
            #print "After Cleaning Record is: " + newRecord
            return newRecord
        else:
            #print "Before 2nd Cleaning Record is: " + newRecord
            newRecord = self.cleanRecord(record=newRecord, delimitter=delimitter, findChar=findChar, replaceChar=replaceChar, startPos=pos2Find+2)
        
        return newRecord
        
    def parseRecord(self, record, delimiter=","):
        #print "Ready to parse a record..."
        #print record
        recParts = []
        # intakes file is delimited with "\r" and outcomes is del with "\r\n"
        findThis = "\r\n"
        if record.find(findThis) == -1:
            record = self.stripData(record)
        else:
            record = self.stripData(record, findThis)
        
        recParts = record.split(delimiter)
        
        return recParts
    
    def suckFile2(self, filename):
        records = []
        print "Ready to suck file2 in %s" % filename
        try:
            reader = csv.reader(open(filename, "rb"))
            for row in reader:
                records.append(row)
        except:
            print "ERROR: filename: %s not found.  Please investigate" % filename
                
        #print 'sucked in %s records' % reader.line_num
        print 'sucked in %s records' % len(records)
        
        return records
    
    def suckFile(self, filename):
        records = []
        print "Ready to suck file in %s" % filename
        try:
            file = open(filename, 'r')
        except:
            print "ERROR: filename: %s not found.  Please investigate" % filename
             
        records = file.readlines()
            
        print 'sucked in %s records' % len(records)
        
        return records
    
    def pushIntoDict(self, dictName, theDict, theKey, theRow, appendRow=False):
        rc = 0
        tmpList = []
        # first check to see if the dictionary has the key already
        if theDict.has_key(theKey):
            rc = 0
            #print 'Key: %s already in Dictionary: %s' % (theKey,dictName), theRow
            #print
            #print 'Existing Value is: ', theDict[theKey]
            #print '*'*80
            if appendRow == True:
                rowVal = theDict[theKey]
                #print "Found existing row %s for key: %s and appending row data %s" (theKey, rowVal, theRow)
                rowVal.append(theRow)
                theDict[theKey] = rowVal
                rc = 2
            else:
                self.failedDictAdd[dictName] += 1
        else:
            if appendRow == True:
                tmpList.append(theRow)
                theDict[theKey] = tmpList
            else:
                theDict[theKey] = theRow
                
            rc = 1
        return rc
    
    def dumpObjToFile(self, dumpObject, filename):
        # function to dump some type of object to a file (normally a debug list to a file)
        print "dump File Processing"
        
        f = open(filename, 'w')
        
        if dir(dumpObject).count('__iter__') > 0:
            # we have an iterator, loop through it
            #for lines in dumpObject:
            f.writelines(dumpObject)
        else:
            f.write(str(dumpObject))
            
        # close the file
        f.close()
    
    def grabFiles(self, directoryToProcess):
        print "Getting Files"
        validFiles = []
        # adding file sucking capability
        files = glob.glob(directoryToProcess)
        # pull list of files
        for file in files:
            print "processing: %s" % file
        
            validFiles.append(file)
        
        print 'Done Grabbing Files'
        return validFiles
    
    def moveFile(self, source, destDir):
        # SBB20090831 Test if the destination exists, if not make it.  Ecapsulated w/ Try
        try:
            if not os.path.exists(destDir):
                os.mkdir(destDir)
                
            shutil.move(source, destDir)        
        except:
            raise
            
    def copyFile(self, source, dest):
        shutil.copy2(source, dest)

    def deleteFile(self, fileDelete):
        try:
            os.remove(fileDelete)
        except:
            print "\T\TFAILURE:Deletion of file %s failed" % fileDelete * 3
            raise
        print "SUCCESS: Deletion of file %s succeeded" % fileDelete
        
    def backupFile(self, project):
        # copy the file to a backup filename we are creating a new copy of the file
        self.copyFile(project, project + ".bak")    
        
    def makeBlock(self, wording, numChars=0):
        # SBB20090902 why pass in the number of characters (fixed block sizes)
        if numChars == 0:
            numChars = len(wording)
            
        if len(wording) >= numChars:
            numChars = len(wording) + 4
        numSpaces = (numChars - (len(wording) + 2)) / 2
        oddSpacing = (numChars - len(wording)) % 2
        print numChars * ("*")
        print "*" + " " * numSpaces + wording + " " * numSpaces + oddSpacing * (" ") + "*"
        print numChars * ("*")

    def sortItems(self, incomingList, colToSort=''):
        from operator import itemgetter
        # this is a single operation to sort a list of dictionaries
        return sorted(incomingList, key=itemgetter(colToSort))

if __name__ == "__main__":
    vld = fileUtilities()
    files = vld.grabFiles('/home/user/Documents/Projects/companyLLC/Ohio/*.csv')
    
    if debug == True:
        debugMessages.log("Valid Files are: ", files)
    
    for file in files:
        recs = vld.suckFile(file)
        # split the records into the components
        for rec in recs:
            #print rec
            parts = vld.parseRecord(rec)
            print parts
