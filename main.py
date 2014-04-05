import os


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

def to_inter_object(inters):
    return [Intersection(*inter.split()) for inter in inters]

def to_street_object(streets):
    return [Street(*street.split()) for street in streets]

def main(filename="paris_54000.txt"):
    lines = []
    with open(filename) as f:
        lines = f.readlines()
    print lines[0]

    (n, m, t, c, s, ) = lines[0].split()

    inter = lines[1:int(n)+1]
    streets = lines[int(n)+1:]
    print inter[0], inter[-1], len(inter)
    print streets[0], streets[-1], len(streets)

    intersobj = to_inter_object(inter)
    streetsobj = to_street_object(streets)

    print intersobj[0].__dict__
    print streetsobj[0].__dict__

main()