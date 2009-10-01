package synthesis.xml

import synthesis.OtherNames
import synthesis.ReleaseOfInformation
import synthesis.Person

/**
 * Created by IntelliJ IDEA.
 * User: dglidden
 * Date: Sep 24, 2009
 * Time: 2:32:53 PM
 * To change this template use File | Settings | File Templates.
 */

public class PersonToXml
{

  Person person

  def getXml(Person person)
  {
    def Person = {
      hmis.Person {
        hmis.PersonID {
          hmis.Hashed(['hmis:DateCollected':person.idDateCollected], person.idHashed)
          hmis.DateOfBirth {
            hmis.Unhashed(['hmis:DateCollected':person.dateOfBirthDateCollected], person.dateOfBirth)
          }
          hmis.Ethnicity {
            hmis.Unhashed(['hmis:DateCollected':person.ethnicityDateCollected], person.ethnicity)
          }
          hmis.Gender {
            hmis.Gender(['hmis:DateCollected':person.genderDateCollected], person.gender)
          }
          hmis.LegalFirstName {
            hmis.Unhashed(['hmis:DateCollected':person.firstNameDateCollected], person.firstName)
          }
          hmis.LegalLastName {
            hmis.Unhashed(['hmis:DateCollected':person.lastNameDateCollected], person.lastName)
          }
          hmis.LegalMiddleName {
            hmis.Unhashed(['hmis:DateCollected':person.middleNameDateCollected], person.middleName)
          }
          hmis.LegalSuffix {
            hmis.Unhashed(['hmis:DateCollected':person.suffixDateCollected], person.suffix)
          }
          hmis.SocialSecurityNumber {
            hmis.Unhashed(['hmis:DateCollected':person.ssnDateCollected], person.ssn)
            hmis.SocialSecurityNumberQualityCode(['hmis:DateCollected':person.ssnQualityCodeDateCollected], person.ssnQualityCode)
          }

          // TODO don't know if this will actually work until this table gets populated
          hmis.OtherNames {
            person.otherNames.each { OtherNames otherName ->
              hmis.OtherFirstName {
                hmis.Unhashed(['hmis:DateCollected':otherName.firstNameDateCollected], otherName.firstName)
              }
              hmis.OtherMiddleName {
                hmis.Unhashed(['hmis:DateCollected':otherName.middleNameDateCollected], otherName.middleName)
              }
              hmis.OtherLastName {
                hmis.Unhashed(['hmis:DateCollected':otherName.lastNameDateCollected], otherName.lastName)
              }
              hmis.OtherSuffix {
                hmis.Unhashed(['hmis:DateCollected':otherName.suffixDateCollected], otherName.suffix)
              }
            }
          }

          // TODO not present anywhere I can find
          hmis.SiteServiceParticipation()

          // TODO pretty sure the "idid" column names are wrong
          hmis.ReleaseOfInformation {
            person.releases.each { ReleaseOfInformation release ->
              hmis.ReleaseOfInformationID {
                hmis.IDNum(['hmis:DateCollected':release.ididNumDateCollected], release.ididNum)
              }
              hmis.SiteServiceID {
                hmis.IDNum(['hmis:DateCollected':release.siteServiceIdidNumDateCollected], release.siteServiceIdidNumDateCollected)
              }
              hmis.Documentation(['hmis:DateCollected':release.documentationDateCollected], release.documentation)
              hmis.EffectivePeriod {
                hmis.StartDate(['hmis:DateCollected':release.startDateDateCollected], release.startDateDateCollected)
                hmis.EndDate(['hmis:DateCollected':release.endDateDateCollected], release.endDate)
              }
              hmis.ReleaseGranted(['hmis:DateCollected':release.releaseGrantedDateCollected], release.releaseGranted)
            }
          }
        }
      }
    }

    return Person
  }

  def getXml()
  {
    return this.getXml(this.person)
  }

}