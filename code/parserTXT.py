import numpy as np
import sys
import os
import matplotlib.pyplot as plt
# returns an array with the signal data


def parseFile(filename):
    f = open(filename)
    signals = []
    for line in f:
        dic = {}
        label_name = line.split()[0]
        data = line.split()[1:]
        dic['label'] = label_name
        dic['data'] = data
        signals.append(dic)

    return signals


signals = parseFile("../data/closed/txt/S001R02.txt")
print(len(signals), len(signals[0]['data']))
# 64 channels x 9760 samples per channel
#   160 samples per second -> 1 minute of file
#   The data is measured in uV
