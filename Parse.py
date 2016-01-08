'''
Parses json file data to dictionary of Airport objects
'''

import json
import Airport


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.airport_dict = {}
        self.translator = {}

    def parse(self):
        json_data = open(self.filename)

        data = json.load(json_data)

        # parse airport data
        for metro in data['metros']:
            code = metro['code']
            name = metro['name']
            country = metro['country']
            continent = metro['continent']
            timezone = metro['timezone']
            coordinates = metro['coordinates']
            population = metro['population']
            region = metro['region']

            # add new airport to dictionary
            airport = Airport.Airport(code, name, country, continent, timezone, coordinates, population, region)
            self.airport_dict[code] = airport

            # add to translator
            self.translator[code] = name

        # parse route data
        for route in data['routes']:
            port1 = route['ports'][0]
            port2 = route['ports'][1]
            distance = route['distance']

            # add routes to dictionary
            self.airport_dict[port1].flights[port2] = distance
            if port2 in self.airport_dict:
                self.airport_dict[port2].flights[port1] = distance

        json_data.close()
