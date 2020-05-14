import pyedflib
import numpy as np
import sys
import os

# argv[1] Directory of the edf file
# argv[2] Directory to save the txt files with the signals data


def get_info(filename):
    f = pyedflib.EdfReader(filename)
    headers = f.getSignalHeaders()
    duration = f.getFileDuration()
    sample_frequencies = f.getSampleFrequencies()
    for w in headers:
        print("Label "+w['label'], "Dimension Unit: " + w['dimension'], "Sample rate "+str(w['sample_rate']), "Physical max " + str(w['physical_max']),
              "Physical min "+str(w['physical_min']))


def get_signals(filename):

    f = pyedflib.EdfReader(filename)

    n = f.signals_in_file

    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)

    rows, columns = sigbufs.shape
    # label_name

    data = ''
    for i in np.arange(rows):
        data += signal_labels[i] + " "
        for j in np.arange(columns):
            data += str(sigbufs[i, j]) + " "
        data += '\n'
    return data


def read_all_edfs(directory, save_directory):
    for filename in os.listdir(directory):
        if (filename.endswith(".edf")):
            data = get_signals(directory+'/'+filename)
            filename = filename.split('.')[0] + ".txt"
            f = open(save_directory + "/" + filename, "w+")
            f.write(data)
            continue
        else:
            continue


read_all_edfs(sys.argv[1], sys.argv[2])
