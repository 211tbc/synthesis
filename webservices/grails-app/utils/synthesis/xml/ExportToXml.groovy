package synthesis.xml
/**
 * Created by IntelliJ IDEA.
 * User: dglidden
 * Date: Sep 28, 2009
 * Time: 3:48:36 PM
 * To change this template use File | Settings | File Templates.
 */

public class ExportToXml {

  def getXml(def export)
  {
    def Export = {
      hmis.Export {
        hmis.ExportID {
          hmis.IDNum(['hmis:DateCollected':export.exportIdDateCollected], export.exportId)
        }
        hmis.ExportDate(['hmis:DateCollected':export.exportDateDateCollected], export.exportDate)
        hmis.ExportPeriod {
          hmis.StartDate(['hmis:DateCollected':export.startDateDateCollected], export.startDate)
          hmis.EndDate(['hmis:DateCollected':export.endDateDateCollected], export.endDate)
        }
        hmis: SoftwareVendor(['hmis:DateCollected':export.softwareVendorDateCollected], export.softwareVendor)
        hmis.SoftwareVersion(['hmis:DateCollected':export.softwareVersionDateCollected], export.softwareVersion)
      }
    }

    return Export
  }

}