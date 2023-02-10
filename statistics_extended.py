import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import map as m
import process as p
import display as disp
from potential import pedestrian_collision
from tqdm.notebook import tqdm

def run_single_time(dim, ped_number):
    mapa, pedestrians = m.test_init(dim, ped_number)
    removed_pedestrians = []
    interactions_single = []
    while(not p.all_out(pedestrians)):
        pedestrians, removed_pedestrians = p.make_step(pedestrians, removed_pedestrians, False)
        ped_id_1, ped_id_2 = pedestrian_collision(pedestrians)
        interactions_single.append(len(ped_id_1))
    return interactions_single

def run_multiple_times(dim, ped_number, number_of_starts):
    interactions_set = []
    for i in tqdm(range(number_of_starts)):
        mapa, pedestrians = m.test_init(dim, ped_number)
        interactions_single = []
        while(not p.all_out(pedestrians)):
            pedestrians = p.make_step(pedestrians, False)
            ped_id_1, ped_id_2 = pedestrian_collision(pedestrians)
            interactions_single.append(len(ped_id_1))
        if(len(interactions_single) == 0):
            interactions_set.append(0)
        else:
            interactions_set.append(mean(interactions_single))
    return interactions_set
    
def test_settings(dim_range, ped_number_range, number_of_starts, save_iter = False):
    interactions = np.zeros([len(dim_range), len(ped_number_range), number_of_starts])
    for i in range(0, len(dim_range)):
        for j in range(0, len(ped_number_range)):
            interactions[i,j,:] = run_multiple_times(dim_range[i], ped_number_range[j], number_of_starts)
    return interactions

def hist(evacuation_time, savefigure = False, plotpath = "./plots/hist.jpg"):
    plt.hist(evacuation_time, rwidth=0.8)
    plt.xlabel("Iterace")
    plt.ylabel("Četnost interakcí")
    if savefigure:
        plt.savefig(plotpath)
    plt.show()

def bar(interactions, dim_range, ped_number_range, savefigure = False, plotpath = "./plots/barplot.jpg"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    num_cols = interactions.shape[1]
    num_rows = interactions.shape[0]
    
    interaction = np.zeros([num_rows, num_cols])
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            interaction[i,j] = mean(interactions[i,j,:])
    
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
    
    ax.set_xticklabels([None,1,None,2,None,3])
    ax.set_yticklabels([None,11,13,17])
    
    ax.set_xlabel('Počet chodců')
    ax.set_ylabel('Rozměr bludiště')
    ax.set_zlabel('Průměrný počet interakcí')

    if savefigure:
        plt.savefig(plotpath)
    plt.show()
    
    
dim_range = range(11,17,2)  
ped_number_range = range(1,4,1)
number_of_starts = 100

interactions = test_settings(dim_range, ped_number_range, number_of_starts)

bar(interactions, dim_range, ped_number_range, "./plots/barplot.jpg")
bar(interactions, dim_range, ped_number_range, "./plots/barplot.pdf")

# interactions_single = run_single_time(21,3)
# hist(interactions_single)

