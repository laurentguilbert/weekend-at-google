# flake8: noqa
import networkx as nx
import sys

from baseobjects import AtchoumParser
from baseobjects import Car
from graph import Graph
from helpers import log_debug

def sort_std2(g, edges):
    edges.sort(key=lambda e: g.edge_visited(e))
    return edges

def move(g, car, max_time):
    edges = g.edges(car.node)

    if car.has_fixed_dest((g.node_lat(car.node), g.node_long(car.node))):
        edges.sort(key=lambda e: car.distante_to_dest(g.node_lat(e[1]), g.node_long(e[1])))
    else:
        edges = [e for e in edges if car.time + g.edge_cost(e) <= max_time]
        edges = sort_std2(g, edges)
    next_node = edges[0] if len(edges) else None
    if next_node is not None:
        car.move(g.edge_dict(next_node), next_node[1])
        g.inc_visited(next_node)
    return next_node

def whilecars(cars, g, max_time):
    for car in cars:
        while move(g, car, max_time) is not None:
            pass

def whilecanmove(cars, g, max_time):
    can_move = True
    while can_move:
        can_move = False
        for car in cars:
            if move(g, car, max_time) is not None:
                can_move = True


def main(func, div_time, filename):
    data = AtchoumParser.from_filename(filename)
    cars_count = data.cars + 200
    max_time = data.time
    start_node = data.start
    g = Graph(data, div_time)


    cars = [Car(node=start_node) for _ in range(cars_count)]

    cars[0].dest_lat = 48.840
    cars[0].dest_long = 2.318

    # cars[1].dest_lat = 48.820
    # cars[1].dest_long = 2.344

    # cars[2].dest_lat = 48.827
    # cars[2].dest_long = 2.315

    # cars[3].dest_lat = 48.842
    # cars[3].dest_long = 2.336

    func(cars, g, max_time)

    cars.sort(key=lambda c: -c.total_len)
    cars = cars[:data.cars]
    print len(cars)
    for car in cars:
        car.export()

    test_total = 0
    for car in cars:
        test_total += car.total_len

    log_debug("results")
    for car in cars:
        log_debug(str(car.total_len))
    log_debug(str(test_total))

def help_and_quit(*args, **kwargs):
    print """python main.py -<n=0>
    -0: use whilecars (divtime False)
    -1: use whilecanmove (divtime False)

    -2: use whilecars (divtime True)
    -3: use whilecanmove (divtime False)
    """
    sys.exit(0)

div_time = False
func = whilecars
filename = "paris_54000.txt"
opts = {
    '-0': whilecars,
    '-2': whilecars,
    '-1': whilecanmove,
    '-3': whilecanmove,
}
opts_div_time = {
    '-0': False,
    '-2': True,
    '-1': False,
    '-3': True,
}
func = help_and_quit
if len(sys.argv) == 1:
    func = whilecars
elif (len(sys.argv) == 2):
    func = opts.get(sys.argv[1], help_and_quit)
    div_time = opts_div_time.get(sys.argv[1], help_and_quit)

main(func, div_time, filename)


def sort_std(g, edges):
    """ deprecated """
    edges.sort(key=lambda e: (g.edge_visited(e), g.edge_score(e)))
    return edges

def sort_my(g, edges):
    """ deprecated: use sortstd"""
    visited = {}
    visited_list = []
    for e in edges:
        slug = g.edge_visited(e)
        if not slug in visited_list:
            visited_list.append(slug)
        if not slug in visited:
            visited[slug] = [e]
        else:
            visited[slug].append(e)

    visited_list.sort()
    res = []
    for k in visited_list:
        l = visited[k]
        l.sort(key=lambda e: g.edge_score(e), reverse=True)
        res += l
    return res
