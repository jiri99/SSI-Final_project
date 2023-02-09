import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

import map as m
import process as p
import display as disp


dim = 21
ped_number = 3

map, pedestrians = m.test_init(dim, ped_number)
removed_pedestrians = []

while(not p.all_out(pedestrians)):
    pedestrians, removed_pedestrians = p.make_step(pedestrians, removed_pedestrians)
    disp.plot_map(pedestrians)
    
