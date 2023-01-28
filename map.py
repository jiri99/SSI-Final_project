import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from copy import deepcopy

"""
@section test_generator
This script provides all the variables needed to run the test
"""


"""!
Function generates a maze map with walls as NaN values.

@param dim  Size of the square map.

@return  Function returns a map of the maze as numpy matrix.
"""
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

"""!
Function evaluates whether there is a wall on the specified field or not.

@param map  Maze map.
@param x  Vertical field index in the maze map.
@param y  Horizontal field index in the maze map.

@return  Function returns a bool value depending on whether there is a wall on the field.
"""
def valid_position(map, x, y):
    return not np.isnan(map[x,y])

"""!
Function generates starting position of pedestrian. 
Function also checks that it does not generate the same position for any two pedestrians.

@param map  Maze map.

@return  Function returns a horizontal and vertical index of map matrix.
"""
def generate_init_position(map):
    dim = len(map)
    x = 0 
    y = 0
    while map[x,y] != 0: 
        x = random.randint(0,dim-1)
        y = random.randint(0,dim-1)
    return x, y

"""!
Function generates starting position and individual map of the maze for each pedestrian.

@param map  Maze map.
@param ped_number  Number of pedestrians.

@return  Function returns a array of dictionaries with informations about pedestrains.
"""
def generate_pedestrian_maps(map, ped_number):
    pedestrians = list()
    map_copy = deepcopy(map)
    for i in range(0, ped_number):
        x_ped, y_ped = generate_init_position(map_copy)
        map_copy[x_ped, y_ped] = 1
        pedestrians.append({"map": deepcopy(map), "x": x_ped, "y": y_ped, "outside": False})
        pedestrians[i][x_ped, y_ped] = 1
    return pedestrians

"""!
Function generates all necessary variables to run the test.

@param dim  Size of the square map.
@param ped_number  Number of pedestrians.

@return  Function returns a maze map and a pedestrian information array.
"""
def test_init(dim, ped_number):
    map = generate_map(dim)
    pedestrians = generate_pedestrian_maps(map, ped_number)
    return map, pedestrians
