import pandas as pd
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

run_results_dir = "results/run1"
run_results = "run_results.csv"
valid_results = "valid_results.csv"
players_data = "clean-data.csv"
run1 = "results/valid/run1_valid_results.csv"
run2 = "results/valid/run2_valid_results.csv"
run3 = "results/valid/run3_valid_results.csv"

def analyse_csvs_df(run_results_dir):
    list = os.listdir(run_results_dir)
    columns = ["Run","Fit","Gen","Cost","Num_Players","Team","BitString"]
    df_results = pd.DataFrame(columns=columns)
    for csv in list:
        name = str(csv)
        df = pd.read_csv(f"results/run1/{csv}")
        df_results = df_results.append(df, ignore_index=True)
    print(df_results.head())
    df_results.to_csv(f"run_results.csv", mode="w")


def drop_invalid_solutions(run_results):
    name = run_results[8:12]
    df = pd.read_csv(run_results)
    old_length = len(df)
    print(f"Initial Dataset is {old_length}")
    df = df[df.Cost <= 100]
    new_length = len(df)
    print(f"Dropping {old_length - new_length} results \n Valid dataset is {new_length}")
    df.to_csv(f"results/valid/{name}_valid_results.csv", mode='w')


def analyse_valid(valid_results):
    df = pd.read_csv(valid_results)
    players = pd.read_csv(players_data)
    max_row = df.loc[df['Fit'].idxmax()]
    best_team = max_row["Team"]
    print(best_team)
    bit_string = np.zeros(523)
    for i in range(523):
        if players.iloc[i]['Player'] in best_team:
            bit_string[i] = 1
    with open("best_team.txt", "wb") as f:
        pickle.dump(bit_string, f)


def most_popular_player(valid_results):
    df = pd.read_csv(valid_results)
    print(len(df))
    players = pd.read_csv(players_data)
    player_string = np.zeros(523)
    for index, row in df.iterrows():
        team = row["Team"]
        for i in range(523):
            if players.iloc[i]['Player'] in team:
                player_string[i] += 1
    print(player_string)
    most_popular_player = players.iloc[player_string.argmax()]["Player"]
    second_most_popular_player = players.iloc[np.where(player_string==50)]["Player"]
    print(most_popular_player)
    print(second_most_popular_player)

def create_boxplot(results_data):
    name = results_data[14:18]
    print(name)
    df = pd.read_csv(results_data)
    df.boxplot(column="Fit")
    plt.ylim(ymin=0, ymax=2100)
    plt.savefig(f'charts/{name}_boxplot.png')
    plt.clf()

analyse_valid(run1)
