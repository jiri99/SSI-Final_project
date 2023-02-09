import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import map as m
import process as p
import display as disp

def run_multiple_times(dim, ped_number, number_of_starts, save_iter = False):
    evacuation_time = []
    for i in range(number_of_starts):
        mapa, pedestrians = m.test_init(dim, ped_number)
        removed_pedestrians = []
        counter = 0
        while(not p.all_out(pedestrians)):
            pedestrians, removed_pedestrians = p.make_step(pedestrians, removed_pedestrians)
            #disp.plot_map(pedestrians)
            #disp.plot_single_map(0)
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


def heatmap(X):
    X = pd.DataFrame(X)
    df = px.data.tips(X)
    fig = px.density_heatmap(df, x="evakuační čas", y="počet chodců")
    fig.show()

def generate_dataset(dim, number_of_starts, groups_of_peds):
    ET = np.zeros((number_of_starts, groups_of_peds))
    for i in range(1,groups_of_peds + 1):
        evacuation_time = run_multiple_times(dim, i, number_of_starts)
        ET[:,i] = evacuation_time
    return ET

ET = generate_dataset(dim = 21, number_of_starts = 200, groups_of_peds = 5)
heatmap(ET)


#box(evacuation_time)
#hist(evacuation_time)
