import numpy as np

def L1(x):
    return np.linalg.norm(x,ord=1)

def L2(x):
    return np.linalg.norm(x,ord=2)
