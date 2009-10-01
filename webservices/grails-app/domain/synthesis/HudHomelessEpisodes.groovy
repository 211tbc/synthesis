package synthesis

/**
 * The HudHomelessEpisodes entity.
 *
 * @author
 *
 *
 */
class HudHomelessEpisodes
{
  static mapping = {
    table 'hud_homeless_episodes'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
    personHistoricalIndexIdPersonHistorical column: 'person_historical_index_id'
  }
  Long id
  String startDate
  Date startDateDateCollected
  String endDate
  Date endDateDateCollected
  // Relation
  PersonHistorical personHistoricalIndexIdPersonHistorical

  static constraints = {
    id()
    startDate(size: 0..32)
    startDateDateCollected(nullable: true)
    endDate(size: 0..32)
    endDateDateCollected(nullable: true)
    personHistoricalIndexIdPersonHistorical()
  }

  String toString()
  {
    return "${id}"
  }
}
