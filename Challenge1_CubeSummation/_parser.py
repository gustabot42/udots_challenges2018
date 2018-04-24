#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Operations parser for Cube Summation
"""

# Local libraries
from cube import Cube


def parser(_input):
    """
    Parse file like input and executes it

    Input format:
    The first line contains an integer T, the number of test-cases. T testcases follow.
    For each test case, the first line will contain two integers N and M separated by a single space.
    N defines the N * N * N matrix.
    M defines the number of operations.
    The next M lines will contain either

         1. UPDATE x y z W
         2. QUERY  x1 y1 z1 x2 y2 z2

    """
    OPERATIONS = ('update', 'query')

    # First line, number of test-cases
    line = next(_input)
    try:
        numtest = int(line)
    except ValueError:
        raise TypeError(f"Expected number of testcase as integer, but received '{line}'")

    if not 1 <= numtest <= 50:
        raise ValueError(f"Number of test-case out of limits: '{numtest}'")

    testcases = []
    for _ in range(numtest):
        # First line of test-case, N, M
        try:
            line = next(_input)
            edgesize, num_operations = [int(i) for i in line.split()]
        except ValueError:
            raise TypeError(f"Expected Edgesize and number operation as integers, but received '{line}'")

        if not 1 <= edgesize <= 100:
            raise ValueError(f"Edge size of cube out of limites: '{edgesize}'")

        if not 1 <= num_operations <= 100:
            raise ValueError(f"Number of operations out of limites: '{num_operations}'")

        # Get operations
        operations = []
        lines = [_input.readline() for _ in range(num_operations)]
        for line in lines:
            function, *args = line.split()
            function = function.lower()
            if function not in OPERATIONS:
                raise AttributeError(f"Function not valid: '{function}'")

            try:
                args = [int(a) for a in args]
            except ValueError:
                raise ValueError(f"Arguments as integer expected, but received '{args}'")

            operations.append((function, args))

        testcases.append((edgesize, operations))

    return testcases

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
