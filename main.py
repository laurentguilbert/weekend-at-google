# flake8: noqa
import networkx as nx

from baseobjects import AtchoumParser


def main(filename="paris_54000.txt"):
    data = AtchoumParser.from_filename(filename)
    inters_obj = data.inters
    streets_obj = data.streets

    # generate graph
    dg = nx.DiGraph()

    for idx, inter in enumerate(inters_obj):
        dg.add_node(idx, inter.__dict__)

    for street in streets_obj:
        dg.add_edge(street.i1, street.i2, weight=street.cost, attr_dict=street.__dict__)
        if street.way == 2:
            dg.add_edge(street.i2, street.i1, weight=street.cost, attr_dict=street.__dict__)

main()
