import numpy as np
import _init_all as init
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
import gen_slide_data as gen_data

def positive_find(score,gate):
    arr=np.array(score)
    #print (arr.shape)
    arr_mask = arr > gate
    if 1 in arr_mask:
        return 1,arr_mask
    else:
        return 0,arr_mask

def transfer_find(score,mask_dat):
    cfg = init.config()
    if cfg.gate_loop_test_mode == 0:
        arr_mask = score > cfg.transfer_gate
    else:
        arr_mask = mask_dat
    return  arr_mask

#0~0.1,0.1~0.2 0.2~0.3,0.3~0.4,0.4~0.5,0.5~0.6,0.6~0.7 0.7~0.8 0.8~0.9 0.9~1
def section_stat(score):
    arr_score = np.array(score)
    gate_cnt = np.zeros(101)
    #for low_gate in range(10):
    for y in range(arr_score.shape[0]):
        for x in range(arr_score.shape[1]):
            if  score[y][x] > 0.000:
                gate_cnt[int(score[y][x]*100)] +=1
    return gate_cnt

def section_bar_img(gate_cnt,(patient_id,node_id)):
    cfg = init.config()
    patch_info = init.path_info()
    all_cnt = sum(gate_cnt)+1
    Y = np.array(gate_cnt)/all_cnt
    X = np.arange(Y.shape[0])/100.0
    fig = plt.figure()
    plt.bar(X[1:],Y[1:],0.005)
    #xmajorLocator = MultipleLocator(20)
    #xmajorFormatter = FormatStrFormatter('%1.2f')
    #plt.show()
    file_name = "Patient_%03d_Node_%02d_score_histogram.jpg"%(patient_id,node_id)
    file_path = os.path.join(patch_info.heatmap,file_name)
    plt.title(file_name)
    plt.savefig(file_path)
    plt.clf() #close image
    plt.cla()  #clean axis
    plt.close() #close windows

def slide_mask(score,gate):
    arr=np.array(score)
    arr_mask = arr > gate
    return  arr_mask

if __name__ == "__main__":
    score = gen_data.gen_slide_score(4,2)
    if positive_find(score,0.8):
        print ("this slide is positive!")
    else:
        print ("this slide is negative")

    if positive_find(score,1.1):
        print ("this slide is positive!")
    else:
        print ("this slide is negative")
