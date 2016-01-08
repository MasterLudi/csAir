"""
Prints dictionary of Airport into json file
"""

import json


class Printer:
    def __init__(self, airport_dict):
        self.airport_dict = airport_dict
        self.routes = []
        self.airports = []
        self.new_dict = {}
        self.build_dictionary()

    def print_to_json(self, filename):
        fp = open(filename, "w")

        json.dump(self.new_dict, fp, indent=4)

        fp.close()

    def build_dictionary(self):
        dic = self.airport_dict

        # build dictionary for each airport
        for code in dic:
            airport = dic[code]
            cell = dict()
            cell['code'] = airport.code
            cell['name'] = airport.name
            cell['country'] = airport.country
            cell['continent'] = airport.continent
            cell['timezone'] = airport.timezone
            cell['coordinates'] = airport.coordinates
            cell['population'] = airport.population
            cell['region'] = airport.region
            self.airports.append(cell)

            for flight in airport.flights:
                cell = dict()
                cell['ports'] = [airport.code, flight]
                cell['distance'] = airport.flights[flight]
                self.routes.append(cell)

        self.new_dict['routes'] = self.routes
        self.new_dict['metros'] = self.airports