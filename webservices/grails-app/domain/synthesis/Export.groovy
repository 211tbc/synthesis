package synthesis

class Export
{
  static mapping = {
    version false

    startDate column: 'export_period_start_date'
    startDateDateCollected column: 'export_period_start_date_date_collected'

    endDate column: 'export_period_end_date'
    endDateDateCollected column: 'export_period_end_date_date_collected'

    softwareVendor column: 'export_software_vendor'
    softwareVendorDateCollected column: 'export_software_vendor_date_collected'

    softwareVersion column: 'export_software_version'
    softwareVersionDateCollected column: 'export_software_version_date_collected'

    // just can't do this with the way grails is currently busted
    // person lazy: false
    // sourceDatabase column: 'export_id'
  }

  String exportId
  Date   exportIdDateCollected

  Date   exportDate
  Date   exportDateDateCollected

  Date   startDate
  Date   startDateDateCollected

  Date   endDate
  Date   endDateDateCollected

  String softwareVendor
  Date   softwareVendorDateCollected

  String softwareVersion
  Date   softwareVersionDateCollected

  // see above
  // Source sourceDatabase

  // gotta figure this part out...
  // static hasMany = [people:Person]
}
