import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy


def plot_single_map(i, pedestrians, debugmode = False, savefigure = False, plotpath = "./plots/maze.jpg"):
    map = deepcopy(pedestrians[i]["map"])
    map[np.isnan(map)] = -1
    if debugmode == True:
        for m in range(len(map)):
            for n in range(len(map)):
                c = map[n,m]
                plt.text(m, n, int(c), va='center', ha='center')
    plt.imshow(map)
    plt.axis('off')
    plt.plot()
    if savefigure == True:
        plt.savefig(plotpath)

def plot_map(pedestrians, savefigure = False, plotpath = "./plots/maze.jpg"):
    map = deepcopy(pedestrians[0]["map"])
    map[map > 1] = 0
    map[np.isnan(map)] = -1
    for i in range(1, len(pedestrians)):
        map[int(pedestrians[i]["x"]), int(pedestrians[i]["y"])] = 1  
    plt.imshow(map)
    plt.axis('off')
    plt.show()
    if savefigure == True:
        plt.savefig(plotpath)

    
