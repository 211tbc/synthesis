from conf import settings
from dbobjects import DB, LastDateTime
from smtplibrary import smtpInterface
import datetime

# FBY :07/31/2017: The script needs to run as a cron job once a day

#import pdb; pdb.set_trace()
db = DB()
session = db.Session()

SMTPRECIPIENTS = {    
    # input processing
    "synthesis":
    {
        'SMTPTOADDRESS': ['eric@alexandriaconsulting.com',],
        'SMTPTOADDRESSCC': [],
        'SMTPTOADDRESSBCC': [],
    }
}

try:
    # Assume that record exists so 
    lifecycle_event = session.query(LastDateTime).filter(LastDateTime.event == 'file received').first()
    event_date_time = lifecycle_event.event_date_time
    time_elapsed = (datetime.datetime.now() - event_date_time)
    if time_elapsed.days >= 3:
        settings.SMTPAUTH = True
        #settings.SMTPTLS = True
        smtp = smtpInterface(settings)
        smtp.setMessageSubject("Warning: No referrals received")
        smtp.setRecipients(SMTPRECIPIENTS['synthesis'])
        text = "You are receiving this message because synthesis has not received an incoming referral in %d days.\r\n" % time_elapsed.days
        smtp.setMessage("%s\r\n" % text)
        smtp.sendMessage()
        settings.SMTPAUTH = False
except:
    pass