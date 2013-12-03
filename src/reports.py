"""
Created on Aug 21, 2013

@author: eric jahn
Stand-alone functions to handle the generation of any kind of report.  
These can be run ad-hoc and the intent is for them to be run by a cron job (e.g. monthly) and 
    emailed to a configured (conf/settings.py report recipient).
"""
from datetime import datetime, timedelta, date
from dateutil import parser
from conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from synthesis.postgresutils import Utils
from sqlalchemy.sql import select, asc
from sqlalchemy.engine import ResultProxy
from dbobjects import Referral, Person, ServiceEvent
from lxml import etree

global age
global personID

def monthlyReferralReport():
    """A script that generates a referral report from the database, and emails it to an program manager."""

    # Query Description (in plain English)
        # Query should include:
            #  number of referrals total within the month
            #  select all referrals where month = last full previous month
            #  call ID
            #  Client ID
            #  referral provider ID
    db = Utils()
    conn = db.synthesis_engine
    now = datetime.now()
    text_message = ""

    end_of_first_day_this_month = datetime(year=now.year, month=now.month, day=1, hour = 23, minute=59, second=59, microsecond=999999)
    #print "end_of_first_day_this_month: " + str(end_of_first_day_this_month)
    end_of_last_day_last_month = end_of_first_day_this_month - timedelta(days=1)
    #print "end_of_last_day_last_month: " + str(end_of_last_day_last_month)
    beginning_of_first_day_last_month = datetime(year=now.year, month=(now.month-1), day=1)#, hour = 0, minute=0, second=0)

    report_range_desc = "Report period from: " + '{:%m-%d-%Y}'.format(beginning_of_first_day_last_month) + " through: " + '{:%m-%d-%Y}'.format(end_of_last_day_last_month)  + "\n"
    text_message += report_range_desc

    subject = "2-1-1 Tampa Bay Cares Referral Report For The " \
        "Month Of " + beginning_of_first_day_last_month.strftime("%B %Y")
    print subject

    #print '{:%Y-%m-%d %H:%M:%S}'.format(beginning_of_first_day_last_month)
    #print '{:%m, %Y}'.format(beginning_of_first_day_last_month)

    #text_message += "referrals list:\n"
    row_id = 1
    htmlroot = etree.Element('html')
    desc = etree.SubElement(htmlroot, 'div')
    desc.text = report_range_desc
    count_text = etree.SubElement(htmlroot, 'div')

    border="1"
    table = etree.SubElement(htmlroot, 'table')
    table.set("border", "1")
    rw1 = etree.SubElement(table, 'tr')
    col1 = etree.SubElement(rw1, 'td')
    col1.text = '#'
    col2 = etree.SubElement(rw1, 'td')
    col2.text = "referral date"
    col3 = etree.SubElement(rw1, 'td')
    col3.text = "referred to"
    col4 = etree.SubElement(rw1, 'td')
    col4.text = "referred to program id"
    col5 = etree.SubElement(rw1, 'td')
    col5.text = "call id"
    col6 = etree.SubElement(rw1, 'td')
    col6.text = "client id"
    col7 = etree.SubElement(rw1, 'td')
    col7.text = "client age"

    s = select([ServiceEvent.id]).where(ServiceEvent.service_event_provision_date\
        >= beginning_of_first_day_last_month).where(ServiceEvent.\
        service_event_provision_date <= end_of_last_day_last_month).\
        order_by(asc(ServiceEvent.service_event_provision_date))
    result = conn.execute(s)
    count  ="number of referrals: " + str(result.rowcount)
    text_message += count + "\n"
    count_text.text = count

    for row in result:
        # "another row is ServiceEvent.id: " + str(row[0])
        serviceeventprovisiondateResults = conn.execute(select([ServiceEvent.\
            service_event_provision_date]).where(ServiceEvent.id == row[0]))
        for provision_date in serviceeventprovisiondateResults:
            service_event_provision_date = provision_date
            #print "service_event_provision_date: " + str(service_event_provision_date)
            service_event_id = row[0]
            s1 = select([Referral]).where(Referral.service_event_index_id == service_event_id)
            referrals = conn.execute(s1) #resultHUD_HMIS_TBC.xml 1 is a collection of the referrals
            for referral in referrals:
                #print "another referral:" + str(referral)
                #print "looking for Person.id: " + str(referral.person_index_id)
                s2 = select([Person]).where(Person.id == referral.person_index_id)
                persons = conn.execute(s2)
                age = ""
                personID = ""
                #print "another person"
                for person in persons:
                    personID = person.person_id_id_num
                    #print "person id is: " + personID
                    persondob = person.person_date_of_birth_unhashed
                    age = str(calculate_age(persondob))
                    #print "age is: " + age
                rwx = etree.SubElement(table, 'tr')
                colx1 = etree.SubElement(rwx, 'td')
                colx1.text = str(row_id)
                colx2 = etree.SubElement(rwx, 'td')
                referral_date = '{:%m-%d-%Y %H:%M}'.format(service_event_provision_date[0])
                colx2.text = referral_date
                colx3 = etree.SubElement(rwx, 'td')
                referred_to = str(referral.referral_agency_referred_to_name)
                colx3.text = referred_to
                colx4 = etree.SubElement(rwx, 'td')
                referred_to_provider_id = str(referral.referral_agency_referred_to_idid_num)
                colx4.text = referred_to_provider_id
                colx5 = etree.SubElement(rwx, 'td')
                call_id = str(referral.referral_call_idid_num)
                colx5.text = call_id
                colx6 = etree.SubElement(rwx, 'td')
                client_id = personID
                colx6.text = client_id
                colx7 = etree.SubElement(rwx, 'td')
                colx7.text = age

                m2 = str(row_id) + ") referral date: " + referral_date +\
                    " referred to: " + referred_to +\
                    " referred to provider id: " + referred_to_provider_id +\
                    " call id: "+ call_id + " client id: " + client_id + " client age: " + \
                     age + "\n"
                text_message += m2
                row_id += 1

    html_message = etree.tostring(htmlroot, pretty_print=True)
    print html_message
    # Mail out the results in a formatted (html) email report
    print text_message
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.SMTPSENDER
    msg['To'] = settings.TBC_REFERRAL_EMAIL_RECIPIENT
    msg['Cc'] = settings.TBC_REFERRAL_EMAIL_CC_RECIPIENT
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text_message, 'plain')
    part2 = MIMEText(html_message, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    try:
        print "trying to send message"
        print "sending to server: " + settings.SMTPSERVER + " port: " + settings.SMTPPORT
        smtpserver = smtplib.SMTP(settings.SMTPSERVER, settings.SMTPPORT)
        smtpserver.set_debuglevel(0)
        if settings.SMTPAUTH:
            smtpserver.ehlo()
            if settings.SMTPTLS:
                smtpserver.starttls()
            smtpserver.ehlo
            smtpserver.login(settings.SMTPUSERNAME, settings.SMTPSENDERPWD)
        smtpserver.sendmail(settings.SMTPSENDER, [settings.TBC_REFERRAL_EMAIL_RECIPIENT,settings.TBC_REFERRAL_EMAIL_CC_RECIPIENT], msg.as_string())
        smtpserver.close
    except Exception as e:
        print type(e)
        print 'send failed:' + e.message

def calculate_age(born):  # from: http://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
    today = date.today()
    if born != None:
        try:
            birthday = born.replace(year=today.year)
        except ValueError: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

if __name__ == "__main__":
    import sys
    monthlyReferralReport()
    sys.exit()
        
#The MIT License
#
#Copyright (c) 2011, Alexandria Consulting LLC
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
