'''This module maps data elements and attributes between two \
different XML formats.  The basic idea here is that these \
functions are called with a something to look for and an XML \
mapping file (see example mapper.xml).  Once this mapping file \
is in memory as a DOM, then lookups can be called upon this \
in-memory mapping.  The lookup would return the equivalent \
matched data element or attribute to the one  being looked up. \ 
You use element_translate() to look up elements and \
attribute_translate() to look up attributes.  So, elements/\
attributes in the first format are looked up for matches in the \
second format.'''
 
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
 
from lxml import etree

def element_translate(lookup_element_name, translation = './translation.xml'):
    '''
    Takes a mapping between two XML Schema and puts that mapping \
    into memory used for both parsing incoming and writing \
    XML.
    
    Look up element matches in the etree in-memory translation \
    matches are returned as lists of corresponding destination \
    elements.  If there are more than one matches, use the parent \
    elements(s) separated by forward slashes to denote more of the \
    parent path.'''

    tree = etree.parse(translation)        
    ns1 = 'http://alexandriaconsulting.com'
    #First look up the matching element
    xpstr1 = '//' + lookup_element_name
    #print 'xpstr1 is:' + xpstr1
    #Then find the subsequent map: element with the same element name,
    #which is the translation.  
    xpstr2 = 'following-sibling::map:' + lookup_element_name
    #print 'xpstr2 is: ' + xpstr2
    #The child embedded in the mapper is the actual match
    xpstr3 = 'child::*'
    matches = tree.xpath(xpstr1) 
    #print 'matches are: ', matches
    results = []
    counter = 1
    
    for item in matches:
        map_element = item.xpath(xpstr2, namespaces={'map': ns1})
        if len(map_element) >> 0:
            #print 'there is a mapped element at:' + map_element[0].tag
            match = map_element[0].xpath(xpstr3)
            #print 'match ' + str(counter) + ' is element named: ' + match[0].tag
            results.append(match)
            counter = counter + 1
        else: 
            print "there is no map following" + str(item)
    return results

def attribute_translate(lookup_attribute_name, translation = './translation.xml'):
    '''
    Takes a mapping between two XML Schema and puts that mapping into \
    memory used for both parsing incoming and writing outputed XML.  \
    Look up attribute matches in the etree in-memory translation \
    matches are returned as lists of corresponding destination attributes.  \  
    If there are more than one matches, use the parent attribute(s) \
    separated by forward slashes to denote more of the parent path \
    (xpath location path syntax).
    '''

    tree = etree.parse(translation)        
    ns1 = 'http://alexandriaconsulting.com'
    xpstr1 = '//@map:' + lookup_attribute_name
    #print 'Lookup expression is: ' + xpstr1
    results = tree.xpath(xpstr1, namespaces={'map': ns1}) 
    #print 'matches are:', results
    if len(results) == 0:
        print 'no results'
        return None
    if len(results) == 1:
        return results
    if len(results) >= 2:
        print 'more than one match; need to further refine your search' 
        return None

if __name__ == "__main__":
    #look up an element
    RESULT1 = element_translate('client', './translation.xml')
    #look up an attribute
    RESULT2 = attribute_translate('date', './translation.xml')
    print "Testing a \"client\" element translation:"
    print RESULT1
    print "Testing a \"date\" attribute translation:"
    print RESULT2