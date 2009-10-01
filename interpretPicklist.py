# The MIT License
# 
# Copyright (c) 2007 Suncoast Partnership 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 


class interpretPickList:
	
	def __init__(self):
		print "started interpretPickList"
		self.pickList = {
		"INCOMETYPESPickOption":{
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
		,"LIVINGSITTYPESPickOption":{
			"Domestic Violence":"domestic violence situation",
			"?":"don&apos;t know (hud)",
			"Emergency Shelter/TH":"emergency shelter (hud)",
			"Foster Care":"foster care/group home (hud)",
			"Hospital":"hospital (hud)",
			"Hotel/Motel":"hotel/motel without emergency shelter(hud)",
			"Jail/Prison":"jail, prison or juvenile facility  (hud)",
			"Living With Family":"living with family (hud)",
			"Living with Friend":"living with friends (hud)",
			"Living With Friend":"living with friends (hud)",
			"Other":"other (hud)",
			"Own Home":"own house/apartment (hud)",
			"Halfway House":"permanent housing for formerly homeless (hud)",
			"Street":"place not meant for habitation (hud)",
			"Psychiatric Facility":"psychiatric hospital or facility (hud)",
			"Refused":"refused (hud)",
			"Rented":"rental house/apartment (hud)",
			"Housing Subsized":"subsidized housing",
			"Treatment Center":"substance abuse treatment center (hud)",
			"Transitional Housing":"transitional housing for homeless(hud)"
		}
		,"ENHANCEDYESNOPickOption":{
			"dontknow":"don&apos;t know (hud)",
			"FALSE":"no (hud)",
			"?":"refused (hud)",
			"TRUE":"yes (hud)",
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
			,'american indian black':"american indian/alaskan native &amp; black/african american (hud 40118)"
			,'american indian white':"american indian/alaskan native &amp; white (hud 40118)"
			,'asian white':"asian &amp; white (hud 40118)"
			,'asian':"asian (hud)"
			,'black':"black or african american (hud)"
			,'black white':"black/african american &amp; white (hud 40118)"
			,'native hawaiian':"native hawaiian/other pacific islander (hud 40118)"
			,'other':"other"
			,'other multi-racial':"other multi-racial (hud 40118)"
			,'pacific islander':"native hawaiian/other pacific islander (hud 40118)"
			,'white':"white (hud)"
			,'hispanic':"other"
			,'':'other'
			}
		,"SexPick":{
			"female":"female",
			"male":"male",
			"confused":"transgender",
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
		,"EthinictyPick":{
			"latino":"hispanic/latino",
			"other":"other"
			}
		}

	def getValue(self, pList, lookupValue):
		if self.pickList.has_key(pList):
			if self.pickList[pList].has_key(lookupValue):
				return 	self.pickList[pList][lookupValue]
			else:
				return ""
			
if __name__ == "__main__":
    vld = interpretPickList()
    files = vld.getValue("entryExitTypePick", "test")
    lookupValues = vld.pickList.keys()
    for dicts in lookupValues:
    	print vld.getValue(dicts, "other")
    
    
    print "Valid Files are: ", files