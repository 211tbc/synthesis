import os
import smtplib
from conf import settings
from clsLogger import clsLogger

# Import the email modules we'll need
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def main():
    
    smtp = smtpInterface(settings)
    smtp.setMessageSubject("Test Message")
    smtp.setTargetSystem('beta2')
    smtp.setRecipients(settings.SMTPRECIPIENTS['testSource'])
    smtp.setMessage("This is a test message...\r\n" )
    smtp.formatMessage()
    smtp.setAttachmentText(os.path.join(smtp.settings.BASE_PATH, 'emailProcessor.py'))
    try:
        smtp.sendMessage()
    except:
        print 'send failed'
    
class smtpInterface:
    def __init__(self, settings):
        print "SMTP Server Started"
        self.settings = settings
        self.log = clsLogger()
        
    def prompt(prompt):
        return raw_input(prompt).strip()

    def setTargetSystem(self, targetsystem):
        self.targetSystem = targetsystem

    def setMessageSubject(self, messageSubject):
        self.messageSubject = messageSubject
        
    def setMessage(self, message):
        self.message = message
        
    def setRecipients(self, Recipients={}):
        self.SMTPRECIPIENTS = Recipients
        
    def setAttachmentText(self, textfile):
   
        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        #print textfile
        #print os.getcwd()
        fp = open(textfile, 'r')
        # Create a text/plain message
        #self.msg = MIMEText(fp.read())
        
        #self.msg.add_header('Content-Disposition', 'attachment', filename=textfile)
        #self.msg.attach( MIMEText(fp.read()) )
        # now attach the attachment
        
        part = MIMEText(fp.read())
        fp.close()
        #part.set_payload( open(file,"r").read() )
        #Encoders.encode_base64(part)
        #part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        # SBB20070427 splitting out the filename from the full path (shows better in the heading of outlook)
        fileNameOnly = os.path.basename(textfile)
        #part.add_header('Content-Disposition', 'attachment', filename=textfile)
        part.add_header('Content-Disposition', 'attachment', filename=fileNameOnly)
        self.msg.attach(part)        
        
    def formatMessage(self):
        self.msg = MIMEMultipart()
        
        try:
            self.fromaddr = self.settings.SMTPSENDER
            # SMTPRECIPTIENTS is where these values come from 
            self.toaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESS']
            self.ccaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESSCC']
            self.bccaddrs = self.SMTPRECIPIENTS['SMTPTOADDRESSBCC']
        except KeyError:
            self.log.logger.exception('Unable to locate an Address')
            
        self.log.logger.info("self.toaddrs")
        self.log.logger.info(self.toaddrs)
        
        # Add the From: and To: headers at the start!
        #self.msg = ("From: %s\r\nTo: %s\r\n\r\n"
        #       % (self.fromaddr, ", ".join(self.toaddrs)))
        self.msg['From'] = self.fromaddr
        self.msg['To'] = ", ".join(self.toaddrs)
        self.msg['CC'] = ", ".join(self.ccaddrs)
        self.msg['BCC'] = ", ".join(self.bccaddrs)
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['Subject'] = self.messageSubject 
        self.msg.attach(MIMEText(self.message))
        self.msg.preamble = 'ODS SuperBuild Process'
        # Guarantees the message ends in a newline
        self.msg.epilogue = ''
     
                
        #self.message = self.message + self.msg.as_string()
        #print type(self.msg)
        #self.message = self.msg.as_string()
        
    def sendMessage(self):
        print "ServerAddress: %s" % self.settings.SMTPSERVER
        server = smtplib.SMTP(self.settings.SMTPSERVER)
        if self.settings.SMTPSENDERPWD != '':
            try:
                server.login(self.settings.SMTPSENDER, self.settings.SMTPSENDERPWD)
            except smtplib.SMTPRecipientsRefused:
                self.log.logger.exception('smtplib.SMTPRecipientsRefused')
                raise
        server.set_debuglevel(0)
        server.sendmail(self.fromaddr, self.toaddrs, self.msg.as_string())
        server.quit()

if __name__ == "__main__":
    main()