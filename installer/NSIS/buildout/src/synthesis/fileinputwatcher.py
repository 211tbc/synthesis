'''
This module watches multiple directories for new files and notifies \
when a new file encountered.  It has posix and non-posix versions.  \
The posix version uses a queue to run the watch as a thread and \
make a non-polling notification.
'''
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

import os, time, exceptions
from time import sleep

# determine what environment we are running under, win32 or POSIX
if os.name == 'nt':
    import win32file
    import win32event
    import win32con
else:
    # POSIX
    try:
        import pyinotify
        from pyinotify import WatchManager, ThreadedNotifier, ProcessEvent, EventsCodes
    except ImportError:
        print 'Could not import pyinotify modules.'

class FileInputWatcher:
    '''controlling class for file monitoring'''

    def __init__(self, dir_to_watch, queue, debug=False): 
        print 'FileInputWatcher Initialized'
        # SBB20090903 Adding debugging capability, not processing multiple file drops into multiple directories.
        if debug:
            print '****************************************Debugging Monitoring..'
        self.debug = debug
        
        self.queue = queue
        self.dir_to_watch = dir_to_watch    
        if os.name == 'nt':   
            self.osiswin32 = True
        else:
            self.osiswin32 = False
        # make a notifier (nothing)
        self.notifier = None
                
    def monitor(self):
        '''The command to start monitoring a directory or set of them.'''
        print 'Monitoring Directories: %s' % self.dir_to_watch
        print "Watching started at %s" % (time.asctime())
        if self.osiswin32:
            print 'Watching win32 OS'              
            return self.watch_win32(self.dir_to_watch)
        else:
            print 'Watching POSIX OS'
            self.watch_posix_start()
            
    def stop_monitoring(self):  
        'os independent method to stop monitoring, but only posix uses it.'
        #self.watch_posix_stop()
        # SBB20090917 Instead of stopping, pause while stuff is being processed, with notifier stopped, any files received are not tracked or processed
        #sleep(5)
        print 'Done Monitoring'
                
    def watch_win32(self, dir_to_watch): #IGNORE:R0201    
        '''os-specific watch command'''
        # Loop forever, listing any file changes. The WaitFor... will
        #  time out every half a second allowing for keyboard interrupts
        #  to terminate the loop.    
        files_added = []
        old_path_contents = []
        new_path_contents = []
        cnt = 0
        try:
            while 1:
                cnt += 1
                #print 'Watching %s' % cnt           
                #old_path_contents = os.listdir(dirToWatch)
                for item in dir_to_watch:
                    change_handle = win32file.FindFirstChangeNotification(item, 0, win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
                    old_path_contents.append(os.listdir(item))               
                result = win32event.WaitForSingleObject(change_handle, 500)
                # If the WaitFor... returned because of a notification (as
                #  opposed to timing out or some error) then look for the
                #  changes in the directory contents.
                if result == win32con.WAIT_OBJECT_0:
                    #new_path_contents = os.listdir(dirToWatch)
                    # build the new list with all the files from all dirs
                    for item in dir_to_watch:
                        new_path_contents.append(os.listdir(item))             
                    files_added = [f for f in new_path_contents if not f in old_path_contents]
                    #files_deleted = [f for f in old_path_contents if not f in new_path_contents]      
                    if files_added:
                        print
                        print time.asctime ()
                        print "Added:", files_added or "Nothing"
                        return files_added
                    #print "Deleted:", files_deleted or "Nothing"           
                win32file.FindNextChangeNotification(change_handle)
        except KeyboardInterrupt:
            return []
        #finally:
        #	win32file.FindCloseChangeNotification(change_handle)
            
    def watch_posix_start(self): #IGNORE:R0201
        '''os-specific command to watch'''
        
        # test to see if we already have a notifier object, if not, make it, otherwise we are already watching a set of folders
        if self.notifier == None:
            try:
                pyinotify.compatibility_mode()
                print 'pyinotify running in compatbility mode'
            except:
                print 'pyinotify running in standard mode'
            try:
                watch_manager = WatchManager()
            except NameError:
                print 'hey'
                return ['POSIX Watch Error']
            mask = EventsCodes.IN_CREATE  #watched events IGNORE:E1101
        
            self.notifier = ThreadedNotifier(watch_manager, EventHandler(self.queue))#IGNORE:W0201
            # SBB20090903 Turn on verbose mode
            self.notifier.VERBOSE = self.debug
            
            watch_manager.add_watch(self.dir_to_watch, mask)
            print 'Starting the threaded notifier on ', self.dir_to_watch
            self.notifier.start()
            print 'Finished...'
                
    def watch_posix_stop(self):#IGNORE:R0201
        'os specific call to stop monitoring'
        print 'Stopping the threaded notifier.'
        self.notifier.stop()
        return
     
class EventHandler(ProcessEvent): #IGNORE:W0232
    '''Event handler processing create events passed in to the \
    watch manager by the notifier.''' 
    def __init__(self, queue):
        self.queue = queue
                
    def process_IN_CREATE(self, event):#IGNORE:C0103
        '''What happens when a file is added'''
        print "Create: %s" %  os.path.join(event.path, event.name)
        self.queue.put(os.path.join(event.path, event.name))