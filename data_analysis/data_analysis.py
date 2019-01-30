__author__ = 'colely'
import numpy as np
from numpy.linalg import *


lst1 = np.array([10, 20, 30, 40])
lst2 = np.array([4, 3, 2, 1])
print(np.dot(lst1.reshape([1, 4]), lst2.reshape([4, 1])))
print(np.concatenate((lst1, lst2), axis=0))
print(np.vstack((lst1, lst2)))
print(np.hstack((lst1, lst2)))
print(np.split(lst1, 4))