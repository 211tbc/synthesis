package synthesis.xml
/**
 * Created by IntelliJ IDEA.
 * User: dglidden
 * Date: Sep 28, 2009
 * Time: 3:51:40 PM
 * To change this template use File | Settings | File Templates.
 */

public class SiteServiceToXml {

  def siteServices

  def getXml(def siteService)
  {
    def SiteService = {
      hmis.SiteService()
    }

    return SiteService
  }

  def getXmlLater(def siteServices)
  {
    def dc = ['hmis:DateCollected':'2001-01-01']

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

    return SiteService
  }

  def getXmlLater()
  {
    return this.getXmlLater(this.siteServices)
  }

}