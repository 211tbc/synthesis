package synthesis

/**
 * The SourceDatabase entity.
 *
 * @author
 *
 *
 */

class Source
{
  static mapping = {
    version false

    email column: 'source_email'
    emailDateCollected column: 'source_email_date_collected'

    contactExtension column: 'source_contact_extension'
    contactExtensionDateCollected column: 'source_contact_extension_date_collected'

    contactLast column: 'source_contact_last'
    contactLastDateCollected column: 'source_contact_last_date_collected'

    contactPhone column: 'source_contact_phone'
    contactPhoneDateCollected column: 'source_contact_phone_date_collected'

    name column: 'source_name'
    nameDateCollected column: 'source_name_date_collected'
  }

  // don't really know what the difference between 'id' and 'database_id'
  String databaseId
  Date   databaseIdDateCollected

  String exportId

  String email
  Date   emailDateCollected

  String contactExtension
  Date   contactExtensionDateCollected

  // supposted to also be a first here
  // String contactFirst
  // Date   contactFirstDateCollected

  String contactLast
  Date   contactLastDateCollected

  String contactPhone
  Date   contactPhoneDateCollected

  String name
  Date   nameDateCollected
}
