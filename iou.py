import numpy as np
import os
import _init_all as init
import gen_slide_data as gen_data

def get_raw_score((patient_id,node_id)):
    #arr_score = np.array((patient_id,node_id))
    iou_cfg = init.iou_config()
    if iou_cfg.get_raw_score_mode == 0:
        raw_score = gen_data.gen_slide_score_form_csv(patient_id,node_id)
    elif iou_cfg.get_raw_score_mode == 1:
        raw_score = gen_data.gen_slide_score_from_np_matrix(patient_id, node_id)
    else:
        print "[ERR] get raw score data fail!"
        raw_score = 0
    return raw_score

def get_mask_score((patient_id,node_id)):
    mask_score = gen_data.gen_slide_score_from_mask_img(patient_id,node_id)
    return mask_score


def iou_calc(raw_score,mask_score, gate):
    '''
    arr=np.array(raw_score)
    gate_score = (arr > gate)*1
    #arr_mask_score = np.array(mask_score) * 1
    x_cnt = gate_score.shape[1]
    y_cnt = gate_score.shape[0]
    set_cnt = 0.0
    subset_cnt = 0.0
    for x in range(x_cnt):
        for y in range(y_cnt):
            if gate_score[y][x] == 1:
                if mask_score[y][x] == 1:
                    subset_cnt +=1
                    set_cnt += 1
                    #print  "11"
                else:
                    set_cnt += 1
                    #print "22"
            else:
                if mask_score[y][x] == 1:
                    #print "33"
                    set_cnt += 1
    '''
    #faster more
    arr = np.array(raw_score)
    gate_score_bool = raw_score > gate
    mask_score_bool_tmp  = mask_score > 0
    mask_score_bool = mask_score_bool_tmp[:arr.shape[0],:arr.shape[1]]
    arr_or = gate_score_bool | mask_score_bool
    arr_and = gate_score_bool & mask_score_bool
    subset_cnt = sum(sum(arr_and))*1.0
    set_cnt = sum(sum(arr_or))*1.0
    val_iou = subset_cnt/set_cnt
    #print "subset:%d allset:%d "%(subset_cnt,set_cnt)
    return val_iou


def slide_all_gate_cale(raw_score,mask_score,patient_id = 0,node_id=0):
    iou_cfg = init.iou_config()
    best_gate_val = 0.0
    best_iou_val = 0.0

    file_name = "Patient_%03d_Node_%02d_iou.csv"%(patient_id,node_id)
    file_path = os.path.join(iou_cfg.iou_out_dir,file_name)
    fd_slide_iou =open(file_path,"ab+")
    file_path = os.path.join(iou_cfg.iou_out_dir,iou_cfg.iou_best_file)
    fd_best_iou = open(file_path,"ab+")
    for cnt in range(int((1-iou_cfg.positive_gate_start)/iou_cfg.positive_gate_step)+1):
        gate = cnt*iou_cfg.positive_gate_step + iou_cfg.positive_gate_start
        val_iou = iou_calc(raw_score,mask_score,gate)
        if val_iou > best_iou_val:
            best_iou_val = val_iou
            best_gate_val = gate
        w_context = "%1.5lf,%1.5lf\n"%(gate,val_iou)
        fd_slide_iou.write(w_context)
        print "Patient:%d Node:%d Gate:%1.5lf IOU:%lf"%(patient_id,node_id,gate,val_iou)
    w_context = "%d,%d,%1.5lf,%1.5lf\n"%(patient_id,node_id,best_gate_val,best_iou_val)
    fd_best_iou.write(w_context)
    fd_best_iou.close()
    fd_slide_iou.close()
    return 0


def iou_init():
    iou_cfg = init.iou_config()
    if os.path.exists(iou_cfg.iou_out_dir):
        msg = 'The path '+iou_cfg.iou_out_dir+ ' is exists.'
    else:
        os.makedirs(iou_cfg.iou_out_dir)
        msg = 'Creat path '+iou_cfg.iou_out_dir
    print (msg)

def main():
    iou_cfg = init.iou_config()
    for patient_id in range(iou_cfg.patient_id_start,iou_cfg.patient_id_end):
        for node_id in range(iou_cfg.node_num):
            print "\n############## patient:%d node:%d ##############"%(patient_id,node_id)
            raw_score = get_raw_score((patient_id,node_id))
            print "raw_score shape:%s" %(str(raw_score.shape))
            mask_score = get_mask_score((patient_id,node_id))
            print "mask_score shape:%s" %(str(mask_score.shape))
            if 1 in mask_score:
                slide_all_gate_cale(raw_score,mask_score,patient_id,node_id)
            else:
                print "the mask is negative"

if __name__ == "__main__":
    iou_init()
    main()

