# https://www.trafiklab.se/api/sl-realtidsinformation-4
# Version 2020-07-10

import requests
import json
import sys

class departure:
    def __init__(self, key, siteId, timewindow):
        self.log = []

        try:
            url = "http://api.sl.se/api2/realtimedeparturesv4.json?key=" + key + "&siteid=" + str(siteId) + "&timewindow=" + str(timewindow)
            response = requests.get(url)
            data = response.text
            parsed = json.loads(data)
            self.log.append("Succesfully called the api.")
        except:
            self.log.append(sys.exc_info()[0])

        self.trainDest = []
        self.trainTime = []
        self.trainNum = []
        for i in parsed["ResponseData"]["Trains"]:
            self.trainDest.append(i["Destination"])
            self.trainTime.append(i["DisplayTime"])
            self.trainNum.append(i["LineNumber"])

        self.busDest = []
        self.busTime = []
        self.busNum = []
        for i in parsed["ResponseData"]["Buses"]:
            self.busDest.append(i["Destination"])
            self.busTime.append(i["DisplayTime"])
            self.busNum.append(i["LineNumber"])

        self.metroDest = []
        self.metroTime = []
        self.metroNum = []
        for i in parsed["ResponseData"]["Metros"]:
            self.metroDest.append(i["Destination"])
            self.metroTime.append(i["DisplayTime"])
            self.metroNum.append(i["LineNumber"])

        self.all = parsed
        self.trains = parsed["ResponseData"]["Trains"]
        self.buses = parsed["ResponseData"]["Buses"]
        self.metros = parsed["ResponseData"]["Metros"]
