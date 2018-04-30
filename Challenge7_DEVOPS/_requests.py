#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Test answers from DEVOPS server
"""


# thirdparty library
import numpy as np
import grequests

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

url = "http://yal.uis.edu.co/check/5000"
increment = 1000

num_requests   = []
mean_responses = []
std_responses  = []

nrequests = 0
while True:
    nrequests += increment
    
    rs = (grequests.get(url) for _ in range(nrequests))
    answers = grequests.map(rs)
    
    if not all(answers):
        print(f"Lost answers at {nrequests} requests")
        break
    
    elapseds = [a.elapsed.total_seconds() for a in answers]
    
    num_requests.append(nrequests)
    mean_responses.append(np.mean(elapseds)*1000)
    std_responses.append(np.std(elapseds)*1000)

    print(f"All good answers at {nrequests} requests")



plt.errorbar(num_requests, mean_responses, std_responses, linestyle='None', marker='o')
plt.savefig('stats.png')
