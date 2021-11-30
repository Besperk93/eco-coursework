import json

pop = []

for p in range(523):
    individual = []
    for i in range(523):
        if i == p:
            individual.append(1)
        else:
            individual.append(0)
    pop.append(individual)

with open("popSeed.json", "w") as file:
    json.dump(pop, file)
