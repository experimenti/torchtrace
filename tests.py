import unittest
import arraytojson
import numpy as np
import harperdb as hdb

class TestDynamicArrayToJson(unittest.TestCase):

    def test_ping(self):
        result = hdb.ping()
        self.assertTrue(result)

    def test_dimension_scale(self):
        #1000x100 matrix
        w1 = np.random.randn(1000, 100)
        result = arraytojson.jsonFromNumpyArray(w1)
       # self.assertTrue(len(result)==999)

    def test_enumerate_narray(self):
        w1 = np.random.randn(100, 100)
        for (k,v) in np.denumerate(w1):
            print('k: '.format(k))
            print('v: '.format(v))


if __name__ == '__main__':
    unittest.main()