import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


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

def plot_map(pedestrians, savefigure = False, plotpath = "./plots/maze.jpg"):
    map = deepcopy(pedestrians[0]["map"])
    map[map > 1] = 0
    map[np.isnan(map)] = -1
    for i in range(1, len(pedestrians)):
        map[int(pedestrians[i]["x"]), int(pedestrians[i]["y"])] = 1  
    plt.imshow(map)
    plt.axis('off')
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

    
