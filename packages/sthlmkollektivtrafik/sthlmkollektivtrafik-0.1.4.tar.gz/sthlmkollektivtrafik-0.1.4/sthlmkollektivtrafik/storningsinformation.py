# https://www.trafiklab.se/api/sl-storningsinformation-2
# Version 2020-07-10

import requests
import json
import sys

class deviations:
    def __init__(self, key, siteId):
        self.msg = []

        try:
            url = "http://api.sl.se/api2/deviations.json?key=" + key + "&siteId=" + str(siteId)
            response = requests.get(url)
            data = response.text
            parsed = json.loads(data)
            self.log.append("Succesfully called the api.")
        except:
            self.log.append(sys.exc_info()[0])

        self.headers = []
        self.details = []
        for i in parsed["ResponseData"]:
            self.headers.append(i["Header"])
            self.details.append(i["Details"])

        self.all = parsed["ResponseData"]