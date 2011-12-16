import sys
import httplib
import urlparse

class SoapEnv():

    def __init__(self, url, action):
        self._action = action
        self._host = urlparse.urlparse(url).netloc
        self._post = urlparse.urlparse(url).path
        # define the soap envelope template
        self._ENVELOPE_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
            <soapenv:Envelope soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Body>
                    %s
                </soapenv:Body>
            </soapenv:Envelope>
        """

    def send_soap_envelope(self, ccd_data):
        # construct the message and header
        soap_env = self._ENVELOPE_TEMPLATE % (ccd_data)
        ws = httplib.HTTP(self._host)
        ws.putrequest("POST", self._post)
        ws.putheader("Host", self._host)
        ws.putheader("User-Agent", "synthesis")
        ws.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
        ws.putheader("Content-length", "%d" % len(soap_env))
        ws.putheader("SOAPAction", "http://%s/%s" % (self._host, self._action))
        ws.endheaders()

        # send the SOAP envelope
        ws.send(soap_env)

        # do we care about the output? if so, the variables "status_code", "status_message" and "response" are likely candidates
        status_code, status_message, header = ws.getreply()
        print "Response: ", status_code, status_message
        print "headers: ", header
        response = ws.getfile().read()
        print response

if __name__ == "__main__":
    # create SOAP object
    soap = SoapEnv(url="http://www.webserviceX.NET/country.asmx", action="GetCountryByCountryCode")
    ccd_data = """<GetCountryByCountryCode xmlns="http://www.webserviceX.NET"><CountryCode>US</CountryCode></GetCountryByCountryCode>"""
    soap.send_soap_envelope(ccd_data)
