package synthesis

/**
 * The OtherNames entity.
 *
 * @author
 *
 *
 */
class OtherNames
{
  static mapping = {
    version false

    firstName column: 'other_first_name_unhashed'
    firstNameHashed column: 'other_first_name_hashed'
    firstNameDateCollected column: 'other_first_name_date_collected'    

    middleName column: 'other_middle_name_unhashed'
    middleNameHashed column: 'other_middle_name_hashed'
    middleNameDateCollected column: 'other_middle_name_date_collected'    

    lastName column: 'other_last_name_unhashed'
    lastNameHashed column: 'other_last_name_hashed'
    lastNameDateCollected column: 'other_last_name_date_collected'    

    suffix column: 'other_suffix_unhashed'
    suffixHashed column: 'other_suffix_hashed'
    suffixDateCollected column: 'other_suffix_date_collected'    

    person column: 'person_index_id'
  }

  String firstName
  String firstNameHashed
  Date   firstNameDateCollected

  String middleName
  String middleNameHashed
  Date   middleNameDateCollected

  String lastName
  String lastNameHashed
  Date   lastNameDateCollected

  String suffix
  String suffixHashed
  Date   suffixDateCollected

  Person person
}
