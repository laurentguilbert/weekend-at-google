import networkx as nx

import baseobjects


class Graph(object):
    def node_lat(self, node):
        return self.g.node[node]['c1']

    def node_long(self, node):
        return self.g.node[node]['c2']

    def node_coord(self, node):
        return (self.g.node[node]['c1'], self.g.node[node]['c2'], )

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
        try:
            self.g[e[0]][e[1]][key] = val
        except:
            pass

    def inc_visited(self, e, *args, **kwargs):
        hit = self.edge_visited(e) + 1
        self.set_edge_attr(e, 'visited', hit)
        self.set_edge_attr((e[1], e[0], ), 'visited', hit)

    def get_node_potential(self, node, exclude=[], depth=5):
        """" lower is better """
        edges = self.edges(node)
        nexclude = exclude + [node]
        if depth == 0:
            return 0
        for edge in edges:
            i = self.edge_visited(edge)
            i += self.get_node_potential(edge[1], nexclude, depth - 1)
        return i

    def __init__(self, atchoum):
        self.atchoum = atchoum

        dg = nx.DiGraph()

        for idx, inter in enumerate(atchoum.inters):
            dg.add_node(idx, **inter.__dict__)

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
