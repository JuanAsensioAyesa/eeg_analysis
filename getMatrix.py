import pyedflib
import numpy as np
import os
import connectivipy as cp
import matplotlib.pyplot as plt
import threshold as th
import networkx as nx

# Calculate the adjacency matrix of the signals in filename
# using PDC.
# The density of the resulting graph would be equal to D%
# Analyzes the alpha waves
# If PDC = true it returns [matrix,(Ar,Vr,PDC-values)]
#   If Signi = True  it returns (Ar,Vr,PDC-values,Significant Values) (alpha = 0.05)
# If List != None it reads from the file the signals with the corresponding index on List


def getMatrix(filename, D=20, PDC=False, Signi=False, List=[]):

    range = np.arange(7, 12)
    #range = [9]
    f = pyedflib.EdfReader(filename)
    n = f.signals_in_file
    data_points = f.getNSamples()[0]

    signals = np.zeros((n, data_points))
    if(len(List) == 0):
        # Read the data of all signals

        for i in np.arange(n):
            signals[i, :] = f.readSignal(i)
    else:

        signals = np.zeros((len(List), data_points))
        for i in np.arange(len(List)):
            signals[i, :] = f.readSignal(List[i])

            # Create the class Data
    data = cp.data.Data(signals, 160)
    data.fit_mvar()
    Ar, Vr = data.mvar_coefficients
    # Calculate the pdc
    # TODO: Check resolution value
    pdc_values = cp.conn.pdc_fun(Ar, Vr, fs=160, resolution=80)

    # number of signals treated
    m = Ar.shape[1]
    sum = np.zeros((m, m))

    for i in range:
        sum = sum + pdc_values[i, :, :]

    np.fill_diagonal(sum, 0)
    sum = sum * 1/len(range)  # Calculates the mean

    # Get the threshold
    threshold = th.threshold(sum, D)

    M = np.zeros((m, m))
    # Apply the threshold to the matrix
    for i in np.arange(m):
        for j in np.arange(m):
            if(sum[i, j] >= threshold):
                M[i, j] = 1

    if (PDC):
        if(Signi):

            pdc_values = data.conn('pdc', resolution=80)

            pdc_significance = data.significance(Nrep=10, alpha=0.05)

            np.fill_diagonal(pdc_significance, 0)

            significant = np.zeros((m, m))

            for i in np.arange(m):
                for j in np.arange(m):
                    if(pdc_significance[i, j] < 0.05):
                        significant[i, j] = sum[i, j]
                    else:
                        M[i, j] = 0
            return M.transpose(), (Ar, Vr, sum, significant)
        else:
            return M.transpose(), (Ar, Vr, sum)
    else:

        return M.transpose()
