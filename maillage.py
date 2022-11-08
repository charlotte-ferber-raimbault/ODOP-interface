# Copyright (C) 2022 Mines Paris (PSL Research University). All rights reserved.

import numpy as np

def maillage(N: int):
    """
    Defines points where pictures are taken in order to be fairly distributed on the half-sphere
    :param N: number of points
    :return: numpy array with the angles of the points, [angle of the belt, angle of the pivot]
    """
    layer_nb = int(np.sqrt(N)) # Number of layers in the hemisphere
    A = np.arange(0, 90+90/(layer_nb - 1), 90/(layer_nb - 1)) # Angle theta of each layer
    B = np.sin(A*np.pi/180) # The number of pictures on each layer depends on the sinus of the layer's angle
    C = ((N-1)/np.sum(B))*B # Scaling factor to have the right number of pictures at the end
    D = np.round(C).astype(int) # The number of picture on a layer is an integer
    frac = D - C # Fractionnary part, useful for correcting rouding mistakes
    
    # Correcting the total number of pictures after rounding errors
    
    if np.sum(D) + 1 != N : # The calculations above affect 0 to the layer theta=0 whereas 1 picture will be taken
        diff = np.sum(D) + 1 - N
        
        if diff > 0:
            while diff > 0:
                a = np.argmax(frac)
                D[a] = D[a] - 1
                frac[a] = 0
                diff -= 1
        else:
            while diff < 0:
                a = np.argmin(frac)
                D[a] = D[a] + 1
                frac[a] = 0
                diff += 1
                
    res = [[0, 0]] # A picture will necessarily be taken at the top of the hemisphere
    for layer in range(1, layer_nb):
        theta = layer*(90/(layer_nb - 1))
        for phi in np.linspace(0, 360, D[layer], endpoint=False):
            res.append([theta, phi])
        
    return np.array(res)
