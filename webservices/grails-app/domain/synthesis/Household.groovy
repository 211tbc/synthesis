package synthesis

/**
 * The Household entity.
 *
 * @author
 *
 *
 */
class Household
{
  static mapping = {
    table 'household'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
  }
  Long id
  String householdIdNum
  Date householdIdNumDateCollected
  String householdIdStr
  Date householdIdStrDateCollected
  String headOfHouseholdIdUnhashed
  Date headOfHouseholdIdUnhashedDateCollected
  String headOfHouseholdIdHashed
  Date headOfHouseholdIdHashedDateCollected

  static constraints = {
    id()
    householdIdNum(size: 0..32)
    householdIdNumDateCollected(nullable: true)
    householdIdStr(size: 0..32)
    householdIdStrDateCollected(nullable: true)
    headOfHouseholdIdUnhashed(size: 0..32)
    headOfHouseholdIdUnhashedDateCollected(nullable: true)
    headOfHouseholdIdHashed(size: 0..32)
    headOfHouseholdIdHashedDateCollected(nullable: true)
  }

  String toString()
  {
    return "${id}"
  }
}
