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
        self.edges = set()

    def add_edge_to(self, other):
        self.edges.add(other)

    def has_edge_to(self, other):
        return other in self.edges

    def __str__(self):
        return self.name

    __repr__ = __str__

class Vote_vertex(Vertex):
    def __init__(self, stay, away, *args, **namedargs):
        super(Vote_vertex, self).__init__(*args, **namedargs)
        self._stay = stay
        self._away = away

    def __str__(self):
        return super(Vote_vertex, self).__str__() + "(s=%s, a=%s)" % (self._stay, self._away)

class Edge(object):
    def __init__(self, vertex1, vertex2):
        self._vertex1 = vertex1
        self._vertex2 = vertex2

    def __str__(self):
        return "%s<-->%s" % (self._vertex1.name, self._vertex2.name)

    __repr__ = __str__


class Graph(object):
    def __init__(self):
        self.verticies = set()
        self.edges = set()

    def add_vertex(self, vertex):
        self.verticies.add(vertex)

    def add_edge(self, vertex1, vertex2):
        e = Edge(vertex1, vertex2)
        self.edges.add(e)
        vertex1.add_edge_to(vertex2)
        vertex2.add_edge_to(vertex1)

    def nbr_verticies(self):
        return len(self.verticies)

    def edge_exist(self, vertex1, vertex2):
        return vertex1.has_edge_to(vertex2)

    def __str__(self):
        output = "verticies:\n" + ",\n".join("\t%s" % v for v in self.verticies) + "\n"
        output += "edges:\n" + "\n".join("\t%s" % e for e in self.edges)
        return output


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


def bipartition_recurse(u, v, visited, node, depth=0):
    if node in visited: return
    visited.add(node)
    if depth % 2 == 0:
        u.add(node)
    else:
        v.add(node)
    for neighbour in node.edges:
        bipartition_recurse(u, v, visited, neighbour, depth + 1)


def bipartition(graph):
    u = set()
    v = set()
    visited = set()
    for node in graph.verticies:
        if not node in visited:
            bipartition_recurse(u, v, visited, node)
    print("u: %s" % u)
    print("v: %s" % v)
    return (u, v)


def bfs_find_free_rec(u_matched, v_matched, v_free, layer, depth=0):
    if len(layer) == 0:
        print("returning empty set")
        return set()
    next_layer = set()
    if depth % 2 == 0:  # On U-side of bipartition.
        for u_node in layer:
            for neighbour in u_node.edges:
                if neighbour not in v_matched:
                    next_layer.add(neighbour)
        print("u next layer: %s\n" % next_layer)
        return bfs_find_free_rec(u_matched, v_matched, v_free, next_layer, depth + 1)
    else:   # On V-side. of bipartition.
        f = set([lnode if lnode in v_free else None for lnode in layer])
        if len(f) > 0:
            print("returning f = %s\n" % f)
            return f
        for v_node in layer:
            for neighbour in v_node.edges:
                if neighbour in u_matched:
                    next_layer.add(neighbour)
        print("v next layer: %s\n" % next_layer)
        return bfs_find_free_rec(u_matched, v_matched, v_free, next_layer, depth + 1)


def hopcoft_karp(u, v):
    u_free = u.copy()
    v_free = v.copy()
    #matching = set()
    u_matched = set()
    v_matched = set()
    more_aug_paths = True
    while more_aug_paths:
        #f = bfs_find_free(u_free, v_free, matched)
        free_u_node = iter(u_free).next()
        print("first free u node is %s\n" % free_u_node)
        f = bfs_find_free_rec(u_matched, v_matched, v_free, {free_u_node})
        if len(f) > 0:




        more_aug_paths = False
    return len(u_matched) + len(v_matched)
        


    return len(matching)

def max_matching(graph):
    return hopcoft_karp(*bipartition(graph))

def main():
    nbr_tests = int(sys.stdin.readline())
    for i in range(nbr_tests):
        conflict_graph = read_votes()
        #print(conflict_graph)
        print(conflict_graph.nbr_verticies() - max_matching(conflict_graph))
    return 0


if __name__ ==  '__main__':
    sys.exit(main())
