import numpy as np

"""
a = np.array([[[0, 1], [1, 2]], [[2, 3], [3, 4]]])
b = np.array([[[0, 0], [1, 1]], [[0, 0], [1, 1]]])

def f(x, y, c):
    return x*y+c

vfunc = np.vectorize(f)

x = vfunc(a, b, 1)

print(x)

"""

a = np.array([[0, 1], [1, 2]])
b = np.array([1, 2])
b = np.transpose(b)
c = np.array([3, 4])

def f(x, y, c):
    return (x + y)*c

vfunc = np.vectorize(f)

x = vfunc(a, b, c)

print(x)