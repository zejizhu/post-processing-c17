#!/usr/bin/env python

import numpy as np
from sklearn import metrics
import rw_data
import os
import stat_sum as stat
import gen_name as gname

def evaluate(truth_ground_file, result_file_name, compare_file_name, sumdata_file_name):
    result_data_map = rw_data.read_result_data_two(result_file_name)
    ground_truth_map = rw_data.read_truth_ground_data(truth_ground_file)

    rw_data.write_compare_data(compare_file_name, ground_truth_map, result_data_map)
    val_kappa=rw_data.calculate_kappa(ground_truth_map, result_data_map)
    #sum_data = stat.sum_stat_info(compare_file_name)
    #rw_data.write_file(sum_data, sumdata_file_name)
    return  val_kappa

def evaluate_main():
    truth_ground_file = gname.get_GT_C16_path()
    result_file_name = gname.get_slide_info_file_path()
    compare_file_name = gname.get_VS_file_path()
    sumdata_file_name = gname.get_result_info_path()

    val = evaluate(truth_ground_file, result_file_name, compare_file_name, sumdata_file_name)
    return val

