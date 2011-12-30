import urllib2

class REST():

    def __init__(self, url):
        self._url = url

    def post(self, ccd_data, test=False):
        request = urllib2.Request(self._url)
        request.add_header("Content-Type", "text/xml")
        if test: request.add_header("Content-Type", "application/x-www-form-urlencoded")
        request.add_header("User-Agent", "synthesis")
        request.add_data(ccd_data)
        response = urllib2.urlopen(request).read()
        # Do we care about the output? If so, the variable "response" is the likely candidate
        return response

if __name__ == "__main__":
    import urllib
    rest = REST("http://search.twitter.com/search.json")
    print rest.post(urllib.urlencode({'q': 'VIC-20'}), test=True)
