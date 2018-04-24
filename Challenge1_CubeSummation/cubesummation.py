#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cube Summation
(Link)[https://www.hackerrank.com/challenges/cube-summation/problem]
"""

# Standard libraries
import sys

# Local libraries
from _parser import execute


if __name__ == "__main__":
    answers = execute(sys.stdin)
    for answer in answers:
        print(answer)
