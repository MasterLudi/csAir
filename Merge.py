

class Merger:

    def __init__(self, dict1, dict2):
        """
        constructor for the merger
        :param dict1: existing airport dictionary
        :param dict2: new airport dictionary to merge
        """
        self.dict1 = dict1
        self.dict2 = dict2

    def merge(self):
        """
        Merges two Airport dictionaries
        :return: merged dictionary
        """

        # merge dict2 to dict1
        dict1 = self.dict1
        dict2 = self.dict2

        for code in dict2:
            if code not in dict1:
                dict1[code] = dict2[code]
            else:
                # update flight info
                for flight in dict2[code].flights:
                    if flight not in dict1[code].flights:
                        dict1[code].flights[flight] = dict2[code].flights[flight]

            for flight in dict1[code].flights:
                dict1[flight].flights[code] = dict1[code].flights[flight]

        return dict1