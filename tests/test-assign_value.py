import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import sys, os
# change script path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import map as m
import process as p
import display as disp


dim = 11
ped_number  = 1

map, pedestrians = m.test_init(dim, ped_number)
removed_pedestrians = []

while(not p.all_out(pedestrians)):
    pedestrians = p.make_step(pedestrians, removed_pedestrians)
    disp.plot_single_map(pedestrians[0], True)
    
