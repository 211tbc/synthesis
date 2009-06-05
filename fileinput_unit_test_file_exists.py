from fileinputwatcher import FileInputWatcher
from time import sleep
import unittest, os, Queue

class FileInputTestCase(unittest.TestCase):
    '''test if the threaded callback is working when file created'''
    def test_file_add(self):
        self.queue = Queue.Queue(0)
        dir = '/home/eric/Desktop'
        file_input_watcher = FileInputWatcher(dir, self.queue)
        if os.path.isfile("/home/eric/Desktop/anyfile") is True:
            os.remove('/home/eric/Desktop/anyfile')
        #Start a monitoring thread.  It ends on its own.
        file_input_watcher.monitor()
        #now make a file whilst pyinotify thread is running
        sleep(1)
        f = open('/home/eric/Desktop/anyfile','w')
        f.close()
        result = self.queue.get(block='true')
        #print 'result is', result
        if result is not None:
            #print 'self.queue.get() is ', result 
            file_input_watcher.stop_monitoring()
        #clean up file mess created
        if os.path.isfile("/home/eric/Desktop/anyfile") is True:
            os.remove('/home/eric/Desktop/anyfile')
        self.assertEqual(result, '/home/eric/Desktop/anyfile')
        
if __name__ == '__main__':
    unittest.main()