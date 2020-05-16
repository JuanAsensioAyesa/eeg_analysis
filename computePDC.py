from getMatrix import getMatrix
import matplotlib.pyplot as plt
import numpy as np
import sys
import os


directory = sys.argv[1]
save_directory = sys.argv[2]
for filename in os.listdir(directory):
    if (filename.endswith(".edf")):
        (M, (Ar, Vr, PDC, Significant)) = getMatrix(
            "./data/closed/edf/S001R02.edf", PDC=True, Signi=True)
        filename = filename.split('.')[0] + ".txt"
        f = open(save_directory + "/" + filename, "w+")
        (n, m) = Significant.shape
        data = str(n)+'\n'
        for i in np.arange(n):
            for j in np.arange(m):
                data += str(Significant[i][j])+' '
            data += '\n'

        f.write(data)
        f.close()
    else:
        continue
