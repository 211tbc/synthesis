'''Unit-tests various XML/CSV validation scenarios (called tests also) in 
selector.py.'''
from selector import Selector, HUDHMIS28XMLTest
import unittest
class SelectorTestCase(unittest.TestCase):
    '''see if the return value is a file path'''
    def test_validation_valid(self):
        '''Tests if HMIS XML 2.8 test is validating properly.'''
        select = Selector()
        instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila.xml'#IGNORE:C0301
        result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        print result
        self.assertEqual(result, True)
    def test_validation_invalid(self):
        '''Tests if HMIS XML 2.8 test is properly invalidating some invalid XML
        '''
        select = Selector()
        instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila_invalid.xml'#IGNORE:C0301
        result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        print result
        self.assertEqual(result, False)
    def test_validation_malformed_xml(self):
        '''Tests if HMIS XML 2.8 test is properly invalidating some malformed 
        XML.  Malformed in this context means missing an end tag or some basic
        XML error.  Not a schema validation driven error.'''
        select = Selector()
        instance_filename = '/home/eric/workspace/reposHUD/trunk/Coastal_HSXML_converter/test_xml/coastal_sheila_malformed.xml'#IGNORE:C0301
        result = select.validate(HUDHMIS28XMLTest(), instance_filename)
        print result
        self.assertEqual(result, None)    
if __name__ == '__main__':
    unittest.main()