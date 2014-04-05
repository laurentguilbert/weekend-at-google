# flake8: noqa
import networkx as nx

from baseobjects import AtchoumParser
from baseobjects import Car
from graph import Graph


def move(g, car, max_time):
    edges = [e for e in g.edges(car.node) if car.time + g.edge_cost(e) <= max_time]
    edges.sort(key=lambda e: (g.edge_visited(e), g.edge_score(e)))
    next_node = edges[0] if len(edges) else None
    if next_node is not None:
        car.move(g.edge_dict(next_node), next_node[1])
        g.inc_visited(next_node)
    return next_node

def main(filename="paris_54000.txt"):
    data = AtchoumParser.from_filename(filename)
    inters_obj = data.inters
    streets_obj = data.streets

    cars_count = data.cars
    max_time = data.time
    start_node = data.start

    # generate graph
    g = Graph(data)

    cars = []

    print cars_count

    for _ in range(cars_count):
        car = Car(node=start_node)
        cars.append(car)
        while move(g, car, max_time) is not None:
            pass
        car.export()

    # remove before submit
    print "####### results #######"
    for car in cars:
        print "#{}".format(car.total_len)
    print "#{}".format(Car.TOTAL_LEN)

main()
