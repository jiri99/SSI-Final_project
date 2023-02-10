import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import map as m
import process as p
import kaleido


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
    if(not_viewed > 200):
        print(removed_pedestrian["map"])
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
    df = pd.DataFrame(columns=range(0,200,10))
    b = range(0,210,10)
    for i in X.columns:
        h = np.histogram(X[i], bins=b)
        df.loc[len(df.index)] = h[0]
    data = pd.DataFrame.to_numpy(df)
    
    fig = px.imshow(data, y=[1,2,3,4], x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], labels={
                     "y": "Počet chodců",
                     "x": "Evakuační čas [v desítkách iterací]"})
    fig.layout.height = 400
    fig.layout.width = 800
    # fig.update_xaxes(range=[min(df.index)+1,max(df.index)+1])
    # fig.update_yaxes(range=[min(df.columns),max(df.columns)])
    if savefigure:
        fig.write_image(plotpath)
    fig.show()

def generate_dataset(dim, number_of_starts, groups_of_peds):
    ET = np.zeros((number_of_starts, groups_of_peds))
    for i in range(1,groups_of_peds + 1):
        evacuation_time, viewed_percent = run_multiple_times(dim, i, number_of_starts)
        ET[:,i-1] = evacuation_time
    return ET, viewed_percent

ET, viewed_percent = generate_dataset(dim = 21, number_of_starts = 100, groups_of_peds = 3)
scatter(viewed_percent, True)

# ET = np.load("./ET.npy")
# heatmap(ET, True)

