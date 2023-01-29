import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from map import valid_position
from copy import deepcopy
import random

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
    if(step["death_end"]):
        rewrite_map(pedestrian)
    current_value = pedestrian["map"][pedestrian["x"], pedestrian["y"]]
    if(current_value != 0):
        pedestrian["map"][step.x, step.y] = current_value - 1
    else:
        max_fields = (len(pedestrian["map"]))**2
        pedestrian["map"][step.x, step.y] = max_fields - 1
    return pedestrian

"""!
Function overwrites the value representing the pedestrian's distance from the exit when the pedestrian is in a dead end.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns a dictionary of new information about the pedestrian.
"""
def rewrite_map(pedestrian):
    pedestrian["map"][pedestrian["x"], pedestrian["y"]] = (len(pedestrian["map"]))**2
    return pedestrian

"""!
Function synchronizes the maps of two pedestrians if they meet in the maze.
Function also synchronizes the distances from the exit in both maps.

@param pedestrian  Dictionary of information about one pedestrian.

@return Function returns a dictionary of new information about the pedestrian.
"""
def synchronize_map(pedestrian):
    ####################
    # Task 12
    ####################
    return pedestrian

