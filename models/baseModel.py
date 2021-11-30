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
from datetime import datetime



data = pd.read_csv("clean-data.csv").reset_index(drop=True)

NBR_PLAYERS = len(data.index)
NUM_GK = 1
DEF_RANGE = [3, 4, 5]
MID_RANGE = [3, 4, 5]
STR_RANGE = [1, 2, 3]

GEN = 250


# As we will use another binary representation we only need to modify the onemax algoriothm a little

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def initPopulation(pcls, ind_init, filename):
    with open(filename, "r") as pop_file:
        contents = json.load(pop_file)
    return pcls(ind_init(c) for c in contents)


toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, NBR_PLAYERS)
toolbox.register("population_guess", initPopulation, list, creator.Individual, "populations/popSeed.json")

# Function to check if team is valid

def check_valid(GKs, DEFs, MIDs, STRs):

    if GKs != NUM_GK:
        return False
    elif DEFs not in DEF_RANGE:
        return False
    elif MIDs not in MID_RANGE:
        return False
    elif STRs not in STR_RANGE:
        return False
    else:
        return True

# Create a (new) fitness function
def evalFantasyTeam(individual):

    value = 0

    cost = 0
    GKs = 0
    DEFs = 0
    MIDs = 0
    STRs = 0
    TEAM = 0

    for i in range(len(individual)):

        if individual[i] == 1:
            if data['Position'][i] == "GK":
                GKs += 1
            elif data['Position'][i] == "DEF":
                DEFs += 1
            elif data['Position'][i] == "MID":
                MIDs += 1
            elif data['Position'][i] == "STR":
                STRs += 1
            TEAM += 1
            value += data['Points'][i]
            cost += data['Cost'][i]

    if TEAM < 11:
        value = -100000
    elif check_valid(GKs, DEFs, MIDs, STRs) == False:
        value = value * -1
    elif TEAM > 11:
        value = value - ((TEAM - 11) * 1000)
    elif cost > 100:
        value = value - (cost + 200)

    return value,


# Register evolutionary operators that we want to use
toolbox.register("evaluate", evalFantasyTeam)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.002)
toolbox.register("select", tools.selTournament, tournsize=3)

# create evolution function

def main():

    pop = toolbox.population_guess()

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=GEN, stats=stats, halloffame=hof, verbose=False)

    return pop, log, hof



def run_multiple_tests(epochs):

    best_vals = []

    columns = ["Run", "Fit", "Gen", "Cost", "Num_Players", "Team", "BitString"]
    results = pd.DataFrame(columns=columns)

    for e in range(epochs):

        pop, log, hof = main()

        best = hof[0].fitness.values[0]
        max = log.select("max")

        # look through the log to see at what generation the best solution was found

        for g in range(GEN):
            fit = max[g]
            if fit == best:
                break


        print(f"max fitness is {best} and it was found at generation {g}")

        team = []
        bit_string = hof[0]
        total_cost = 0
        for i in range(523):
            if hof[0][i] == 1:
                team.append(data['Player'][i])
                total_cost += data['Cost'][i]
        print(f"Team Members: {len(team)}")
        print(f"Total Cost: {total_cost}")
        print(team)

        best_vals.append(best)
        results.loc[len(results)] = [str(e), str(best), str(g), str(total_cost), str(len(team)), str(team), bit_string]

    print(f"The average fitness for these parameters is: {np.mean(best_vals)}")
    print(f"With Standard Deviation: {np.std(best_vals)}")
    now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    results.to_csv(f"results/base_results_{epochs}_{now}.csv", mode="w")

run_multiple_tests(4)
