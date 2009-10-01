import groovy.xml.MarkupBuilder
import synthesis.xml.PersonToXml
import synthesis.Person
import synthesis.Source
import synthesis.Export
import synthesis.xml.SourceDatabaseToXml
import synthesis.Source

class XmlController
{

  def index = { }

  // retrieve and output XML based on a Person ID
  def person = {
    // this will eventually be passed in from parameters
    def personId = 1
    Person person = Person.get(personId)
    Export export = Export.findByExportId(person.exportId)
    Source source = Source.findByExportId(export.exportId)

    def xml = new SourceDatabaseToXml()
    xml.people = [person]
    xml.export = export
    xml.source = source
    render(text:xml.xml, contentType: 'text/xml', encoding: 'UTF-8')
  }

  // retrieve and output XML based on an Export ID (Would this ever really happen?)
  def export = {
    def w = new StringWriter()
    def builder = new MarkupBuilder(w)

    builder.html {
      head {
        title("Not yet implemented")
      }
      body {
        p("Not yet implemented")
      }
    }

    render w.toString()
  }

  // retrieve and output XML based on a Source ID
  def source = {
    // this will eventually be passed in from parameters
    def sourceId = 1
    def source = Source.get(sourceId)
    def export = Export.findByExportId(source.exportId)
    def people = Person.findAllByExportId(export.exportId)

    def xml = new SourceDatabaseToXml()
    xml.source = source
    xml.export = export
    xml.people = people

    render(text:xml.xml, contentType:'text/xml', encoding: 'UTF-8')
  }

  // profit!
}
