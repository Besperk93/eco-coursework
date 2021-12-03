import pickle

with open("best_team.txt", 'rb') as f:
    bit_string = pickle.load(f)

print(bit_string)

with open("best_team_as_string", "w") as output:
    output.write(str(bit_string))
