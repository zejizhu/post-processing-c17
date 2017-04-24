import os
import os.path as osp
import sys
import numpy as np

g_positive_gate = 0.0

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)



class config:
    def __init__(self):
        self.positive_gate = 0.88
        self.transfer_gate = 0.80
        #self.positive_gate_map1 = 0.95
        #self.positive_gate_map2 = 0.80
        self.max_patient_num = 100
        # #0: get score from .csv ,
        # #1,get score from numpy matrix
        # #2 get score from image
        # #3,get score from random data
        # #4,get score from mask image
        self.get_score_mode = 0
        ## get score from .csv
        ### 0: from patient_xxx_node_xx.csv   :patient:xx node:xx
        ### 1:from test_xxx.csv :test_id:xx
        self.get_csv_mode = 1
        # 0 # donot run the evaluate test
        # 1 # run the evaluate test
        self.eva_mode = 1             ######################## evaluate mode
        # #0 no heatmap output
        # #1 heatmap output
        self.output_heatmap_mode = 0  ######################### heatmap mode
        # # 0 just one positive_gate
        # # 1 positive_gate loop test
        self.gate_loop_test_mode = 1   ########################## loop mode
        self.gen_slide_info_xml_mode = 1  ##create the positive slide xml file
        self.save_np_score_mode = 1     ##save the raw score as the numpy file
        self.gate_start = 0.7
        self.gate_end = 1.0
        self.gate_step = 0.01
        self.output_max_positive_region = 0  ########################### max positive region
        self.sort_mode = 0  # 0, ITC use the cell count,#1, ITC just use the region size
        self.step = 256
        self.inflate_level = 1
        self.slide_norm_cfg = "slide_info.npy"
        self.slide_raw_cfg = "camelyon17_pixel_spacing.txt"
        self.slide_size_cfg = "camelyon17_image_size.txt"
        self.slide_type=["negative","itc","micro","macro"]
        self.slide_info_file = "slide_info_gate"
        self.result_csv_file = "Semptian_pnstage_threshold"
        self.expand_size = 75.0  #75um is the equivalent size of tumor cells
        self.patch_tumor_cell_cnt =30
        self.node_num = 5
        self.gap_size =0.243
        self.cell_gate = 0.1
        self.pst_patient = 0
        self.pst_node = 1
        self.pst_xsize = 2
        self.pst_ysize = 3
        self.pst_xgap = 4
        self.pst_ygap = 5
        # #0: donot statistics
        # #1: statistics info
        #self.stat_slide_info_mode = 0


class path_info:
    def __init__(self):
        self.input = 'csv_outs_tf_hsd2_no_distort_11w'
        self.config = 'config'
        self.raw_score = 'raw_score'
        self.heatmap = 'heatmap'
        self.slide_info = 'slide_info'
        self.pns_info = 'pN_stage'
        #self.slide_info = 'outs'
        #self.pns_info = 'outs'
        self.outs = "outs"
        self.mask_dir='mask'

class slide:
    def __init__(self):
        self.start_id = 0
        self.end_id = 27
        self.img_size = 256
        self.cut_num = 28
        self.patient_num = 3
        self.node_num = 5
        self.offset = 0
        self.c1_start_cnt = 29

class iou_config:
    def __init__(self):
        self.positive_gate_start = 0.50
        self.positive_gate_step = 0.0001
        self.patient_id_start = 0
        self.patient_id_end = 27
        # 0 get score from csv
        # 1 get score from numpy matrix
        self.get_raw_score_mode = 1
        self.node_num = 5
        self.score_dir = "raw_score"
        self.mask_dir = "mask"
        self.iou_out_dir = "iou"
        self.iou_best_file = "best_iou.csv"

class stat_config:
    def __init__(self):
        self.num = 0
        self.GT_file_C16="GT_C16.csv" #config/GT_C16.csv
        self.GT_file_C17 = "GT_C17.csv" #config/GT_C17.csv
        self.c17_pnstage = "C17_train_test_ground_truth.csv"
        self.vs_file="result_vs_threshold" #outs/vs_gate_xxx.csv
        self.info_file="result_info.csv" #outs/result_info.csv
        self.gate_kappa_file = "threshold_kappa.csv" # outs/gate_kappa.csv
        self.patient_kappa_file = "patient_kappa.csv"
        # #1: ground true contain itc
        # #0 except ITC
        self.gt_itc_mode = 0
        # #1 clca the pnstage kappa file
        # #0 do nothing
        self.pnstage_kappa_mode = 0
        self.GT_str16=["negative","micro","macro"]
        self.GT_str17 = ["negative","itc","micro","macro"]
        self.eva_str=["negative","itc","micro","macro"]

def set_positive_gate(gate):
    global g_positive_gate
    g_positive_gate = gate
def get_positive_gate():
    global g_positive_gate
    return g_positive_gate

def get_raw_config():
    paths = path_info()
    cfg = config()
    file_path = os.path.join(paths.config,cfg.slide_raw_cfg)
    arr_cfg = np.zeros((cfg.max_patient_num*cfg.node_num,6))
    inputs = open(file_path,'r')
    loop_cnt = 0
    for line in inputs:
        dat = line.split(" = ")
        if dat[0] == "Filename":
            #Test_002.tif
            #patient_013_node_1.tif
            arr_cfg[loop_cnt][cfg.pst_patient] = float(dat[1][8:11])
            arr_cfg[loop_cnt][cfg.pst_node] = float(dat[1][17])
        if dat[0] == "  x-pixels":
            arr_cfg[loop_cnt][cfg.pst_xsize] = float(dat[1])
        if dat[0] =="  y-pixels":
            arr_cfg[loop_cnt][cfg.pst_ysize] = float(dat[1])
        if dat[0] =="  spacingx":
            arr_cfg[loop_cnt][cfg.pst_xgap] = float(dat[1])
        if dat[0] == "  spacingy":
            arr_cfg[loop_cnt][cfg.pst_ygap] = float(dat[1])
            loop_cnt +=1
    #file_path = os.path.join(paths.config, cfg.slide_norm_cfg)
    np.save(cfg.slide_norm_cfg,arr_cfg)
    return  arr_cfg

def get_size_config():
    paths = path_info()
    cfg = config()
    file_path = os.path.join(paths.config,cfg.slide_size_cfg)
    arr_cfg = np.loadtxt(file_path,delimiter=',')
    norm_cfg_path = os.path.join(paths.config,cfg.slide_norm_cfg)
    np.save(norm_cfg_path,arr_cfg)
    return  arr_cfg

def get_config():
    cfg = config()
    paths = path_info()
    norm_cfg_path = os.path.join(paths.config, cfg.slide_norm_cfg)
    return np.load(norm_cfg_path)

def get_patient_img_param(patient_id,node_id):
    '''
    :param patient_id:
    :param node_id:
    :return: [patient_id,node_id,x_size,y_size,x_gap,y_gap]
    '''
    cfg = config()
    arr_cfg = np.array(get_config())
    for id in range(arr_cfg.shape[0]):
        if arr_cfg[id][cfg.pst_patient] == patient_id:
            if arr_cfg[id][cfg.pst_node] == node_id:
                return arr_cfg[id]
    return [0,0,0,0]

def all_dir_check():
    paths = path_info()
    cfg = config()

    if osp.exists(paths.input):
        msg = 'The path '+paths.input+ ' is exists.'
    else:
        msg = 'Cannot find [' +paths.input+'] folder. '
        print (msg)
        return 1
    print(msg)

    if cfg.get_score_mode ==4:
        if osp.exists(paths.mask_dir):
            msg = 'The path ' + paths.mask_dir + ' is exists.'
        else:
            msg = 'Cannot find [' + paths.mask_dir + '] folder. '
            print (msg)
            return 1
        print(msg)

    if osp.exists(paths.config):
        msg = 'The path '+paths.config+ ' is exists.'
        get_size_config()
    else:
        msg = 'Cannot find [' +paths.config+'] folder. '
        #print (msg)
        #return 1
    print(msg)

    if osp.exists(paths.raw_score):
        msg = 'The path '+paths.raw_score+ ' is exists.'
    else:
        os.makedirs(paths.raw_score)
        msg = 'Creat path '+paths.raw_score
    print(msg)

    if osp.exists(paths.heatmap):
        msg = 'The path '+paths.heatmap+ ' is exists.'
    else:
        os.makedirs(paths.heatmap)
        msg = 'Creat path '+paths.heatmap
    print (msg)

    if osp.exists(paths.slide_info):
        msg = 'The path '+paths.slide_info+ ' is exists.'
    else:
        os.makedirs(paths.slide_info)
        msg = 'Creat path '+paths.slide_info
    print (msg)

    if osp.exists(paths.outs):
        msg = 'The path '+paths.outs+ ' is exists.'
    else:
        os.makedirs(paths.outs)
        msg = 'Creat path '+paths.outs
    print (msg)

    if osp.exists(paths.pns_info):
        msg = 'The path '+paths.pns_info+ ' is exists.'
    else:
        os.makedirs(paths.pns_info)
        msg = 'Creat path '+paths.pns_info
    print (msg)
    return 0

if __name__ == "__main__": 
    if all_dir_check():
        print "The patch check fail!"
    else:
        print "The path check success."
