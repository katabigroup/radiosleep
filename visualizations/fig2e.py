import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import pandas as pd


# function to plot the scatter plot with the 95% confidence interval and the diagonal line
def plot_scatter(gt_tsts, pred_tsts, xlabel, ylabel, title, xlim, ylim, xy_text, tick_interval):
    fig, ax = plt.subplots(figsize=(6, 6))

    # seaborn scatter plot with the 95% confidence interval. do not plot the points, increase alpha of confidence interval
    sns.regplot(x=gt_tsts, y=pred_tsts, ci=95, scatter=False,
                line_kws={"color": "#0000ff", "alpha": 0.8, 'linewidth': 3}, ax=ax)

    # scatter plot, but fill the circles with the color
    ax.scatter(gt_tsts, pred_tsts, color="#fa7e76", s=30, alpha=0.5, edgecolors="none")

    # annotate on the plot the r value and the p value
    r_value, p_value = stats.pearsonr(gt_tsts, pred_tsts)

    actual_p_value = p_value

    if p_value == 0:
        p_value = 0.0

    # convert p value to scientific notation
    p_value = "{:.1E}".format(p_value)
    if "E" in p_value:
        part1 = p_value.split("E")[0]
        part2 = p_value.split("E")[1]
        part2 = "\\times 10^{{{}}}".format(part2)
        p_value = part1 + part2

    # create the label text in scientific notation latex format
    if actual_p_value < 0.001:
        label_text = "$r = {:.2f}$, $p < 0.001$".format(r_value)
    else:
        label_text = "$r = {:.2f}$, $p = {}$".format(r_value, p_value)

    # set the axis labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    lim = (xlim[0] - tick_interval / 2, xlim[1])

    ax.set_xlim(lim)
    ax.set_ylim(lim)

    # set the x and y ticks
    ax.set_xticks(np.arange(xlim[0], xlim[1], tick_interval),
                  np.arange(xlim[0], xlim[1], tick_interval), fontsize=24)
    ax.set_yticks(np.arange(ylim[0], ylim[1], tick_interval),
                  np.arange(ylim[0], ylim[1], tick_interval), fontsize=24)

    l, r = xlim
    xy_text = (l + 0.03 * (r - l), r - 0.08 * (r - l))

    ax.annotate(label_text, xy=xy_text, xycoords='data', fontsize=24)

    ax.tick_params(axis="both", which="major", labelsize=24)
    ax.yaxis.label.set_size(24)
    ax.xaxis.label.set_size(24)

    # remove the frame from the plot
    sns.despine()

    # save the figure
    plt.savefig(os.path.join(f"figures/fig2e", title + ".png"), dpi=300,
                bbox_inches="tight")
    plt.close()


sleep_metrics_dir = '../results/sleep_stages/mgh_rf.csv'
sleep_metrics = pd.read_csv(sleep_metrics_dir)

gt_tsts = sleep_metrics['gt_tst'].values
pred_tsts = sleep_metrics['pred_tst'].values

gt_sleep_efficiencies = sleep_metrics['gt_sleep_efficiency'].values
pred_sleep_efficiencies = sleep_metrics['pred_sleep_efficiency'].values

gt_sleep_onset_latencies = sleep_metrics['gt_sol'].values
pred_sleep_onset_latencies = sleep_metrics['pred_sol'].values

gt_wake_durations = sleep_metrics['gt_waso'].values
pred_wake_durations = sleep_metrics['pred_waso'].values

# plot the scatter plot for each metric
plot_scatter(gt_tsts, pred_tsts, "Total Sleep Time (hours)", "Model Prediction", "Total Sleep Time (TST)",
             xlim=[2, 9], ylim=[2, 9], xy_text=(3, 7), tick_interval=1)
plot_scatter(gt_sleep_efficiencies, pred_sleep_efficiencies, "Sleep Efficiency (%)",
             "Model Prediction", "Sleep Efficiency", xlim=[30, 105], ylim=[30, 105], xy_text=(60, 90),
             tick_interval=15)
plot_scatter(gt_sleep_onset_latencies, pred_sleep_onset_latencies, "Sleep Onset Latency (hours)", "Model Prediction",
             "SOL", xlim=[0, 6], ylim=[0, 6], xy_text=(1, 5), tick_interval=1)
plot_scatter(gt_wake_durations, pred_wake_durations, "WASO (hours)", "Model Prediction",
             "Wake After Sleep Onset (WASO)", xlim=[0, 5], ylim=[0, 5], xy_text=(1, 4), tick_interval=1)
