#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Unittest for peaksvalleys
"""

from random import randint
import numpy as np
import unittest
from peaksvalleys import count_peaksvalleys


class TestPeaksValleys(unittest.TestCase):

    def test_length_valid(self):
        self.assertEqual(count_peaksvalleys([ ]), (0, 0))
        self.assertEqual(count_peaksvalleys([0]), (0, 0))
        self.assertEqual(count_peaksvalleys([0]*500), (0, 0))
        self.assertEqual(count_peaksvalleys([0]*250), (0, 0))

    def test_length_invalid(self):
        with self.assertRaises(TypeError):
            count_peaksvalleys(None)
            count_peaksvalleys([0]*501)

    def test_type_valid(self):
        array = np.random.randint(10, size=10)
        self.assertTrue(len(count_peaksvalleys(array)) == 2)

    def test_type_invalid(self):
        array = np.random.rand(10)
        with self.assertRaises(TypeError):
            count_peaksvalleys(array)

    def test_peaksvalleys_exist(self):
        self.assertEqual(count_peaksvalleys([10, 20, 15, 2, 23, 90, 67]), (2, 3))
        self.assertEqual(count_peaksvalleys([5, 10, 20, 15]), (1, 2))
        self.assertEqual(count_peaksvalleys([5, 4]), (1, 1))

    def test_peaksvalleys_notexist(self):
        i = np.random.randint(10, size=1)[0]
        self.assertEqual(count_peaksvalleys([i, i]), (0, 0))
        self.assertEqual(count_peaksvalleys([i]*10), (0, 0))

    def test_peaksvalleys_random(self):
        array = [0]*100
        i = np.random.randint(100, size=1)[0]
        array.insert(i, 1)
        self.assertEqual(count_peaksvalleys(array), (1, 0))

        array = [0]*100
        i = np.random.randint(100, size=1)[0]
        array.insert(i, -1)
        self.assertEqual(count_peaksvalleys(array), (0, 1))


if __name__ == '__main__':
    unittest.main()
