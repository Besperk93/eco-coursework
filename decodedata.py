import pandas as pd
import numpy as np
import pickle

players_data = "clean-data.csv"
data = "bitstring_results_25-11-2021_14-54-52"

df = pd.read_csv(data, sep="w")
players = pd.read_csv(players_data)

print(df.head())

max = df['Fit'].max()

max_row = df.loc[df['Fit'].idxmax()]

best_team = max_row['Team']

print(best_team)

bit_string = np.zeros(523)

for i in range(523):
    if players.iloc[i]['Player'] in best_team:
        bit_string[i] = 1

with open("best_team.txt", 'wb') as f:
    pickle.dump(bit_string, f)
