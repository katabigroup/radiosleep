import os
import sys
import pandas as pd
import numpy as np

datasets_and_breathing_channels = ["mgh-rf"]

df_results = pd.DataFrame(columns=["dataset", "demo", "num_samples", "4-class_acc"])

for dataset_breathing_channel in datasets_and_breathing_channels:
    dataset, breathing_channel = dataset_breathing_channel.split("-")

    df = pd.read_csv("../results/sleep_stages/%s_%s.csv"%(dataset, breathing_channel), index_col = 0, low_memory = False)

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
                    "All": uid_all,
                    "Male": uid_male,
                    "Female": uid_female,
                    "Young": uid_young,
                    "Middle": uid_middle,
                    "Old": uid_old,
                    "Asian": uid_asian,
                    "Black": uid_black,
                    "White": uid_white,
                    "Others":uid_others,
                    }

    for demo, ids in demographics.items():
        num_samples = len(ids)
        four_class_acc = df.loc[ids, "four_class_acc"].values * 100
        acc_mean_4class = np.mean(four_class_acc)
        acc_std_4class = np.std(four_class_acc)

        # save the results in df_results using pd concat
        acc_4class = "%.1f +-%.1f"%(acc_mean_4class, acc_std_4class)
        
        df_results = pd.concat([df_results, pd.DataFrame([[dataset, demo, num_samples, acc_4class]], columns=["dataset", "demo", "num_samples", "4-class_acc",])], ignore_index=True)

    df_results.to_csv("tables/table2b.csv", index=False)