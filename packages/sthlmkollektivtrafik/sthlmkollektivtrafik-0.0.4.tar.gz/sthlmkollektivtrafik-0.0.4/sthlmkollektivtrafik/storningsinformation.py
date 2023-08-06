# https://www.trafiklab.se/api/sl-storningsinformation-2

import requests
import json


class deviations:
    def __init__(self, key, siteId):
        url = "http://api.sl.se/api2/deviations.json?key=" + key + "&siteId=" + str(siteId)

        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)

        self.headers = []
        self.details = []
        for i in parsed["ResponseData"]:
            self.headers.append(i["Header"])
            self.details.append(i["Details"])

        self.all = parsed["ResponseData"]

        
