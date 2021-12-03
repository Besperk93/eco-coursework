import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

test_data_dir = "results/test1"
test_results_csv = "test_results.csv"

def analyse_csvs_json(data_loc):
    results = {}
    list = os.listdir(data_loc)
    for csv in list:
        name = str(csv)
        df = pd.read_csv(f"results/test1/{csv}")
        box_plot = df.boxplot(column='Fit')
        plt.savefig(f"charts/boxplot_{name}.png")
        avg = df['Fit'].mean()
        max = df['Fit'].max()
        results[name] = [avg, max]
    with open(f"test_results.json", "w") as f:
        json.dump(results, f)

def analyse_csvs_df(data_loc):
    list = os.listdir(data_loc)
    columns = ["Run","Fit","Gen","Cost","Num_Players","Team","BitString"]
    df_results = pd.DataFrame(columns=columns)
    for csv in list:
        name = str(csv)
        df = pd.read_csv(f"results/test1/{csv}")
        df['Config'] = name
        df_results = df_results.append(df, ignore_index=True)
    df_results.to_csv(f"test_results.csv", mode="w")

def create_comparison_plots(data_loc):
    df_results = pd.read_csv(data_loc)
    df_results = df_results[["Run","Fit","Gen","Cost","Num_Players","Team","BitString", "Config"]]
    df_results = df_results[~df_results.Config.str.match('.*random.*|.*shuffle.*|.*uniform.*')]
    empty = df_results[df_results.Config.str.match('.*empty.*')]
    empty.boxplot(column='Fit')
    plt.ylim(ymin=0, ymax=2000)
    plt.savefig('charts/empty_boxplot.png')
    plt.clf()
    onePicked = df_results[df_results.Config.str.match('.*onePicked.*')]
    onePicked.boxplot(column='Fit')
    plt.ylim(ymin=0, ymax=2000)
    plt.savefig('charts/onePicked_boxplot.png')
    plt.clf()
    onePoint = df_results[df_results.Config.str.match('.*onePoint.*')]
    onePoint.boxplot(column='Fit')
    plt.ylim(ymin=0, ymax=2000)
    plt.savefig('charts/onePoint_boxplot.png')
    plt.clf()
    twoPoint = df_results[df_results.Config.str.match('.*twoPoint.*')]
    twoPoint.boxplot(column='Fit')
    plt.ylim(ymin=0, ymax=2000)
    plt.savefig('charts/twoPoint_boxplot.png')
    plt.clf()
    twoPoint.to_csv('two_point_test.csv', mode='w')

create_comparison_plots(test_results_csv)
