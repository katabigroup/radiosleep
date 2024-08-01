import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def plot_confusion_matrix(cm_stack, classes, fig_name, cmap=plt.cm.Blues, fontsize = 10):
    cm_stack = cm_stack.astype(float)

    cm = np.mean(cm_stack, axis = 0)
    cms = np.std(cm_stack, axis = 0)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0, fontsize = 14)
    plt.yticks(tick_marks, classes, fontsize = 14)

    thresh = cm.max() / 2.

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, '{0:.1f}'.format(cm[i, j]) + '\n$\pm$' + '{0:.1f}'.format(cms[i, j]),
                    horizontalalignment="center",
                    verticalalignment="center", fontsize=fontsize,
                    color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('PSG Labels', fontsize = 14)
    plt.xlabel('Predictions label', fontsize = 14)

    # set figsize
    plt.gcf().set_size_inches(6, 5)

    plt.tight_layout(pad = 0.3)
    plt.savefig("visualizations/%s.png"%(fig_name), dpi = 300)
    plt.close()

# load the csv file
df_five_class_recs = pd.read_csv("../results/sleep_stages/mgh_new_rf_five_class_recs.csv")
df_four_class_recs = pd.read_csv("../results/sleep_stages/mgh_new_rf_four_class_recs.csv")

five_class_recs = []
four_class_recs = []

# loop through the files and unflatten the arrays
for i in tqdm(range(df_five_class_recs.shape[0])):

    five_class_rec_flatten = df_five_class_recs.iloc[i, 1:].values
    four_class_rec_flatten = df_four_class_recs.iloc[i, 1:].values

    five_class_rec = five_class_rec_flatten.reshape(5, 5)
    four_class_rec = four_class_rec_flatten.reshape(4, 4)

    five_class_recs.append(five_class_rec)
    four_class_recs.append(four_class_rec)

five_class_recs = np.stack(five_class_recs)
four_class_recs = np.stack(four_class_recs)

five_classes_name = ["Wake", "N1", "N2", "N3/Deep", "REM"]
fig_name = "fig2c_five_class_recs_cm"
plot_confusion_matrix(five_class_recs, five_classes_name, fig_name, cmap = "Blues", fontsize = 15)

four_classes_name = ["Wake", "Light", "Deep", "REM"]
fig_name = "fig2c_four_class_recs_cm"
plot_confusion_matrix(four_class_recs, four_classes_name, fig_name, cmap = "Blues", fontsize = 18)