import networkx as nx

import baseobjects


class Graph(object):
    def edge_dict(self, e):
        return self.g[e[0]][e[1]]

    def edge_attr(self, e, key):
        return self.g[e[0]][e[1]][key]

    # getter shortcuts
    def edge_cost(self, e):
        return self.edge_attr(e, 'cost')

    def edge_len(self, e):
        return self.edge_attr(e, 'len')

    def edge_score(self, e):
        return self.edge_attr(e, 'score')

    def edge_visited(self, e):
        return self.edge_attr(e, 'visited')

    def set_edge_attr(self, e, key, val):
        self.g[e[0]][e[1]][key] = val

    def inc_visited(self, e, *args, **kwargs):
        self.set_edge_attr(e, 'visited', self.edge_visited(e) + 1)

    def cmp_edge_score(self, e, e1, *args, **kwargs):
        """ e[score] > e1[score] """
        return self.edge_score(e) > self.edge_score(e1)

    def __init__(self, atchoum):
        self.atchoum = atchoum

        dg = nx.DiGraph()

        for idx, inter in enumerate(atchoum.inters):
            dg.add_node(idx, inter.__dict__)

        for street in atchoum.streets:
            attr_dict = {
                'cost': street.cost,
                'len': street.len,
                'score': street.score,
                'visited': 0,
            }
            dg.add_edge(street.i1, street.i2, **attr_dict)
            if street.way == baseobjects.WAY.DOUBLE:
                dg.add_edge(street.i2, street.i1, **attr_dict)

        self.g = dg

    def edges(self, start_node):
        return self.g.edges(start_node)
