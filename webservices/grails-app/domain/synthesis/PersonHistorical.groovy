package synthesis

/**
 * The PersonHistorical entity.
 *
 * @author
 *
 *
 */
class PersonHistorical
{
  static mapping = {
    table 'person_historical'
    // version is set to false, because this isn't available by default for legacy databases
    version false
    id generator: 'sequence', params: [name: 'person_historical_id_seq']
    // person column:'person_index_id'
  }

  Long id
  Long personHistoricalIdNum
  Date personHistoricalIdNumDateCollected
  String personHistoricalIdStr
  Date personHistoricalIdStrDateCollected
  Long barrierCode
  Date barrierCodeDateCollected
  String barrierOther
  Date barrierOtherDateCollected
  Long childCurrentlyEnrolledInSchool
  Date childCurrentlyEnrolledInSchoolDateCollected
  Long currentlyEmployed
  Date currentlyEmployedDateCollected
  Long currentlyInSchool
  Date currentlyInSchoolDateCollected
  Long degreeCode
  Date degreeCodeDateCollected
  String degreeOther
  Date degreeOtherDateCollected
  Long developmentalDisability
  Date developmentalDisabilityDateCollected
  Long domesticViolence
  Date domesticViolenceDateCollected
  Long domesticViolenceHowLong
  Date domesticViolenceHowLongDateCollected
  Date dueDate
  Date dueDateDateCollected
  Long employmentTenure
  Date employmentTenureDateCollected
  Long healthStatus
  Date healthStatusDateCollected
  Long highestSchoolLevel
  Date highestSchoolLevelDateCollected
  Long hivaidsStatus
  Date hivaidsStatusDateCollected
  Long hoursWorkedLastWeek
  Date hoursWorkedLastWeekDateCollected
  Long hudChronicHomeless
  Date hudChronicHomelessDateCollected
  Long hudHomeless
  Date hudHomelessDateCollected
  Long lengthOfStayAtPriorResidence
  Date lengthOfStayAtPriorResidenceDateCollected
  Long lookingForWork
  Date lookingForWorkDateCollected
  Long mentalHealthIndefinite
  Date mentalHealthIndefiniteDateCollected
  Long mentalHealthProblem
  Date mentalHealthProblemDateCollected
  Long nonCashSourceCode
  Date nonCashSourceCodeDateCollected
  String nonCashSourceOther
  Date nonCashSourceOtherDateCollected
  String personEmail
  Date personEmailDateCollected
  String personPhoneNumber
  Date personPhoneNumberDateCollected
  Long physicalDisability
  Long physicalDisabilityDataColStage
  Date physicalDisabilityDateCollected
  Date physicalDisabilityDateEffective
  Long pregnancyStatus
  Date pregnancyStatusDateCollected
  Long priorResidence
  Date priorResidenceDateCollected
  String priorResidenceOther
  Date priorResidenceOtherDateCollected
  Long reasonForLeaving
  Date reasonForLeavingDateCollected
  String reasonForLeavingOther
  Date reasonForLeavingOtherDateCollected
  Date schoolLastEnrolledDate
  Date schoolLastEnrolledDateDateCollected
  String schoolName
  Date schoolNameDateCollected
  Long schoolType
  Date schoolTypeDateCollected
  String subsidyOther
  Date subsidyOtherDateCollected
  Long subsidyType
  Date subsidyTypeDateCollected
  Long substanceAbuseIndefinite
  Date substanceAbuseIndefiniteDateCollected
  Long substanceAbuseProblem
  Date substanceAbuseProblemDateCollected
  java.math.BigDecimal totalIncome
  Date totalIncomeDateCollected
  Long vocationalTraining
  Date vocationalTrainingDateCollected

  // Person person

  String toString()
  {
    return "${id}"
  }
}
