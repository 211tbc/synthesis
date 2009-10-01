package synthesis

/**
 * The Races entity.
 *
 * @author
 *
 *
 */
class Races
{
  static mapping = {
    table 'races'
    version false
    id generator: 'sequence', params: [name: 'races_id_seq']
    person column: 'person_index_id'
  }

  Long id
  Long raceUnhashed
  String raceHashed
  Date raceDateCollected

  Person person

  String toString()
  {
    return "${id}"
  }
}
