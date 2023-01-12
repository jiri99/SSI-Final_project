import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def generate_map(dim):
    map = np.zeros([dim, dim])
    ####################
    # Task 1
    ####################
    return map

def valid_position(map, x, y):
    return not np.isnan(map[x,y])

def generate_init_position(map):
    x, y = 0
    ####################
    # Task 2
    ####################
    return x, y

def generate_pedestrian_maps(map, ped_number):
    pedestrians = list()
    for i in range(0, ped_number):
        x_ped, y_ped = generate_init_position(map)
        ####################
        # Task 3
        ####################
        pedestrians.append({"map": map, "x": x_ped, "y": y_ped})
    return pedestrians

def test_init(dim, ped_number):
    map = generate_map(dim)
    pedestrians = generate_pedestrian_maps(map, ped_number)
    return map, pedestrians
