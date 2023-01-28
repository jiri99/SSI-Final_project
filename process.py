import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from potential import *
from copy import deepcopy
import random

"""!
@section process
This script provides finding the next steps of pedestrians, resolving conflicts and making these steps.
"""

"""!
Function evaluates whether the pedestrian is outside the maze.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns a boolean value depending on whether the pedestrian is outside the maze or not.
"""
def pedestrian_out(pedestrian):
    outside = False
    dim = len(pedestrian["map"])
    if((pedestrian["x"] == 0) or (pedestrian["y"] == 0) or (pedestrian["x"] == dim-1) or (pedestrian["y"] == dim-1)):
        outside = True
    return outside

"""!
Function evaluates whether all the pedestrians are out of the maze.

@param pedestrians  Array of dictionaries with information about pedestrains.

@return Function returns a boolean value depending on whether all the pedestrians are out of the maze.
"""
def all_out(pedestrians):
    outside = True
    for pedestrian in pedestrians:
        if(pedestrian_out(pedestrian) == False):
            outside = False
    return outside

"""!
Function finds all the possible steps for a single pedestrian.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns the coordinates of possible destination fields as a DataFrame.
"""
def avalible_steps(pedestrian):
    steps = pd.DataFrame({"x": [], "y": []})
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if((not np.isnan(pedestrian["map"][int(pedestrian["x"]+i), int(pedestrian["y"]+j)])) and (j!=0 or i!=0)):
                steps.loc[len(steps.index)] = [int(pedestrian["x"]+i), int(pedestrian["y"]+j)]
    return steps

"""!
Function selects the best of all possible steps for a single pedestrian.

@param steps  DataFrame of the coordinates of the possible destination fields of the pedestrian.
@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns the index of the selected best step of the pedestrian.
"""
def best_step(steps, pedestrian):
    values = []
    for index, row in steps.iterrows():
        values.append(pedestrian["map"][int(row.x), int(row.y)])
    steps["values"] = values
    step = steps[steps.values == steps.values.min()]
    index = random.randint(0,len(step.index)-1)
    chosen_step = steps.iloc[index]
    return chosen_step

"""!
Function finds the coordinates of the best step of the pedestrian.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns the coordinates of the best step field.
"""
def next_ped_step(pedestrian):
    steps = avalible_steps(pedestrian)
    chosen_step = best_step(steps, pedestrian)
    x = chosen_step.x
    y = chosen_step.y
    return x, y 

"""!
Function detects whether more pedestrians want to enter the same field.

@param all_steps  DataFrame of the coordinates of the possible destination fields of all pedestrians.

@return Function returns a boolean value depending on whether the function found the same next step field for more pedestrians.
"""
def find_conflicts(all_steps):
    conflict = False

    if all_steps.duplicated() == True:
        conflict = True
    return conflict

"""!
Function selects one of the pedestrians who want to enter the same field.
Function then keeps that pedestrian's step the same and leaves the rest of these pedestrians standing.

@param pedestrians  Array of dictionaries with information about pedestrains.
@param all_steps  DataFrame of the coordinates of the possible destination fields of all pedestrians.

@return Function returns a modified DataFrame of the coordinates of the possible destination fields of all pedestrians.
"""
def solve_conflicts(pedestrians, all_steps):
    duplicated_rows = all_steps[all_steps.duplicated(keep = False)]
    while(len(duplicated_rows) > 0):
        duplicated = all_steps[(all_steps.x == duplicated_rows.iloc[0]["x"]) & (all_steps.y == duplicated_rows.iloc[0]["y"])]
        chosen_ped_index = random.randint(0,len(duplicated)-1)
        index_left = duplicated.index[chosen_ped_index]
        for index, rows in duplicated.iterrows():
            if(index != index_left):
                all_steps.iloc[index].x = pedestrians[index]["x"]
                all_steps.iloc[index].y = pedestrians[index]["y"]
        duplicated_rows = all_steps[all_steps.duplicated(keep = False)]
    return all_steps

"""!
Function creates a DataFrame of all pedestrians' steps.

@param pedestrians  Array of dictionaries with information about pedestrains.

@return Function returns the steps of all pedestrians as a DataFrame
"""   
def next_steps(pedestrians):
    all_steps = pd.DataFrame({"x": [], "y": []})
    for pedestrian in pedestrians:
        if(not pedestrian_out(pedestrian)):
            all_steps.loc[len(all_steps.index)] = next_ped_step(pedestrian)
        else:
            pedestrian["outside"] = True
    return all_steps

"""!
Function moves the pedestrians to the new fields.

@param pedestrians  Array of dictionaries with information about pedestrains.

@return Function returns an array of dictionaries with new information about pedestrains.
"""
def make_step(pedestrians):
    all_steps = next_steps(pedestrians)
    final_steps = solve_conflicts(pedestrians, all_steps)
    for index, row in final_steps.iterrows():
        pedestrians[index]["x"] = row.x
        pedestrians[index]["y"] = row.y
    return pedestrians
