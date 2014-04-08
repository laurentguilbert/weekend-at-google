# flake8: noqa
import networkx as nx
import sys

from baseobjects import AtchoumParser
from baseobjects import Car
from graph import Graph
from helpers import log_debug

def move0(g, car, max_time):
    """
    -0: 1.548
    """
    edges = g.edges(car.node)

    if car.has_fixed_dest(): #-score
        #edges.sort(key=lambda e: (g.edge_visited(e), car.distance_to_dest(*g.node_coord(e[1])), g.edge_score(e), ))
        edges.sort(key=lambda e: (g.edge_visited(e), car.closer_to_dest(*g.node_coord(e[1])), car.distance_to_dest(*g.node_coord(e[1])), g.edge_score(e), ) )
        #edges.sort(key=lambda e: (g.edge_visited(e), g.edge_score(e)))
    else:
        edges = [e for e in edges if car.time + g.edge_cost(e) <= max_time]
        # edges.sort(key=lambda e: (g.edge_visited(e), g.edge_score(e))) # -score
        edges.sort(key=lambda e: (g.edge_visited(e), g.get_node_potential(e[1], exclude=[e[0]]), ))  # -score

    next_node = edges[0] if len(edges) else None
    if next_node is not None:
        car.move(g.edge_dict(next_node), next_node[1], g.node_coord(next_node[1]))
        g.inc_visited(next_node)
    return next_node

def move(g, car, max_time):
    edges = g.edges(car.node)
    edges = [e for e in edges if car.time + g.edge_cost(e) <= max_time]
    if len(car.visited_nodes) < 100:
        edges.sort(key=lambda e: (g.edge_visited(e), car.cardinal(*g.node_coord(e[1])), ))
    else:
        # edges.sort(key=lambda e: (g.edge_visited(e), g.edge_score(e))) # - score
        edges.sort(key=lambda e: (g.edge_visited(e), g.get_node_potential(e[1], exclude=[e[0]]), ))
    # print edges
    # print "=="
    next_node = edges[0] if len(edges) else None
    if next_node is not None:
        car.move(g.edge_dict(next_node), next_node[1], g.node_coord(next_node[1]))
        g.inc_visited(next_node)
    return next_node

def move2(g, car, max_time):
    edges = g.edges(car.node)
    edges = [e for e in edges if car.time + g.edge_cost(e) <= max_time]
    edges.sort(key=lambda e: (g.edge_visited(e), car.move_left(*g.node_coord(e[1])), ))
    # print edges
    # print "=="
    next_node = edges[0] if len(edges) else None
    if next_node is not None:
        car.move(g.edge_dict(next_node), next_node[1], g.node_coord(next_node[1]))
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


def main(func, filename):
    data = AtchoumParser.from_filename(filename)
    cars_count = data.cars#+ 200
    max_time = data.time
    start_node = data.start
    g = Graph(data)

    start_coord = (g.node_lat(start_node), g.node_long(start_node), )
    cars = [Car(node=start_node, node_coord=start_coord) for _ in range(cars_count)]

    cars[0].add_dests(48.840, 2.318, 100)
    # cars[1].add_dests(48.840, 2.318, 100)
    cars[1].add_dests(48.850, 2.293, 100)
    cars[2].add_dests(48.832, 2.356, 150)
    # cars[3].add_dests(48.879, 2.389, 50)
    # cars[1].dest_lat = 48.820
    # cars[1].dest_long = 2.344
    # cars[2].dest_lat = 48.827
    # cars[2].dest_long = 2.315

    # cars[3].dest_lat = 48.842
    # cars[3].dest_long = 2.336

    func(cars, g, max_time)

    #cars.sort(key=lambda c: -c.total_len)
    #cars = cars[:data.cars]
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
    -0: use whilecars
    -1: use whilecanmove
    """
    sys.exit(0)

div_time = False
func = whilecars
filename = "paris_54000.txt"
opts = { '-0': whilecars, '-1': whilecanmove, }
func = help_and_quit
if len(sys.argv) == 1:
    func = whilecars
elif (len(sys.argv) == 2):
    func = opts.get(sys.argv[1], help_and_quit)

main(func, filename)
