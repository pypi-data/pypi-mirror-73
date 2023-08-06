# https://www.trafiklab.se/api/sl-realtidsinformation-4

import requests
import json

class departure:
    def __init__(self, key, siteId, timewindow):

        url = "http://api.sl.se/api2/realtimedeparturesv4.json?key=" + key + "&siteid=" + str(siteId) + "&timewindow=" + str(timewindow)

        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)

        text = []
        self.all = parsed
        self.trains = parsed["ResponseData"]["Trains"]
        self.buses = parsed["ResponseData"]["Buses"]
        self.metros = parsed["ResponseData"]["Metros"]
