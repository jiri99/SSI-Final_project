# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 00:10:52 2023

@author: fucsi
"""
import map as mp
import init_position as ip


dim = 11
map = mp.generate_map(dim)


ped_number  = 3
def generate_pedestrian_maps(map, ped_number):
    
    pedestrians = list()
    for i in range(0, ped_number):
        x_ped, y_ped = ip.generate_init_position(map)
        map[x_ped, y_ped] = 1
        pedestrians.append({"map": map, "x": x_ped, "y": y_ped})
        
    return pedestrians

pedestrians = generate_pedestrian_maps(map, ped_number)
