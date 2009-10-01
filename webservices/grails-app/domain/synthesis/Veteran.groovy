package synthesis

/**
 * The Veteran entity.
 *
 * @author
 *
 *
 */
class Veteran
{
  static mapping = {
    table 'veteran'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
    personHistoricalIndexIdPersonHistorical column: 'person_historical_index_id'
  }
  Long id
  Long serviceEra
  Date serviceEraDateCollected
  Long militaryServiceDuration
  Date militaryServiceDurationDateCollected
  Long servedInWarZone
  Date servedInWarZoneDateCollected
  Long warZone
  Date warZoneDateCollected
  String warZoneOther
  Date warZoneOtherDateCollected
  Long monthsInWarZone
  Date monthsInWarZoneDateCollected
  Long receivedFire
  Date receivedFireDateCollected
  Long militaryBranch
  Date militaryBranchDateCollected
  String militaryBranchOther
  Date militaryBranchOtherDateCollected
  Long dischargeStatus
  Date dischargeStatusDateCollected
  String dischargeStatusOther
  Date dischargeStatusOtherDateCollected
  // Relation
  PersonHistorical personHistoricalIndexIdPersonHistorical

  static constraints = {
    id()
    serviceEra(nullable: true, max: 9999999999L)
    serviceEraDateCollected(nullable: true)
    militaryServiceDuration(nullable: true, max: 9999999999L)
    militaryServiceDurationDateCollected(nullable: true)
    servedInWarZone(nullable: true, max: 9999999999L)
    servedInWarZoneDateCollected(nullable: true)
    warZone(nullable: true, max: 9999999999L)
    warZoneDateCollected(nullable: true)
    warZoneOther(size: 0..50)
    warZoneOtherDateCollected(nullable: true)
    monthsInWarZone(nullable: true, max: 9999999999L)
    monthsInWarZoneDateCollected(nullable: true)
    receivedFire(nullable: true, max: 9999999999L)
    receivedFireDateCollected(nullable: true)
    militaryBranch(nullable: true, max: 9999999999L)
    militaryBranchDateCollected(nullable: true)
    militaryBranchOther(size: 0..50)
    militaryBranchOtherDateCollected(nullable: true)
    dischargeStatus(nullable: true, max: 9999999999L)
    dischargeStatusDateCollected(nullable: true)
    dischargeStatusOther(size: 0..50)
    dischargeStatusOtherDateCollected(nullable: true)
    personHistoricalIndexIdPersonHistorical()
  }

  String toString()
  {
    return "${id}"
  }
}
