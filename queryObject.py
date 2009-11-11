#!/usr/bin/env python

from optparse import OptionParser

class queryObject:
    def __init__(self):
        
        usage = "usage: %prog [options] arg"
        
        parser = OptionParser(usage)
        parser.add_option("-i", "--IDvendor", dest="vendorID", type="string",
                          help="ID of vendor requesting report", metavar="ID")
        parser.add_option("-s", "--startdate", dest="startDate", type="string",
                          help="start date of reporting", metavar="StartDate")
        
        parser.add_option("-e", "--enddate", dest="endDate", type="string",
                          help="end date of reporting", metavar="EndDate")
        
        (self.options, self.arg) = parser.parse_args()
        
        #print 'options' ,options
        #print "arg:", arg
        
        #print 'options.vendorID=%s' % options.vendorID
        if self.options.vendorID == None or self.options.startDate == None or self.options.endDate == None:
            parser.print_help()
            self.options = None
            #raise 'error'
            
        
    def getOptions(self):
        return self.options

def main():
    optParse = queryObject()
    options = optParse.getOptions()
    if options != None:
        print options.vendorID
    
if __name__ == '__main__':
    main()
    

    
    

