import unittest
import arraytojson
import numpy

class TestDynamicArrayToJson(unittest.TestCase):

    def test_dimension_scale(self):
        #10x10 matrix
        dimensions = 10
        result = arraytojson.numpyArrayToJson(10)
        self.assertTrue(len(result)==9)

if __name__ == '__main__':
    unittest.main()