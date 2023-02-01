import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from copy import deepcopy
import random
import process as p

"""
@section potential
This script provides assignment of distances from the exit to pedestrians' fields.
"""

"""!
Function assigns a value representing the pedestrian's distance from the exit to the field where the pedestrian is standing.

@param pedestrian  Dictionary of information about one pedestrian.
@param step  Coordinates of the next step field of the pedestrian.

@return Function returns a dictionary of new information about the pedestrian.
"""
def assign_value(pedestrian, step):
    if(step["dead_end"]):
        rewrite_map(pedestrian)
    current_value = pedestrian["map"][pedestrian["x"], pedestrian["y"]]
    if(current_value != 0):
        pedestrian["map"][step.x, step.y] = current_value - 1
    else:
        max_fields = (len(pedestrian["map"]))**2
        if(step["crossroad"] and pedestrian["map"][step.x, step.y] != 0):
            pedestrian["map"][step.x, step.y] = max_fields - 1
        else:
            pedestrian["map"][step.x, step.y] = max_fields - 1
    return pedestrian

"""!
Function overwrites the value representing the pedestrian's distance from the exit when the pedestrian is in a dead end.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns a dictionary of new information about the pedestrian.
"""
def rewrite_map(pedestrian):
    max_fields = (len(pedestrian["map"]))**2
    pedestrian["map"][pedestrian["x"], pedestrian["y"]] = max_fields
    crossroad = False
    pedestrian_copy = deepcopy(pedestrian)
    while(not crossroad):
        steps = p.avalible_steps(pedestrian_copy)
        if(pedestrian_copy["y"] < steps.y.max()):
            crossroad = True
        else:
            chosen_step = p.best_step(steps, pedestrian_copy)
            step_x = int(chosen_step.x)
            step_y = int(chosen_step.y)
            pedestrian["map"][step_x, step_y] = 0
            pedestrian_copy["map"][step_x, step_y] = max_fields
            pedestrian_copy["x"] = step_x
            pedestrian_copy["y"] = step_y
    return pedestrian

"""!
The function detects pedestrian collisions in the maze.

@param pedestrians  Array of dictionaries with information about pedestrains.

@return Function returns a lists of pedestrians id.
"""
def pedestrian_collision(pedestrians):
    id_1 = []
    id_2 = []
    for i in range(0, len(pedestrians)):
        for j in range(i, len(pedestrians)):
            if(not (pedestrians[i]["outside"] or pedestrians[j]["outside"])):
                vec_1 = np.array([pedestrians[i]["x"],pedestrians[i]["y"]])
                vec_2 = np.array([pedestrians[j]["x"],pedestrians[j]["y"]])
                if(np.linalg.norm(vec_1-vec_2) == 1):
                    id_1.append(i)
                    id_2.append(j)
    return id_1, id_2

"""!
Function synchronizes the maps of two pedestrians if they meet in the maze.
Function also synchronizes the distances from the exit in both maps.

@param pedestrian_1  Dictionary of information about one pedestrian.
@param pedestrian_2  Dictionary of information about one pedestrian.

@return Function returns a dictionaries of new information about the pedestrian.
"""
def synchronize_map(pedestrian_1, pedestrian_2):
    dim = len(pedestrian_1["map"])
    for i in range(0,dim):
        for j in range(0,dim):
            val_1 = pedestrian_1["map"][i,j]
            val_2 = pedestrian_2["map"][i,j]
            if(not (np.isnan(val_1) and np.isnan(val_2))):
                if(val_1 == 0 and val_2 != 0):
                    pedestrian_1["map"][i,j] = val_2
                elif(val_1 != 0 and val_2 == 0):
                    pedestrian_2["map"][i,j] = val_1
                else:
                    pedestrian_1["map"][i,j] = min(val_1,val_2)
                    pedestrian_2["map"][i,j] = min(val_1,val_2)
    current_1 = pedestrian_1["map"][pedestrian_1["x"],pedestrian_1["y"]]
    current_2 = pedestrian_2["map"][pedestrian_2["x"],pedestrian_2["y"]]
    if(current_1 > current_2):
        for i in range(pedestrian_1["x"],dim):
            pedestrian_2["map"][i,pedestrian_2["y"]] = 0
            pedestrian_1["map"][i,pedestrian_1["y"]] = 0
    else:
        for i in range(pedestrian_2["x"],dim):
            pedestrian_2["map"][i,pedestrian_2["y"]] = 0
            pedestrian_1["map"][i,pedestrian_1["y"]] = 0
    return pedestrian_1, pedestrian_2

