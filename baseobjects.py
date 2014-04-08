# flake8: noqa
from helpers import enum, EXAMPLES_LINES, calc_dist

WAY = enum(UNIQUE=1, DOUBLE=2)

class Car(object):
    CAR_ID = 1
    TOTAL_LEN = 0

    def __init__(self, node, node_coord):
        self.id = Car.CAR_ID
        Car.CAR_ID += 1
        self.time = 0
        self.total_len = 0

        self.node = node
        self.prev_coord = node_coord
        self.node_coord = node_coord
        self.visited_nodes = [node]

        self.dests = []
        self.past_dests = []

    DEST_LAT = 0
    DEST_LONG = 1
    DEST_MAX_MOVE = 2
    DEST_MOVE = 3
    DEST_ACCEPTABLE_DIST = 4
    # DEST_DIST = 5

    def add_dests(self, lat, lon, max_move=None, acceptable_dist=None):
        # lat, lon, max_move, move, acceptable_dist
        self.dests.append([lat, lon, max_move, 0, acceptable_dist])

    def move_left(self, lat, lon):
        d1 = 0.0
        d2 = 0.0
        try:
            d1 = (self.prev_coord.lon - self.node_coord.lon) / (self.prev_coord.lat - self.node_coord.lat)
            d2 = (self.prev_coord.lon - lon) / (self.prev_coord.lat - lat)
            d1 = abs(d1)
            d2 = abs(d2)
            return d2 - d1
        except:
            import sys
            return sys.maxint

    def cardinal(self, lat, lon):
        """ va dans 4 directions """
        dir = self.id % 4
        if dir == 0:
            return self.node_coord[1] - lon
        elif dir == 1:
            return lon - self.node_coord[1]
        elif dir == 2:
            return self.node_coord[0] - lat
        else:
            return lat - self.node_coord[0]

    def inc_dest_move_if_needed(self, dest=None):
        if dest is None:
            if len(self.dests) == 0:
                return
            dest = self.dests[0]
        dest[Car.DEST_MOVE] += 1

    def has_fixed_dest(self):
        if len(self.dests) == 0:
            return False
        dest = self.dests[0]

        reach = False
        if dest[Car.DEST_MAX_MOVE] != None:
            if dest[Car.DEST_MAX_MOVE] <= dest[Car.DEST_MOVE]:
                reach = True
        if reach is False and dest[Car.DEST_ACCEPTABLE_DIST] is not None:
            lat, lon = self.node_coord
            dist = calc_dist(lat, lon, dest[Car.DEST_LAT], dest[Car.DEST_LONG])
            if dist < dest[Car.DEST_ACCEPTABLE_DIST]:  # 0.002
                reach = True

        if reach is True:
            self.past_dests.append(dest)
            self.dests.pop(0)
            return self.has_fixed_dest()
        return True

    def closer_to_dest(self, lat, lon):
        if len(self.dests) == 0:
            return 0
        dest = self.dests[0]

        latO, lonO = self.node_coord
        latD = dest[Car.DEST_LAT]
        lonD = dest[Car.DEST_LONG]
        dO = calc_dist(latO, lonO, latD, lonD)
        d = calc_dist(lat, lon, latD, lonD)
        # pour std sort
        if d > dO:
            return 3
        elif d == dO:
            return 2
        else:
            return 1

    def distance_to_dest(self, lat, lon):
        dest = self.dests[0]
        return calc_dist(lat, lon, dest[Car.DEST_LAT], dest[Car.DEST_LONG])

    def add_time(self, time):
        self.time += time

    def move(self, edge_dict, dest_node, dest_node_coord):
        self.add_time(edge_dict['cost'])
        self.node = dest_node
        self.prev_coord = self.node_coord
        self.node_coord = dest_node_coord
        self.visited_nodes.append(dest_node)
        self.inc_dest_move_if_needed()

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
        # return float(self.len) / (float(self.cost) * 2)
        return float(self.cost) / float(self.len)


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
