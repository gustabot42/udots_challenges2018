# Udots Challenge - 2018

## Challenge 2 - Count peaks and valleys

Given an array of integers with length N, count peak and valleys.
An array element is peak if it is NOT smaller than its neighbors.
An array element is valley if it is NOT greater than its neighbors.
For corner elements, we need to consider only one neighbor.

**Note**: This definition of peak and valley consider EQUAL comparison peak and valley,
this generates vicious cases like:

``` Python
assert count_peak_valeys([1,1,1,1]) == (4, 4)
```

In the function the definition was changed as:
An array element is peak if it is greater than its neighbors.
An array element is valley if it is smaller than its neighbors.


### Explanation of solution

The solution was implemented with python3,
it use the vector operations with numpy library find the answer.


### Architecture and deployment

#### Install

The solution use python3 and the thirdparty library numpy, install dependencies:

``` bash
$ pip install numpy
```


#### Execution

the library 'peaksvalleys' expect a CVS list input,
for execution use like this:

``` bash
$ python peaksvalleys.py
10, 20, 15, 2, 23, 90, 67
2 3
```


#### Test

For test the library Unittest was used, execute like this:

``` bash
$ python test.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.024s

OK
