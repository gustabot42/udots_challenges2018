#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cube model for Cube Summation
"""

# thirdparty libraries
import numpy as np


class Cube():
    """
    Cube data and methods
    """
    def __init__(self, edgesize):
        self.edgesize = edgesize
        self.cube = np.zeros((edgesize, edgesize, edgesize), dtype=np.int64)

    def __getitem__(self, key):
        x, y, z = key
        return self.cube[x-1, y-1, z-1]

    def update(self, x, y, z, w):
        """
        Update cube in position x, y, z with value w
        """
        if not -10e9 < w < 10e9:
            raise ValueError(f"W value out of range: '{w}'")

        self.cube[x-1, y-1, z-1] = w

    def query(self, x1, y1, z1, x2, y2, z2):
        """
        Query sub cube and return sum of all its elements
        """
        if not (x1 <= x2 and y1 <= y2 and z1 <= z2):
            raise ValueError(f"Invalid coordenates for query: '{x1}, {y1}, {z1}', '{x2}, {y2}, {z2}'")

        # Change index start
        x1, y1, z1 = x1-1, y1-1, z1-1
        x2, y2, z2 = x2-1, y2-1, z2-1

        subcube = self.cube[x1:x2+1, y1:y2+1, z1:z2+1]

        return subcube.sum()
