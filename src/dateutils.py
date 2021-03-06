"""
The MIT License

Copyright (c) 2011, Alexandria Consulting LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from datetime import datetime, date, time, timedelta
from time import strptime

#def fixDate(self, inputDate):
def  fixDate(inputDate):		# JCS
    isIsoTimeFormat = '%Y-%m-%dT%H:%M:%S'
    #dateParts = strptime(s, "%m/%d/%Y")[0:3]
    #newDate = datetime(*strptime(inputDate, "%d-%b-%y")[0:3]).isoformat()
    # test the inputDate length, it might be 08/08/2007 or 08/08/07
    # SBB20091007 if the incoming date is already a Datetimeobject simply send back the isoformat
    if isinstance(inputDate, datetime) or isinstance(inputDate, date):
        # SBB20100225 Replaceing isoformat() with less precision, same format just dropping the Microseconds.
        #return inputDate.isoformat()
            #ECJ20100909: the datetime strftime() methods require year >= 1900
            try:
                return inputDate.strftime(isIsoTimeFormat)	#self.isIsoTimeFormat)
            except ValueError:
                print("bad date string passed to fixDate: ", inputDate, " so sending back blank date")
                #We should return None instead of a blank date, because this might cause validation issues (empty string dates)
                inputDate = None
                return inputDate    
    # SBB20100225 Replacing isoformat() with less precision, same format just dropping the Microseconds.
    if inputDate == "" or inputDate == None:
    #return datetime.now().isoformat()
            return datetime.now().strftime(isIsoTimeFormat)	#self.isIsoTimeFormat)

    else:
    #newDate = self.getDateTimeObj(inputDate).isoformat()
        newDate = getDateTimeObj(inputDate).strftime(isIsoTimeFormat)	#self.isIsoTimeFormat)
        if self.debug == True:
            self.debugMessages.log("FUNCTION: fixDate() incoming date is: %s and clean date is: %s\n" % (inputDate, newDate))
            return newDate
           
def fixDateNoTime(self, inputDate):
#dateParts = strptime(s, "%m/%d/%Y")[0:3]
#newDate = datetime(*strptime(inputDate, "%d-%b-%y")[0:3]).isoformat()
# test the inputDate length, it might be 08/08/2007 or 08/08/07
    
        if input == "":
            print("empty date encountered!" + self)

        else:
            newDate = self.getDateTimeObj(inputDate).date()
            if self.debug == True:
                self.debugMessages.log("FUNCTION: fixDate() incoming date is: %s and clean date is: %s\n" % (inputDate, newDate))
            return newDate
    
def dateStringToDateObject(self, dateString):#Takes MM/DD/YYYY and turns into a standard dateTime object
#dateString = "16/6/1981"
    date_object = time.strptime(dateString, "%d/%m/%Y")
    return date_object
    
    
def convertIntegerToDate(self, intDate):
    #if intDate == "":
    #    intDate = 0
    # SBB20070628 New test, we might still have Junk in our data, need to clean up and test it.  If junk remove the value
    if not intDate.isdigit():
        if intDate == "":
            #intDate = 0
            #ECJ20071111 Had to change this so blank dates don't result in 1900-01-01
            return
        else:
            self.errorMsgs.append("WARNING: during conversion of an integer to date format this string was passed: %s which is not all numbers" % intDate)
            intDate = 0
 
    td = timedelta(days=int(intDate))
    # Excel dates are Days since 1900-01-01 = 1
    newDate = date(1900,1,1) + td
    if self.debug == True:
        print('Incoming Date is: %s and converted Date is: %s' % (intDate, newDate.isoformat()))
 
    return newDate.isoformat()
        
def convertIntegerToDateTime(self, intDate):
    #if intDate == "":
    #    intDate = 0
    # SBB20070628 New test, we might still have Junk in our data, need to clean up and test it.  If junk remove the value
    if not intDate.isdigit():
        #ECJ20071111 Had to change this so blank dates don't result in 1900-01-01
        if intDate == "":            
            return
        else:
            self.errorMsgs.append("WARNING: during conversion of an integer to date format this string was passed: %s which is not all numbers" % intDate)
            intDate = 0

    td = timedelta(days=int(intDate))
    # Excel dates are Days since 1900-01-01 = 1
    isodate = date(1900,1,1) + td
    isodatetime = str(isodate)+'T00:00:00'
    if self.debug == True:
        print('Incoming Date is: %s and converted Date is: %s' % (intDate, isodatetime))
    return isodatetime

def getDateTimeObj(inputDate): 	#:self, 
        dateParts = inputDate.split('/')
        if len(dateParts[2]) == 4:
            inputDateFmt = "%m/%d/%Y"
        else:
        # can't determine the date format, try to determine from other attributes
            if len(inputDate) == 10 or len(inputDate) == 9:
                inputDateFmt = "%m/%d/%Y"
            else:
                inputDateFmt = "%m/%d/%y"
            
        # format a Datetime Obj so we can do some math on it.
        newDate = datetime(*strptime(inputDate, inputDateFmt)[0:3])
        return newDate
