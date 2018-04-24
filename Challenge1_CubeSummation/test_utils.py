#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Utils for test cubesummation
"""

# Standard libraries
from random import choice
# Thirdparty libraries
import numpy as np

def random_update_string(edgesize):
    """Return update operation string with random values x y z w
        UPDATE x y z w
    """
    x, y, z = np.random.randint(edgesize, size=3) + np.array([1, 1, 1])
    w = int(np.random.uniform(-10e9, 10e9))
    return f'UPDATE {x} {y} {z} {w}'

def random_query_string(edgesize):
    """Return query operation string with random values x1 y1 z1 x2 y2 z2
        QUERY x1 y1 z1 x2 y2 z2
    """
    x1, y1, z1 = np.random.randint(edgesize, size=3) + np.array([1, 1, 1])
    x2, y2, z2 = np.random.randint(edgesize, size=3) + np.array([1, 1, 1])
    return f'QUERY {x1} {y1} {z1} {x2} {y2} {z2}'

def random_input_string(testcase, first_edgesize=None, first_num_operations=None):
    RANDOM_OPERATIONS_STRING = (random_update_string, random_query_string)

    text = f"{testcase}"

    if first_edgesize is None and first_num_operations is None:
        operations = [choice(RANDOM_OPERATIONS_STRING)(first_edgesize) for _ in range(first_num_operations)]

        text += f"\n{first_edgesize} {first_num_operations}"
        text += f"\n" + "\n".join(operations)

        testcase -= 1

    for _ in range(testcase):
        edgesize = np.random.randint(100, size=1)[0] + 1
        num_operations = np.random.randint(100, size=1)[0] + 1
        operations = [choice(RANDOM_OPERATIONS_STRING)(edgesize) for _ in range(num_operations)]

        text += f"\n{edgesize} {num_operations}\n"
        text += f"\n" + "\n".join(operations)

    return text
