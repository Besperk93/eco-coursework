import array
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from deap import algorithms
from deap import base
from deap import creator
from deap import tools


# Create an instance of a knapsack problem

items = {}

NBR_ITEMS = 100
MAX_WEIGHT = 300

for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(1, 100))



# As we will use another binary representation we only need to modify the onemax algoriothm a little

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, NBR_ITEMS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Create a (new) fitness function
def evalKnapsack(individual):

    value = 0
    weight = 0

    for i in range(len(individual)):
        if individual[i] == 1:
            weight += items[i][0]
            value += items[i][1]

    if weight > MAX_WEIGHT:
        value = value * -1

    return value,


# Register evolutionary operators that we want to use
toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.15)
toolbox.register("select", tools.selTournament, tournsize=2)

# create evolution function

def main():

    pop = toolbox.population(n=100)

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=1.0, mutpb=0.35, ngen=200, stats=stats, halloffame=hof, verbose=False)

    return pop, log, hof



pop, log, hof = main()

best = hof[0].fitness.values[0]
max = log.select("max")

# look through the log to see at what generation the best solution was found

for i in range(200):
    fit = max[i]
    if fit == best:
        break


print(f"max fitness is {best} and it was found at generation {i}")
