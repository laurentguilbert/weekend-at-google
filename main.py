# flake8: noqa
import networkx as nx

from baseobjects import AtchoumParser


def get_edge_dict(dg, e):
    return dg[e[0]][e[1]]

def set_edge_attr(dg, e, key, val):
    dg[e[0]][e[1]][key] = val

def main(filename="example.txt"):
    data = AtchoumParser.from_filename(filename)
    inters_obj = data.inters
    streets_obj = data.streets

    cars_count = data.cars
    max_cost = data.time
    start_node = data.start

    print "cars count: {}".format(cars_count)
    print "max cost: {}".format(max_cost)
    print "start node: {}".format(start_node)

    # generate graph
    dg = nx.DiGraph()

    for idx, inter in enumerate(inters_obj):
        dg.add_node(idx, inter.__dict__)

    for street in streets_obj:
        attr_dict = {
            'weight': street.cost,
            'len': street.len,
            'score': street.score,
            'visited': False,
        }
        dg.add_edge(street.i1, street.i2, **attr_dict)
        if street.way == 2:
            dg.add_edge(street.i2, street.i1, **attr_dict)

    for e in dg.edges(start_node):
        e_dict = get_edge_dict(dg, e)

        print e_dict

main()
