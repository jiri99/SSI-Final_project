import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from copy import deepcopy


def generate_map(dim):
    map = np.zeros([dim, dim])
    for i in range(0,dim):
        map[i,0] = np.nan
        map[0,i] = np.nan
        map[dim-1,i] = np.nan
        map[i,dim-1] = np.nan
    doors = random.sample(range(1, dim-2), math.ceil(dim/2))
    for i in range(2, dim, 2):
        for j in range(0,dim):
            if(not (doors[int(i/2)] == j)):
                map[j,i] = np.nan
            else:
                map[j,i] = 0
    return map

def valid_position(map, x, y):
    return not np.isnan(map[x,y])

def generate_init_position(map):
    dim = len(map)
    x = 0 
    y = 0
    while map[x,y] != 0: 
        x = random.randint(0,dim-1)
        y = random.randint(0,dim-1)
    return x, y

def generate_pedestrian_maps(map, ped_number):
    pedestrians = list()
    map_copy = deepcopy(map)
    for i in range(0, ped_number):
        x_ped, y_ped = generate_init_position(map_copy)
        map_copy[x_ped, y_ped] = 1
        pedestrians.append({"map": deepcopy(map), "x": x_ped, "y": y_ped, "outside": False})
        pedestrians[i]["map"][x_ped, y_ped] = 1
    return pedestrians

def test_init(dim, ped_number):
    map = generate_map(dim)
    pedestrians = generate_pedestrian_maps(map, ped_number)
    return map, pedestrians
