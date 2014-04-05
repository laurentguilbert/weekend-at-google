# flake8: noqa
from helpers import enum, EXAMPLES_LINES

WAY = enum(UNIQUE=1, DOUBLE=2)

class Car(object):
    CAR_ID = 1
    TOTAL_LEN = 0

    def __init__(self, node):
        self.node = node
        self.id = Car.CAR_ID
        self.time = 0
        self.total_len = 0
        self.visited_nodes = [node]
        Car.CAR_ID += 1

    def add_time(self, time):
        self.time += time

    def move(self, edge_dict, dest_node):
        self.add_time(edge_dict['cost'])
        self.node = dest_node
        self.visited_nodes.append(dest_node)

        if edge_dict['visited'] == 0:
            self.total_len += edge_dict['len']
            Car.TOTAL_LEN += edge_dict['len']

    def export(self):
        print len(self.visited_nodes)
        for node in self.visited_nodes:
            print node


class Intersection(object):
    def __init__(self, c1, c2):
        self.c1 = float(c1)
        self.c2 = float(c2)


class Street(object):
    def __init__(self, inter1, inter2, way, cost, len):
        self.i1 = int(inter1)
        self.i2 = int(inter2)
        self.way = int(way)
        self.cost = int(cost)
        self.len = int(len)

    @property
    def score(self):
        return float(self.len) # / (float(self.cost) * 2)


class AtchoumParser(object):
    def __init__(self, inters, streets, time, cars, start):
        self.inters = inters
        self.streets = streets
        self.time = int(time)
        self.cars = int(cars)
        self.start = int(start)

    @staticmethod
    def from_lines(lines=EXAMPLES_LINES):
        def to_inter_object(inters):
            return [Intersection(*inter.split()) for inter in inters]

        def to_street_object(streets):
            return [Street(*street.split()) for street in streets]

        (n, m, time, cars, start, ) = lines[0].split()

        n = int(n)
        m = int(m)
        inters = lines[1:n + 1]
        streets = lines[n + 1:]
        if len(inters) != n: raise Exception("fock 1")
        if len(streets) != m: raise Exception("fock 2")

        inters = to_inter_object(inters)
        streets = to_street_object(streets)

        return AtchoumParser(inters, streets, time, cars, start)

    @staticmethod
    def from_filename(filename):
        lines = []
        with open(filename) as f:
            lines = f.readlines()
        return AtchoumParser.from_lines(lines)
