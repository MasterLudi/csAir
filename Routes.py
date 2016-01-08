import Graph
import Airport


class Routes:

    def __init__(self, airport_dic):
        self.airport_dict = airport_dic
        self.graph = Graph.Graph()
        self.build_graph()

    def build_graph(self):
        """
        build graph using airport dictionary, with code names being vertices
        :return: void
        """

        # for each airport, add an edge to an airport it has a flight to
        for departure in self.airport_dict:
            for arrival in self.airport_dict[departure].flights:
                dist = self.airport_dict[departure].flights[arrival]
                self.graph.add_edge(departure, arrival, dist)

    def longest_single_flight(self):
        return self.graph.longest_edges

    def shortest_single_flight(self):
        return self.graph.shortest_edges

    def average_distance(self):
        return self.graph.average_weight()

    def biggest_population(self):
        """
        find the cit with the biggest population
        :return: str code
        """

        population = 0

        largest_metro = []

        for item in self.airport_dict.items():
            airport = item[1]
            if population < airport.population:
                population = airport.population
                largest_metro = [airport.code]
            elif population == airport.population:
                largest_metro.append(airport.code)

        return largest_metro

    def smallest_population(self):
        """
        find the city with the smallest population
        :return: str code
        """

        population = float("inf")
        smallest_metro = []

        for item in self.airport_dict.items():
            airport = item[1]
            if airport.population < population:
                population = airport.population
                smallest_metro = [airport.code]
            elif population == airport.population:
                smallest_metro.append(airport.code)

        return smallest_metro

    def average_population(self):
        """
        calculate average population among all cities
        :return: float average
        """

        total_population = 0
        num_cities = 0
        for item in self.airport_dict.items():
            airport = item[1]
            total_population = total_population + airport.population
            num_cities += 1

        average = float(total_population)/float(num_cities)

        return average

    def list_of_continents(self):
        """
        Create dictionary with key: continent, val: list of city names
        :return: {continent: [cities]}
        """

        continents = {}
        for item in self.airport_dict.items():
            airport = item[1]
            if airport.continent not in continents:
                continents[airport.continent] = []
            continents[airport.continent].append(airport.name)

        return continents

    def list_of_hub_cities(self):
        """
        return a list of cities with the most outgoing flights
        :return: [code]
        """
        return self.graph.largest_degree()

    def add_city(self, info):
        """
        Add city to the route with given info. Note that [coordiantes] is in [N:50,E:50] format
        :param info: list of strings with code, name, country, continent, timezone, coordinates, population, region
        :return: void
        """
        if info[0] in self.airport_dict:
            print(info[0], "already in the system")
            return -1

        tmp = info[5].split(",")
        latitude = tmp[0].split(":")
        longitude = tmp[1].split(":")

        coordinate = dict()
        coordinate[latitude[0]] = latitude[1]
        coordinate[longitude[0]] = longitude[1]

        airport = Airport.Airport(info[0], info[1], info[2], info[3], info[4], coordinate, info[6], info[7])
        self.airport_dict[info[0]] = airport

        # add to graph
        self.graph.add_vertex(info[0])

        return 0

    def remove_city(self, code):
        """
        Remove a city and all the routes associated with the city in the graph
        :param code:
        :return:
        """
        # delete all the associated route
        for flight in self.airport_dict[code].flights:
            del self.airport_dict[flight].flights[code]

        # delete airport
        del self.airport_dict[code]

        self.graph.remove_vertex(code)

    def add_route(self, code1, code2, weight):
        self.airport_dict[code1].flights[code2] = weight
        self.graph.add_edge(code1, code2, int(weight))

    def remove_route(self, code1, code2):
        del self.airport_dict[code1].flights[code2]
        self.graph.remove_edge(code1, code2)

    def distance(self, route):
        return self.graph.path_weight(route)

    def cost(self, route):
        """
        Calculates the total cost of the route. First leg costs $.35/km, and $-.50/km is applied to additional leg.
        Once it hits $0/km, it's free after that
        :param route: list of city codes [c1, c2, c3,...]
        :return: float value of calculated cost
        """
        graph = self.graph

        unit_cost = .35
        total_cost = 0

        for i in range(0, len(route)-1):
            leg_cost = unit_cost * graph.edge_weight(route[i], route[i+1])

            if leg_cost < 0:
                print("No flight from", route[i], "to", route[i+1])
                return -1

            total_cost += leg_cost

            if unit_cost > 0:
                unit_cost -= .05

        return total_cost

    def time(self, route):
        """
        Calculates total flight time. All planes fly at 750 kph, takes 200km to accelerates/de-accelerates from/to 0 kph.
        If flight distance less than 400km, doesn't reach 750 kph and uniformly accelerates throughout the flight
        :param route: list of city codes representing path
        :return: total flight time + layover in minutes
        """

        graph = self.graph
        layover_time = 120
        total_time = 0
        velocity = 750/60

        for i in range(0, len(route)-1):
            dist = graph.edge_weight(route[i], route[i+1])

            if dist < 0:
                print("No flight from", route[i], "to", route[i+1])
                return -1

            if dist <= 400:
                total_time += dist / velocity * 2
            else:
                total_time += (dist + 400) / velocity

            if 0 < i < len(route) - 1:
                total_time += layover_time
                layover_time -= 10

        return total_time







