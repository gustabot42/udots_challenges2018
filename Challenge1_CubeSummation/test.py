#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Test for Cube Summation
"""

# Standard libraries
import io
import unittest
# Thirdparty libraries
import numpy as np

# Local libraries
from test_utils import random_input_string
from cube import Cube
from _parser import execute

class TestCubeSummation(unittest.TestCase):
    """
    Test for Cube Summation
    """

    def setUp(self):
        self.edgsize = 8
        self.cube = Cube(self.edgsize)

    def test_update(self):
        x, y ,z = np.random.randint(self.edgsize+1, size=3)
        w = int(np.random.uniform(-10e9, 10e9))
        self.cube.update(x, y ,z, w)

        self.assertEqual(self.cube[x, y, z], w)

    def test_update_value_invalid(self):
        x, y ,z = np.random.randint(self.edgsize+1, size=3)
        w = int(np.random.uniform(10e9, 20e9))

        with self.assertRaises(ValueError):
            self.cube.update(x, y ,z, w)

    def test_update_index_invalid(self):
        x, y ,z = np.random.randint(self.edgsize+1, self.edgsize+10, size=3)
        w = int(np.random.uniform(10e9, 20e9))

        with self.assertRaises(ValueError):
            self.cube.update(x, y ,z, w)

    def test_query(self):
        self.cube.update(1, 2, 2, 7)
        self.cube.update(3, 3, 3, 7)
        self.cube.update(4, 4, 4, 7)
        self.cube.update(6, 6, 8, 7)

        x1, y1, z1, x2, y2, z2 = 2, 2, 2, 6, 6, 6
        r = self.cube.query(x1, y1, z1, x2, y2, z2)
        self.assertEqual(r, 14)

    def test_input_values_invalid(self):
        text = random_input_string(51, 101, 10)
        _input = io.StringIO(text)
        with self.assertRaises(ValueError):
            execute(_input)

        text = random_input_string(2, 101, 10)
        _input = io.StringIO(text)
        with self.assertRaises(ValueError):
            execute(_input)

        text = random_input_string(2, 4, 1001)
        _input = io.StringIO(text)
        with self.assertRaises(ValueError):
            execute(_input)


    def test_input_valid(self):
        with open('test_data\output.txt') as output:
            results = output.readlines()
            results = [int(r) for r in results]

        with open('test_data\input.txt') as _input:
            self.assertEqual(results, execute(_input))

if __name__ == '__main__':
    unittest.main()
