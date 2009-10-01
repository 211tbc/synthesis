package synthesis
/**
 * The Person entity.
 *
 * @author
 *
 *
 */
class Person
{
  static mapping = {
    version false

    idUnhashed column: 'person_id_unhashed'
    idHashed column: 'person_id_hashed'
    idDateCollected column: 'person_id_date_collected'

    dateOfBirth column: 'person_date_of_birth_unhashed'
    dateOfBirthHashed column: 'person_date_of_birth_hashed'
    dateOfBirthDateCollected column: 'person_date_of_birth_date_collected'

    ethnicity column: 'person_ethnicity_unhashed'
    ethnicityHashed column: 'person_ethnicity_hashed'
    ethnicityDateCollected column: 'person_ethnicity_date_collected'

    gender column: 'person_gender_unhashed'
    genderHashed column: 'person_gender_hashed'
    genderDateCollected column: 'person_gender_date_collected'

    firstName column: 'person_legal_first_name_unhashed'
    firstNameHashed column: 'person_legal_first_name_hashed'
    firstNameDateCollected column: 'person_legal_first_name_date_collected'

    lastName column: 'person_legal_last_name_unhashed'
    lastNameHashed column: 'person_legal_last_name_hashed'
    lastNameDateCollected column: 'person_legal_last_name_date_collected'

    middleName column: 'person_legal_middle_name_unhashed'
    middleNameHashed column: 'person_legal_middle_name_hashed'
    middleNameDateCollected column: 'person_legal_middle_name_date_collected'

    suffix column: 'person_legal_suffix_unhashed'
    suffixHashed column: 'person_legal_suffix_hashed'
    suffixDateCollected column: 'person_legal_suffix_date_collected'

    ssn column: 'person_social_security_number_unhashed'
    ssnHashed column: 'person_social_security_number_hashed'
    ssnDateCollected column: 'person_social_security_number_date_collected'

    ssnQualityCode column: 'person_social_sec_number_quality_code'
    ssnQualityCodeDateCollected column: 'person_social_sec_number_quality_code_date_collected'
  }

  // if we can get the mappings worked out, this should turn into a direct relationship
  // to the Export object
  String  idUnhashed
  String  idHashed
  Date    idDateCollected

  Date    dateOfBirth
  String  dateOfBirthHashed
  Date    dateOfBirthDateCollected

  Integer ethnicity
  String  ethnicityHashed
  Date    ethnicityDateCollected

  Integer gender
  String  genderHashed
  Date    genderDateCollected

  String  firstName
  String  firstNameHashed
  Date    firstNameDateCollected

  String  lastName
  String  lastNameHashed
  Date    lastNameDateCollected

  String  middleName
  String  middleNameHashed
  Date    middleNameDateCollected

  String  suffix
  String  suffixHashed
  Date    suffixDateCollected

  String  ssn
  String  ssnHashed
  Date    ssnDateCollected

  String  ssnQualityCode
  Date    ssnQualityCodeDateCollected

  String  exportId

  static hasMany = [otherNames:OtherNames, releases:ReleaseOfInformation]
}
