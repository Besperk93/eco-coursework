import json
import random

# random
pop = []
for p in range(523):
    individual = []
    for i in range(523):
        rand = random.randint(0, 1)
        individual.append(rand)
    pop.append(individual)

with open("populations/randomSeed.json", "w") as file:
    json.dump(pop, file)

# Empty
pop = []
for p in range(523):
    individual = []
    for i in range(523):
        individual.append(0)
    pop.append(individual)

with open("populations/emptySeed.json", "w") as file:
    json.dump(pop, file)

# onePick
pop = []
for p in range(523):
    individual = []
    for i in range(523):
        if i == p:
            individual.append(1)
        else:
            individual.append(0)
    pop.append(individual)

with open("populations/oneSeed.json", "w") as file:
    json.dump(pop, file)
