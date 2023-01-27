import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from potential import *
from copy import deepcopy
import random


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
            if((not np.isnan(pedestrian["map"][int(pedestrian["x"]+i), int(pedestrian["y"]+j)])) and (j!=0 or i!=0)):
                steps.loc[len(steps.index)] = [int(pedestrian["x"]+i), int(pedestrian["y"]+j)]
    return steps

def best_step(steps, pedestrian):
    values = []
    for index, row in steps.iterrows():
        values.append(pedestrian["map"][int(row.x), int(row.y)])
    steps["values"] = values
    step = steps[steps.values == steps.values.min()]
    index = random.randint(0,len(step.index)-1)
    chosen_step = steps.iloc[index]
    return chosen_step

def next_ped_step(pedestrian):
    steps = avalible_steps(pedestrian)
    chosen_step = best_step(steps, pedestrian)
    x = chosen_step.x
    y = chosen_step.y
    return x, y 

def find_conflicts(all_steps):
    conflict = False

    if all_steps.duplicated() == True:
        conflict = True
    return conflict

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
    
def next_steps(pedestrians):
    all_steps = pd.DataFrame({"x": [], "y": []})
    for pedestrian in pedestrians:
        if(not pedestrian_out(pedestrian)):
            all_steps.loc[len(all_steps.index)] = next_ped_step(pedestrian)
        else:
            pedestrian["outside"] = True
    return all_steps

def make_step(pedestrians):
    all_steps = next_steps(pedestrians)
    final_steps = solve_conflicts(pedestrians, all_steps)
    for index, row in final_steps.iterrows():
        pedestrians[index]["x"] = row.x
        pedestrians[index]["y"] = row.y
    return pedestrians
