import groovy.xml.StreamingMarkupBuilder

def namespaces = [:]
namespaces.hmis = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd"
namespaces.airs = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
namespaces.xsi = "http://www.w3.org/2001/XMLSchema-instance"

def dateCollected = '2004-08-01T00:00:00'

def xml = new StreamingMarkupBuilder()

xml.encoding = 'UTF-8'

def dc = ['hmis:dateCollected': dateCollected]

def Export = {
   hmis.Export {
      hmis.ExportID {
         hmis.IDNum(dc, '1')
      }
      hmis.ExportDate(dc, dateCollected)
      hmis.ExportPeriod {
         hmis.StartDate(dc, dateCollected)
         hmis.EndDate(dc, dateCollected)
      }
      hmis:SoftwareVendor(dc, 'HMIS_\'R_Us')
      hmis.SoftwareVersion(dc, '1.1')
   }
}

def SiteService = {
   hmis.SiteService {
      airs.Name('Shelter From The Storm')
      airs.Phone(TollFree: '1', Confidential: '1') {
         airs.PhoneNumber('800.342.1209')
      }
      airs.Taxonomy {
         airs.Code('BH-180')
      }
      hmis.SiteServiceID {
         hmis.IDNum(dc, '1567')
      }
      hmis.FIPSCode(dc, '2502711010')
      hmis.FacilityCode(dc, '034')
      hmis.COCCode(dc, '027')
      hmis.SiteServiceType(dc, '1')
      hmis.SiteServiceTypeOther(dc)
      hmis.IndividualFamilyCode(dc, '1')
      hmis.TargetPopulation(dc, 'Individuals')
      hmis.SiteID {
         hmis.IDNum(dc, '0')
      }
   }
}

def Person = {
   hmis.Person {
      hmis.PersonID {
         hmis.Hashed(dc, 'DCF017Y0')
         hmis.DateOfBirth {
            hmis.Unashed(dc, '01-01-1970')
         }
         hmis.Ethnicity {
            hmis.Unashed(dc, '0')
         }
         hmis.Gender {
            hmis.Unhashed(dc, '1')
         }
         hmis.LegalFirstName {
            hmis.Unhashed(dc, 'George')
         }
         hmis.LegalLastName {
            hmis.Unhashed(dc, 'Washington')
         }
         hmis.LegalMiddleName()
      }
   }
}

def SourceDatabase = {
   mkp.xmlDeclaration()
   mkp.declareNamespace('hmis' : namespaces.hmis)
   mkp.declareNamespace('airs' : namespaces.airs)
   mkp.declareNamespace('xsi' : namespaces.xsi)

   hmis.SourceDatabase {
      hmis.DatabaseID {
         hmis.IDNum(dc, '1')
      }
      hmis.DatabaseContactEmail(dc, 'test@test.com')
      hmis.DatabaseContactExtension(dc, '75511')
      hmis.DatabaseContactFirst(dc, 'Normal')
      hmis.DatabaseContactLast(dc, 'Fell')
      hmis.DatabaseContactPhone(dc, '6179234567')
      hmis.DatabaseName(dc, 'Hal_the_Database')
      out << Export
      out << SiteService
      out << Person
   }
}

def writer = new FileWriter('test.xml')
writer << xml.bind(SourceDatabase)

