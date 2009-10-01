/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package synthesis.xml

import groovy.xml.StreamingMarkupBuilder
import synthesis.OtherNames
import synthesis.ReleaseOfInformation

/**
 * The root util class for taking groovy objects that have been imported from the database
 * and converting them into an XML representation via StreamingMarkupBuilder
 *
 * @author dglidden
 */
class SourceDatabaseToXml
{
  def namespaces = [:]
  def xml

  // this is the root element
  def source
  // these are the direct child elements of SourceDatabase
  def export
  def siteService
  def people // list
  def household

  /**
   * Default constructor
   */
  SourceDatabaseToXml()
  {
    namespaces.hmis = "http://www.hmis.info/schema/2_8/HUD_HMIS_2_8.xsd"
    namespaces.airs = "http://www.hmis.info/schema/2_8/AIRS_3_0_draft5_mod.xsd"
    namespaces.xsi = "http://www.w3.org/2001/XMLSchema-instance"

    xml = new StreamingMarkupBuilder()
    xml.encoding = 'UTF-8'
  }

  /**
   * Do the actual building of the XML for the source database
   * Import the other elements from their own builder classes
   */
  def getXml()
  {
    def SourceDatabase = {
      mkp.xmlDeclaration()
      mkp.declareNamespace('hmis': namespaces.hmis)
      mkp.declareNamespace('airs': namespaces.airs)
      mkp.declareNamespace('xsi': namespaces.xsi)

      hmis.SourceDatabase {
        hmis.DatabaseID {
          // TODO check if it's IDNum or IDStr
          hmis.IDNum(['hmis:DateCollected':source.databaseIdDateCollected], source.databaseId)
        }
        hmis.DatabaseContactEmail(['hmis:DateCollected':source.emailDateCollected], source.email)
        hmis.DatabaseContactExtension(['hmis:DateCollected':source.contactExtensionDateCollected], source.contactExtension)
        hmis.DatabaseContactFirst()
        hmis.DatabaseContactLast(['hmis:DateCollected':source.contactLastDateCollected], source.contactLast)
        hmis.DatabaseContactPhone(['hmis:DateCollected':source.contactPhoneDateCollected], source.contactPhone)
        hmis.DatabaseName(['hmis:DateCollected':source.nameDateCollected], source.name)
        out << new ExportToXml().getXml(export)
        // TODO no SiteService in the database at the moment?
        out << new SiteServiceToXml().getXml(siteService)
        people.each { person ->
          out << new PersonToXml().getXml(person)
        }
        out << new HouseholdToXml().getXml(household)
      }
    }

    return xml.bind(SourceDatabase)
  }
}

