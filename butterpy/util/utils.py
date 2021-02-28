import random
def random_coord(dim):
    random.seed()
    return [random.random() for _ in range(dim)]

def get_file_lines(filename):
    with open(filename) as file:
        return [line for line in file]

from numpy import cos, sin, array
def rotation_matrix(c,b,a):
    cosa, cosb, cosc = cos(a), cos(b), cos(c)
    sina, sinb, sinc = sin(a), sin(b), sin(c)
    return array([
        [cosa*cosb, cosa*sinb*sinc - sina*cosc, cosa*sinb*cosc + sina*sinc],
        [sina*cosb, sina*sinb*sinc + cosa*cosc, sina*sinb*cosc - cosa*sinc],
        [-sinb, cosb*sinc, cosb*cosc]
    ])
