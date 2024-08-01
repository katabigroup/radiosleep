import os
import sys
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import pingouin as pg
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import r2_score

datasets_channel = {
    "mgh_full_new": ["rf", "abdominal"],
    "shhs1_new": ["abdominal"],
    "shhs2_new": ["abdominal"],
    "wsc_new": ["abdominal"],
    "mesa_new": ["abdominal"],
    "mros1_new": ["abdominal"],
    "mros2_new": ["abdominal"],
}

results = pd.DataFrame(columns = ["dataset", "channel", "icc", "r"])

results_dir = "../results/respiratory_events"
for ds in datasets_channel:
    for channel in datasets_channel[ds]:
        df_ds_ch = pd.read_csv("%s/%s_%s.csv"%(results_dir, ds, channel), index_col = 0)
        
        filenames = df_ds_ch.index
        gt_ahis_array = df_ds_ch["gt_ahi"].values
        pred_ahis_array = df_ds_ch["pred_ahi"].values

        # now compute icc
        data_gt = pd.DataFrame({'filename': filenames, 'ahi': gt_ahis_array, 'rater': "GT"})
        data_pred = pd.DataFrame({'filename': filenames, 'ahi': pred_ahis_array, 'rater': 'Pred'})
        data = pd.concat([data_gt, data_pred])

        icc_result = pg.intraclass_corr(data=data, targets='filename', raters = "rater", ratings = "ahi", nan_policy='omit').round(3)
        icc3k = icc_result.iloc[5]["ICC"]

        # get confidence interval from icc_result
        icc3k_ci = icc_result.iloc[5]["CI95%"]
        icc_combined = "%s (%s)"%(icc3k, icc3k_ci)

        # then compute the pearson correlation coefficient
        corr, p = pearsonr(gt_ahis_array, pred_ahis_array)
        corr = corr.round(3)

        # save result in dataframe
        results = pd.concat([results, pd.DataFrame({"dataset": [ds], "channel": [channel], "icc": [icc_combined], "r": [corr]})])

# save results
results.to_csv("tables/fig3a.csv", index = False)