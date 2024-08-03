import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score
from tqdm import tqdm


# from local import ds_tags_of_interests


def get_acc(filenames, filename_gt_stage_dict, filename_pred_stage_dict):
    acc_list = []
    for filename in filenames:
        gt_stage = filename_gt_stage_dict[filename]
        pred_stage = filename_pred_stage_dict[filename]

        assert (len(gt_stage) == len(pred_stage))

        # find the accuracy
        accuracy = accuracy_score(gt_stage, pred_stage) * 100
        acc_list.append(accuracy)

    acc_list = np.array(acc_list)
    return acc_list


ds_list = ["mgh"]
ch_list = ["rf"]

tag_to_label_folder = "dx_cat/tag_to_label"

ds_ch_list = zip(ds_list, ch_list)

ds_tags_of_interests = {
    "mgh": {
        "Cardiovascular": [
            "myocardial infarction",  #"dx_cci_mi",
            "hypertension",  # "dx_elix_hyp",
            "valvular disease",  #"dx_elix_valv",
            "congestive heart failure",  #"dx_elix_chf",
            "cardiac arrhythmias",  #"dx_elix_carit",
            "peripheral vascular disease",  #"dx_merge_pvd",
        ],
        "Respiratory": [
            "chronic pulmonary disease",  #"dx_elix_cpd",
            "pulmonary circulation disorder",  #"dx_elix_pcd",
        ],
        "Immune": [
            "rheumatoid arthritis",  #"dx_merge_rheumd",
            "diabetes",  #"dx_merge_diabete",
            "cancer",  #"dx_merge_cancer",
        ],
        "Neurological": [
            "cerebrovascular disease",  #"dx_cci_cevd",
            "dementia",  #"dx_cci_dementia",
            "other neurological disorders",  #"dx_elix_ond",
        ],
    },
}

all_data = []
all_color = []
all_text = []
all_xlabels = []

ds = "mgh"
ch = "rf"
results_dir = "../results/sleep_stages"
metrics_csv_path_root = os.path.join(results_dir, "%s_%s.csv" % (ds, ch))
metrics_csv_path = metrics_csv_path_root
metrics_csv = pd.read_csv(metrics_csv_path)

dx_acc_dict = dict()
# dx_acc_dict["all"] = metrics_csv["four_class_acc"].values * 100

for dx_type, dx_tags in ds_tags_of_interests[ds].items():
    dx_acc_dict = dict()

    for dx_tag in dx_tags:
        dx_acc_dict[dx_tag] = metrics_csv[metrics_csv[dx_tag] == 1]["four_class_acc"].values * 100

    data = list([dx_acc_dict[dx_tag] for dx_tag in dx_tags])
    text = []

    # sort the barplots based on the mean accuracy
    mean_acc = [np.mean(data_) for data_ in data]

    if dx_type in ['Neurological', 'Immune']:
        pass
    else:
        sort_idx = np.argsort(mean_acc)[::-1]
        data = [data[i] for i in sort_idx]
        dx_tags = [dx_tags[i] for i in sort_idx]

    # label the mean accuracy at the top of the bar, with the total number of samples
    for i, acc in enumerate(data):
        num_samples = len(acc)
        mean_acc = np.mean(acc)
        text.append("%.1f \n (n = %d)" % (mean_acc, num_samples))

    # assign dx_tags_color with the tab10 colormap
    dx_tags_color = {}
    for i, dx_tag in enumerate(dx_tags):
        # different shades of blue
        if dx_type == "Respiratory":
            dx_tags_color[dx_tag] = sns.color_palette("Greens", 9)[5 - i]
        # different shades of green
        elif dx_type == "Cardiovascular":
            dx_tags_color[dx_tag] = sns.color_palette("Blues", 9)[5 - i]
        # different shades of purple
        elif dx_type == "Immune":
            dx_tags_color[dx_tag] = sns.color_palette("Purples", 9)[5 - i]
        # different shades of orange
        elif dx_type == "Neurological":
            dx_tags_color[dx_tag] = sns.color_palette("Oranges", 9)[5 - i]
        elif dx_type == "Narcolepsy":
            dx_tags_color[dx_tag] = sns.color_palette("Reds", 9)[5 - i]
        else:
            assert False

    colors = [dx_tags_color[dx_tag] for dx_tag in dx_tags]  # [::-1]

    dx_labels = dx_tags

    if dx_type != 'Cardiovascular':
        all_data += [np.array([0])]
        all_color += [(0, 0, 0)]
        all_text += [""]
        all_xlabels += [""]

    all_data += data
    all_color += colors
    all_text += text
    all_xlabels += dx_labels

fig, ax = plt.subplots(figsize=(len(all_data) * 1.7 + 1, 8))

sns.barplot(data=all_data, palette=all_color, capsize=0.2, err_kws={"linewidth": 3.0}, width=0.8, )

print(all_data)
for data in all_data:
    print(np.mean(data), '+-', np.std(data))

fontsize = 15

# label the mean accuracy at the top of the bar, with the total number of samples
for i, text in enumerate(all_text):
    ax.text(i, 87, text, ha="center", va="bottom", fontsize=fontsize)

# def func(x):
#     if len(x) < 30:
#         # l = (30 - len(x)) // 2
#         # r = 30 - len(x) - l
#         r = 0
#         l = 30 - len(x)
#         return ''.join([" "] * l) + x + ''.join([" "] * r)
#     return x
# all_xlabels = [func(x) for x in all_xlabels]
ax.set_xticks(np.arange(len(all_xlabels)), all_xlabels, rotation=45)
# ax.set_ylabel("Sleep Stage Accuracy (%)")
ax.set_ylim(bottom=60, top=90)

# add title as the ds
# ax.set_title(dx_type, fontsize=15)

# increase the font size of the x and y ticks
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
ax.yaxis.label.set_size(fontsize)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# add grid lines on the y axis that lies below the graph
ax.grid(axis="y", color="gray", linestyle="--", alpha=0.5)

# remove top padding
plt.subplots_adjust(top=0.95, bottom=0.15, left=0.15, right=0.95, hspace=0.2, wspace=0.2)

# fix the splines at fixed location
# ax.spines['bottom'].set_position(('data', 0))
plt.tight_layout(pad=0)

plt.savefig("figures/fig4b/%s_%s.png" % (ds, ch), dpi=300)
plt.close()
