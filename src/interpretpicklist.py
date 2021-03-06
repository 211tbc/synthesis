"""
The MIT License

Copyright (c) 2011, Alexandria Consulting LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

class Interpretpicklist:
	
	def __init__(self):
		print("started Interpretpicklist")
		self.pickList = {
		    # SBB20091021 HMIS only defines 1-4, I enumerated the remaining types
		    "RELATIONSHIPSPickOption":
			{
			"5":"daughter",
			"6":"father",
			"7":"granddaughter",
			"8":"grandfather",
			"9":"grandmother",
			"10":"grandson",
			"11":"husband",
			"12":"mother",
			"13":"other non-relative",
			"3":"other relative",
			"14":"self",
			"4":"significant other",
			"1":"son",
			"15":"step-daughter",
			"16":"step-son",
			"17":"unknown",
			"2":"wife"
			}
 		    ,"LENGTHOFTHESTAYPickOption":
			{
	                "1":"don't know (hud)",
        	        "2":"more than one week, but less than one month (hud)",
        	        "3":"more than three months, but less than one year (hud)",
        	        "4":"one to three months (hud)",
        	        "5":"one week or less (hud)",
        	        "6":"one year or longer (hud)",
        	        "7":"other",
        	        "8":"refused (hud)"
			}

			# New picklist, straight out of the schema - Are numbers correct?
                    ,"LIVINGSITTYPESPickOption":
                        {
                        "1":"don't know (hud)",
                        "2":"emergency shelter, including hotel or motel paid for with emergency shelter voucher(hud)",
                        "3":"foster care home or foster care group home (hud)",
                        "4":"hospital (non-psychiatric) (hud)",
                        "5":"hotel or motel paid for without emergency shelter voucher (hud)",
                        "6":"jail, prison or juvenile detention facility (hud)",
                        "7":"other (hud)",
                        "8":"owned by client, no housing subsidy (hud)",
                        "9":"owned by client, with housing subsidy (hud)",
                        "10":"permanent housing for formerly homeless persons(such as shp, s+c, or sro mod rehab)(hud)",
                        "11":"place not meant for habitation inclusive of 'non-housing service site(outreach programs only)'(hud)",
                        "12":"psychiatric hospital or other psychiatric facility (hud)",
                        "13":"refused (hud)",
                        "14":"rental by client, no housing subsidy (hud)",
                        "15":"rental by client, with other (non-vash) housing subsidy (hud)",
                        "16":"rental by client, with vash housing subsidy (hud)",
                        "17":"safe haven (hud)",
                        "18":"staying or living in a family member's room, apartment or house (hud)",
                        "19":"staying or living in a friend's room, apartment or house (hud)",
                        "20":"subsidized housing",
                        "21":"substance abuse treatment facility or detox center (hud)",
                        "22":"transitional housing for homeless persons (including homeless youth) (hud)"
                        }
		# This is the old picklist - xml doesn't validate if use this
#		,"LIVINGSITTYPESPickOption":{
#			"Domestic Violence":"domestic violence situation",
#			"?":"don't know (hud)",
#			"Emergency Shelter/TH":"emergency shelter (hud)",
#			"Foster Care":"foster care/group home (hud)",
#			"Hospital":"hospital (hud)",
#			"Hotel/Motel":"hotel/motel without emergency shelter(hud)",
#			"Jail/Prison":"jail, prison or juvenile facility  (hud)",
#			"Living With Family":"living with family (hud)",
#			"Living with Friend":"living with friends (hud)",
#			"Living With Friend":"living with friends (hud)",
#			"Own Home":"own house/apartment (hud)",
#			"Halfway House":"permanent housing for formerly homeless (hud)",
#			"Street":"place not meant for habitation (hud)",
#			"Psychiatric Facility":"psychiatric hospital or facility (hud)",
#			"Refused":"refused (hud)",
#			"Rented":"rental house/apartment (hud)",
#			"Housing Subsized":"subsidized housing",
#			"Treatment Center":"substance abuse treatment center (hud)",
#			"Transitional Housing":"transitional housing for homeless(hud)",
#			"1":"emergency shelter (hud)",
#			"2":"transitional housing for homeless(hud)",
#			"3":"permanent housing for formerly homeless (hud)",
#			"4":"psychiatric hospital or facility (hud)",
#			"5":"substance abuse treatment center (hud)",
#			"6":"hospital (hud)",
#			"7":"jail, prison or juvenile facility  (hud)",
#			"8":"don't know (hud)",
#			"9":"refused (hud)",
#			"10":"rental house/apartment (hud)",
#			"11":"own house/apartment (hud)",
#			"12":"living with family (hud)",
#			"13":"living with friends (hud)",
#			"14":"hotel/motel without emergency shelter(hud)",
#			"15":"foster care/group home (hud)",
#			"16":"place not meant for habitation (hud)",
#			"17":"other (hud)"
#                        }


		    ,"HOUSINGSTATUSPickOption":
			{
			"1":"don't know (hud)",
			"2":"imminently losing their housing (hud)",
			"3":"literally homeless (hud)",
			"4":"refused (hud)",
			"5":"stably housed (hud)",
			"6":"unstably housed and at-risk of losing their housing (hud)",
			"7":None,
			"8":None
			}
		    ,"ROIDocumentationPickOption":
			{
			"4":"none",
			"3":"other",
			"1":"signed statement from client",
			"2":"verbal consent",
			"5":"verification from other institiution"
			}
		    ,"MILITARYBRANCHPickOption":
			{
			    '2':"air force (hud)",
			    '1':"army (hud)",
			    '4':"marines (hud)",
			    '3':"navy (hud)",
			    '5':"other (hud)"						# Coast Guard, National Reserve...
			}
		,"INCOMETYPESPickOption":{
			"":"a veteran&apos;s disability payment (hud)",
			"":"alimony",
			"":"alimony or other spousal support (hud)",
			"":"annuities",
			"":"child support (hud)",
			"Stipend":"contributions from other people",
			"":"dividends (investments)",
			"Employment Income":"earned income (hud)",
			"":"employment/job",
			"Food Stamps":"food stamps (hud)",
			"":"general assistance (hud)",
			"":"interest (bank)",
			"":"medicaid (hud)",
			"":"medicare (hud)",
			"No Financial Resources":"no financial resources (hud)",
			"":"other (hud)",
			"":"other tanf-funded services (hud)",
			"":"pension from a former job (hud)",
			"":"pension/retirement",
			"":"private disability insurance (hud)",
			"":"railroad retirement",
			"":"rental income",
			"":"retirement disability",
			"Social Security":"retirement income from social security (hud)",
			"":"schip (hud)",
			"":"section 8, public housing or rental assistance (hud)",
			"Self-Employed":"self employment wages",
			"":"special supplemental nutrition program for wic (hud)",
			"Social Security Disability Income (SSD)":"ssdi (hud)",
			"Supplemental Security Income (SSI)":"ssi (hud)",
			"":"state disability",
			"":"tanf (hud)",
			"":"tanf child care services (hud)",
			"":"tanf transportation services (hud)",
			"Unemployment Benefits":"unemployment insurance (hud)",
			"Veteran's Health Care":"veteran&apos;s administration (va) medical services (hud)",
			"Veteran's Benefits":"veteran&apos;s pension (hud)",
			"":"worker&apos;s compensation (hud)"
	         	}
#		2.8 Picklists <xsd:simpleType name="residenceBase">
#        <xsd:annotation>
#            <xsd:documentation xml:lang="en">    
#                Residence Type
#                1 = Emergency shelter
#                2 = Transitional housing
#                3 = Permanent housing
#                4 = Psychiatric hospital or other psychiatric facility
#                5 = Substance abuse treatment facility or detox center
#                6 = Hospital (non-psychiatric)
#                7 = Jail, prison or juvenile detention facility
#                8 = Don't know
#                9 = Refused
#                10 = Room apartment or house that you rent
#                11 = Apartment or house that you own
#                12 = Staying or living in a family member's room, apartment or house
#                13 = Staying or living in a friend's room, apartment or house
#                14 = Hotel or motel paid for without emergency shelter voucher
#                15 = Foster care home or foster care group home
#                16 = Place not meant for habitation
#                17 = Other
#            </xsd:documentation>
#            
		,"ENHANCEDYESNOPickOption":{
			"dontknow":"don&apos;t know (hud)",
			"8":"don&apos;t know (hud)",
			"FALSE":"no (hud)",
			"?":"refused (hud)",
			"9":"refused (hud)",
			"TRUE":"yes (hud)",
			"1":"yes (hud)",
			"0":"no (hud)",
			"":"no (hud)",
			"other":"ENHANCEDYESNOPickOption"
		}
		,"HOMELESSREASONPickOption":{
			"Addiction":"addiction",
			"Divorce":"divorce",
			"Domestic Violence":"domestic violence",
			"Evicted within past week":"evicted within past week",
			"Family-Personal Illness":"family/personal illness",
			"Jail/Prison":"jail/prison",
			"Moved to seek work":"moved to seek work",
			"Other":"other",
			"Physical-Mental Disability":"physical/mental disabilities",
			"Unable to pay rent-mortgage":"unable to pay rent/mortgage",
			"other":"HOMELESSREASONPickOption"
		}
		,"EntryExitTypePick":{
			"test":"hud-40118",
			"":"basic entry/exit",
			"":"standard entry",
			"other":"quick call"}
		,"FundSourcesPick":{
			"":"cap",
			"":"fema",
			"":"hud shelter+care",
			"":"hud supportive housing program",
			"":"internal budget",
			"other":"title iii"}
		,"ReasonUnmetNeedPick":{
			"":"all services full",
			"":"client not eligible",
			"":"client refused service",
			"":"service does not exist",
			"other":"service not accessible"}
		,"ServiceOutcomePick":{
			"":"fully met",
			"":"not met",
			"":"partially met",
			"other":"service pending"}
		,"EeDestinationPick":{
			"LOC-ES":"emergency shelter",
			"TX-IADF":"institution: inpatient alcohol/drug facility",
			"J-IJP":"institution: jail/prison",
			"LOC-IPH":"institution: psychiatric hospital",
			"OTH-OTH":"other",
			"TH-OSPH":"other: other supportive housing",
			"UNK-OS":"other: places not meant for habitation (street)",
			"ISH-PHS":"permanent: home subsidized house/apartment",
			"INH-PHO":"permanent: homeownership",
			"INH-PFF":"permanent: moved in with family/friends",
			"ISH-POSH":"permanent: other subsidized house/apartment",
			"ISH-PPH":"permanent: public housing",
			"INH-PR":"permanent: rental house/apartment (no subsidy)",
			"ISH-PS8":"permanent: section 8",
			"ISH-PSPC":"permanent: shelter plus care",
			"TH-TFF":"transitional: moved in with family/friends",
			"TH-TFH":"transitional: transitional housing for homeless",
			"UNK-UNK":"unknown",
			"LOC-HM":"Hospital - Medical",
			"LOC-NH":"Nursing Home",
			"other":"Test Value"
			}
		,"EereasonLeavingPick":{
			"":"completed program",
			"":"criminal activity / violence",
			"":"death",
			"":"disagreement with rules/persons",
			"":"left for housing opp. before completing program",
			"":"needs could not be met",
			"":"non-compliance with program",
			"":"non-payment of rent",
			"":"other",
			"":"reached maximum time allowed",
			"other":"unknown/disappeared"
			}
		,"RacePick":{
			'alaskan':"american indian or alaska native (hud)"
			,'1':"american indian or alaska native (hud)"
			,'american indian black':"american indian/alaskan native &amp; black/african american (hud 40118)"
			,'american indian white':"american indian/alaskan native &amp; white (hud 40118)"
			,'asian white':"asian &amp; white (hud 40118)"
			,'asian':"asian (hud)"
			,'2':"asian (hud)"
			,'black':"black or african american (hud)"
			,'3':"black or african american (hud)"
			,'black white':"black/african american &amp; white (hud 40118)"
			,'native hawaiian':"native hawaiian/other pacific islander (hud 40118)"
			,'4':"native hawaiian/other pacific islander (hud 40118)"
			,'other':"other"
			,'other multi-racial':"other multi-racial (hud 40118)"
			,'pacific islander':"native hawaiian/other pacific islander (hud 40118)"
			,'white':"white (hud)"
			,'5':"white (hud)"
			,'hispanic':"other"
			,'':'other'
			}
		,"SexPick":{
			"female":"female",
			"0":"female",
			"male":"male",
			"1":"male",
			"confused":"transgender",  #ECJ20100808 omg!!!
			"other":"unknown"
			}
		,"EmploymentPick":{
			"Full Time":"full time"
			,'Part Time':"part time"
			,'Retired':"retired"
			,'Temporary':"seasonal work"
			,'Volunteer':"volunteer work only"
			,'Disability Check':'retired'
			,'School':'seasonal work'
			,'Unemployed':'seasonal work'
			}
		,"EthnicityPick":{
			"0":"non-hispanic/non-latino (hud)",
			"1":"hispanic/latino (hud)",
			"8":"don't know (hud)",
			"9":"refused (hud)"
			}
		}

	def getValue(self, pList, lookupValue):
		if self.pickList.has_key(pList):
			if self.pickList[pList].has_key(lookupValue):
				return 	self.pickList[pList][lookupValue]
			else:
				return ""
			
if __name__ == "__main__":
	vld = Interpretpicklist()
	files = vld.getValue("entryExitTypePick", "test")
	lookupValues = vld.pickList.keys()
	for dicts in lookupValues:
		print(vld.getValue(dicts, "other"))
	print("Valid Files are: ", files)
