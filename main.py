# flake8: noqa
import networkx as nx

from baseobjects import AtchoumParser


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
        dg.add_edge(street.i1, street.i2, weight=street.cost, len=street.len)
        if street.way == 2:
            dg.add_edge(street.i2, street.i1, weight=street.cost, len=street.len)

    print dg[start_node]

main()
