import os
import numpy as np
import pandas as ps


def sum_stat_info(file_name):
    # statistics
    negative_negative = []
    negative_micro = []
    negative_macro = []

    micro_negative = []
    micro_micro = []
    micro_macro = []

    macro_negative = []
    macro_micro = []
    macro_macro = []

    negative_negative_num = 0
    negative_micro_num = 0
    negative_macro_num = 0

    micro_negative_num = 0
    micro_micro_num = 0
    micro_macro_num = 0

    macro_negative_num = 0
    macro_micro_num = 0
    macro_macro_num = 0
    sum_data = []

    with open(file_name, 'rb') as csvFile:
        readFile = ps.read_csv(csvFile,header=None)
        for _, df_row in readFile.iterrows():
            if ((df_row[0] == 'negative') & (df_row[1] == 'negative')):
                negative_negative.append(df_row[2])
                negative_negative_num = negative_negative_num + 1

            elif ((df_row[0] == 'negative') & (df_row[1] == 'micro')):
                negative_micro.append(df_row[2])
                negative_micro_num = negative_micro_num + 1

            elif ((df_row[0] == 'negative') & (df_row[1] == 'macro')):
                negative_macro.append(df_row[2])
                negative_macro_num = negative_macro_num + 1

            elif ((df_row[0] == 'micro') & (df_row[1] == 'negative')):
                micro_negative.append(df_row[2])
                micro_negative_num = micro_negative_num + 1

            elif ((df_row[0] == 'micro') & (df_row[1] == 'micro')):
                micro_micro.append(df_row[2])
                micro_micro_num = micro_micro_num + 1

            elif ((df_row[0] == 'micro') & (df_row[1] == 'macro')):
                micro_macro.append(df_row[2])
                micro_macro_num = micro_macro_num + 1

            elif ((df_row[0] == 'macro') & (df_row[1] == 'negative')):
                macro_negative.append(df_row[2])
                macro_negative_num = macro_negative_num + 1

            elif ((df_row[0] == 'macro') & (df_row[1] == 'micro')):
                macro_micro.append(df_row[2])
                macro_micro_num = macro_micro_num + 1

            elif ((df_row[0] == 'macro') & (df_row[1] == 'macro')):
                macro_macro.append(df_row[2])
                macro_macro_num = macro_macro_num + 1
    sum_data = [('negative_negative',negative_negative_num, negative_negative),
                ('negative_micro',negative_micro_num, negative_micro),
                ('negative_macro',negative_macro_num, negative_macro),
                ('micro_negative', micro_negative_num,micro_negative),
                ('micro_micro', micro_micro_num, micro_micro),
                ('micro_macro', micro_macro_num, micro_macro),
                ('macro_negative', macro_negative_num, macro_negative),
                ('macro_micro', macro_micro_num, macro_micro),
                ('macro_macro', macro_macro_num, macro_macro)]
    #print sum_data
    return sum_data

