import matplotlib.pyplot as plt
import numpy as np
import map as m
import process as p
import display as disp

def run_multiple_times(dim, ped_number, number_of_starts, save_iter = False):
    evacuation_time = []
    for i in range(number_of_starts):
        mapa, pedestrians = m.test_init(dim, ped_number)
        counter = 0
        while(not p.all_out(pedestrians)):
            pedestrians = p.make_step(pedestrians)
            disp.plot_map(pedestrians)
            counter += 1
            if counter > pow(dim,2):
                counter = 0
                break
        evacuation_time.append(counter)
    if save_iter == True:
        np.save("./ev_time", evacuation_time)
    return evacuation_time
    
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
    
    
evacuation_time = run_multiple_times(dim = 21, ped_number = 3, number_of_starts = 5)
box(evacuation_time)
hist(evacuation_time)
