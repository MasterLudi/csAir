
'''
Contains specific information for an airport such as code, name, country, etc.
'''


class Airport:

    def __init__(self, code, name, country, continent, timezone, coordinates, population, region):
        '''
        constructor for the Airport class
        '''
        self.code = code
        self.name = name
        self.country = country
        self.continent = continent
        self.timezone = timezone
        self.coordinates = coordinates
        self.population = population
        self.region = region
        self.flights = {}
