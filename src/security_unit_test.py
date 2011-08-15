'''Unit-tests various encryption/decryption scenarios (called tests also) in 
security.py.'''

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

from security import Security
import unittest
import os
import testcase_settings

class CryptTestCase(unittest.TestCase):
    '''see if the return value is a file path'''
    #def test_decrypt2Stream(self):
    #    '''
    #    '''
        
    def test_decrypt_valid(self):
        '''Tests to see if we can decrypt a known file and compare that with existing 'unencrypted' version of the file'''
        security = Security()
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_ENCRYPTED_FILE)
        sourceFile = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        dData = security.decryptFile(instance_filename)
        stream = open(sourceFile, 'r')
        uData = stream.read()
        self.assertEqual(uData, dData)
        stream.close()
        
    def test_encrypt_valid(self):
        '''Tests we can encrypt a file.  Encrypted file will be compared against a known "encrypted" file outside of framework'''
        
        security = Security()
        #instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila.xml'#IGNORE:C0301
        instance_filename = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_DECRYPTED_FILE)
        outputFile = instance_filename + ".asc"
        inputFile = os.path.join("%s" % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        #result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        security.setFingerprint(testcase_settings.XML_ENCRYPT_FINGERPRINT)
        security.encryptFile(instance_filename, outputFile)
        dData = security.decryptFile(outputFile)
        # read the input file contents
        stream = open(inputFile, 'r')
        uData = stream.read()
        self.assertEqual(uData, dData)
        stream.close()
        
        
if __name__ == '__main__':
    # Wipe the DB first
    #import postgresutils
    #UTILS = postgresutils.Utils()
    #UTILS.blank_database()
    
    unittest.main()