#!/usr/bin/env python

import numpy as np
import os
import csv
import pandas as pd

def pnstage(node_data):
    data = np.array(node_data)
#statistics
    negetive_num = np.sum(data == 'negative')
    itc_num = np.sum(data == 'itc')
    micro_num = np.sum(data == 'micro')
    macro_num = np.sum(data == 'macro')
    meta_num = macro_num + micro_num
    pn_stage = ""
#determine pn_stage
    if macro_num > 0:
        if meta_num > 3:
            pn_stage = 'pN2'
        else: 
            pn_stage = 'pN1'
    else:
        if micro_num > 0:
            pn_stage = 'pN1mi'
        else:
            if itc_num > 0:
                pn_stage = 'pN0(i+)'
            else:
                if negetive_num == 5:
                    pn_stage = 'pN0'
                else: 
                    print 'error'
    return pn_stage

def write_result(node_data, pn_stage, path, patient_id):
    #generate item name
    item_name = ['patient_' + '%03d'%(patient_id) + '.zip', 
                'patient_' + '%03d'%(patient_id) + '_node_0.tif',
                'patient_' + '%03d'%(patient_id) + '_node_1.tif',
                'patient_' + '%03d'%(patient_id) + '_node_2.tif',
                'patient_' + '%03d'%(patient_id) + '_node_3.tif',
                'patient_' + '%03d'%(patient_id) + '_node_4.tif']
    #print item_name
                
#check file and table header   
    if os.path.exists(path):
        csvfile = open (path, 'ab+')
        writer = csv.writer(csvfile)
    else:
        csvfile = open (path, 'ab+')
        writer = csv.writer(csvfile)
        writer.writerow(['patient', 'stage'])
        
#write data in file        
    write_data = [(item_name[0], pn_stage),
                 (item_name[1], node_data[0]),
                 (item_name[2], node_data[1]),
                 (item_name[3], node_data[2]),
                 (item_name[4], node_data[3]),
                 (item_name[5], node_data[4])]
    #print write_data
    writer.writerows(write_data)
    csvfile.close()
   
def result(node_data, path, patient_id):
    pn_stage = pnstage(node_data)
    write_result(node_data, pn_stage, path, patient_id)

