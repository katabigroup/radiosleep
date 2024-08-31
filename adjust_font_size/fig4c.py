import torch
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def pval_to_stars(p):
    if p <= 0.001:
        return '***'
    elif p <= 0.01:
        return '**'
    elif p <= 0.05:
        return '*  '
    elif p <= 0.1:
        return '.'
    else:
        return 'ns'


def draw_significance_line(x1, x2, y, y_sep, text, ax):
    if text in ['*', '**', '***', '*  ']:
        ax.plot([x1 + 0.1, x1 + 0.1, x2 - 0.1, x2 - 0.1], [y, y + y_sep, y + y_sep, y], lw=1.5, c='k')
        ax.text((x1 + x2) * 0.5, y + y_sep, text, ha='center', va='bottom')


def plot_rows(plot_df, p_values_df_for_metric, yname, title_name, plot_name, viz_save_dir, bar_width=0.5, ylim=[0, 8]):
    # assert that the plot_df["Dataset"] only contains one unique value
    assert (len(plot_df["Dataset"].unique()) == 1)

    # load the tab20 color palette
    palette = sns.color_palette("tab20c", 20)

    # check if the word "Medication" is in the column ["On Medication"]
    if "On Medication" in plot_df["On Medication"].values:
        include_medication = True
    else:
        include_medication = False

    if include_medication:
        fig, ax = plt.subplots(1, 1, figsize=(3, 4), sharey=True)

        # sns.boxplot(x = "On Medication", y = yname, data = plot_df, showfliers = False, palette = [palette[6], palette[1], palette[2]], ax = ax, showcaps = False, width = bar_width)

        bp = plt.boxplot([plot_df[plot_df["On Medication"] == "Control"][yname].values,
                          plot_df[plot_df["On Medication"] == "On Medication"][yname].values,
                          plot_df[plot_df["On Medication"] == "Not on Medication"][yname].values], showfliers=False,
                         showcaps=False, widths=bar_width, meanline=False, patch_artist=True,
                         showmeans=False)

        # remove median line in boxplot, and replace with mean line
        if False:
            for median in bp['medians']:
                median.set_visible(False)

            for mean in bp["means"]:
                mean.set_color("black")
                mean.set_linewidth(1)
                # solid line
                mean.set_linestyle("-")

        else:
            # change the color of the median line to black
            for median in bp['medians']:
                median.set_color('black')

        # add boxplot colors
        for patch, color in zip(bp['boxes'], [palette[6], palette[2], palette[3]]):
            patch.set_facecolor(color)

        # add x axis labels
        # ax.set_xticklabels(["Control", "On Medication", "Not on Medication"])
        print(p_values_df_for_metric)
        n_control = p_values_df_for_metric['Num Control'].iloc[0]
        n_meds = p_values_df_for_metric['Num On Meds'].iloc[0]
        n_no_meds = p_values_df_for_metric['Num No Meds'].iloc[0]
        ax.set_xticklabels([
            f"Control\n(n={n_control})",
            f"Meds\n(n={n_meds})",
            f"No Meds\n(n={n_no_meds})"]
        )

        # add statistical significance
        # y_max = np.max(plot_df[yname])
        # if yname == 'REM Latency (hours)':
        y_max = ylim[1]

        y_sep = y_max * 0.03
        y_line = y_max - y_sep * 8  # Adjust this as needed

        p_value_12 = np.abs(p_values_df_for_metric['Ext On Meds'].iloc[0])
        # p_value_23 = np.abs(p_values_df_for_metric['Ext Combined'])
        p_value_13 = np.abs(p_values_df_for_metric['Ext No Meds'].iloc[0])

        # Drawing lines and annotations
        draw_significance_line(1, 2, y_line, y_sep, pval_to_stars(p_value_12), ax)
        # draw_significance_line(2, 3, y_line, pval_to_stars(p_value_23), ax)
        draw_significance_line(1, 3, y_line + y_sep * 4, y_sep, pval_to_stars(p_value_13), ax)



    else:
        fig, ax = plt.subplots(1, 1, figsize=(2.5, 4), sharey=True)
        # sns.boxplot(x = "On Medication", y = yname, data = plot_df, showfliers = False, palette = [palette[5], palette[1]], ax = ax, showcaps = False, width = bar_width)

        bp = plt.boxplot([plot_df[plot_df["On Medication"] == "Control"][yname].values,
                          plot_df[plot_df["On Medication"] == title_name][yname].values], showfliers=False,
                         showcaps=False, widths=bar_width, meanline=False, patch_artist=True,
                         showmeans=False)

        # add x axis labels
        # ax.set_xticklabels(["Control", title_name])
        n_control = p_values_df_for_metric['Num Control'].iloc[0]
        n_dx = p_values_df_for_metric['Num Dx'].iloc[0]

        display_name = title_name
        if title_name == 'rheumatoid_arthritis':
            display_name = 'RA'

        ax.set_xticklabels([
            f"Control\n(n={n_control})",
            f"{display_name}\n(n={n_dx})",
        ])

        if False:
            for median in bp['medians']:
                median.set_visible(False)

            for mean in bp["means"]:
                mean.set_color("black")
                mean.set_linewidth(1)
                mean.set_linestyle("-")

        else:
            # change the color of the median line to black
            for median in bp['medians']:
                median.set_color('black')

        # add boxplot colors
        for patch, color in zip(bp['boxes'], [palette[6], palette[1]]):
            patch.set_facecolor(color)

        # add statistical significance
        y_max = np.max(plot_df[yname])
        # if yname == 'Duration of REM Stage':
        #     y_max = 3.5
        # if yname == 'Proportion of REM Stage':
        #     y_max = min(y_max, 0.4)
        # if yname == 'REM Latency (hours)':
        y_max = ylim[1]

        print('yname', yname)
        y_sep = y_max * 0.03
        y_line = y_max - y_sep * 4  # Adjust this as needed

        p_value_12 = np.abs(p_values_df_for_metric['Ext Combined'].iloc[0])

        # Drawing lines and annotations
        draw_significance_line(1, 2, y_line, y_sep, pval_to_stars(p_value_12), ax)

    # set the y tick labels to be 6
    ax.tick_params(axis="y", labelsize=12)
    ax.tick_params(axis="x", labelsize=12)

    # set the size of the y axis label to 12
    # ax.set_ylabel(yname, fontsize = 12)

    # start plot from at least 0 (max between min and 0)
    # ax.set_ylim(bottom = -0.1)
    ax.set_ylim(ylim)
    ax.set_yticks(np.arange(0, y_max, 1))

    # remove the x axis label
    ax.set_xlabel("")

    # add y axis grid lines
    ax.yaxis.grid(True)

    # remove all splines
    sns.despine()

    # plot the title_name
    # fig.suptitle(title_name, fontsize = 10)

    # tight layout for the figure
    fig.tight_layout()
    Path(f"figures/fig4c/{disease}").mkdir(parents=True, exist_ok=True)
    fig.savefig(f"figures/fig4c/{disease}/{name}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    for log_fn in Path('../results/statistical_analysis').glob('*/*.pt'):
        name = log_fn.stem
        disease = log_fn.parent.stem
        info = torch.load(log_fn)
        print(info.keys(), log_fn)
        plot_df = info['plot_df']
        p_values_df_for_metric = info['p_values_df_for_metric']
        yname = info['yname']
        plot_name = info['plot_name']
        title_name = info['title_name']
        ylim = info['ylim']
        bar_width = info['bar_width']
        plot_rows(plot_df, p_values_df_for_metric, yname, title_name, plot_name, None, bar_width, ylim)
