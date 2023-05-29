from source.utils.process import Process
"""
Creating random tests

"""


import random

processes = []

n = 7
burst = 10
priority = 5


def randNumber(num):
    return random.randint(1, num)


# To ensure that first process arrives at time 0
processes.append(Process(0, 0, randNumber(burst), randNumber(priority)))

for i in range(1, n):
    p = Process(i, randNumber(n), randNumber(burst), randNumber(priority))
    processes.append(p)

