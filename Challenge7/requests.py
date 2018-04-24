#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Test answers from DEVOPS server
"""


# thirdparty library
import grequests


url = "http://yal.uis.edu.co/check/1000"
num_request = 5000

rs = (grequests.get(url) for _ in range(num_request))
answers = grequests.map(rs)

good_answers = 0
for answer in answers:
    if answer is not None:
        good_answers += 1

print(f"The server answered to ´{good_answers}´ requests of '{num_request}'")
