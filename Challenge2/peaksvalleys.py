#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Count peaks and valleys
"""

# Standart and thirdparty libraries
import sys
import numpy as np


def count_peaksvalleys(array):
    """
    Return count of peaks and valleys elements from a sequence of integers

    * An array element is peak if it is greater than its neighbors.
    * An array element is valley if it is smaller than its neighbors.
    * For corner elements, we need to consider only one neighbor.
    * Array elements must be between 0 and 500 (inclusive)
    * Sequence could be list, tuple or numpy array elements
    """
    # Convert to numpy array
    if not isinstance(array, (list, tuple, np.ndarray)):
        raise TypeError("Array is no a valid sequence")
    array = np.array(array)

    # Check size
    if not len(array) <= 500:
        raise ValueError("Array size out of limits")

    # Check type
    if not all(isinstance(e, np.integer) for e in array):
        raise TypeError("One or more elements of the array are not integers")

    # Special cases
    if len(array) <= 1:
        return (0, 0)

    # Comparative arrays
    smaller_right = array < np.roll(array, -1)
    smaller_left  = array < np.roll(array,  1)
    greater_right = array > np.roll(array, -1)
    greater_left  = array > np.roll(array,  1)

    # Get extremes values and calculate middle ones
    valleys_mask = np.concatenate(
        ([smaller_right[0]], smaller_right[1:-1] * smaller_left[1:-1], [smaller_left[-1]]))
    peaks_mask = np.concatenate(
        ([greater_right[0]], greater_right[1:-1] * greater_left[1:-1], [greater_left[-1]]))

    return sum(peaks_mask), sum(valleys_mask)


if __name__ == "__main__":
    array = next(sys.stdin)
    array = [int(a.strip("{ }\n")) for a in array.split(", ") if a]
    peaks, valleys = count_peaksvalleys(array)
    print(peaks, valleys)
