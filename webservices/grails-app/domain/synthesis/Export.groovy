package synthesis

class Export
{
  static mapping = {
    version false

    periodStartDate column: 'export_period_start_date'
    periodStartDateDateCollected column: 'export_period_start_date_date_collected'

    periodEndDate column: 'export_period_end_date'
    periodEndDateDateCollected column: 'export_period_end_date_date_collected'

    softwareVendor column: 'export_software_vendor'
    softwareVendorDateCollected column: 'export_software_vendor_date_collected'

    softwareVersion column: 'export_software_version'
    softwareVersionDateCollected column: 'export_software_version_date_collected'

    // this really should be working
    // people column: 'export_id'

    // because of the reversedness of the relation between Source and Export this isn't currently working
    // source column: 'export_id'
  }

  String exportId
  Date   exportIdDateCollected

  Date   exportDate
  Date   exportDateDateCollected

  Date   periodDtartDate
  Date   periodStartDateDateCollected

  Date   periodEndDate
  Date   periodEndDateDateCollected

  String softwareVendor
  Date   softwareVendorDateCollected

  String softwareVersion
  Date   softwareVersionDateCollected

  // see above
  // static hasOne = [source:Source]

  // this really should be working
  // static hasMany = [people:Person]
}
