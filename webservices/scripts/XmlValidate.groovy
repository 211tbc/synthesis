import javax.xml.XMLConstants
import javax.xml.transform.stream.StreamSource
import javax.xml.validation.SchemaFactory

def basePath  = '/Users/dglidden/Src/synthesis/python/InputFiles/'
def xsdFile   = "${basePath}/HUD_HMIS_2_8.xsd"
def testFile1 = "${basePath}/Example_Extend_HUD_HMIS_2_8_Instance.xml"
def testFile2 = "${basePath}/Example_HUD_HMIS_2_8_Instance.xml"
def testFile3 = "${basePath}/coastal_sheila_invalid.xml"
def testFile4 = "${basePath}/coastal_sheila_malformed.xml"

def factory   = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI)
def schema    = factory.newSchema(new StreamSource(new FileReader(xsdFile)))
def validator = schema.newValidator()

assert validator.validate(new StreamSource(new FileReader(testFile1)))
assert validator.validate(new StreamSource(new FileReader(testFile2)))
assert validator.validate(new StreamSource(new FileReader(testFile3)))
shouldFail { validator.validate(new StreamSource(new FileReader(testFile4))) }

// should be a validating XmlParser instance
new XmlParser(true, false).parseText(testFile2)


