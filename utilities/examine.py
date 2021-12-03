import pandas as pd
import numpy as np

# open up the csv with and prepare some lists

data = pd.read_csv("clean-data.csv").reset_index(drop=True)

num_players = len(data.index)
points = data['Points']
cost = data['Cost']

# Create empty arrays for each position thats as long as all of the players
GK = np.zeros(num_players)
MID = np.zeros(num_players)
DEF = np.zeros(num_players)
STR = np.zeros(num_players)

for i in range(num_players):
    if data['Position'][i] == 'GK':
        GK[i] = 1
    elif data['Position'][i] == 'DEF':
        DEF[i] = 1
    elif data['Position'][i] == 'MID':
        MID[i] = 1
    elif data['Position'][i] == 'STR':
        STR[i] =  1

GKs = data[GK == 1]
# print(masked_data.head())

print(f"The total number of players in the data is {num_players}")
print(f"The total number of goalkeepers in the data is {GK.sum()}")
print(f"The total number of defenders in the data is {DEF.sum()}")
print(f"The total number of midfielders in the data is {MID.sum()}")
print(f"The total number of strikers in the data is {STR.sum()}")

print(data.describe())
