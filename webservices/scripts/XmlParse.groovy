import groovy.xml.DOMBuilder
import groovy.xml.Namespace
import groovy.xml.dom.DOMCategory
import groovy.util.slurpersupport.GPathResult

def basePath  = '/Users/dglidden/Src/synthesis/python/InputFiles'
def xsdFile   = "${basePath}/HUD_HMIS_2_8.xsd"
def testFile1 = "${basePath}/Example_Extend_HUD_HMIS_2_8_Instance.xml"
def testFile2 = "${basePath}/Example_HUD_HMIS_2_8_Instance.xml"
def testFile3 = "${basePath}/coastal_sheila_invalid.xml"
def testFile4 = "${basePath}/coastal_sheila_malformed.xml"


// using XmlSlurper (works. recommended way of handling XML)
println '*** XmlSlurper'
def databaseDoc = new XmlSlurper().parse(testFile2)
def namespaces = [:]
namespaces.hmis = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd"
namespaces.airs = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
namespaces.xsi="http://www.w3.org/2001/XMLSchema-instance"
databaseDoc.declareNamespace(namespaces)


// println xmlSlurpDoc.DatabaseID.IDNum
assert databaseDoc.'hmis:DatabaseContactEmail' == 'test@test.com'
assert databaseDoc.DatabaseID.IDNum == 1
assert databaseDoc.DatabaseID.IDNum.@dateCollected == '2004-08-01T00:00:00'

assert databaseDoc.'hmis:SiteService'.'airs:Name' == 'Shelter From The Storm'
assert databaseDoc.'hmis:SiteService'.'airs:Phone'.@TollFree == '1'

assert databaseDoc.'hmis:Person'.size() == 3

assert databaseDoc.'hmis:Person'[0].'hmis:PersonID' == 'DCF017Y0'
assert databaseDoc.'hmis:Person'[0].'hmis:LegalFirstName' == 'George'
assert databaseDoc.'hmis:Person'[0].'hmis:LegalLastName' == 'Washington'

assert databaseDoc.'hmis:Person'[1].'hmis:PersonID' == '7451'
assert databaseDoc.'hmis:Person'[1].'hmis:LegalFirstName' == 'Robert'
assert databaseDoc.'hmis:Person'[1].'hmis:LegalLastName' == 'Kennedy'

assert databaseDoc.'hmis:Person'[2].'hmis:PersonID' == '1234763'
assert databaseDoc.'hmis:Person'[2].'hmis:LegalFirstName' == ''
assert databaseDoc.'hmis:Person'[2].'hmis:LegalLastName' == ''



