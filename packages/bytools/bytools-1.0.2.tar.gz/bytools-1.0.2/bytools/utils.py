import numpy as np

def hello():
    print('Hello! this is bytools')

def random_color():
    b = np.random.randint(0, 256)
    g = np.random.randint(0, 256)
    r = np.random.randint(0, 256)
    return (b, g, r)
