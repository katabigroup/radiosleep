import os
import sys
import numpy as np
import pandas as pd

datasets_chs = {
                'mgh': ["rf", "abdominal", "thorax"],
                "umass": ["rf", "abdominal", "thorax"],
                'shhs1': ["abdominal", "thorax"],
                'shhs2': ["abdominal", "thorax"],
                'wsc': ["abdominal", "thorax"],
                'mesa': ["abdominal", "thorax"],
                'mros1': ["abdominal", "thorax"],
                'mros2': ["abdominal", "thorax"],
                }

results_ds = pd.DataFrame(columns=["dataset", "ch", "four_class_acc"])

for dataset, chs in datasets_chs.items():
    for ch in chs:
        # load the results from from csv
        results = pd.read_csv(f"../results/sleep_stages/{dataset}_{ch}.csv")

        four_class_acc_mean = results["four_class_acc"].mean() * 100
        four_class_acc_std = results["four_class_acc"].std() * 100

        four_class_acc = f"{four_class_acc_mean:.1f} ± {four_class_acc_std:.1f}"

        results_ds = results_ds.append({"dataset": dataset, "ch": ch, "four_class_acc": four_class_acc}, ignore_index=True)
        
results_ds.to_csv("tables/fig2a.csv", index=False)