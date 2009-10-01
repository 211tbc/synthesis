package synthesis.xml

import synthesis.PersonHistorical

/**
 * Created by IntelliJ IDEA.
 * User: dglidden
 * Date: Sep 28, 2009
 * Time: 4:27:19 PM
 * To change this template use File | Settings | File Templates.
 */

public class PersonHistoricalToXml {

  PersonHistorical personHistorical

  def getXml(PersonHistorical personHistorical)
  {
    def PersonHistorical = {
      hmis.PersonHistorical()
    }

    return PersonHistorical
  }

}