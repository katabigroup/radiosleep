"""
load the csv files, and change the index column to integers
"""

import os
import numpy as np
import pandas as pd

deidentify_sleep_stage = True
deidentify_respiratory_event = False

if deidentify_sleep_stage:
    # 1. Deidentify sleep stages
    results_dir = "sleep_stages_raw"
    deidentify_dir = "sleep_stages"

    datasets = ["mgh", "mgh", "mgh", "shhs1", "shhs1", "shhs1", "shhs2", "shhs2", "shhs2", "wsc", "wsc", "wsc", "mros1", "mros1", "mros1", "mros2", "mros2", "mros2", "umass", "umass", "umass", "mesa", "mesa"]
    chs = ["rf", "thorax", "abdominal", "thorax", "abdominal", "thorax", "abdominal", "thorax", "abdominal", "thorax", "abdominal", "thorax", "thorax", "abdominal", "thorax", "thorax", "abdominal", "thorax", "rf", "thorax", "abdominal", "abdominal", "thorax"]

    # zip
    ds_ch_list = zip(datasets, chs)

    for ds, ch in ds_ch_list:
        csv_path = os.path.join(results_dir, "%s_%s.csv"%(ds, ch))
        results = pd.read_csv(csv_path, index_col=0)

        # change the index column such that each unique patient has a unique integer id
        if (ds == "mgh") or (ds == "umass"):
            results["uid"] = results.index
            results["uid"] = pd.factorize(results["uid"])[0]
        else:
            results["uid"] = results.index
        results.set_index("uid", inplace=True)

        # save the deidentified csv
        deidentify_csv_path = os.path.join(deidentify_dir, "%s_%s.csv"%(ds, ch))
        results.to_csv(deidentify_csv_path)

if deidentify_respiratory_event:
    # 2. Deidentify respiratory events
    results_dir = "respiratory_events_raw"
    deidentify_dir = "respiratory_events"

    datasets = ["mgh_full_new", "mgh_full_new", "shhs1_new", "shhs2_new", "wsc_new", "mros1_new", "mros2_new", "mesa_new"]
    chs = ["rf", "abdominal", "abdominal", "abdominal", "abdominal", "abdominal", "abdominal", "abdominal", "abdominal"]

    # zip
    ds_ch_list = zip(datasets, chs)

    for ds, ch in ds_ch_list:
        csv_path = os.path.join(results_dir, "%s_%s.csv"%(ds, ch))
        results = pd.read_csv(csv_path, index_col=0)

        # change the index column such that each unique patient has a unique integer id
        if (ds == "mgh_full_new") or (ds == "umass"):
            results["uid"] = results.index
            results["uid"] = pd.factorize(results["uid"])[0]
        else:
            results["uid"] = results.index
        results.set_index("uid", inplace=True)

        # save the deidentified csv
        deidentify_csv_path = os.path.join(deidentify_dir, "%s_%s.csv"%(ds, ch))
        results.to_csv(deidentify_csv_path)