import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from tqdm import tqdm

ds_list = ["mgh", "shhs", "wsc", "mros"]
ch_list = ["rf", "thorax", "thorax", "thorax"]

# ds_list = ["shhs1"]
# ch_list = ["thorax"]

ds_ch_list = zip(ds_list, ch_list)

dx_cats = ["all", "cardiovascular", "respiratory", "immune", "neurological"]
# dx_labels = ["Whole Dataset", "Cardiovascular", "Respiratory", "Immune", "Neurological"]
dx_labels = ["All", "Cardio", "Resp", "Immune", "Neural"]

dx_cats_color = {"all": sns.color_palette("Greys", 10)[3],
                 "cardiovascular": sns.color_palette("Blues", 10)[4],
                 "respiratory": sns.color_palette("Greens", 10)[4],
                 "immune": sns.color_palette("Purples", 10)[4],
                 "neurological": sns.color_palette("Oranges", 10)[4]}

results_dir = "../results/sleep_stages"

FONT_SIZE = 30

for ds, ch in ds_ch_list:

    # load the csv, where the row/index name is "uid"
    if ds == "mgh":
        visits = [1]
        metrics_csv_path_root = os.path.join(results_dir, "%s_%s.csv" % (ds, ch))
    elif ds == "wsc":
        visits = [1]
        metrics_csv_path_root = os.path.join(results_dir, "%s_%s.csv" % (ds, ch))
    elif ds == "shhs":
        visits = [1, 2]
        metrics_csv_path_root = os.path.join(results_dir, "shhs{0}_%s.csv" % (ch))
    elif ds == "shhs1":
        visits = [1]
        metrics_csv_path_root = os.path.join(results_dir, "shhs1_%s.csv" % (ch))
    elif ds == "shhs2":
        visits = [2]
        metrics_csv_path_root = os.path.join(results_dir, "shhs2_%s.csv" % (ch))
    elif ds == "mros":
        visits = [1, 2]
        metrics_csv_path_root = os.path.join(results_dir, "mros{0}_%s.csv" % (ch))
    elif ds == "mros1":
        visits = [1]
        metrics_csv_path_root = os.path.join(results_dir, "mros1_%s.csv" % (ch))
    elif ds == "mros2":
        visits = [2]
        metrics_csv_path_root = os.path.join(results_dir, "mros2_%s.csv" % (ch))
    else:
        assert False

    filename_gt_stage_dict = {}
    filename_pred_stage_dict = {}
    dx_acc_dict = dict()

    metrics_csv_list = []

    for visit in visits:
        if len(visits) > 1:
            metrics_csv_path = metrics_csv_path_root.format(visit)
        else:
            metrics_csv_path = metrics_csv_path_root

        metrics_csv = pd.read_csv(metrics_csv_path)
        metrics_csv_list.append(metrics_csv)

    metrics_csv = pd.concat(metrics_csv_list)
    dx_acc_dict["all"] = metrics_csv["four_class_acc"].values * 100

    for dx_cat in dx_cats[1:]:
        dx_acc_dict[dx_cat] = metrics_csv[metrics_csv[dx_cat] == 1]["four_class_acc"].values * 100

    for dx_cat in dx_cats:
        if dx_cat not in dx_acc_dict:
            dx_acc_dict[dx_cat] = []

    # now barplot with errorbar
    fig, ax = plt.subplots(figsize=(6, 5.5))

    data = list([dx_acc_dict[dx_cat] for dx_cat in dx_cats])

    colors = [dx_cats_color[dx_cat] for dx_cat in dx_cats]

    sns.barplot(data=data, palette=colors, capsize=0.2, err_kws={"linewidth": 3.0}, width=0.8)

    # label the mean accuracy at the top of the bar, with the total number of samples
    for i, acc in enumerate(data):
        num_samples = len(acc)
        mean_acc = np.nanmean(acc)

        # ignore if mean acc is nan
        if not np.isnan(mean_acc):
            # ax.text(i, 87, "%.1f \n (n = %d)" % (mean_acc, num_samples), ha="center", va="bottom", fontsize=18)
            ax.text(i, 86, "%.0f" % (mean_acc), ha="center", va="bottom", fontsize=FONT_SIZE)

    x_pos = np.arange(len(dx_cats))

    ax.set_xticks(x_pos)
    ax.set_xticklabels(dx_labels, rotation=0)
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(bottom=60, top=90)

    # let yticks to be every 10
    ax.set_yticks(np.arange(65, 86, 5))

    # increase the font size of the x and y ticks
    ax.xaxis.set_tick_params(labelsize=FONT_SIZE, rotation=45)
    ax.yaxis.set_tick_params(labelsize=FONT_SIZE)
    ax.xaxis.label.set_size(FONT_SIZE)
    ax.yaxis.label.set_size(FONT_SIZE)

    # remove all spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # add grid lines on the y axis that lies below the graph
    ax.grid(axis="y", color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout(pad=0)

    os.system("mkdir -p figures/fig4a")
    plt.savefig("figures/fig4a/%s_%s.png" % (ds, ch), dpi=300)
    plt.close()