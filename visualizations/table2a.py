import os
import sys
import pandas as pd
import numpy as np

datasets_and_breathing_channels = ["mgh-rf"]
for ds in ['shhs1', 'shhs2', 'wsc', 'mesa', 'mros1', 'mros2']:
    datasets_and_breathing_channels.append(ds + '-thorax')

df_results = pd.DataFrame(columns=["dataset",
                                   "gap (sex) mean", "gap (sex) std",
                                   "gap (age) mean", "gap (age) std",
                                   "gap (race) mean", "gap (race) std"])

for dataset_breathing_channel in datasets_and_breathing_channels:
    dataset, breathing_channel = dataset_breathing_channel.split("-")

    df = pd.read_csv("../results/sleep_stages/%s_%s.csv" % (dataset, breathing_channel), index_col=0, low_memory=False)

    uid_all = set(df.index)
    uid_male = set(df[df.sex == 1].index)
    uid_female = set(df[df.sex == 2].index)
    uid_young = set(df[df.age < 40].index)
    uid_middle = set(df[(df.age >= 40) & (df.age < 60)].index)
    uid_old = set(df[df.age >= 60].index)

    uid_asian = set(df[df.race == 3].index)
    uid_black = set(df[df.race == 2].index)
    uid_white = set(df[df.race == 1].index)
    uid_others = uid_all - uid_asian - uid_black - uid_white

    demographics = {
        # "All": uid_all,
        "Male": uid_male,
        "Female": uid_female,
        "Young": uid_young,
        "Middle": uid_middle,
        "Old": uid_old,
        "Asian": uid_asian,
        "Black": uid_black,
        "White": uid_white,
        "Others": uid_others,
    }

    cate = {
        "Male": "sex",
        "Female": "sex",
        "Young": "age",
        "Middle": "age",
        "Old": "age",
        "White": "race",
        "Asian": "race",
        "Black": "race",
        "Others": "race",
    }
    acc_dict = {
        "sex": [],
        "age": [],
        "race": [],
    }
    for demo, ids in demographics.items():
        num_samples = len(ids)
        if num_samples == 0:
            continue
        four_class_acc = df.loc[list(ids), "four_class_acc"].values * 100
        # dataset [wsc] has empty line
        acc_mean_4class = np.nanmean(four_class_acc)
        acc_std_4class = np.nanstd(four_class_acc)
        acc_dict[cate[demo]].append(acc_mean_4class)

    new_row = {"dataset": dataset}

    msg = f"{dataset}"
    for k, v in acc_dict.items():
        n = len(v)
        t = []
        for i in range(n):
            for j in range(i + 1, n):
                t.append(abs(v[i] - v[j]))
        the_mean, the_std = np.round(np.mean(t), 2), np.round(np.std(t), 2)

        msg += f"\t{the_mean}\t{the_std}"
        new_row[f'gap ({k}) mean'] = the_mean
        new_row[f'gap ({k}) std'] = the_std
    print(msg)

    df_results = pd.concat([df_results, pd.DataFrame([new_row], columns=df_results.columns)],
                           ignore_index=True)
print(df_results.columns)
df_results.to_csv("tables/table2a.csv", index=False)
print('average gap (sex) mean', df_results['gap (sex) mean'].mean())
print('average gap (age) mean', df_results['gap (age) mean'].mean())
print('average gap (race) mean', df_results['gap (race) mean'].mean())
