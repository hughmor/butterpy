import random

def random_coord(dim):
    random.seed()
    return [random.random() for _ in range(dim)]