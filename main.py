import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

import map as m
import process as p

dim = 20
ped_number  = 3

map, pedestrians = m.test_init(dim, ped_number)

while(not p.all_out(pedestrians)):
    pedestrians = p.make_step(pedestrians)