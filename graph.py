import networkx as nx

import baseobjects

class Graph(object):
    def edge_dict(self, e):
        return self.g[e[0]][e[1]]
    def edge_attr(self, e, key):
        return self.g[e[0]][e[1]][key]

    # getter shortcuts
    def edge_cost(self, e):
        return self.edge_attr('cost')
    def edge_len(self, e):
        return self.edge_attr('len')
    def edge_score(self, e):
        return self.edge_attr('score')
    def edge_is_visited(self, e):
        return self.edge_attr('visited')

    def set_edge_attr(self, e, key, val):
        self.g[e[0]][e[1]][key] = val
    def set_edge_visited(self, e, *args, **kwargs):
        self.set_edge_attr('visited', True)

    def cmp_edge_score(self, e, e1, *args, **kwargs):
        """ e[score] > e1[score] """
        return self.edge_attr(e, 'score') > self.edge_attr(e1, 'score')

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
                'visited': False,
            }
            dg.add_edge(street.i1, street.i2, **attr_dict)
            if street.way == baseobjects.WAY.DOUBLE:
                dg.add_edge(street.i2, street.i1, **attr_dict)

        self.g = dg

    def edges(self, start_node):
        return self.g.edges(start_node)