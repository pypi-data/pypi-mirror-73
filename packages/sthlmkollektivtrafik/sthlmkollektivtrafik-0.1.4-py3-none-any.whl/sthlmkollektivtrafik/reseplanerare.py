# https://www.trafiklab.se/api/sl-reseplanerare-31
# Version 2020-07-10

import requests
import json

class searchJourney:
    def __init__(self, key, startId, destId):
        url = "https://api.sl.se/api2/TravelplannerV3_1/trip?key=" + key + "&originExtId=" + str(startId) + "&destExtId=" + str(destId)
        response = requests.get(url)
        data = response.text
        parsed = json.loads(data)

        self.journey = []
        for tripNum in range(len(parsed["Trip"])):
            trip = []
            for i in range(0, len(parsed["Trip"][tripNum]["LegList"]["Leg"]), 3):

                leg = []
                leg.append(parsed["Trip"][tripNum]["LegList"]["Leg"][i]["Origin"]["time"])
                leg.append(parsed["Trip"][tripNum]["LegList"]["Leg"][i]["Origin"]["name"])
                try: leg.append(parsed["Trip"][tripNum]["LegList"]["Leg"][i]["Product"]["name"]) 
                except: print("e")
                leg.append(parsed["Trip"][tripNum]["LegList"]["Leg"][i]["Destination"]["time"])
                leg.append(parsed["Trip"][tripNum]["LegList"]["Leg"][i]["Destination"]["name"])
                trip.append(leg)

            self.journey.append(trip)