import Parse
import Routes
import webbrowser
import Printer
import Merge


def main():
    """
    Main loop for the user interface
    :return: void
    """
    global parser1
    global airport_dict
    global routes
    global translator

    # parse the json data to get airport_dict
    parser1 = Parse.Parser("map_data.json")
    parser1.parse()
    parser2 = Parse.Parser("cmi_hub.json")
    parser2.parse()
    translator = merge(parser1.translator, parser2.translator)
    merger = Merge.Merger(parser1.airport_dict, parser2.airport_dict)
    routes = Routes.Routes(merger.merge())
    airport_dict = routes.airport_dict

    while True:
        opt = print_menu()

        if opt == "1":
            print_city_list()

        elif opt == "2":
            print_city()

        elif opt == "3":
            print_stats()

        elif opt == "4":
            draw_map()

        elif opt == "5":
            print_edit()

        elif opt == "6":
            print_route()

        elif opt == "7":
            print_shortest_path()

        elif opt == "p":
            save_file()

        elif opt == "q":
            break

        else:
            print("wrong input!")


def print_menu():
    print("------------------------------------------------------")
    print("Please select one of the following or press 'q' to quit")
    print("1 : List of all the cities in CSAir network")
    print("2 : Information on a specific city")
    print("3 : Statistics of CSAir's network")
    print("4 : Open CSAir route map in web browser")
    print("5 : Edit existing route/city info")
    print("6 : Information on a specific route")
    print("7 : Shortest path between two cities")
    print("p : Print to a file")
    print("------------------------------------------------------")
    return input()


def print_edit_menu():
    print("Please select the following or press 'b to go back")
    print("1 : Remove a city")
    print("2 : Remove a route")
    print("3 : Add a city")
    print("4 : Add a route")
    print("5 : Edit an existing city")
    return input()


def print_city_menu():
    print("Please select an input option to query on city info or press 'b' to go back")
    print("1 : Code")
    print("2 : Name")
    print("3 : View list of the city")
    return input()


def print_stats_menu():
    print("Please select one of the following or press 'b' to go back")
    print("1 : Longest single flight")
    print("2 : Shortest single flight")
    print("3 : Average distance of all flights")
    print("4 : Biggest city served by CSAir")
    print("5 : Smallest city served by CSAir")
    print("6 : Average population of all cities served by CSAir")
    print("7 : List of continents & cities served by CSAir")
    print("8 : Hub cities in CSAir network")
    return input()


def print_route():
    print("Enter the city codes/ cities in a route separated by space")
    print("   ex) NYC YYZ CHI")
    raw = input()
    codes = raw.split(" ")

    for i in range(0, len(codes)):
        codes[i] = codes[i].upper()

    dist = routes.distance(codes)
    if dist < 0:
        return
    cost = routes.cost(codes)
    if cost < 0:
        return
    time = routes.time(codes)
    if time < 0:
        return

    time_hour = int(time / 60)
    time_min = time - time_hour * 60

    print("Distance = ", dist)
    print("Cost = $%.2f" % cost)
    print("Time taken = ", time_hour, "hr", int(time_min), "min")


def print_line():
    print("------------------------------------------------------")


def print_edit():
    """
    Print user options for editing the info of city/route and make changes to the existing map.
    :return: void
    """
    opt = print_edit_menu()
    print_line()

    # remove a city
    if opt == "1":
        print("Input city code or the name of the city to remove")
        raw = input()
        code = get_code(raw)

        if code == "":
            print(raw, "is not a valid city")
            return

        routes.remove_city(code)

    # remove a route
    elif opt == "2":
        print("Input 2 city codes/names separated with space to remove a route")
        raw = input()
        raw = raw.split(" ")

        if len(raw) != 2:
            print("Invalid input")
            return

        code1 = get_code(raw[0])
        code2 = get_code(raw[1])

        if code1 == "":
            print("input", raw[0], "is invalid")
            return
        if code2 == "":
            print("input", raw[1], "is invalid")
            return

        routes.remove_route(code1, code2)

    # add a city with all necessary info
    elif opt == "3":
        print("Input city to add as following with each item separated with space")
        print("[code] [name] [country] [continent] [timezone] [coordinates] [population] [region]")
        print("[coordinates] should be in this format: [N:50,E:50] with no space")
        raw = input()
        raw = raw.split(" ")

        if len(raw) != 8:
            print("Invalid input")
            return

        if int(raw[6]) < 0:
            print("population cannot be negative!")
            return

        if routes.add_city(raw) < 0:
            return

        print_city_info(airport_dict[raw[0].upper()])

    # add a route with all necessary info
    elif opt == "4":
        print("Input 2 city codes/names and distance separated with space to add a route")
        print("  ex) MEX CMI 5000")
        raw = input()
        raw = raw.split(" ")

        if len(raw) != 3:
            print("Invalid input")
            return

        code1 = get_code(raw[0])
        code2 = get_code(raw[1])

        if code1 == "":
            print("input", raw[0], "is invalid")
            return
        if code2 == "":
            print("input", raw[1], "is invalid")
            return
        if int(raw[2]) < 0:
            print("Distance cannot be negative!")
            return

        routes.add_route(code1.upper(), code2.upper(), raw[2])

    # edit an existing city
    elif opt == "5":
        print("Input a city code/name to edit")
        raw = input()
        code = get_code(raw)
        if code == "":
            print("Input", raw, "is invalid")
            return
        edit_city(code)

    elif opt == "b":
        return

    else:
        print("wrong input")


def print_stats():
    """
    Print user options for statistic info on route, and gets input and print out info accordingly.
    :return: void
    """
    opt = print_stats_menu()

    # longest single flight
    if opt == "1":
        print("Longest single flight(s):")
        flight_list = routes.longest_single_flight()
        for flight in flight_list:
            print("Departing from : " + flight[0] + " - " + translator[flight[0]])
            print("Arriving to : " + flight[1] + " - " + translator[flight[1]])
            print("Distance : " + str(flight[2]))

    # shortest single flight
    elif opt == "2":
        print("Shortest single flight(s):")
        flight_list = routes.shortest_single_flight()
        for flight in flight_list:
            print("Departing from : " + flight[0] + " - " + translator[flight[0]])
            print("Arriving to : " + flight[1] + " - " + translator[flight[1]])
            print("Distance : " + str(flight[2]))

    # avg distance
    elif opt == "3":
        print("Average distance:")
        print("%.2f" % routes.average_distance(), "mi.")

    # biggest city by population
    elif opt == "4":
        print("Biggest city:")
        city_list = routes.biggest_population()
        for city in city_list:
            print(city, "-", translator[city])
            print("population :", airport_dict[city].population)

    # smallest city by population
    elif opt == "5":
        print("Smallest city:")
        city_list = routes.smallest_population()
        for city in city_list:
            print(city, "-", translator[city])
            print("population :", airport_dict[city].population)

    # avg size of cities
    elif opt == "6":
        print("Average population of all cities served by CSAir")
        print(routes.average_population())

    # list of continents
    elif opt == "7":
        cont_dict = routes.list_of_continents()
        for item in cont_dict:
            print(item, ": ", end="")
            for city in cont_dict[item]:
                print(city + ", ", end="")
            print("")

    # hub cities
    elif opt == "8":
        print("Hub cities in CSAir network:")
        hub_list = routes.list_of_hub_cities()
        for hub in hub_list:
            print(hub, "-", translator[hub])

    elif opt == "b":
        return

    else:
        print("invalid input!")


def print_shortest_path():
    print("Enter two cities separated by a space")
    raw = input()
    raw = raw.split(" ")

    if len(raw) != 2:
        print("Invalid input")
        return

    city1 = get_code(raw[0])
    city2 = get_code(raw[1])
    if city1 == "":
        print(city1, "is invalid city")
        return
    if city2 == "":
        print(city2, "is invalid city")
        return

    shortest = routes.graph.shortest_path(city1, city2)
    distance = shortest[0]
    shortest.pop(0)
    print("shortest path : ", shortest)
    print("distance : ", distance)
    # print("shortest path : ", shortest)


def get_code(city):
    """
    translate city name to code or return code
    :param city: city name or code
    :return: null string if invalid, code otherwise
    """
    city = city.upper()
    if city not in airport_dict:
        city = city.title()
        if city not in translator:
            return ""
        return translator[city]
    else:
        return city


def print_city_info(airport):
    print("Code : " + airport.code)
    print("Name : " + airport.name)
    print("Country : " + airport.country)
    print("Continent : " + airport.continent)
    print("Timezone : " + str(airport.timezone))
    print("Latitude, Longitude : ", end="")
    print(airport.coordinates)
    print("Population : " + str(airport.population))
    print("Region : " + str(airport.region))
    print("List of cities via single non-stop flight : ")
    for code in airport.flights:
        print("    " + code + " - " + translator[code] + " (" + str(airport.flights[code]) + " km)")


def print_city():
    """
    Gets input and print city info accordingly. 1: code, 2: city name, 3: view city list, b: back to menu
    """

    opt = print_city_menu()

    if opt == "1":
        print("Please enter the code: ")
        raw = input()
        code = raw.upper()
        if code not in airport_dict:
            print(raw, "is not a valid city code")
        else:
            print_city_info(airport_dict[code])

    elif opt == "2":
        print("Please enter the city name: ")
        raw = input()
        name = raw.lower()
        code = routes.get_code(name)
        if code == "":
            print(raw, "is not a valid city name")
        else:
            print_city_info(airport_dict[code])

    elif opt == "3":
        print_city_list()

    elif opt == "b":
        return

    else:
        print("wrong input!")


def print_city_list():
    for code in airport_dict:
        print(airport_dict[code].code + " - " + airport_dict[code].name)


def draw_map():
    url = create_url()
    webbrowser.open(url)


def create_url():
    url = "http://www.gcmap.com/mapui?P="

    for departure in airport_dict:
        for arrival in airport_dict[departure].flights:
            url += departure
            url += "-"
            url += arrival
            url += ","

    url = url[:-1]
    url += "&MS=wls2&MC=DFW&PM=b:disc7%2b%22%25t%25+%28N%2212&PW=3&DU=mi"

    return url


def edit_city(code):
    raw = print_edit_city_menu()
    raw = raw.split(" ")
    opt = raw[0]
    val = raw[1]
    airport = airport_dict[code]

    if len(raw) != 2:
        print("invalid input")
        return

    if opt == "1":
        airport.code = val

    elif opt == "2":
        airport.name = val

    elif opt == "3":
        airport.country = val

    elif opt == "4":
        airport.continent = val

    elif opt == "5":
        airport.timezone = val

    # ex) N:50,E:50
    elif opt == "6":
        airport.coordinates = {}
        val = val.split(",")
        latitude = val[0].split(":")
        longitude = val[1].split(":")
        airport.coordinates[latitude[0]] = latitude[1]
        airport.coordinates[longitude[0]] = longitude[1]

    elif opt == "7":
        if int(val) < 0:
            print("population cannot be negative")
            return
        airport.population = val

    elif opt == "8":
        airport.region = val

    elif opt == "b":
        return

    else:
        print("Invalid input")


def print_edit_city_menu():
    print("Please input following option number and info as format [number] [info] separated with a space:")
    print("1 : Code")
    print("2 : Name")
    print("3 : Country")
    print("4 : Continent")
    print("5 : Timezone")
    print("6 : Coordinates (example format--N:50,E:50--without space)")
    print("7 : Population")
    print("8 : Region")
    print("b : back")
    return input()


def save_file():
    print("Enter the name of the file with .json extension")
    filename = input()
    printer = Printer.Printer(airport_dict)
    printer.print_to_json(filename)


def merge(dict1, dict2):
    merged = dict1.copy()
    merged.update(dict2)
    return merged


if __name__ == '__main__':
    main()
