import unittest
import arraytojson
import numpy

class TestDynamicArrayToJson(unittest.TestCase):

    def dimension_scale(self):
        arraytojson.scaleNumpy()
        self.assertTrue('')

if __name__ == '__main__':
    unittest.main()