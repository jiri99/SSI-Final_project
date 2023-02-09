import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import sys, os
# change script path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import map as m
import process as p
import display as disp
from potential import pedestrian_collision

def run_multiple_times(dim, ped_number, number_of_starts):
    interaction = []
    for i in range(number_of_starts):
        mapa, pedestrians = m.test_init(dim, ped_number)
        interaction_counter = 0
        while(not p.all_out(pedestrians)):
            pedestrians = p.make_step(pedestrians, False)
            ped_id_1, ped_id_2 = pedestrian_collision(pedestrians)
            interaction_counter += len(ped_id_1)
        interaction.append(interaction_counter)
    return interaction
    
def test_settings(dim_range, ped_number_range, number_of_starts, save_iter = False):
    interactions = np.zeros([len(dim_range), len(ped_number_range)])
    for i in range(0, len(dim_range)):
        for j in range(0, len(ped_number_range)):
            interactions[i,j] = mean(run_multiple_times(dim_range[i], ped_number_range[j], number_of_starts))
    return interactions

def box(evacuation_time, savefigure = False, plotpath = "./plots/hist.jpg"):
    plt.boxplot(evacuation_time)
    plt.xlabel("evakuační čas")
    plt.ylabel("počet pozorování")
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

def hist(evacuation_time, savefigure = False, plotpath = "./plots/hist.jpg"):
    plt.hist(evacuation_time, rwidth=0.8)
    plt.xlabel("evakuační čas")
    plt.ylabel("počet pozorování")
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

def bar(interaction, savefigure = False, plotpath = "./plots/barplot.jpg"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    num_cols = interaction.shape[1]
    num_rows = interaction.shape[0]
     
    xpos = np.arange(0, num_cols, 1)
    ypos = np.arange(0, num_rows, 1)
    xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
     
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros(num_cols * num_rows)
     
    dx = np.ones(num_rows * num_cols) * 0.5
    dy = np.ones(num_cols * num_rows) * 0.5
    dz = interaction.flatten()
    
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
    
    ax.set_xlabel('Rozměr bludiště')
    ax.set_ylabel('Počet chodců')
    ax.set_zlabel('Počet interakcí')

    if savefigure:
        plt.savefig(plotpath)
    plt.show()
    
dim_range = range(11,18,2)  
ped_number_range = range(1,4,1)
number_of_starts = 5

interactions = test_settings(dim_range, ped_number_range, number_of_starts)
bar(interactions)
