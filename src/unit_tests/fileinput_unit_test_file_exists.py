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

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from fileinputwatcher import FileInputWatcher
from time import sleep
import unittest, Queue
import testcase_settings

class FileInputTestCase(unittest.TestCase):
    '''test if the threaded callback is working when file created'''
    def test_file_add(self):
        self.queue = Queue.Queue(0)
        dir = testcase_settings.INPUTFILES_PATH
        testFile = testcase_settings.TEST_FILE
        file_input_watcher = FileInputWatcher(dir, self.queue)
        if os.path.isfile(os.path.join(dir, testFile)) is True:
            os.remove(os.path.join(dir, testFile))
        #Start a monitoring thread.  It ends on its own.
        file_input_watcher.monitor()
        #now make a file whilst pyinotify thread is running
        sleep(1)
        f = open(os.path.join(dir, testFile),'w')
        f.close()
        result = self.queue.get(block='true')
        #print 'result is', result
        if result is not None:
            #print 'self.queue.get() is ', result 
            file_input_watcher.stop_monitoring()
        #clean up file mess created
        if os.path.isfile(os.path.join(dir, testFile)) is True:
            os.remove(os.path.join(dir, testFile))
        self.assertEqual(result, os.path.join(dir, testFile))
        
if __name__ == '__main__':
    unittest.main()
