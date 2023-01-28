import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from copy import deepcopy
import random


def assign_value(pedestrian, step):
    current_value = pedestrian["map"][pedestrian["x"], pedestrian["y"]]
    if(current_value != 0):
        pedestrian["map"][step.x, step.y] = current_value - 1
    else:
        max_fields = (len(pedestrian["map"]))**2
        pedestrian["map"][step.x, step.y] = max_fields - 1
    if(step["death_end"]):
        rewrite_map(pedestrian)
    return pedestrian

def rewrite_map(pedestrian):
    pedestrian["map"][pedestrian["x"], pedestrian["y"]] = (len(pedestrian["map"]))**2
    return pedestrian

def synchronize_map(pedestrian):
    ####################
    # Task 12
    ####################
    return pedestrian

