package synthesis

/**
 * The PersonAddress entity.
 *
 * @author
 *
 *
 */
class PersonAddress
{
  static mapping = {
    table 'person_address'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
    personHistoricalIndexIdPersonHistorical column: 'person_historical_index_id'
  }
  Long id
  Date addressPeriodStartDate
  Date addressPeriodStartDateDateCollected
  Date addressPeriodEndDate
  Date addressPeriodEndDateDateCollected
  String preAddressLine
  Date preAddressLineDateCollected
  String line1
  Date line1DateCollected
  String line2
  Date line2DateCollected
  String city
  Date cityDateCollected
  String county
  Date countyDateCollected
  String state
  Date stateDateCollected
  String zipcode
  Date zipcodeDateCollected
  String country
  Date countryDateCollected
  Long isLastPermanentZip
  Date isLastPermanentZipDateCollected
  Long zipQualityCode
  Date zipQualityCodeDateCollected
  // Relation
  PersonHistorical personHistoricalIndexIdPersonHistorical

  static constraints = {
    id()
    addressPeriodStartDate(nullable: true)
    addressPeriodStartDateDateCollected(nullable: true)
    addressPeriodEndDate(nullable: true)
    addressPeriodEndDateDateCollected(nullable: true)
    preAddressLine(size: 0..32)
    preAddressLineDateCollected(nullable: true)
    line1(size: 0..32)
    line1DateCollected(nullable: true)
    line2(size: 0..32)
    line2DateCollected(nullable: true)
    city(size: 0..32)
    cityDateCollected(nullable: true)
    county(size: 0..32)
    countyDateCollected(nullable: true)
    state(size: 0..32)
    stateDateCollected(nullable: true)
    zipcode(size: 0..10)
    zipcodeDateCollected(nullable: true)
    country(size: 0..32)
    countryDateCollected(nullable: true)
    isLastPermanentZip(nullable: true, max: 9999999999L)
    isLastPermanentZipDateCollected(nullable: true)
    zipQualityCode(nullable: true, max: 9999999999L)
    zipQualityCodeDateCollected(nullable: true)
    personHistoricalIndexIdPersonHistorical()
  }

  String toString()
  {
    return "${id}"
  }
}
