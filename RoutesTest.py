import unittest
import Graph
import Parse
import Routes


class RoutesTest(unittest.TestCase):

    def setUp(self):
        self.parser = Parse.Parser("test_map_data.json")
        self.parser.parse()
        self.translator = self.parser.translator
        self.routes = Routes.Routes(self.parser.airport_dict)
        self.airport_dict = self.routes.airport_dict
        self.graph = self.routes.graph

    def test_shortest_path(self):
        dist = 4651+3158+2714
        path = [dist, 'BUE', 'BOG', 'MEX', 'CHI']
        self.assertEqual(self.graph.shortest_path("BUE", "CHI"), path)

    def test_weight(self):
        v1 = 'BOG'
        v2 = 'LIM'
        v3 = 'MEX'
        v4 = 'CHI'
        weight = 1879+4231+2714
        self.assertEqual(self.graph.path_weight([v1, v2, v3, v4]), weight)

    def test_remove_vertex(self):
        v = 'LIM'
        self.graph.remove_vertex(v)
        self.assertFalse(v in self.graph.vertices)
        for u in self.graph.vertices:
            self.assertFalse(v in self.graph.vertices[u].out_edges)
            self.assertFalse(v in self.graph.vertices[u].in_edges)

    def test_remove_edge(self):
        u = 'MEX'
        v = 'CHI'
        self.graph.remove_edge(u, v)
        self.assertFalse(u in self.graph.vertices[v].in_edges)
        self.assertFalse(v in self.graph.vertices[u].out_edges)
        self.assertEqual(self.graph.shortest_path(u, v), -1)

    def test_edges(self):
        longest = [4651, ['BUE', 'BOG'], ['BOG', 'BUE']]
        shortest = [1680, ['BUE', 'SAO'], ['SAO', 'BUE']]

        short_test = self.graph.shortest_edge()
        long_test = self.graph.longest_edge()

        self.assertEqual(long_test[0], longest[0])
        self.assertEqual(short_test[0], shortest[0])
        
        self.assertEquals(len(short_test), len(shortest))
        self.assertEqual(len(long_test), len(longest))

    def test_distance(self):
        dist = self.routes.distance(['LIM', 'MEX', 'BOG'])
        self.assertEqual(dist, 4231+3158)

    def test_cost(self):
        cost = self.routes.cost(['LIM', 'MEX', 'BOG'])
        ans = 4231*.35 + 3158*.3
        self.assertEqual(cost, ans)

if __name__ == '__main__':
    unittest.main()
