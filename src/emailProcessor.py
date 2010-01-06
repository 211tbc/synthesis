
from smtpLibrary import smtpInterface
from conf import settings
import os

class XMLProcessorNotifier(smtpInterface):
    def __init__(self, docName):
        self.mailSystem = smtpInterface(settings)
        folderName = os.path.split(docName)[0]
        self.mailSystem.setRecipients(settings.SMTPRECIPIENTS[folderName])
        self.docName = docName
        
    def notifyValidationFailure(self, failureMsgs=''):
        self.mailSystem.setMessageSubject('XMLDocument FAILED Validation')
        self.mailSystem.setMessage('This email is a notification that we recieved XML document: %s.  \r\n' \
                                   'This Document FAILED to Validate proprerly.\r\n ' \
                                   'Error is: %s' % (self.docName, failureMsgs))
        self.sendMessage()
        
    def notifyDuplicateDocumentError(self, failureMsgs=''):
        self.mailSystem.setMessageSubject('XMLDocument Process Import FAILED')
        self.mailSystem.setMessage('This email is a notification that we recieved XML document: %s.  \r\n' \
                                   'This Document FAILED to import because it would create duplicate records in the database.\r\n ' \
                                   'Error is: %s' % (self.docName, failureMsgs))
        self.sendMessage()
    
    def notifyValidationSuccess(self):
        self.mailSystem.setMessageSubject('Success: XMLDocument PASSED Validation')
        self.mailSystem.setMessage('This email is a notification that we recieved XML document: %s.  This Document PASSED Validation proprerly.' % self.docName)
        self.sendMessage()
    
    def sendMessage(self):
        self.mailSystem.formatMessage()
        #mailSystem.setAttachmentText(os.path.join(smtp.settings.BASE_PATH, 'emailProcessor.py'))
        self.mailSystem.sendMessage()
