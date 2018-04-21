#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cube Summation
(Link)[https://www.hackerrank.com/challenges/cube-summation/problem]
"""

# Standart and thirdparty libraries
import sys
import numpy as np

# Local libraries
from _parser import parser

class Cube():
    """
    Cube data and methods
    """
    def __init__(self, edgesize):
        self.edgesize = edgesize
        self.cube = np.zeros((edgesize, edgesize, edgesize), dtype=np.int64)

    def update(self, x, y, z, w):
        """
        Update cube in position x, y, z with value w
        """
        if not -10e9 < w < 10e9:
            raise ValueError(f"W value out of range: '{w}'")

        # Change index start
        x, y, z = x-1, y-1, z-1
        self.cube[x, y, z] = w

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


def execute(text):
    testcases = parser(text)
    answers = []
    for edgesize, operations in testcases:
        cube = Cube(edgesize)
        for function, args in operations:
            answer = getattr(cube, function)(*args)
            if answer is not None:
                answers.append(answer)

    return answers


if __name__ == "__main__":
    answers = execute(sys.stdin)
    for answer in answers:
        print(answer)
