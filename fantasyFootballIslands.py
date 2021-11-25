import array
import random
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from deap import algorithms
from deap import base
from deap import creator
from deap import tools


data = pd.read_csv("clean-data.csv").reset_index(drop=True)

NBR_PLAYERS = len(data.index)

# Create masks for each of the positions
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


creator.create("FitnessMax", base.Fitness, weights(1.0,))
creator.create("")
