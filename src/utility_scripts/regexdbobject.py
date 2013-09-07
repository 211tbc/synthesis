import fileinput
import sys
#fin = open('dbobjects.py', 'r')
#fout = open('dbobjects_new.py', 'r+')


#all_lines = f.readlines()
#for line in all_lines:

count = 0
for line in fileinput.FileInput('dbobjects.py', inplace=1, backup='.backupbyfileinput'):

    altered_line = line[0:-1]
    newstring = None
    count = count +1
    if count in range(74,1742):
        splitline = altered_line.split()
        if splitline:
            if splitline[0] == "def":
                #print "***********************************************************"
                #print count, ": ", line
                #print "splitline is: ", splitline
                if "_" in altered_line:
                    no_underscore = altered_line.split("_") 
                    #print "split: ", no_underscore
                    for item in no_underscore:
                        #print "item is", item[0:3]
                        if item[0:3] != "def":
                            #print "item doesn't have def:", item
                            if item[0:3] == "map":
                                continue
                            else:
                                #print "raw item (not a map) is: ", item
                                capped = item.capitalize()
                                #print "capitalization yields: ", capped
                                if newstring:
                                    newstring = newstring + capped
                                #print "newstring has grown to: ", newstring
                                
                        else:
                            #print "item has a 'def' in it:", item
                            #newstring = item[0:4]
                            newstring = "class " + item[4:].capitalize()
                    if newstring:
                        newstring = newstring + "(Base):\n"
                        sys.stdout.write(newstring)
                        #print "newstring is finally", newstring
                    else:
                        sys.stdout.write(line)
                else:
                    sys.stdout.write(line)
                    #print "no underscores, so this line has already been altered"
            else:
                sys.stdout.write(line)
        else:
            sys.stdout.write(line)
    else:
        sys.stdout.write(line)      
  