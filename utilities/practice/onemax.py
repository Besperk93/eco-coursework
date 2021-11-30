import array
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from deap import algorithms
from deap import base
from deap import creator
from deap import tools


# Create a fitness function template (and add it to the creator factory)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Create an individual (and add it to the creator factory)
creator.create("Individual", list, fitness=creator.FitnessMax)

# Create a toolbox for the algorithms to use

toolbox = base.Toolbox()

# Register an attribute with the toolbox, our individuals will be made up of these attributes
toolbox.register("attr_bool", random.randint, 0, 1)

# Register an individual with the toolbox, it will be of class Individual and consist of 100 attributes
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)

# Register a population with the toolbox, it will be made up of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Create a fitness function
def evalOneMax(individual):
    return sum(individual),

# Register evolutionary operators that we want to use
toolbox.register("evaluate", evalOneMax)
# One point crossover
toolbox.register("mate", tools.cxOnePoint)
# Flipbit with probability 0.05
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# Selection tournament of size 3
toolbox.register("select", tools.selTournament, tournsize=3)

# create evolution function

def main():

    pop = toolbox.population(n=200)

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=1.0, mutpb=0.05, ngen=200, stats=stats, halloffame=hof, verbose=False)

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
