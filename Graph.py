

class Graph:

    def __init__(self):
        self.vertices = {}

    def add_edge(self, v1, v2, distance):
        """
        Add edge to the graph
        :param v1: from vertex
        :param v2: to vertex
        :return:
        """
        if v1 not in self.vertices:
            self.vertices[v1] = Vertex()
        if v2 not in self.vertices:
            self.vertices[v2] = Vertex()

        self.vertices[v1].out_edges[v2] = distance
        self.vertices[v2].in_edges[v1] = distance

    def longest_edge(self):
        """
        find longest edge(s). index 0 will
        always be the weight and the rest
        of the indices contain the edges
        :return: list of longest edges
        """
        longest_dist = -1
        longest_edges = []
        for v1 in self.vertices:
            for v2 in self.vertices[v1].out_edges:
                dist = self.vertices[v1].out_edges[v2]

                if longest_dist < dist:
                    longest_dist = dist
                    longest_edges = [dist, [v1, v2]]

                elif longest_dist == dist:
                    longest_edges.append([v1, v2])

        return longest_edges

    def shortest_edge(self):

        shortest_dist = float('inf')
        shortest_edges = []

        for v1 in self.vertices:
            for v2 in self.vertices[v1].out_edges:
                dist = self.vertices[v1].out_edges[v2]

                if shortest_dist > dist:
                    shortest_dist = dist
                    shortest_edges = [dist, [v1, v2]]

                elif shortest_dist == dist:
                    shortest_edges.append([v1, v2])


        return shortest_edges

    def average_weight(self):
        total = 0.0
        count = 0.0
        for v1 in self.vertices:
            for v2 in self.vertices[v1].out_edges:
                total += self.vertices[v1].out_edges[v2]
                count += 1.0
        return total/count

    def largest_outdegree(self):
        delta = 0
        vertices = []
        for item in self.vertices.items():
            v = item[1]
            if delta < len(v.out_edges):
                delta = len(v.out_edges)
                vertices = [item[0]]
            elif delta == len(v.out_edges):
                vertices.append(item[0])
        return vertices

    def largest_degree(self):
        delta = 0
        vertices = []
        for item in self.vertices.items():
            v = item[1]
            if delta < len(v.out_edges) + len(v.in_edges):
                delta = len(v.out_edges) + len(v.in_edges)
                vertices = [item[0]]
            elif delta == len(v.out_edges) + len(v.in_edges):
                vertices.append(item[0])
        return vertices

    def add_vertex(self, v):
        self.vertices[v] = Vertex()

    def remove_vertex(self, v):
        self.vertices.pop(v)
        for u in self.vertices:
            if v in self.vertices[u].in_edges:
                self.vertices[u].in_edges.pop(v)
            if v in self.vertices[u].out_edges:
                self.vertices[u].out_edges.pop(v)

    def remove_edge(self, v1, v2):
        self.vertices[v1].out_edges.pop(v2)
        self.vertices[v2].in_edges.pop(v1)

    def shortest_path(self, v1, v2):
        """
        computes shortest path between two vertices using Dijkstra's algorithm
        :return: list of edges [v1,u1,u2,..,v2]
        """
        dist = {}
        prev = {}
        Q = []
        dist[v1] = 0
        path = [v2]

        for v in self.vertices:
            if v != v1:
                dist[v] = float('inf')
                prev[v] = ''
            Q.append(v)

        while len(Q) != 0:
            minimum = float('inf')
            for v in Q:
                if dist[v] <= minimum:
                    minimum = dist[v]
                    u = v

            Q.remove(u)

            for v in self.vertices[u].out_edges:
                alt = dist[u] + self.vertices[u].out_edges[v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        if dist[v2] == float('inf'):
            print('no path from', v1, "to", v2)
            return -1
        u = v2
        while u != v1:
            path.insert(0, prev[u])
            u = prev[u]

        dist = self.path_weight(path)
        path.insert(0, dist)

        return path


    def path_weight(self, path):
        """
        given the path, calculate the weight
        :param path: [v1,v2,v3,...]
        :return: weight
        """
        weight = 0
        for i in range(0, len(path)-1):
            vi = path[i]
            vj = path[i+1]

            if vj not in self.vertices[vi].out_edges:
                print("No connection from", path[i], "to", path[i+1])
                return -1

            weight += self.vertices[vi].out_edges[vj]

        # print(weight)
        return weight

    def edge_weight(self, v1, v2):
        """
        Given two vertices get the weight of the edge
        :return: weight
        """
        if v2 not in self.vertices[v1].out_edges:
            return -1
        return self.vertices[v1].out_edges[v2]


class Vertex:

    def __init__(self):
        # edges hash dictionary {vertex : weight}
        self.out_edges = {}
        self.in_edges = {}

