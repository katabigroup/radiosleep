import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats

ds = "mgh_full_new"
channel = "rf"

results_dir = "../results/respiratory_events"
df_ds_ch = pd.read_csv("%s/%s_%s.csv"%(results_dir, ds, channel), index_col = 0)

gt_ahis = df_ds_ch["gt_ahi"].values
pred_ahis = df_ds_ch["pred_ahi"].values

fig_boxplot, ax_boxplot = plt.subplots(1, 1, figsize=(6, 5))

normal_indices = np.where(gt_ahis < 5)[0]
mild_indices = np.where(np.logical_and(gt_ahis >= 5, gt_ahis < 15))[0]
moderate_indices = np.where(np.logical_and(gt_ahis >= 15, gt_ahis < 30))[0]
severe_indices = np.where(gt_ahis >= 30)[0]

# now we need to get the predicted ahis for each category
normal_pred_ahis = pred_ahis[normal_indices]
mild_pred_ahis = pred_ahis[mild_indices]
moderate_pred_ahis = pred_ahis[moderate_indices]
severe_pred_ahis = pred_ahis[severe_indices]

# compute the p-values between consecutive categories using mann-whitney u test
p_normal_mild = stats.mannwhitneyu(normal_pred_ahis, mild_pred_ahis, alternative = "less")[1]
p_mild_moderate = stats.mannwhitneyu(mild_pred_ahis, moderate_pred_ahis, alternative = "less")[1]
p_moderate_severe = stats.mannwhitneyu(moderate_pred_ahis, severe_pred_ahis, alternative = "less")[1]

print("p_normal_mild", p_normal_mild)
print("p_mild_moderate", p_mild_moderate)
print("p_moderate_severe", p_moderate_severe)

boxplot_colors = [sns.color_palette("Blues", 10)[4]] * 4

# boxplot labels
boxplot_labels = ["Normal", "Mild", "Moderate", "Severe"]

# boxplot data
boxplot_data = [normal_pred_ahis, mild_pred_ahis, moderate_pred_ahis, severe_pred_ahis]

# plot the boxplot using sns, but create dataframe first
boxplot_df = pd.DataFrame(boxplot_data).transpose()
boxplot_df.columns = boxplot_labels

# remove outliers from the boxplot
sns.boxplot(data = boxplot_df, ax = ax_boxplot, palette = boxplot_colors, showfliers = False)

ax_boxplot.set_ylim([0, 70])
ax_boxplot.yaxis.grid(True)

# remove right and top splines
ax_boxplot.spines["right"].set_visible(False)
ax_boxplot.spines["top"].set_visible(False)

ax_boxplot.set_xlabel("PSG Labeled AHI", fontsize=18)
ax_boxplot.set_ylabel("Predicted AHI", fontsize=18)
ax_boxplot.tick_params('y', labelsize=15)
ax_boxplot.tick_params('x', labelsize=15)

# save the boxplot for fig_boxplot
fig_boxplot.tight_layout(pad=1)
fig_boxplot.savefig(os.path.join("visualizations", "fig3b.png"))

plt.tight_layout(pad = 0.1)
plt.close()