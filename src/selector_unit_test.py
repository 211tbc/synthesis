'''Unit-tests various XML/CSV validation scenarios (called tests also) in 
selector.py.'''

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

from selector import Selector
import unittest
import os
import testcase_settings
import postgresutils

class SelectorTestCase(unittest.TestCase):
    '''see if the return value is a file path'''
    def test_validation_valid(self):
        '''Tests if HMIS XML 2.8 test is validating properly.'''
        self.Wipe_DB_clean()
        select = Selector()
        #instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila.xml'#IGNORE:C0301
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, True, False])
        
    def test_validation_invalid(self):
        '''Tests if HMIS XML 2.8 test is properly invalidating some invalid XML
        '''
        self.Wipe_DB_clean()
        select = Selector()
        #instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila_invalid.xml'#IGNORE:C0301
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_INVALID)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, True, False])
        
    def test_validation_valid_n_shred(self):
        '''Tests if HMIS XML 2.8 test is properly validating some valid XML and Shredding into the DB
        '''
        self.Wipe_DB_clean()
        select = Selector()
        #instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila_invalid.xml'#IGNORE:C0301
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        result = select.validate(instance_filename, True)
        print result
        self.assertEqual(result, [False, True, False])
        
    def test_db_values(self):
        ''' Tests to see if we have XML Data in our DB
            After shredding the XML_FILE_VALID file, our db should contain
            3 records in the [Person] table,
            2 records in [Person_Address]
        '''
        self.Wipe_DB_clean()
        select = Selector()
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        result = select.validate(instance_filename, True)
        print result
        self.assertEqual(result, False)
        
    def test_validation_malformed_xml(self):
        '''Tests if HMIS XML 2.8 test is properly invalidating some malformed 
        XML.  Malformed in this context means missing an end tag or some basic
        XML error.  Not a schema validation driven error.'''
        self.Wipe_DB_clean()
        select = Selector()
        #instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila_malformed.xml'#IGNORE:C0301
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_MALFORMED)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        result = select.validate(instance_filename, False)
        print result
        self.assertEqual(result, [False, None, False])
        
    def Wipe_DB_clean(self):
        UTILS = postgresutils.Utils()
        UTILS.blank_database()
        
if __name__ == '__main__':
    # Wipe the DB first
    #import postgresutils
    #UTILS = postgresutils.Utils()
    #UTILS.blank_database()
    
    unittest.main()