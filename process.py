import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position


def pedestrian_out(pedestrian):
    outside = False
    dim = len(pedestrian["map"])
    if(pedestrian["x"] == 0 or pedestrian["y"] == 0 or pedestrian["x"] == dim or pedestrian["y"] == dim ):
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
            if(not np.isnan(pedestrian["map"][pedestrian["x"]+i,pedestrian["y"]+j]) and j!=0 and i!=0):
                steps.loc[len(steps.index)] = [int(pedestrian["x"]+i),int(pedestrian["y"]+j)]
    return steps

def best_step(steps, pedestrian):
    values = []
    for index, row in steps.iterrows():
        values.append(pedestrian["map"][row.x,row.y])
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

def rewrite_map(pedestrian):
    ####################
    # Task 9
    ####################
    return pedestrian

def find_conflicts(pedestrians, all_steps):
    conflict = False
    ####################
    # Task 7
    ####################
    return conflict

def solve_conflicts(pedestrians, all_steps):
    ####################
    # Task 7
    ####################
    return all_steps
    
def next_steps(pedestrians):
    all_steps = pd.DataFrame({"x": [], "y": []})
    for pedestrian in pedestrians:
        all_steps.loc[len(all_steps.index)] = next_ped_step(pedestrian)
    return all_steps

def make_step(pedestrians):
    ####################
    # Task 7
    ####################
    return pedestrians
