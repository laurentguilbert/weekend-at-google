def enum(**enums):
    return type('Enum', (), enums)

EXAMPLES_LINES = [
    "3 2 3000 2 0",
    "48.8582 2.2945",
    "50.0 3.09",
    "51.424242 3.02",
    "0 1 1 30 250",
    "1 2 2 45 200",
]

def log_debug(str):
    print "#{}".format(str)


from math import sqrt

def calc_dist(xo, yo, xd, yd):
    return sqrt(pow(xd - xo, 2) + pow(yd - yo, 2))
