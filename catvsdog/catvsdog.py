#!/usr/bin/env python2
 # coding=utf8
""""
Determine the subset of dogs and cats that gets to stay in the program to maximize view vote satisfaction.

1. Draw the "conflict graph" G_c = V, E, with V = set of votes, E = edge between every votes that has a conflict in choice.
2. We're interested in the complement of G_c, the compatible graph G_cmpat where and edge represents a non-conflict between two votes. In G_cmpat we want to find the largest connected component that is complete i.e. the largest subset of verticies that are all connected directly to each other.
3. Constructing G_compat from G_c takes extra time so we extract this number from G_c. By studying examples we see that the number we want from G_cmpat is |V| - (min vertex cover) in G_c. Min vertex cover is a hard problem but luckily G_c is bipartite (since each vote must contain 1 dog and 1 cat, therefore in an example of 3 votes, G_c could look like v1-v2-v3 but an edge from v1 to v3 could not exist for this 1dog1cat-reason). The bipartiteness enables us to use the Köning's theorem which states equivalence between min vertex cover and maximum edge matching in bipartite graphs.
4. Thus return as answer |V| - maxedgematch(G_c), which can be done with Network Flow. However the best algo seems to be Hopcroft-Karp's, so lets use that one.
"""

import sys

class Vertex(object):
    def __init__(self, name):
        self.name = name

class Vote_vertex(Vertex):
    def __init__(self, stay, away, *args, **namedargs):
        super(Vote_vertex, self).__init__(*args, **namedargs)
        self.stay = stay
        self.away = away

class Edge(object):
    def __init__(self, vertex1, vertex2):
        self._vertex1 = vertex1
        self._vertex2 = vertex1

class Graph(object):
    def __init__(self):
        self._verticies = set()
        self._edges = set()

    def add_vertex(self, vertex):
        self._verticies.add(vertex)

    def add_edge(self, vertex1, vertex2):
        e = Edge(vertex1, vertex2)
        self._edges.add(e)


def read_votes():
    nbr_cats, nbr_dogs, nbr_votes = (int(num) for num  in sys.stdin.readline().split())
    graph = Graph()
    stay_votes = {}
    away_votes = {}
    i = 1
    for vote in range(nbr_votes):
        stay, away = sys.stdin.readline().split()
        node = Vote_vertex(stay, away, "v%d" % i)
        i += 1

        if stay in away_votes:
            for conflict_node in away_votes[stay]:
                graph.add_edge(node, conflict_node)

        if away in stay_votes:
            for conflict_node in stay_votes[away]:
                graph.add_edge(node, conflict_node)

        if stay in stay_votes:
            stay_votes[stay].add(node)
        else:
            stay_votes[stay] = {node}

        if away in away_votes:
            away_votes[away].add(node)
        else:
            away_votes[away] = {node}


def main():
    nbr_tests = int(sys.stdin.readline())
    for i in range(nbr_tests):
        compat_graph = read_votes()
    return 0


if __name__ ==  '__main__':
    sys.exit(main())
