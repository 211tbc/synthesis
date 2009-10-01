package synthesis.xml

import synthesis.Household

/**
 * Convert Household groovy object to XML
 */

public class HouseholdToXml
{

  Household household

  def getXml(Household household)
  {
    def Household = {
      hmis.Household()
    }

    return Household
  }

  def getXml()
  {
    return this.getXml(this.household)
  }
}