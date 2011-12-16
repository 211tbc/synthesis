import urllib
import urllib2

class REST():

    def __init__(self, url):
        self._url = url

    def post(self, ccd_data):
        params = urllib.urlencode(ccd_data)
        response = urllib2.urlopen(self._url, params).read()
        # Do we care about the output? If so, the variable "response" is the likely candidate
        print response

if __name__ == "__main__":
    #####################################################################
    # This test uses the REST api to the GeoNames geographical database #
    #####################################################################
    
    # Create the REST object
    rest = REST("http://api.geonames.org/findNearbyPostalCodes")

    # I have *no* idea what kind of data the REST client is expected to work with so I'm
    # assuming the data will be a dictionary
    ccd_data = {'username': 'demo', 'country': 'US', 'postalcode': '33068', 'radius': '10'}

    # POST the data
    rest.post(ccd_data)
