import numpy as np

a = np.array([[[0, 1], [1, 2]], [[2, 3], [3, 4]]])
print(a)
print('---')
r = np.sum(a, axis=(1, 2))
print(r)