package synthesis

/**
 * The Members entity.
 *
 * @author
 *
 *
 */
class Members
{
  static mapping = {
    table 'members'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
    householdIndexIdHousehold column: 'household_index_id'
  }
  Long id
  String personIdUnhashed
  Date personIdUnhashedDateCollected
  String personIdHashed
  Date personIdHashedDateCollected
  String relationshipToHeadOfHousehold
  Date relationshipToHeadOfHouseholdDateCollected
  // Relation
  Household householdIndexIdHousehold

  static constraints = {
    id()
    personIdUnhashed(size: 0..32)
    personIdUnhashedDateCollected(nullable: true)
    personIdHashed(size: 0..32)
    personIdHashedDateCollected(nullable: true)
    relationshipToHeadOfHousehold(size: 0..32)
    relationshipToHeadOfHouseholdDateCollected(nullable: true)
    householdIndexIdHousehold()
  }

  String toString()
  {
    return "${id}"
  }
}
