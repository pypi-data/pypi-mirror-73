# https://www.trafiklab.se/api/sl-platsuppslag

import requests
import json

class search:
    def __init__(self, key, searchString):

        if len(searchString) < 3:
            return

        response = requests.get("http://api.sl.se/api2/typeahead.json?key=" + key + "&searchstring=" + searchString + "&stationsonly=true")
        data = response.text
        parsed = json.loads(data)

        self.all = parsed
        self.code = parsed["StatusCode"]
        self.responses = len(parsed["ResponseData"])
        self.stations = parsed["ResponseData"]
        self.name = parsed["ResponseData"][0]["Name"]
        self.id = parsed["ResponseData"][0]["SiteId"]
        self.type = parsed["ResponseData"][0]["Type"]