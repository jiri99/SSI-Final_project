import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from potential import assign_value, pedestrian_collision, synchronize_map
from copy import deepcopy
import random
pd.options.mode.chained_assignment = None

"""
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
    for i, j in zip([-1,0,1,0],[0,-1,0,1]):
        if((not np.isnan(pedestrian["map"][pedestrian["x"]+i, pedestrian["y"]+j])) and (j!=0 or i!=0)):
            steps.loc[len(steps.index)] = [pedestrian["x"]+i, pedestrian["y"]+j]
    return steps.astype({"x": int, "y": int})

"""!
Function selects the best of all possible steps for a single pedestrian.

@param steps  DataFrame of the coordinates of the possible destination fields of the pedestrian.
@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns the index of the selected best step of the pedestrian.
"""
def best_step(steps, pedestrian):
    values = []
    for index, row in steps.iterrows():
        values.append(pedestrian["map"][row.x, row.y])
    steps["value"] = values
    step = steps[steps.y == steps.y.max()]
    step = step[step.value == step.value.min()]
    if(len(step.index) == 0):
        print("send help")
    index = random.randint(0,len(step.index)-1)
    chosen_step = steps.iloc[step.index[index]]
    return chosen_step

"""!
Function finds the coordinates of the best step of the pedestrian.
Function also detects whether the pedestrian is in a dead end, at a crossroad or is walking along a corridor.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns the coordinates of the best step field and boolean values depending on whether the pedestrian is in a dead end or crossroad.
"""
def next_ped_step(pedestrian):
    steps = avalible_steps(pedestrian)
    chosen_step = best_step(steps, pedestrian)
    x = chosen_step.x
    y = chosen_step.y
    if(len(steps) == 1):
        in_dead_end = True
        crossroad = False
    elif(len(steps) > 2):
        in_dead_end = False
        crossroad = True
    else:
        in_dead_end = False
        crossroad = False
    return x, y, in_dead_end, crossroad

"""!
Function creates a DataFrame of all pedestrians' steps.

@param pedestrians  Array of dictionaries with information about pedestrains.

@return Function returns the coordinates of steps of all pedestrians 
and boolean values depending on whether the pedestrian is in a dead end or crossroad as a DataFrame
"""
def next_steps(pedestrians):
    all_steps = pd.DataFrame({"x": [], "y": [], "dead_end": [], "crossroad": []})
    for pedestrian in pedestrians:
        if(not pedestrian_out(pedestrian)):
            all_steps.loc[len(all_steps.index)] = next_ped_step(pedestrian)
    return all_steps.astype({"x": int, "y": int, "dead_end": bool, "crossroad": bool})

"""!
Function detects whether more pedestrians want to enter the same field.

@param all_steps  DataFrame of the coordinates of the possible destination fields of all pedestrians
and information about whether pedestrians are in a dead end or crossroad.

@return Function returns a boolean value depending on whether the function found the same next step field for more pedestrians.
"""
def find_conflicts(all_steps):
    conflicts = all_steps.loc[all_steps.duplicated(keep = False)].astype({"x": int, "y": int, "dead_end": bool, "crossroad": bool})
    return conflicts

"""!
Function selects one of the pedestrians who want to enter the same field.
Function then keeps that pedestrian's step the same and leaves the rest of these pedestrians standing.

@param pedestrians  Array of dictionaries with information about pedestrains.
@param all_steps  DataFrame of the coordinates of the possible destination fields of all pedestrians
and information about whether pedestrians are in a dead end or crossroad.

@return Function returns a modified DataFrame of the coordinates of the possible destination fields of all pedestrians.
"""
def solve_conflicts(pedestrians, all_steps):
    duplicated_rows = find_conflicts(all_steps)
    while(len(duplicated_rows) > 0):
        duplicated = all_steps[(all_steps.x == duplicated_rows.iloc[0]["x"]) & (all_steps.y == duplicated_rows.iloc[0]["y"])]
        chosen_ped_index = random.randint(0,len(duplicated)-1)
        index_left = duplicated.index[chosen_ped_index]
        for index, rows in duplicated.iterrows():
            if(index != index_left):
                all_steps.x[index] = pedestrians[index]["x"]
                all_steps.y[index] = pedestrians[index]["y"]
        duplicated_rows = find_conflicts(all_steps)
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
        pedestrians[index] = assign_value(pedestrians[index], row)
        pedestrians[index]["x"] = row.x
        pedestrians[index]["y"] = row.y
    for index in range(0,len(pedestrians)):
        if(pedestrian_out(pedestrians[index])):
            pedestrians.pop(index)
            break
    ped_id_1, ped_id_2 = pedestrian_collision(pedestrians)
    if(len(ped_id_1) != 0 and len(ped_id_2) != 0):
        for i in range(0,len(ped_id_1)):
            pedestrians[ped_id_1[i]], pedestrians[ped_id_2[i]] = synchronize_map(pedestrians[ped_id_1[i]], pedestrians[ped_id_2[i]])
    return pedestrians
