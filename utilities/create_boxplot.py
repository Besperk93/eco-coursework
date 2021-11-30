import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

results = pd.read_csv('results/onePoint_results_10_30-11-2021_15-59-38.csv')

box_plot = results.boxplot(column='Fit')

now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
plt.savefig(f"charts/boxplot_{now}.png")
plt.show()
