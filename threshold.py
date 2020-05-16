import numpy as np 

def threshold(matrix,D):
    
    V = matrix.flatten()

    return np.percentile(V,[100-D])
   
    

    