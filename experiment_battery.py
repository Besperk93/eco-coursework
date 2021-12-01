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


class experiment:

    def run_experiment(self):
        for pops in self.POPSEEDS:
            try:
                self.get_meta_attr(self.DATA_LOC)
                self.initiate_deap()
                self.establish_evaluator()
                self.establish_selection()
                self.establish_population(pops)
            except Exception as e:
                print(f"Error establishing population parameters: {repr(e)}")
            for cx in self.cxPARAMS:
                try:
                    self.establish_crossover(cx)
                except Exception as e:
                    print(f"Error establishing crossover params: {repr(e)}")
                for mx in self.mutPARAMS:
                    try:
                        self.establish_mutator(mx)
                    except Exception as e:
                        print(f"Error establishing mutation params: {repr(e)}")
                    try:
                        self.run_multiple_tests(self.EPOCHS, mx, cx, pops)
                    except Exception as e:
                        print(f"Error running main: {repr(e)}")


    def run_multiple_tests(self, epochs, mut, cross, popSeed):

        best_vals = []

        columns = ["Run", "Fit", "Gen", "Cost", "Num_Players", "Team", "BitString"]
        results = pd.DataFrame(columns=columns)

        for e in range(epochs):

            try:
                pop, log, hof = self.main()

                best = hof[0].fitness.values[0]
                max = log.select("max")
            except Exception as e:
                print(f"Error setting up hall of fame: {repr(e)}")

            # look through the log to see at what generation the best solution was found

            for g in range(self.GEN):
                fit = max[g]
                if fit == best:
                    break


            # print(f"max fitness is {best} and it was found at generation {g}")

            team = []
            bit_string = hof[0]
            total_cost = 0
            for i in range(523):
                if hof[0][i] == 1:
                    team.append(self.data['Player'][i])
                    total_cost += self.data['Cost'][i]
            # print(f"Team Members: {len(team)}")
            # print(f"Total Cost: {total_cost}")
            # print(team)

            best_vals.append(best)
            results.loc[len(results)] = [str(e), str(best), str(g), str(total_cost), str(len(team)), str(team), bit_string]

        # print(f"The average fitness for these parameters is: {np.mean(best_vals)}")
        # print(f"With Standard Deviation: {np.std(best_vals)}")
        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        results.to_csv(f"results/test1/{popSeed}_{cross}_{mut}_{epochs}_{now}.csv", mode="w")

    def main(self):
        try:
            pop = self.toolbox.population_guess()
            hof = tools.HallOfFame(1)
            toolbox = self.toolbox
        except Exception as e:
            print(f"Error with pop/hof: {repr(e)}")

        try:
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("avg", np.mean)
            stats.register("std", np.std)
            stats.register("min", np.min)
            stats.register("max", np.max)
        except Exception as e:
            print(f"Error setting up stats: {repr(e)}")

        try:
            pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=self.GEN, stats=stats, halloffame=hof, verbose=False)
            return pop, log, hof
        except Exception as e:
            print(f"Error running algo: {repr(e)}")

    def establish_selection(self):
        self.toolbox.register("select", tools.selTournament, tournsize=3)


    def establish_population(self, population):
        if population == "random":
            self.toolbox.register("population_guess", self.initPopulation, list, creator.Individual, "populations/randomSeed.json")
        elif population == "empty":
            self.toolbox.register("population_guess", self.initPopulation, list, creator.Individual, "populations/emptySeed.json")
        elif population == "onePicked":
            self.toolbox.register("population_guess", self.initPopulation, list, creator.Individual, "populations/oneSeed.json")

    def establish_evaluator(self):
        self.toolbox.register("evaluate", self.evalFantasyTeam)

    def establish_mutator(self, mutate):
        if mutate == "flipBit":
            self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.002)
        elif mutate == "shuffle":
            self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.002)
        else:
            print(f"Unknown mutation operator provided")

    def establish_crossover(self, mate):
        if mate == "onePoint":
            self.toolbox.register("mate", tools.cxOnePoint)
        elif mate == "twoPoint":
            self.toolbox.register("mate", tools.cxTwoPoint)
        elif mate == "uniform":
            self.toolbox.register("mate", tools.cxUniform, indpb=0.002)
        else:
            print(f"Unknown crossover operator provided")

    def initPopulation(self, pcls, ind_init, filename):
        try:
            with open(filename, "r") as pop_file:
                contents = json.load(pop_file)
            return pcls(ind_init(c) for c in contents)
        except Exception as e:
            print(f"Error creating population: {repr(e)}")

    def initiate_deap(self):
        try:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)
            self.toolbox = base.Toolbox()
            self.toolbox.register("attr_bool", random.randint, 0, 1)
            self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, self.NBR_PLAYERS)
        except Exception as e:
            print(f"Error initiating Deap instance: {repr(e)}")

    def evalFantasyTeam(self, individual):

        value = 0
        cost = 0
        GKs = 0
        DEFs = 0
        MIDs = 0
        STRs = 0
        TEAM = 0

        for i in range(len(individual)):

            if individual[i] == 1:
                if self.data['Position'][i] == "GK":
                    GKs += 1
                elif self.data['Position'][i] == "DEF":
                    DEFs += 1
                elif self.data['Position'][i] == "MID":
                    MIDs += 1
                elif self.data['Position'][i] == "STR":
                    STRs += 1
                TEAM += 1
                value += self.data['Points'][i]
                cost += self.data['Cost'][i]

        if TEAM < 11:
            value = -100000
        elif self.check_valid(GKs, DEFs, MIDs, STRs) == False:
            value = value * -1
        elif TEAM > 11:
            value = value - ((TEAM - 11) * 1000)
        elif cost > 100:
            value = value - (cost + 200)

        return value,

    def check_valid(self, GKs, DEFs, MIDs, STRs):

        if GKs != self.NUM_GK:
            return False
        elif DEFs not in self.DEF_RANGE:
            return False
        elif MIDs not in self.MID_RANGE:
            return False
        elif STRs not in self.STR_RANGE:
            return False
        else:
            return True

    def get_meta_attr(self, data_loc):
        try:
            self.data = pd.read_csv(data_loc).reset_index(drop=True)
            self.NBR_PLAYERS = len(self.data.index)
            self.NUM_GK = 1
            self.DEF_RANGE = [3, 4, 5]
            self.MID_RANGE = [3, 4, 5]
            self.STR_RANGE = [1, 2, 3]
        except Exception as e:
            print(f"Error getting meta attributes: {repr(e)}")

    def __init__(self, data_loc, generations, epochs):
        self.DATA_LOC = data_loc
        self.GEN = generations
        self.EPOCHS = epochs
        self.cxPARAMS = ["onePoint", "twoPoint", "uniform"]
        self.mutPARAMS = ["flipBit", "shuffle"]
        self.POPSEEDS = ["random", "empty", "onePicked"]


dry_run = experiment("clean-data.csv", 100, 10)

dry_run.run_experiment()
