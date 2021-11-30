import pickle
import numpy as np
import pandas as pd

# check the constraints
# the function MUST be passed a list of length num_players in which each bit is set to 0 or 1

with open("best_team.txt", 'rb') as f:
    bit_string = pickle.load(f)

print(bit_string)

data = (pd.read_csv("clean-data.csv")
        .reset_index(drop=True))

num_players = len(data.index)

points = data['Points']
cost = data['Cost']

gk = np.zeros(num_players)
mid = np.zeros(num_players)
defe = np.zeros(num_players)
stri = np.zeros(num_players)

for i in range(num_players):
    if data['Position'][i] == 'GK':
        gk[i] = 1
    elif data['Position'][i] == 'DEF':
        defe[i] = 1
    elif data['Position'][i] == 'MID':
        mid[i] = 1
    elif data['Position'][i] == 'STR':
        stri[i]=1


def check_constraints(individual):

    broken_constraints = 0

    # exactly 11 players
    c1 = np.sum(individual)
    if  c1 != 11:
        broken_constraints+=1
        print("total players is %s " %(c1))


    #need cost <= 100"
    c2 = np.sum(np.multiply(cost, individual))
    if c2 > 100:
        broken_constraints+=1
        print("cost is %s " %(c2))

    # need only 1 GK
    c3 = np.sum(np.multiply(gk, individual))
    if  c3 != 1:
        broken_constraints+=1
        print("goalies is %s " %(c3))

    # need less than 3-5 DEF"
    c4 = np.sum(np.multiply(defe,individual))
    if  c4 > 5 or c4 < 3:
        broken_constraints+=1
        print("DEFE is %s " %(c4))

    #need 3- 5 MID
    c5 = np.sum(np.multiply(mid,individual))
    if  c5 > 5 or c5 < 3:
        broken_constraints+=1
        print("MID is %s " %(c5))

    # need 1 -1 3 STR"
    c6 = np.sum(np.multiply(stri,individual))
    if c6 > 3 or c6 < 1:
        broken_constraints+=1
        print("STR is %s " %(c6))

    # get indices of players selected
    selectedPlayers = [idx for idx, element in enumerate(individual) if element==1]

    totalpoints = np.sum(np.multiply(points, individual))


    print("total broken constraints: %s" %(broken_constraints))
    print("total points: %s" %(totalpoints))
    print("total cost is %s" %(c2))
    print("selected players are %s" %(selectedPlayers))

    return broken_constraints, totalpoints

check_constraints(bit_string)
