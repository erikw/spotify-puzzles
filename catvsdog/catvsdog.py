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
        self._name = name

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name

    __unicode__ = __str__

class Vote_vertex(Vertex):
    def __init__(self, stay, away, *args, **namedargs):
        super(Vote_vertex, self).__init__(*args, **namedargs)
        self._stay = stay
        self._away = away
        self._edges = set()

    def add_edge_to(self, other):
        self._edges.add(other)

    def has_edge_to(self, other):
        return other in self._edges

    def __str__(self):
        return super(Vote_vertex, self).__str__() + "(s=%s, a=%s)" % (self._stay, self._away)

    __unicode__ = __str__

class Edge(object):
    def __init__(self, vertex1, vertex2):
        self._vertex1 = vertex1
        self._vertex2 = vertex2

    def __str__(self):
        return "%s<-->%s" % (self._vertex1.get_name(), self._vertex2.get_name())

    __unicode__ = __str__

class Graph(object):
    def __init__(self):
        self._verticies = set()
        self._edges = set()

    def add_vertex(self, vertex):
        self._verticies.add(vertex)

    def add_edge(self, vertex1, vertex2):
        e = Edge(vertex1, vertex2)
        self._edges.add(e)
        vertex1.add_edge_to(vertex2)
        vertex2.add_edge_to(vertex1)

    def nbr_verticies(self):
        return len(self._verticies)

    def edge_exist(self, vertex1, vertex2):
        return vertex1.has_edge_to(vertex2)

    def __str__(self):
        output = "verticies:\n" + ",\n".join("\t%s" % v for v in self._verticies) + "\n"
        output += "edges:\n" + "\n".join("\t%s" % e for e in self._edges)
        return output

    __unicode__ = __str__


def add_conflict_edges(graph, node, node_set):
        for conflict_node in node_set:
            if not graph.edge_exist(node, conflict_node):
                graph.add_edge(node, conflict_node)


def read_votes():
    nbr_cats, nbr_dogs, nbr_votes = (int(num) for num  in sys.stdin.readline().split())
    graph = Graph()
    stay_votes = {}
    away_votes = {}
    i = 1
    for vote in range(nbr_votes):
        stay, away = sys.stdin.readline().split()
        node = Vote_vertex(stay, away, "v%d" % i)
        graph.add_vertex(node)
        i += 1
        if stay in away_votes:
            add_conflict_edges(graph, node, away_votes[stay])
        if away in stay_votes:
            add_conflict_edges(graph, node, stay_votes[away])

        if stay in stay_votes:
            stay_votes[stay].add(node)
        else:
            stay_votes[stay] = {node}

        if away in away_votes:
            away_votes[away].add(node)
        else:
            away_votes[away] = {node}
    return graph

def hopcoft_karp(graph):
    

def max_matching(graph):
    return hopcoft_karp(graph)

def main():
    nbr_tests = int(sys.stdin.readline())
    for i in range(nbr_tests):
        conflict_graph = read_votes()
        #print(conflict_graph)
        print(conflict_graph.nbr_verticies() - max_matching(conflict_graph))
    return 0


if __name__ ==  '__main__':
    sys.exit(main())
