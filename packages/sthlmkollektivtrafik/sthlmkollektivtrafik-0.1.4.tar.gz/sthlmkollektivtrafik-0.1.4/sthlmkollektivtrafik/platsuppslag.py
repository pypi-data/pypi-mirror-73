# https://www.trafiklab.se/api/sl-platsuppslag
# version: 2020-07-10

import requests
import json
import sys

class search:
    def __init__(self, key, searchString):
        self.log = []

        try:
            response = requests.get("http://api.sl.se/api2/typeahead.json?key=" + key + "&searchstring=" + searchString + "&stationsonly=true")
            data = response.text
            parsed = json.loads(data)
            self.log.append("Succesfully called the api.")
        except:
            self.log.append(sys.exc_info()[0])

        try:
            self.all = parsed
            self.code = int(parsed["StatusCode"])
            self.responses = len(parsed["ResponseData"])
            self.stations = parsed["ResponseData"]
            self.name = parsed["ResponseData"][0]["Name"]
            self.id = int(parsed["ResponseData"][0]["SiteId"])
            self.type = parsed["ResponseData"][0]["Type"]
        except:
            self.all = "-"
            self.code = "-"
            self.responses = 0
            self.stations = "-"
            self.name = "-"
            self.id = "-"
            self.type = "-"
            self.log.append(sys.exc_info()[0])