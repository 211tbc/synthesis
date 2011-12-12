#!/usr/bin/env python

import optparse
from optparse import OptionParser
from datetime import datetime

'''
Formats the processing options for "nodebuilder.py" module.

Usage: nodebuilder.py [options] arg

Options:
  -h, --help            show this help message and exit
  -i ID, --IDvendor=ID  ID of vendor requesting report
  -s StartDate, --startdate=StartDate
                        start date of reporting
  -e EndDate, --enddate=EndDate
                        end date of reporting
  -r Reported, --reported=True or False
                        if the data has been reported before
  -a AllDates, --alldates
                        report all dates
                        
'''

class QueryObject:
    def __init__(self, suppress_usage_message=False):
        
        if suppress_usage_message:
            parser = OptionParser(usage=optparse.SUPPRESS_USAGE)
        else:
            usage = "usage: %prog [options] arg"
            parser = OptionParser(usage=usage)
        parser.add_option("-i",  dest="configID", type="string",
                          help="Configuration ID of Vendor requesting report", metavar="ID")
        parser.add_option("-s",  dest="startDate", type="string",
                          help="start date of reporting", metavar="StartDate")
        
        parser.add_option("-e",  dest="endDate", type="string",
                          help="end date of reporting", metavar="EndDate")
        
        parser.add_option("-a", action="store_true", dest="alldates",
                          help="Select all dates", metavar="AllDates")

        #parser.add_option("-r", "--reported", dest="reported",
        #                  help="1=True or 0=False use the reported boolean indicator in the tables for data selection", metavar="Reported")
        parser.add_option("-r", action="store_true", dest="reported",
                          help="Select data that has already been reported (reported = True).  Omit both -r and -u to simply use date selection", metavar="Reported")
        
        parser.add_option("-u",  action="store_true", dest="unreported",
                          help="Select data that has never been reported (reported = False or None).  Omit both -r and -u to simply use date selection", metavar="Reported")    

        self.parser = parser
        
        (self.options, self.arg) = parser.parse_args()
        
        #print 'options' ,options
        #print "arg:", arg
        
        #print 'options.vendorID=%s' % options.vendorID
        if self.options.configID == None or (self.options.alldates == None and \
			(self.options.startDate == None or self.options.endDate == None)):
            if not suppress_usage_message: parser.print_help()
            self.options = None
            return
            #raise 'error'
            
        # convert the date strings to date values
        try:
            self.options.startDate = datetime.strptime(self.options.startDate, '%Y-%m-%d')
            self.options.endDate = datetime.strptime(self.options.endDate, '%Y-%m-%d')
        except:
            #print '==== parse dates error (because there are none)'
            if self.options.alldates == None:	# JCS
                if not suppress_usage_message: parser.print_help()
                raise
        
    def getOptions(self):
        return self.options

def main():
    optParse = QueryObject()
    options = optParse.getOptions()
    if options != None:
        print options.configID

    print optParse.parser.parse_args(['-a', '-u', '-i000'])

if __name__ == '__main__':
    main()
    

    
    

