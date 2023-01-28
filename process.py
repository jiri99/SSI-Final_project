import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from potential import *
from copy import deepcopy
import random

pd.options.mode.chained_assignment = None

def pedestrian_out(pedestrian):
    outside = False
    dim = len(pedestrian["map"])
    if((pedestrian["x"] == 0) or (pedestrian["y"] == 0) or (pedestrian["x"] == dim-1) or (pedestrian["y"] == dim-1)):
        outside = True
    return outside

def all_out(pedestrians):
    outside = True
    for pedestrian in pedestrians:
        if(pedestrian_out(pedestrian) == False):
            outside = False
    return outside

def avalible_steps(pedestrian):
    steps = pd.DataFrame({"x": [], "y": []})
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if((not np.isnan(pedestrian["map"][pedestrian["x"]+i, pedestrian["y"]+j])) and (j!=0 or i!=0)):
                steps.loc[len(steps.index)] = [pedestrian["x"]+i, pedestrian["y"]+j]
    return steps.astype({"x": int, "y": int})

def best_step(steps, pedestrian):
    values = []
    for index, row in steps.iterrows():
        values.append(pedestrian["map"][row.x, row.y])
    steps["value"] = values
    step = steps[steps.value == steps.value.min()]
    index = random.randint(0,len(step.index)-1)
    chosen_step = steps.iloc[step.index[index]]
    return chosen_step

def next_ped_step(pedestrian):
    steps = avalible_steps(pedestrian)
    chosen_step = best_step(steps, pedestrian)
    x = chosen_step.x
    y = chosen_step.y
    if(len(steps) == 1):
        in_death_end = True
        crossroad = False
    elif(len(steps) > 2):
        in_death_end = False
        crossroad = True
    else:
        in_death_end = False
        crossroad = False
    return x, y, in_death_end, crossroad

def next_steps(pedestrians):
    all_steps = pd.DataFrame({"x": [], "y": [], "death_end": [], "crossroad": []})
    for pedestrian in pedestrians:
        if(not pedestrian_out(pedestrian)):
            all_steps.loc[len(all_steps.index)] = next_ped_step(pedestrian)
        else:
            pedestrian["outside"] = True
    return all_steps.astype({"x": int, "y": int, "death_end": bool, "crossroad": bool})

def find_conflicts(all_steps):
    conflicts = all_steps.loc[all_steps.duplicated(keep = False)].astype({"x": int, "y": int, "death_end": bool, "crossroad": bool})
    return conflicts

def solve_conflicts(pedestrians, all_steps):
    duplicated_rows = find_conflicts(all_steps)
    while(len(duplicated_rows) > 0):
        duplicated = all_steps[(all_steps.x == duplicated_rows.iloc[0]["x"]) & (all_steps.y == duplicated_rows.iloc[0]["y"])]
        chosen_ped_index = random.randint(0,len(duplicated)-1)
        index_left = duplicated.index[chosen_ped_index]
        for index, rows in duplicated.iterrows():
            if(index != index_left):
                all_steps.iloc[index].x = pedestrians[index]["x"]
                all_steps.iloc[index].y = pedestrians[index]["y"]
        duplicated_rows = find_conflicts(all_steps)
    return all_steps    

def make_step(pedestrians):
    all_steps = next_steps(pedestrians)
    final_steps = solve_conflicts(pedestrians, all_steps)    
    for index, row in final_steps.iterrows():
        pedestrians[index] = assign_value(pedestrians[index], row)
        pedestrians[index]["x"] = row.x
        pedestrians[index]["y"] = row.y
    return pedestrians
