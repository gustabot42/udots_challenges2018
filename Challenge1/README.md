# Ubidots Challenge - 2018

## Challenge 1 - Cube Summation

You must solve this HackerRank challenge:
(link)[https://www.hackerrank.com/challenges/cube-summation]


### Explanation of solution

The solution was implemented with python3,
it define a 'Class' Cube for data and method encapsulation,
and a 'parser' for reading the input in the format proposed in HackerRank.


### Architecture and deployment

#### Install

The solution use python3 and the thirdparty library numpy, install dependencies:

´´´ bash
$ pip install numpy
´´´


#### Execution

the library 'cubesummation' expect a file like input with the format proposed in HackerRank,
for execution use like this:

´´´ bash
$ python3 cubesummation.py < test_data/input.txt
4
4
27
0
1
1
´´´


#### Test

To test the library Unittest was used, execute it like this:

´´´ bash
$ python3 test.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.129s

OK
´´´
