# plot the channel wiese ICC as a confusion matrix

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from sklearn.metrics import cohen_kappa_score

channels = ["rf", "abdominal", "thorax"]
channel_names = ["Wireless Signal", "Abdominal Belt", "Thoracic Belt"]

num_channels = len(channels)

confusion_matrix = np.zeros((num_channels, num_channels))
np.fill_diagonal(confusion_matrix, 1)

confusion_matrix_ci = np.chararray((num_channels, num_channels), itemsize=20)
np.fill_diagonal(confusion_matrix_ci, "[1.00, 1.00]")

for i in range(num_channels):
    for j in range(num_channels):
        if i == j:
            continue

        if j > i:
            continue

        channel_i = channels[i]
        channel_j = channels[j]

        kappa = pd.read_csv(f"../results/sleep_stages/kappa_{channel_i}_{channel_j}.csv")["kappa"].values

        mean_kappa = np.mean(kappa)
        std_kappa = np.std(kappa)

        confusion_matrix[i, j] = mean_kappa
        confusion_matrix_ci[i, j] = "[%.2f, %.2f]"%(mean_kappa - 1.96*std_kappa/np.sqrt(len(kappa)), mean_kappa + 1.96*std_kappa/np.sqrt(len(kappa)))

        confusion_matrix[j, i] = confusion_matrix[i, j]
        confusion_matrix_ci[j, i] = confusion_matrix_ci[i, j]

fig, ax = plt.subplots(figsize=(6, 6))
sns.heatmap(confusion_matrix, annot=False, ax=ax, cmap="Blues", vmin=0.00, vmax=1, fmt=".2f")

# remove the colorbar
cbar = ax.collections[0].colorbar
cbar.remove()

# # plot the x and y axis labels
ax.set_xticklabels(channel_names, fontsize=15, rotation=0, size=15)
ax.set_yticklabels(channel_names, fontsize=15, rotation=90, size=15)

# Loop over data dimensions and create text annotations, where the first row of the text is the ICC value and the second row is the CI
for i in range(num_channels):
    for j in range(num_channels):

        # convert the numpy char array to string
        icc_ij = confusion_matrix[i, j]
        ci_ij = confusion_matrix_ci[i, j].decode("utf-8")

        ax.text(j + 0.5, i + 0.4, "%.2f"%(confusion_matrix[i, j]), ha="center", va="center", color="white", fontsize=20)

        ax.text(j + 0.5, i + 0.6, "%s"%(ci_ij), ha="center", va="center", color="white", fontsize=10)

plt.tight_layout()

fig.savefig("visualizations/fig2b.png")
plt.close()