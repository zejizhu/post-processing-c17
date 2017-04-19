#!/usr/bin/env python
import numpy as np
import os
import csv
import string
import pandas as ps
import sklearn
import stat_sum as stat
import _init_all as init

def write_file(csv_data,data_file_name):
    if os.path.exists(data_file_name):
        csvfile = open (data_file_name, 'a')
        writer = csv.writer(csvfile)
    else:
        csvfile = open (data_file_name, 'a')
        writer = csv.writer(csvfile)
        writer.writerow(['item', 'num', 'list'])

    writer.writerows(csv_data)
    #print csv_data
    csvfile.close()

def read_csv_data(file_name, usecol):
    arr = np.loadtxt(file_name, delimiter=',', usecols=(usecol,))
    return arr

def read_truth_ground_data(file_name):
    with open(file_name, 'rb') as csvFile:
        readFile = ps.read_csv(csvFile)
        ground_truth_map = {int(df_row[0].split('_')[1])
                            : df_row[3].lower().replace('none', 'negative') for _, df_row in readFile.iterrows()}
        #print ground_truth_map
    return ground_truth_map


def read_result_data_two(file_name):
    with open(file_name, 'rb') as csvFile:
        readFile = ps.read_csv(csvFile)
        result_data_map = {int(df_row[0])*5+int(df_row[1])
                            : df_row[6].lower() for _, df_row in readFile.iterrows()}
        #print result_data_map
    return result_data_map

def write_compare_data(file_name, ground_truth, result):
    csvfile = open(file_name, 'a')
    writer = csv.writer(csvfile)
    csv_data = []
    for i in result.keys():
        csv_data.append((ground_truth[i], result[i], i))

    #print csv_data
    writer.writerows(csv_data)
    csvfile.close()
    stat.sum_stat_info(file_name)


def calculate_kappa(ground_truth_map, result_map):
    stage_list = ['itc', 'micro', 'macro', 'negative']
    stat_cfg = init.stat_config()
    ground_truth_stage_list = []
    result_stage_list = []

    for patient_id, result_stage in result_map.iteritems():
        if stat_cfg.gt_itc_mode == 0:
            result_stage = result_stage.replace('itc','negative')
        result_stage_list.append(result_stage)
        ground_truth_stage_list.append(ground_truth_map[patient_id])

    #print ground_truth_stage_list, result_stage_list

    # Return the Kappa score.
    cohen_kappa_score = sklearn.metrics.cohen_kappa_score(y1=ground_truth_stage_list, y2=result_stage_list, labels=stage_list,weights='quadratic')
    #print cohen_kappa_score
    return cohen_kappa_score
