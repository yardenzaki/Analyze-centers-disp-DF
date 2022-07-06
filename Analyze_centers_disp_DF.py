## README:
"""
This Script takes a "centers_displ.csv" file i.e. - the center X,Y displacements of - 2 objects  and returns Pairplots, Histograms, Q-Q plots and Distributions comparison betqeen the
LoS of each center (simulation / test centers)
The output units (pixel / urad) can be controlled by "IFOV" parameter and "USE_ANGULAR" flag.

steps:
1. Duplicate "centers_displ.csv" -> one for test and one for simulation -> make sure you know which is which -> for each of the files, change columns titles to be "Center_0..." (i.e. not  "Center_1...")
2. "center_title" var is controlling the titles of the plots. change it if necessary.
3. Run the script and pick ".csv" files according to the screen prints instructions.
4. after each selection the script will plot the above mentioned plots.

Notes:
* The plots are not saved automatically
* there are 3 main functions that could be commented / uncommented:
    1. Pairplot - makes paiplots
    2. Histograms - makes hisograms , Q-Q plots
    3. compare_dist - plots 2 hisograms (test / simulation) to compare the dists.

** V01 - 06/07/22 What's new?
    1. Added: Correlation Heatmap and Distributions comparison plots
    2. Auto - Saving Figures

@Author: Yarden Zaki
@Date: 07/01/2022
@Version: 1.0
@Links: https://github.com/yardenzaki
@License: MIT
"""


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from scipy import stats
import tkinter as tk
from tkinter import filedialog




global USE_ANGULAR , IFOV
IFOV = 6.52
USE_ANGULAR = True

def make_delta_disp_df():
    cwd = os.getcwd()
    root = tk.Tk()
    root.withdraw()
    df_path = filedialog.askopenfilename()
    centers_df = pd.read_csv(df_path)
    print(centers_df.head(20))

    delta_disp_DF = pd.DataFrame()
    delta_disp_DF["Frame"] = centers_df.loc[1:, "Frame"].astype(int)
    # df['Column1'].shift(-1) - df['Column1']
    delta_disp_DF["Center_0_DX"] = centers_df.loc[0:, "Center_0_X"] - centers_df.loc[0:, "Center_0_X"].shift(1)
    delta_disp_DF["Center_0_DY"] = centers_df.loc[0:, "Center_0_Y"] - centers_df.loc[0:, "Center_0_Y"].shift(1)
    print(delta_disp_DF.head(5))



    if USE_ANGULAR:
        delta_disp_DF["Center_0_DX"] = IFOV * delta_disp_DF["Center_0_DX"]
        delta_disp_DF["Center_0_DY"] = IFOV * delta_disp_DF["Center_0_DY"]
        # delta_disp_DF["LoS error (RSS)"] = (delta_disp_DF["Center_0_DX"] **2 + delta_disp_DF["Center_0_DY"] **2)**0.5

    # Switching "Center_i" notation to Test / Simulation
    delta_disp_DF = delta_disp_DF.rename(columns=renaming_fun)
    return delta_disp_DF


def renaming_fun(x):
    #print("x",x)
    if "Center_0" in x:
        print(x.split("_")[2])
        return  x.split("_")[2]
    else:
        return x

def compare_dist(delta_disp_DF_Simulation,delta_disp_DF_Test):

    plt.figure()
    mean =delta_disp_DF_Simulation["DX"].mean()
    std = delta_disp_DF_Simulation["DX"].std()
    RMS = (mean**2 + std**2)**(0.5)
    RMS = round(RMS, 2)
    ax_hist_x = sns.distplot(delta_disp_DF_Simulation["DX"], fit=norm , label="Simulation RMS=" + str(RMS))
    mean =delta_disp_DF_Test["DX"].mean()
    std = delta_disp_DF_Test["DX"].std()
    RMS = (mean**2 + std**2)**(0.5)
    RMS = round(RMS, 2)
    ax_hist_x = sns.distplot(delta_disp_DF_Test["DX"], fit=norm,label="Test RMS=" + str(RMS) )

    if USE_ANGULAR:
        title = "DX (urad) Distrib. Comparison"
    else:
        title = "DX (pixels) Distrib. Comparison"

    plt.title(title)
    x_lim = ax_hist_x.get_xlim()
    y_lim = ax_hist_x.get_ylim()
    plt.legend()
    plt.grid()
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')

    plt.figure()
    mean =delta_disp_DF_Simulation["DY"].mean()
    std = delta_disp_DF_Simulation["DY"].std()
    RMS = (mean**2 + std**2)**(0.5)
    RMS = round(RMS, 2)
    ax_hist_y = sns.distplot(delta_disp_DF_Simulation["DY"], fit=norm,label="Simulation RMS= " + str(RMS))
    mean =delta_disp_DF_Test["DY"].mean()
    std = delta_disp_DF_Test["DY"].std()
    RMS = (mean**2 + std**2)**(0.5)
    RMS = round(RMS, 2)
    ax_hist_y = sns.distplot(delta_disp_DF_Test["DY"], fit=norm,label="Test RMS= "+ str(RMS))
    if USE_ANGULAR:
        title = "DY (urad) Distrib. Comparison"
    else:
        title = "DY (pixels) Distrib. Comparison"

    plt.title(title)
    x_lim = ax_hist_y.get_xlim()
    y_lim = ax_hist_y.get_ylim()
    plt.legend()
    plt.grid()
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')
    return

def Corr_Heatmaps(center_title,df):
    """

    :param center_title:
    :param df:
    :return: the corr. matrix between DX and DY in df
    """
    corr = np.corrcoef(list(df['DX']), list(df['DY']))
    print("CORR",corr)

    plt.figure(figsize=(6, 6))
    heatmap = sns.heatmap(df.corr(), vmin=-1, vmax=1, annot=True, cmap='BrBG')
    title = 'Correlation Heatmap - ' + center_title
    heatmap.set_title(title , fontdict={'fontsize': 18}, pad=12);
    # save heatmap as .png file
    # dpi - sets the resolution of the saved image in dots/inches
    # bbox_inches - when set to 'tight' - does not allow the labels to be cropped
    plt.savefig( title+'.png', dpi=300, bbox_inches='tight')


    return

def Pairplot(center_title,df):
    delta_disp_DF_Simulation = df
    # scatterplot
    sns.set()
    cols = ['Frame', "DX", "DY"]
    g = sns.pairplot(delta_disp_DF_Simulation[cols], height=2.5, corner=True)
    title = " PairPlot - " + center_title
    plt.suptitle(title)
    g.map_lower(sns.kdeplot, levels=4, color=".2")
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')


def Histograms(center_title,df):
    delta_disp_DF_Simulation = df


    ################################## Histograms:
    '''
    Histogram - Kurtosis and skewness.
    Normal probability plot - Data distribution should closely follow the diagonal that represents the normal distribution.
    '''
    fig = plt.figure()
    for_hist_x = delta_disp_DF_Simulation[["DX"]].copy()
    print(for_hist_x.describe())
    mean = round(delta_disp_DF_Simulation["DX"].mean(), 2)
    std = round(delta_disp_DF_Simulation["DX"].std(), 2)
    var = round(delta_disp_DF_Simulation["DX"].var(), 2)
    skew = round(delta_disp_DF_Simulation["DX"].skew(), 2)
    kurt = round(delta_disp_DF_Simulation["DX"].kurt(), 2)
    new_line = '\n'
    stats_str = f" Statistics: {new_line} mean: {mean} {new_line} std.: {std} {new_line} var.: {var} {new_line} skewness: {skew} {new_line} kurtosis: {kurt}  "
    ax_hist_x = sns.distplot(delta_disp_DF_Simulation["DX"], fit=norm)
    if USE_ANGULAR:
        title = "DX (urad) Histogram"
    else:
        title = "DX (pixels) Histogram"

    title = title + " - " + center_title

    plt.title(title)

    x_lim = ax_hist_x.get_xlim()
    y_lim = ax_hist_x.get_ylim()
    ax_hist_x.text(0.85 * x_lim[0], 0.7 * y_lim[1], stats_str, bbox=dict(facecolor='blue', alpha=0.1))
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')
    ###
    fig = plt.figure()
    res = stats.probplot(delta_disp_DF_Simulation["DX"], plot=plt)
    title = "Q-Q plot DX - " + center_title
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')

    ###
    for_hist_y = delta_disp_DF_Simulation[["DY"]].copy()
    print(for_hist_y.describe())
    ###

    ###
    fig = plt.figure()
    mean = round(delta_disp_DF_Simulation["DY"].mean(), 2)
    std = round(delta_disp_DF_Simulation["DY"].std(), 2)
    var = round(delta_disp_DF_Simulation["DY"].var(), 2)
    skew = round(delta_disp_DF_Simulation["DY"].skew(), 2)
    kurt = round(delta_disp_DF_Simulation["DY"].kurt(), 2)
    new_line = '\n'
    stats_str = f" Statistics: {new_line} mean: {mean} {new_line} std.: {std} {new_line} var.: {var} {new_line} skewness: {skew} {new_line} kurtosis: {kurt}  "
    ax_hist_y = sns.distplot(delta_disp_DF_Simulation["DY"], fit=norm)
    if USE_ANGULAR:
        title = "DY (urad) Histogram"
    else:
        title = "DY (pixels) Histogram"

    title = title + " - " + center_title
    plt.title(title)
    x_lim = ax_hist_y.get_xlim()
    y_lim = ax_hist_y.get_ylim()
    ax_hist_y.text(0.85 * x_lim[0], 0.7 * y_lim[1], stats_str, bbox=dict(facecolor='blue', alpha=0.1))
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')
    ###
    fig = plt.figure()
    res = stats.probplot(delta_disp_DF_Simulation["DY"], plot=plt)
    title = "Q-Q plot DY - " + center_title
    plt.savefig(title + '.png', dpi=300, bbox_inches='tight')
    ###




############### SIMULATION Centers
center_title = "Simulation"  # "Test_" or "Simulation_"
print("Pick" , center_title , ".CSV - Dataframe")
delta_disp_DF_Simulation = make_delta_disp_df()
#print(delta_disp_DF_Simulation.head(20))

Corr_Heatmaps(center_title,delta_disp_DF_Simulation)
Pairplot(center_title,delta_disp_DF_Simulation)
Histograms(center_title,delta_disp_DF_Simulation)

plt.show()


############### TEST Centers
center_title = "Test"  # "Test_" or "Simulation_"
print("Pick" , center_title , ".CSV - Dataframe")
delta_disp_DF_Test = make_delta_disp_df()
#print(delta_disp_DF_Test.head(20))

Corr_Heatmaps(center_title,delta_disp_DF_Test)
Pairplot(center_title,delta_disp_DF_Test)
Histograms(center_title,delta_disp_DF_Test)

plt.show()


compare_dist(delta_disp_DF_Simulation,delta_disp_DF_Test)

plt.show()
