import unittest
import arraytojson
import numpy
import harperdb as hdb

class TestDynamicArrayToJson(unittest.TestCase):

    def test_ping(self):
        result = hdb.ping()
        self.assertTrue(result)

    def test_dimension_scale(self):
        #10x10 matrix
        dimensions = 10
        result = arraytojson.numpyArrayToJson(10)
        print(result)
        self.assertTrue(len(result)==9)

if __name__ == '__main__':
    unittest.main()