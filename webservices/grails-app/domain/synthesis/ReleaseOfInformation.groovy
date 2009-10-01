package synthesis

/**
 * The ReleaseOfInformation entity.
 *
 * @author
 *
 *
 */
class ReleaseOfInformation
{
  static mapping = {
    version false

    ididNum column: 'release_of_information_idid_num'
    ididNumDateCollected column: 'release_of_information_idid_num_date_collected'

    ididStr column: 'release_of_information_idid_str'
    ididStrDateCollected column: 'release_of_information_idid_str_date_collected'

    person column: 'person_index_id'
  }

  String ididNum
  Date ididNumDateCollected

  String ididStr
  Date ididStrDateCollected

  String siteServiceIdidNum
  Date siteServiceIdidNumDateCollected

  String siteServiceIdidStr
  Date siteServiceIdidStrDateCollected

  String documentation
  Date documentationDateCollected

  String startDate
  Date startDateDateCollected

  String endDate
  Date endDateDateCollected

  String releaseGranted
  Date releaseGrantedDateCollected

  Person person

}
