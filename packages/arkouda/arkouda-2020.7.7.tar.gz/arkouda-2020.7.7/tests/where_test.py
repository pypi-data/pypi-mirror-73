import numpy as np
import warnings
from itertools import product
from context import arkouda as ak
from base_test import ArkoudaTest
warnings.simplefilter("always", UserWarning)
SIZE = 10

'''
Tests the Arkouda where functionality and compares results to the
analogous Numpy were results.
'''
class WhereTest(ArkoudaTest):

    def test_where_equivalence(self):
        npA = {'int64': np.random.randint(0, 10, SIZE),
               'float64': np.random.randn(SIZE),
               'bool': np.random.randint(0, 2, SIZE, dtype='bool')}
        akA = {k: ak.array(v) for k, v in npA.items()}
        npB = {'int64': np.random.randint(10, 20, SIZE),
               'float64': np.random.randn(SIZE)+10,
               'bool': np.random.randint(0, 2, SIZE, dtype='bool')}
        akB = {k: ak.array(v) for k, v in npB.items()}
        npCond = np.random.randint(0, 2, SIZE, dtype='bool')
        akCond = ak.array(npCond)
        scA = {'int64': 42, 'float64': 2.71828, 'bool': True}
        scB = {'int64': -1, 'float64': 3.14159, 'bool': False}
        dtypes = set(npA.keys())
        failures = 0
        tests = 0
        for dtype in dtypes:
            for (ak1, ak2), (np1, np2) in zip(product((akA, scA), (akB, scB)),
                                              product((npA, scA), (npB, scB))):
                tests += 1
                akres = ak.where(akCond, ak1[dtype], ak2[dtype]).to_ndarray()
                npres = np.where(npCond, np1[dtype], np2[dtype])
                if not np.allclose(akres, npres, equal_nan=True):
                    self.assertWarning(warnings.warn("{} !=\n{}".format(akres, npres)))
                    failures += 1
        self.assertEqual(0,failures)
