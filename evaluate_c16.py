import os
import numpy as np
import auc

dir_c16_outs = "C16_auc_outs"

DIR_INPUT = "csv_outs_tf_hsd2_no_distort_11w"
DIR_CONFIG = "config"
FILE_C16_GT_CSV = "GT_C16.csv"
MEAN_COUNT = 1
TEST_SET_CONUT = 130

def get_score_mean(file_path):
    score_data = np.loadtxt(file_path, delimiter=',', usecols=(3,))
    score_data.sort()
    max_score = score_data[MEAN_COUNT * (-1):]
    mean_score = sum(max_score) / (MEAN_COUNT * 1.0)
    return mean_score


def get_score_1(file_path):
    score_data = np.loadtxt(file_path, delimiter=',', usecols=(2,))
    score_data.sort()
    max_score = score_data[MEAN_COUNT * (-1):]
    arr_score = max_score > 0.99
    positive_cnt = sum(arr_score)
    #mean_score = sum(max_score) / (MEAN_COUNT * 1.0)
    score = positive_cnt / (MEAN_COUNT*1.0)
    return score

def get_score(file_path):
    #return  get_score_mean(file_path)
    return get_score_mean(file_path)

def get_slide_score(slide_id):
    files = os.listdir(DIR_INPUT)
    part_name = "test_%03d.tif_test_" %(slide_id)
    file_name = "null"
    for f in files:
        if f.find(part_name) >= 0:
            file_name = f
            break
    file_path = os.path.join(DIR_INPUT,file_name)
    if os.path.exists(file_path):
        return get_score(file_path)
    else:
        print ("The file %s is not find!" %(file_path))
    return 0

def get_testset_score():
    test_score = np.zeros(TEST_SET_CONUT)
    for i in range(TEST_SET_CONUT):
        test_score[i] = get_slide_score(i+1)
    return test_score

def get_ground_truth():
    file_path =os.path.join(DIR_CONFIG,FILE_C16_GT_CSV)
    files = open(file_path,"r")
    gt_score = np.zeros(TEST_SET_CONUT)
    test_id = 0
    for lines in files:
        param = lines.split(",")
        file_name = "Test_%03d" %(test_id+1)
        if param[0] == file_name:
            #print param[3]
            if param[3].find("None") >=0:
                #print  "######  None"
                gt_score[test_id] = 0
            else:
                #print  "##### positive"
                gt_score[test_id] = 1
            test_id +=1
    return gt_score

def save_testset_score(eva_score,gt_score):
    file_name = "C16_test_slide_info_%d.csv" %(MEAN_COUNT)
    fig_path =os.path.join(dir_c16_outs,file_name)
    test_dat = np.array([eva_score,gt_score]).T
    np.savetxt(fig_path,test_dat,fmt='%1.3lf',delimiter=",")
    return 0

def evaluate_c16_main():
    eva_score = get_testset_score()
    #print "##################################"
    #print eva_score
    gt_score = get_ground_truth()
    #print "++++++++++++++++++++++++++++++++++++"
    #print gt_score
    #print "================================="
    save_testset_score(eva_score,gt_score)
    fig_name = "c16_auc_mean_cnt_%d.jpg" %(MEAN_COUNT)
    fig_path =os.path.join(dir_c16_outs,fig_name)
    #print gt_score.shape
    #print eva_score.shape

    auc_score = auc.auc(gt_score,eva_score,fig_path)
    print ("Meat count:%d C16 AUC is :%0.4lf" %(MEAN_COUNT,auc_score))

def evaluate_c16_init():
    if os.path.exists(dir_c16_outs):
        print ("%s is exists!" %(dir_c16_outs))
    else:
        os.makedirs(dir_c16_outs)


def main():
    evaluate_c16_init()
    evaluate_c16_main()

if __name__ == '__main__':
    main()