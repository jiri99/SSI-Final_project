# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:05:52 2023

@author: Jiří
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

dim = 20
ped_number  = 3

def generate_map(dim):
  map = np.zeros([dim, dim])
  ####################
  # Task 1
  ####################
  return map

def valid_position(map, x, y):
  return not map[x,y]

def generate_init_positions(map):
  ####################
  # Task 2
  ####################
  return map

def generate_pedestrian_map(map, ped_number):
  pedestrians = list()
  for i in range(0, ped_number):
    map_init = generate_init_positions(map)
    pedestrians.append({"map": map_init})
  return pedestrians

map = generate_map(dim)
pedestrians = generate_pedestrian_map(map, ped_number)
