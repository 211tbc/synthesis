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

    contactFirst column: 'source_contact_first'
    contactFirstDateCollected column: 'source_contact_first_date_collected'

    contactLast column: 'source_contact_last'
    contactLastDateCollected column: 'source_contact_last_date_collected'

    contactPhone column: 'source_contact_phone'
    contactPhoneDateCollected column: 'source_contact_phone_date_collected'

    name column: 'source_name'
    nameDateCollected column: 'source_name_date_collected'
  }

  // want to get it so we can map this directly to an Export object, but failing at the moment
  String exportId

  // TODO explain the difference between 'id' and 'source_id'
  String sourceId
  Date   sourceIdDateCollected

  String email
  Date   emailDateCollected

  String contactExtension
  Date   contactExtensionDateCollected

  String contactFirst
  Date   contactFirstDateCollected

  String contactLast
  Date   contactLastDateCollected

  String contactPhone
  Date   contactPhoneDateCollected

  String name
  Date   nameDateCollected

  // not really working right now because of weird FK mapping
  // Export export

  // TODO this probably aught to work except there is currently no association between Source and Household
  // Household household
}
