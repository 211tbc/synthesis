__author__ = 'eric'

SOAP_TRANSPORT_PROPERTIES = {
    "CCD"                               : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "SOURCE_OBJECT"                     : "SubmissionSet01",
    "DOCUMENT_OBJECT"                   : "Document01",
    "ASSOCIATION_SECTION"               : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "ATTACHMENT_SECTION"                : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "MIME_BORDER_SECTION"               : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "START_UUID"                        : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "XML_UUID"                          : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "MESSAGE_ID_UUID"                   : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "EXTRINSIC_OBJECT_UUID"             : "7edca82f-054d-47f2-a032-9b2a5b5186c1", # <== Where does this value come from?
    "AUTHOR_UUID"                       : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "EXTRINSIC_UUID"                    : "93606bcf-9494-43ec-9b4e-a7748d1a838d", # <== Where does this value come from?
    "REGISTRY_UUID"                     : "a7058bb9-b4e4-4307-ba5b-e3f0ab85e12d", # <== Where does this value come from?
    "REGISTRY_PACKAGE_UNIQUE_ID_UUID"   : "96fdda7c-d067-4183-912e-bf5ee74998a8", # <== Where does this value come from?
    "REGISTRY_PACKAGE_SOURCE_ID_UUID"   : "554ac39e-e3fe-47fe-b233-965d2a147832", # <== Where does this value come from?
    "REGISTRY_PACKAGE_PATIENT_ID_UUID"  : "6b5aea1a-874d-4603-a4bc-96a0a7b38446", # <== Where does this value come from?
    "PATIENT_ID"                        : "", # <== Where does this value come from?
    "SOURCE_ID"                         : "", # <== Where does this value come from?
    "UNIQUE_ID"                         : "", # <== Where does this value come from?
    "ASSOCIATION_ID"                    : "ID_00000000_0", # <== Where does this value come from?
    "ASSOCIATION_VALUE"                 : "Original", # <== Where does this value come from?
    "EXTRINSIC_AUTHOR_PERSON"           : "", # <== Where does this value come from?
    "REGISTRY_AUTHOR_PERSON"            : "", # <== Where does this value come from?
    "CONTENT_TYPE_CODE_UUID"            : "aa543740-bdda-424e-8c96-df4873be8500", # <== Where does this value come from?
    "CONTENT_TYPE_CODE_NODE_REPRESENTATION" : "History and Physical", # <== Where does this value come from?
    "CONTENT_TYPE_CODE_CODING_SCHEME"       : "Connect-a-thon contentTypeCodes", # <== Where does this value come from?
    "CONTENT_TYPE_CODE_LOCALIZED_STRING"    : "History and Physical", # <== Where does this value come from?
    "SUBMISSION_TIME"                   : "", #<== Is format YYYYMMDDHHMMSS? Is this module responsible for generating this?
    "CREATION_TIME"                     : "", #<== Is format YYYYMMDD? Is this module responsible for generating this?
    "LANGUAGE_CODE"                     : "", # <== Leave this blank. It will be assigned by the soaptransport module.
    "SOURCE_PATIENT_ID"                 : "", # <== Where does this value come from?
    "CLASS_CODE_UUID"                   : "41a5887f-8865-4c09-adf7-e362475b143a", # <== Where does this value come from?
    "CLASS_CODE_NODE_REPRESENTATION"    : "History and Physical", # Where does this value come from?
    "CLASS_CODE_VALUE"                  : "Connect-a-thon classCodes", # Where does this value come from?
    "CLASS_CODE_NAME"                   : "History and Physical", # Where does this value come from?
    "CONFIDENTIALITY_CODE_UUID"         : "f4f85eac-e6cb-4883-b524-f2705394840f", # <== Where does this value come from?
    "CONFIDENTIALITY_CODE_NODE_REPRESENTATION" : "1.3.6.1.4.1.21367.2006.7.101", # Where does this value come from?
    "CONFIDENTIALITY_CODE_VALUE"        : "Connect-a-thon confidentialityCodes", # Where does this value come from?
    "CONFIDENTIALITY_CODE_NAME"         : "Clinical-Staff", # Where does this value come from?
    "FORMAT_CODE_UUID"                  : "a09d5840-386c-46f2-b5ad-9c3699a4309d", # <== Where does this value come from?
    "FORMAT_CODE_NODE_REPRESENTATION"   : "CDAR2/IHE 1.0", # Where does this value come from?
    "FORMAT_CODE_VALUE"                 : "Connect-a-thon formatCodes", # Where does this value come from?
    "FORMAT_CODE_NAME"                  : "CDAR2/IHE 1.0", # Where does this value come from?
    "HEALTHCARE_FACILITY_TYPE_CODE_UUID" : "f33fb8ac-18af-42cc-ae0e-ed0b0bdb91e1", # <== Where does this value come from?
    "HEALTHCARE_FACILITY_TYPE_CODE_NODE_REPRESENTATION" : "Outpatient", # Where does this value come from?
    "HEALTHCARE_FACILITY_TYPE_CODE_VALUE" : "Connect-a-thon healthcareFacilityTypeCodes", # Where does this value come from?
    "HEALTHCARE_FACILITY_TYPE_CODE_NAME" : "Outpatient", # Where does this value come from?
    "PRACTICE_SETTING_CODE_UUID"        : "cccf5598-8b07-4b77-a05e-ae952c785ead", # <== Where does this value come from?
    "PRACTICE_SETTING_CODE_NODE_REPRESENTATION" : "General Medicine", # Where does this value come from?
    "PRACTICE_SETTING_CODE_VALUE"       : "Connect-a-thon practiceSettingCodes", # Where does this value come from?
    "PRACTICE_SETTING_CODE_NAME"        : "General Medicine", # Where does this value come from?
    "RECEIVING_PROVIDER_ID"                          : "", # <== Leave this blank. It will be assigned by the soaptransport module
    "TYPE_CODE_UUID"                    : "f0306f51-975f-434e-a61c-c59651d33983", # <== Where does this value come from?
    "TYPE_CODE_NODE_REPRESENTATION"     : "34108-1", # Where does this value come from?
    "TYPE_CODE_VALUE"                   : "LOINC", # Where does this value come from?
    "TYPE_CODE_NAME"                    : "Outpatient Evaluation And Management", # Where does this value come from?
    "DOCUMENT_ENTRY_PATIENTID_UUID"     : "58a6f841-87b3-4a3e-92fd-a8ffeff98427", # <== Where does this value come from?
    "DOCUMENT_ENTRY_UNIQUEID_UUID"      : "2e82c1f6-a085-4c72-9da3-8640a32e42ab", # <== Where does this value come from?
    "SUBMISSION_SET_UUID"               : "a54d6aa5-d40d-43f9-88c5-b4633d873bdd", # <== Where does this value come from?
    "SUBMISSION_SET_ID"                 : "ID_000000_0", # <== Where does this value come from?
    "DIRECT_FROM"                       : "<Referer From Address used in SOAP envelope header>", # It's not an actual email - it will just send the referral to their referral workflow.
    "DIRECT_TO"                       : "<A Netsmart TO Address used in SOAP envelope header>",
    #
    # The following are optional
    #
    "REGISTRY_PACKAGE_NAME_TAG"         : "", # Where does this value come from?
    "REGISTRY_PACKAGE_DESCRIPTION_TAG"  : "", # Where does this value come from?
    "EXTRINSIC_NAME_TAG"                : "", # Where does this value come from?
    "EXTRINSIC_DESCRIPTION_TAG"         : "", # Where does this value come from?
    "EXTRINSIC_AUTHOR_INSTITUTION_SLOT" : "", # Where does this value come from?
    "EXTRINSIC_AUTHOR_ROLE_SLOT"        : "", # Where does this value come from?
    "EXTRINSIC_AUTHOR_SPECIALTY_SLOT"   : "", # Where does this value come from?
    "REGISTRY_AUTHOR_INSTITUTION_SLOT"  : "", # Where does this value come from?
    "REGISTRY_AUTHOR_ROLE_SLOT"         : "", # Where does this value come from?
    "REGISTRY_AUTHOR_SPECIALTY_SLOT"    : "", # Where does this value come from?
    "SERVICE_START_TIME"                : "", # Is format YYYYMMDDHHMM? Where does this value come from?
    "SERVICE_STOP_TIME"                 : "", # Is format YYYYMMDDHHMM? Where does this value come from?
    "SOURCE_PATIENT_INFO"               : "", # Where do these values come from?
}
