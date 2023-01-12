# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 22:52:13 2023

@author: fucsi
"""
import map as mp
import random


dim = 11
map = mp.generate_map(dim)

def generate_init_position(map):
    x = 0 
    y = 0
    
    while map[x,y] != 0: 
        x = random.randint(0,dim-1)
        y = random.randint(0,dim-1)  
    return x, y

x, y = generate_init_position(map)