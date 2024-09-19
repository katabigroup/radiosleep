import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

data, chn = 'mgh', 'rf'

df = pd.read_csv(f'../results/sleep_stages/{data}_{chn}.csv')

df['four_class_acc'] *= 100

dx_acc_dict = {
    'Male': list(df[df['sex'] == 1]['four_class_acc']),
    'Female': list(df[df['sex'] == 2]['four_class_acc']),
    'Young': list(df[df['age'] < 40]['four_class_acc']),
    'Middle': list(df[(df['age'] >= 40) & (df['age'] < 60)]['four_class_acc']),
    'Old': list(df[df['age'] >= 60]['four_class_acc']),
    'White': list(df[df['race'] == 1]['four_class_acc']),
    'Black': list(df[df['race'] == 2]['four_class_acc']),
    'Asian': list(df[df['race'] == 3]['four_class_acc']),
    'Others': list(df[df['race'] == 0]['four_class_acc']),
}

dx_cats_color = {
    'Male': sns.color_palette("Greys", 10)[3],
    'Female': sns.color_palette("Blues", 10)[4],
    'Young': sns.color_palette("Greys", 10)[3],
    'Middle': sns.color_palette("Blues", 10)[4],
    'Old': sns.color_palette("Greens", 10)[4],
    'Asian': sns.color_palette("Greys", 10)[3],
    'Black': sns.color_palette("Blues", 10)[4],
    'White': sns.color_palette("Greens", 10)[4],
    'Others': sns.color_palette("Purples", 10)[4],
}


def plot_acc_figure(dx_cats):
    if len(dx_cats) == 4:
        space = 1
    elif len(dx_cats) == 3:
        space = 1
    elif len(dx_cats) == 2:
        space = 1

    fig, ax = plt.subplots(figsize=(6.5 / 5 * len(dx_cats), 5.5))

    data = list([dx_acc_dict[dx_cat] for dx_cat in dx_cats])

    colors = [dx_cats_color[dx_cat] for dx_cat in dx_cats]

    print(len(data))
    print(len(colors))

    sns.barplot(data=data, palette=colors, capsize=0.2, err_kws={"linewidth": 3.0}, width=0.8)
    FONT_SIZE = 30

    # label the mean accuracy at the top of the bar, with the total number of samples
    for i, acc in enumerate(data):
        num_samples = len(acc)
        mean_acc = np.mean(acc)
        # ax.text(i, mean_acc + 2, "%.1f \n (n = %d)"%(mean_acc, num_samples), ha = "center", va = "bottom", fontsize = 18)

        # ignore if mean acc is nan
        if not np.isnan(mean_acc):
            # ax.text(i, 87, "%.1f \n (n = %d)" % (mean_acc, num_samples), ha="center", va="bottom", fontsize=18)
            ax.text(i, 86, "%.0f" % (mean_acc), ha="center", va="bottom", fontsize=FONT_SIZE)

    x_pos = np.arange(len(dx_cats))
    dx_labels = [" " * (space - len(dx_cat)) + dx_cat[0].upper() + dx_cat[1:] for dx_cat in dx_cats]

    ax.set_xticks(x_pos)
    ax.set_xticklabels(dx_labels, rotation=0)
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(bottom=60, top=90)

    ax.set_yticks(np.arange(65, 86, 5))

    # increase the font size of the x and y ticks
    plt.xticks(fontsize=FONT_SIZE, rotation=40)
    plt.yticks(fontsize=FONT_SIZE)
    ax.yaxis.label.set_size(FONT_SIZE)

    # remove all spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # add grid lines on the y axis that lies below the graph
    ax.grid(axis="y", color="gray", linestyle="--", alpha=0.5)

    plt.tight_layout(pad=0)

    title_str = '-'.join(dx_cats)

    plt.savefig(f"./figures/graph_abstract/{title_str}.png", dpi=300)
    plt.close()


if __name__ == '__main__':
    dx_cats = ['Male', 'Female']
    plot_acc_figure(dx_cats)
    dx_cats = ['Young', 'Middle', 'Old']
    plot_acc_figure(dx_cats)
    dx_cats = ['Asian', 'Black', 'White', 'Others']
    plot_acc_figure(dx_cats)
