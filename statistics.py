import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import map as m
import process as p


def run_multiple_times(dim, ped_number, number_of_starts, save_iter = False):
    evacuation_time = []
    viewed_percent = pd.DataFrame({"t": [], "f": []})
    for i in range(number_of_starts):
        mapa, pedestrians = m.test_init(dim, ped_number)
        removed_pedestrians = []
        counter = 0
        while(not p.all_out(pedestrians)):
            for pedestrian in pedestrians:
                pedestrian["time"] = counter
            pedestrians, removed_pedestrians = p.make_step(pedestrians, removed_pedestrians)
            #disp.plot_map(pedestrians)
            #disp.plot_single_map(0)
            counter += 1
            if counter > pow(dim,2):
                counter = 0
                break
        evacuation_time.append(counter)
        for removed_pedestrian in removed_pedestrians:
            viewed_percent.loc[len(viewed_percent.index)] = map_viewed(removed_pedestrian)
    if save_iter == True:
        np.save("./ev_time", evacuation_time)
    return evacuation_time, viewed_percent

def map_viewed(removed_pedestrian):
    dim = len(removed_pedestrian["map"])
    unique, counts = np.unique(removed_pedestrian["map"], return_counts=True)
    values = dict(zip(unique, counts))
    not_viewed = values[0]
    viewed_percent = 1 - not_viewed/((dim-2)*((dim-1)/2) + (dim-1)/2)
    return viewed_percent*100, removed_pedestrian["time"]
    
def box(evacuation_time, savefigure = False, plotpath = "./plots/box.jpg"):
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

def scatter(viewed_percent, savefigure = False, plotpath = "./plots/scatter.jpg"):
    viewed_percent = viewed_percent[viewed_percent["f"] <= 100]
    viewed_percent.plot.scatter(x='t', y='f', c='DarkBlue', xlabel='Čas', ylabel='Procent odkryté mapy')
    if savefigure:
        plt.savefig(plotpath)

def heatmap(X, savefigure = False, plotpath = "./plots/heatmap.jpg"):
    X = pd.DataFrame(X)
    df = pd.DataFrame(columns=range(0,200,25))
    b = range(0,225,25)
    for i in X.columns:
        h = np.histogram(X[i], bins=b)
        df.loc[len(df.index)] = h[0]
    fig = px.density_heatmap(df, x=df.index, y=df.columns, labels={
                     "index": "Počet chodců",
                     "value": "Evakuační čas"})
    # fig.update_xaxes(range=[1,3])
    # fig.update_yaxes(range=[0,len(b)-1])
    if savefigure:
        fig.write_image(plotpath)
    fig.show()

def generate_dataset(dim, number_of_starts, groups_of_peds):
    ET = np.zeros((number_of_starts, groups_of_peds))
    for i in range(1,groups_of_peds + 1):
        evacuation_time, viewed_percent = run_multiple_times(dim, i, number_of_starts)
        ET[:,i-1] = evacuation_time
    return ET, viewed_percent

ET, viewed_percent = generate_dataset(dim = 21, number_of_starts = 5, groups_of_peds = 3)
scatter(viewed_percent, True)
heatmap(ET, True)

