''' HUD 3.0 XML export plugin '''

** LAST TOUCHED: 6.24.2010

    
'''
    This code is in a very rough state!
    
    Notes:
        - base class is defined
        - uses HMISXML28Writer as template
        - stripped out all non-3.0 specific code for now, 
          need to add from the 2.8 writer
        - started carrying over re-usable methods from 2.8
        - started defining new elements for 3.0 specific
'''





class HMISXML30Writer(DBObjects.databaseObjects):
	
    
    hmis_namespace = "http://www.hmis.info/schema/3_0/HUD_HMIS.xsd" 
    airs_namespace = "http://www.hmis.info/schema/3_0/AIRS_3_0_mod.xsd"
    nsmap = {"hmis" : hmis_namespace, "airs" : airs_namespace}	


    #####  insert xml specific stuff from 2.8
    

    def createDoc(self):
    	root_element = ET.Element("records")
    	root_element.attrib["xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"
    	root_element.attrib["xsi:noNamespaceSchemaLocation"] = "hud_2010_30_01.xsd" 
    	root_element.attrib["schema_revision"] = "2010_30_01"
    	root_element.text = "\n"
    	return root_element



    def createHouseholds(self, records):
    	households = ET.SubElement(records, "households")
    	return households
    
    def createHousehold(self, households):
    	keyval = 'household'
    	sysID = self.xmlU.generateSysID(keyval)
    	recID = self.xmlU.generateRecID(keyval)	
    	household = ET.SubElement(households, "household")
    	household.attrib["system_id"] = sysID	
    	household.attrib["date_added"] = datetime.now().isoformat()
    	household.attrib["date_updated"] = datetime.now().isoformat()
    	Type = ET.SubElement(household, "type")
    	Type.text = "familystatusPickOption" #this needs to be made dynamic
    	name = ET.SubElement(household, "name")
    	name.text = "tok100Type"
    	return household
	    
    def createMembers(self, household):
	    members = ET.SubElement(household, "members")
    	return members
    
    def createMember(self, members):
    	keyval = 'member'
    	recID = self.xmlU.generateRecID(keyval)	
    	member = ET.SubElement(members, "member")
        member.attrib["record_id"] = recID
    	member.attrib["date_added"] = datetime.now().isoformat()
    	member.attrib["date_updated"] = datetime.now().isoformat()
    	return member
    
    def customizeMember(self, member):
    	client_id = ET.SubElement(member, "client_id")
    	date_entered = ET.SubElement(member, "date_entered")
    	date_ended = ET.SubElement(member, "date_ended")
    	head_of_household = ET.SubElement(member, "head_of_household")
    	relationship = ET.SubElement(member, "relationship")








        xpRegion = 'hmis:Region'
        xpRegionIDIDNum = 'hmis:RegionID/hmis:IDNum'
        xpRegionIDIDStr = 'hmis:RegionID/hmis:IDStr'
        xpSiteServiceID = 'hmis:SiteServiceID'
        xpRegionType = 'hmis:RegionType'
        xpRegionTypeDateCollected = 'hmis:RegionType/@hmis:dateCollected'
        xpRegionTypeDateEffective = 'hmis:RegionType/@hmis:dateEffective'
        xpRegionTypeDataCollectionStage = 'hmis:RegionType/@hmis:dataCollectionStage'
        xpRegionDescription = 'hmis:RegionDescription'
        xpRegionDescriptionDateCollected = 'hmis:RegionDescription/@hmis:dateCollected'
        xpRegionDescriptionDateEffective = 'hmis:RegionDescription/@hmis:dateEffective'
        xpRegionDescriptionDataCollectionStage = 'hmis:RegionDescription/@hmis:dataCollectionStage'

    def createRegion(self, records):
    	region = ET.SubElement(records, "region")
    	return region
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
    	
        xpAgency = 'hmis:Agency'
        xpAgencyDelete = '@hmis:Delete'
        xpAgencyDeleteOccurredDate = '@hmis:DeleteOccurredDate'
        xpAgencyDeleteEffective = '@hmis:DeleteEffective'
        xpAirsKey = 'airs:Key'
        xpAirsName = 'airs:Name'
        xpAgencyDescription = 'airs:AgencyDescription'
        xpIRSStatus = 'airs:IRSStatus'
        xpSourceOfFunds = 'airs:SourceOfFunds'
        xpRecordOwner = '@hmis:RecordOwner'
        xpFEIN = '@hmis:FEIN'
        xpYearInc = '@hmis:YearInc'
        xpAnnualBudgetTotal = '@hmis:AnnualBudgetTotal'
        xpLegalStatus = '@hmis:LegalStatus'
        xpExcludeFromWebsite = '@hmis:ExcludeFromWebsite'
        xpExcludeFromDirectory = '@hmis:ExcludeFromDirectory'    	

    def createAgency(self, records):
    	agency = ET.SubElement(records, "agency")
    	return agency



        xpSite = 'airs:Site'
        xpSiteDeleteOccurredDate = '@airs:DeleteOccurredDate'
        xpSiteDeleteEffective = '@airs:DeleteEffective'
        xpSiteDelete = '@airs:Delete'
        xpKey = 'airs:Key'
        xpName = 'airs:Name'
        xpSiteDescription = 'airs:SiteDescription'
        xpPhysicalAddressPreAddressLine = 'airs:PhysicalAddress/airs:PreAddressLine'
        xpPhysicalAddressLine1 = 'airs:PhysicalAddress/airs:Line1'
        xpPhysicalAddressLine2 = 'airs:PhysicalAddress/airs:Line2'
        xpPhysicalAddressCity = 'airs:PhysicalAddress/airs:City'
        xpPhysicalAddressCounty = 'airs:PhysicalAddress/airs:County'
        xpPhysicalAddressState = 'airs:PhysicalAddress/airs:State'
        xpPhysicalAddressZipCode = 'airs:PhysicalAddress/airs:ZipCode'
        xpPhysicalAddressCountry = 'airs:PhysicalAddress/airs:Country'
        xpPhysicalAddressReasonWithheld = 'airs:PhysicalAddress/airs:ReasonWithheld'
        xpPhysicalAddressConfidential = 'airs:PhysicalAddress/@airs:Confidential'
        xpPhysicalAddressDescription = 'airs:PhysicalAddress/@airs:Description' 
        xpMailingAddressPreAddressLine = 'airs:MailingAddress/airs:PreAddressLine'
        xpMailingAddressLine1 = 'airs:MailingAddress/airs:Line1'
        xpMailingAddressLine2 = 'airs:MailingAddress/airs:Line2'
        xpMailingAddressCity = 'airs:MailingAddress/airs:City'
        xpMailingAddressCounty = 'airs:MailingAddress/airs:County'
        xpMailingAddressState = 'airs:MailingAddress/airs:State'
        xpMailingAddressZipCode = 'airs:MailingAddress/airs:ZipCode'
        xpMailingAddressCountry = 'airs:MailingAddress/airs:Country'
        xpMailingAddressReasonWithheld = 'airs:MailingAddress/airs:ReasonWithheld'
        xpMailingAddressConfidential = 'airs:MailingAddress/@airs:Confidential'
        xpMailingAddressDescription = 'airs:MailingAddress/@airs:Description'       
        xpNoPhysicalAddressDescription = 'airs:NoPhysicalAddress/airs:Description'        
        xpNoPhysicalAddressExplanation = 'airs:NoPhysicalAddress/airs:Explanation'        
        xpDisabilitiesAccess = 'airs:DisabilitiesAccess'
        xpPhysicalLocationDescription = 'airs:PhysicalLocationDescription'
        xpBusServiceAccess = 'airs:BusServiceAccess'
        xpPublicAccessToTransportation = 'airs:PublicAccessToTransportation'
        xpYearInc = 'airs:YearInc'
        xpAnnualBudgetTotal = 'airs:AnnualBudgetTotal'
        xpLegalStatus = 'airs:LegalStatus'
        xpExcludeFromWebsite = 'airs:ExcludeFromWebsite'
        xpExcludeFromDirectory = 'airs:ExcludeFromDirectory'
        xpAgencyKey = 'airs:AgencyKey'


    def createSite(self, records):
    	site = ET.SubElement(records, "site")
    	return site


    def createService(self, services):
    	keyval = 'service'
    	sysID = self.xmlU.generateSysID(keyval)
    	#append the service start date to the client's serviceid so the service system_ids are unique for each service
    	#since we don't store services in the database
    	date_for_service_id = self.dsRec['Date']
    	date_object_format = self.fixDateNoTime(date_for_service_id)
    	sysID = sysID + str(date_object_format)
    	recID = self.xmlU.generateRecID(keyval)
    	service = ET.SubElement(services, "service")
    	service.attrib["record_id"] = recID
    	service.attrib["system_id"] = sysID
    	#We should have the shelter switch to a 4 digit year, then change the %y to %Y
    	service.attrib["date_added"] = datetime.now().isoformat()
    	service.attrib["date_updated"] = datetime.now().isoformat()
    	service.text = "\n"
    	service.tail = "\n"
	
    	return service
    
    
    def createNeed(self, needs):
    	keyval = 'need'
    	sysID = self.xmlU.generateSysID(keyval)
	
    	#append the need start date to the client's need_id so the need system_ids are unique for each need
    	#since we don't store needs in the database
    	date_for_need_id = self.dsRec['Date']
    	#We should have the shelter switch to a 4 digit year, then change the %y to %Y
    	date_object_format = self.fixDateNoTime(date_for_need_id)
    	sysID = sysID + str(date_object_format)
    	recID = self.xmlU.generateRecID(keyval)
	
    	need = ET.SubElement(needs, "need")
    	need.attrib["record_id"] = recID 
    	need.attrib["system_id"] = sysID
	
    	need.attrib["date_added"] = datetime.now().isoformat()
    	need.attrib["date_updated"] = datetime.now().isoformat()
	
	
    	return need
    
        def customizeNeed(self, need):	
    	provider_id = ET.SubElement(need, "provider_id")
    	provider_id.text = "14"
	
	
    	status = ET.SubElement(need, "status")
    	status.text = "closed"
	
	
    	code = ET.SubElement(need, "code")
    	code.attrib["type"] = "airs taxonomy"
    	code.text = "BH-180"
	
	
    	if self.debug == True:
    		notes = ET.SubElement(need, "notes")
    		notes.text = 'Client ID: %s' % self.dsRec['Client ID']
    		notes.tail = '\n'
		
    	date_set = ET.SubElement(need, "date_set")
    	# ECJ20071114: The Need date_set will be the same day as the service provided date
    	orig_format = self.dsRec['Date']
    	#We should have the shelter switch to a 4 digit year, then change the %y to %Y
    	date_set_datetime_object_format = self.fixDate(orig_format) 
    	date_set.text = date_set_datetime_object_format
	
	    



    def writeOutXML(self):
    	tree = ET.ElementTree(self.root_element)
    	if self.debug == True:
    	    print "trying to write XML to: %s " % os.path.join(self.outDirectory, "page.xml")
		
    	tree.write(os.path.join(self.outDirectory, "page.xml"))
	
if __name__ == "__main__":
    vld = HMISXML30Writer(".")
    files = vld.processXML()
    vld.prettify()
    vld.writeOutXML()
