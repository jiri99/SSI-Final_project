import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

"""
@section display
This script provides a plot of map with pedestrians' positions.
"""

"""!
Function plots the map of a single pedestrian.

@param pedestrian  Dictionary of information about one pedestrian.
"""
def plot_single_map(pedestrian, debugmode = False, savefigure = False, plotpath = "./plots/maze.jpg"):
    map = deepcopy(pedestrian["map"])
    map[np.isnan(map)] = -1
    if debugmode:
        for m in range(len(map)):
            for n in range(len(map)):
                c = map[n,m]
                plt.text(m, n, int(c), va='center', ha='center')
    plt.imshow(map)
    plt.axis('off')
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

"""!
Function plots the map of all pedestrians.

@param pedestrians  Array of dictionaries with information about pedestrains.
"""
def plot_map(pedestrians, savefigure = False, plotpath = "./plots/maze.jpg"):
    if(len(pedestrians) == 0):
        return
    map = deepcopy(pedestrians[0]["map"])
    map[map > 1] = 0
    map[np.isnan(map)] = -1
    for i in range(0, len(pedestrians)):
        map[int(pedestrians[i]["x"]), int(pedestrians[i]["y"])] = 1  
    plt.imshow(map)
    plt.axis('off')
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

    
