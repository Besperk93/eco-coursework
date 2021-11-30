import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv('bitstring_results_10-11-2021_03-49-56.csv', sep="w")

box_plot = results.boxplot(column='Fit')

plt.savefig("boxplot_1.png")
plt.show()
