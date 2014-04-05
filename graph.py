import networkx as nx

class Graph(object):
    def get_edge_dict(self, e):
        return self.dg[e[0]][e[1]]

    def get_edge_attr(self, e, key):
        self.dg[e[0]][e[1]][key] = val

    def edge_len(self, e):
        return self.get_edge_attr('len')
    def edge_score(self, e):
        return self.get_edge_attr('score')
    def edge_is_visited(self, e):
        return self.get_edge_attr('visited')

    def set_edge_attr(self, e, key, val):
        self.dg[e[0]][e[1]][key] = val

    def edge_set_visited(self, e, *args, **kwargs):
        self.set_edge_attr('visited', True)

    def cmp_edge_score(self, e, e1, *args, **kwargs):
        """ e[score] > e1[score] """
        return self.get_edge_attr(e, 'score') > self.get_edge_attr(e1, 'score')

    def __init__(self, atchoum):
        self.atchoum = atchoum

        dg = nx.DiGraph()

        for idx, inter in enumerate(atchoum.inters):
            dg.add_node(idx, inter.__dict__)

        for street in atchoum.streets:
            attr_dict = {
                'weight': street.cost,
                'len': street.len,
                'score': street.score,
                'visited': False,
            }
            dg.add_edge(street.i1, street.i2, **attr_dict)
            if street.way == 2:
                dg.add_edge(street.i2, street.i1, **attr_dict)

        self.dg = dg
