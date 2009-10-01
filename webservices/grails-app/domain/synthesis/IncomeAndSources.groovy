package synthesis

/**
 * The IncomeAndSources entity.
 *
 * @author
 *
 *
 */
class IncomeAndSources
{
  static mapping = {
    table 'income_and_sources'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'identity', column: 'id'
    personHistoricalIndexIdPersonHistorical column: 'person_historical_index_id'
  }
  Long id
  Long amount
  Date amountDateCollected
  Long incomeSourceCode
  Date incomeSourceCodeDateCollected
  String incomeSourceOther
  Date incomeSourceOtherDateCollected
  // Relation
  PersonHistorical personHistoricalIndexIdPersonHistorical

  static constraints = {
    id()
    amount(nullable: true, max: 9999999999L)
    amountDateCollected(nullable: true)
    incomeSourceCode(nullable: true, max: 9999999999L)
    incomeSourceCodeDateCollected(nullable: true)
    incomeSourceOther(size: 0..32)
    incomeSourceOtherDateCollected(nullable: true)
    personHistoricalIndexIdPersonHistorical()
  }

  String toString()
  {
    return "${id}"
  }
}
