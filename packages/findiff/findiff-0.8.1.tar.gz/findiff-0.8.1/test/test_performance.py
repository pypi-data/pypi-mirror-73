import sys
sys.path.insert(1, '..')

import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
from findiff.operators import FinDiff
import time


class TestPerformance(unittest.TestCase):

    def _test_findiff_vs_matrix(self):

        x, y = [np.linspace(0, 1, 200)]*2
        X, Y = np.meshgrid(x, y, indexing='ij')
        u = X**3 + Y**3

        d = FinDiff(0, x[1]-x[0], 2) + FinDiff(1, y[1]-y[0], 2)

        start = time.time()
        d(u)
        stop = time.time()

        start = time.time()
        dt_findiff = stop - start
        stop = time.time()

        dt_const = stop - start

        mat = d.matrix(u.shape)

        start = time.time()
        mat.dot(u.reshape(-1))
        stop = time.time()

        dt_matrix = stop - start

        print("FinDiff: ", dt_findiff)
        print("Matrix construction: ", dt_const)
        print("Matrix: ", dt_matrix)