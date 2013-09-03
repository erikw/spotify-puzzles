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
import copy

#DEBUG_MODE = True
DEBUG_MODE = False

def debug(text):
    if DEBUG_MODE: print(text)

class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.neighbours = set()

    def add_edge_to(self, other):
        self.neighbours.add(other)

    def has_edge_to(self, other):
        return other in self.neighbours

    def __eq__(self, other):
        return self.name == other.name and self.neighbours == other.neighbours

    def __str__(self):
        return self.name

    __repr__ = __str__

class Vote_vertex(Vertex):
    def __init__(self, stay, away, *args, **namedargs):
        super(Vote_vertex, self).__init__(*args, **namedargs)
        self._stay = stay
        self._away = away

    def __eq__(self, other):
        #return self._stay == other._stay and self._away == other._away
        return Vertex.__eq__(self, other) and self._stay == other._stay and self._away == other._away # TODO how in py?

    def __str__(self):
        return super(Vote_vertex, self).__str__() + "(s=%s, a=%s)" % (self._stay, self._away)

class Edge(object):
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def __str__(self):
        return "%s<-->%s" % (self.vertex1.name, self.vertex2.name)

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
    nbr_cats, nbr_dogs, nbr_votes = (int(num) for num in sys.stdin.readline().split())
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
    for neighbour in node.neighbours:
        bipartition_recurse(u, v, visited, neighbour, depth + 1)


def bipartition(graph):
    u = set()
    v = set()
    visited = set()
    for node in graph.verticies:
        if not node in visited:
            bipartition_recurse(u, v, visited, node)
    #debug("bipartiton:")
    #debug("u: %s" % u)
    #debug("v: %s" % v)
    return (u, v)



def free_verticies(u, v, matching):
    u_free = u.copy()
    v_free = v.copy()
    for (m_u, m_v) in matching:
        u_free.discard(m_u)
        v_free.discard(m_v)
    return (u_free, v_free)


def dfs_rec(cur_node, end_nodes, path, discarded_nodes):
    if cur_node in end_nodes:
        path.append(cur_node)
        return True
    else:
        path.append(cur_node)
        #debug("poppin' in {:s}, discarded_nodes={:s}".format(cur_node, discarded_nodes))
        for neighbour in cur_node.neighbours:
            if neighbour not in discarded_nodes and neighbour not in path and dfs_rec(neighbour, end_nodes, path, discarded_nodes):
                return True
        path.pop()
        return False

def partial_dfs(u, v, matching, start_node, end_nodes, discarded_nodes):
    debug("DFS from {:s} to end nodes: {:s}".format(start_node, end_nodes))
    path = []
    if len(end_nodes) > 0:
        if dfs_rec(start_node, end_nodes, path, discarded_nodes):
            discarded_nodes.update(path)
            #i = 0
            #for node in path:
                #for neighbour in node.neighbours:
                    #neighbour.neighbours.remove(node)
                #if i % 2 == 0:
                    #u.discard(node)
                #else:
                    ##debug("discardingin in v {:s}".format(node))
                    #v.discard(node)
                #i += 1
    return path

def tuplify_edges(verticies):
    if len(verticies) < 2:
        return ()
    edges = []
    node_a = verticies[0]
    i = 0
    for node_b in verticies[1:]:
        if i % 2 == 0:
            edges.append((node_a, node_b))
        else:
            edges.append((node_b, node_a))
        node_a = node_b
        i += 1
    return tuple(edges)


#def maximal_set_aug_paths(u_orig, v_orig, matching):
def maximal_set_aug_paths(u, v, matching):
    debug("Searching for new vertex-disjoint paths.")

    paths = set()

    u_free, v_free = free_verticies(u, v, matching)
    debug("u_free: {:s}".format(u_free))
    debug("v_free: {:s}".format(v_free))
    discarded_nodes = set()
    for u_node in u_free:
        path = partial_dfs(u, v, matching, u_node, v_free, discarded_nodes)
        if len(path) > 0:
            debug("path found: {:s}".format(path))
            paths.add(tuplify_edges(path))
    return paths


def hopcoft_karp(u, v):
    matching = set() # set of edges tuples. U nodes always at pos 0 in the tuples
    more_augmenting_paths = True
    while more_augmenting_paths:
        aug_paths = maximal_set_aug_paths(u, v, matching)
        if len(aug_paths) > 0:
            for path in aug_paths:
                #matching = symmetric_difference(matching, path)
                matching =  matching.symmetric_difference(path)
                debug("extending match to {:s}".format(matching))
        else:
            debug("no more aug paths")
            more_augmenting_paths = False
    #debug("matching:---")
    #debug(matching)
    #debug("end-matching:---")
    return matching

def max_matching(graph):
    u, v = bipartition(graph)
    return hopcoft_karp(u, v)

def main():
    nbr_tests = int(sys.stdin.readline())
    if nbr_tests == 0:
        print("0")
    else:
        for i in range(nbr_tests):
            conflict_graph = read_votes()
            debug(conflict_graph)
            print(conflict_graph.nbr_verticies() - len(max_matching(conflict_graph)))
    return 0


if __name__ ==  '__main__':
    sys.exit(main())
