import  _init_all as init
import os

def gen_section_score_txt_name(patient_id,node_id,step):
    file_name = "Patient_"+str(patient_id).zfill(3)+"_Node_"+str(node_id).zfill(2)+"_Step_"+str(step)+".txt"
    return file_name

def gen_section_score_dat_name(patient_id,node_id,step):
    file_name = "Patient_"+str(patient_id).zfill(3)+"_Node_"+str(node_id).zfill(2)+"_Step_"+str(step)+".dat"
    return file_name

def gen_section_score_npy_name(patient_id,node_id,step):
    file_name = "Patient_%03d_Node_%02d_Step_%d.npy"%(patient_id,node_id,step)
    return file_name

def gen_heatmap_img_name(patient_id,node_id,step,threshold):
    file_name = "Patient_"+str(patient_id).zfill(3)+"_Node_"+str(node_id).zfill(2)+"_Step_"+str(step)+"_Threshold_"+str(threshold)+".jpg"
    #file_name = "Patient_%03_Node_%02d_Step_%d_Gate_%1.2lf.jpg"%(patient_id,node_id,step,threshold)
    return file_name

def gen_raw_heatmap_img_name(patient_id,node_id,step):
    file_name = "Patient_"+str(patient_id).zfill(3)+"_Node_"+str(node_id).zfill(2)+"_Step_"+str(step)+"_Raw.jpg"
    return file_name

def gen_slide_score_file_name(patient_id,node_id,step):
    #donot change it
    #file_name = "patient"+str(patient_id).zfill(3)+"_"+str(node_id).zfill(2)+"_"+str(step)+".csv"
    path_info = init.path_info()
    files = os.listdir(path_info.input)
    file_name_part = "patient_%03d_node_%d.tif_test_"%(patient_id,node_id)
    for f in files:
        if  f.find(file_name_part) >= 0:
            return f
    return "null"

def gen_slide_score_test_file_name(patient_id,node_id,step):
    #donot change it
    test_id = patient_id*5 + node_id
    file_name = "test_"+str(test_id).zfill(3)+".tif_test_W???_H???.csv"
    return file_name

def get_slide_score_test_csv_name(patient_id,node_id,step):
    path_info = init.path_info()
    files = os.listdir(path_info.input)
    test_id = patient_id*5 + node_id
    file_name_part = "test_%03d.tif_test_"%(test_id)
    for f in files:
        if f.find(file_name_part) >= 0:
            return f
    return "null"

def gen_positive_xml_file_name(pathient_id,node_id,threshold):
    path_info = init.path_info()
    file_name = "patient_%03d_node_%d_threshold_%1.4lf.xml" %(pathient_id,node_id,threshold)
    file_path = os.path.join(path_info.slide_info,file_name)
    return file_path



def get_GT_C16_path():
    #cfg = init.config()
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    path_file = os.path.join(path_info.config,stat_cfg.GT_file_C16)
    return  path_file

def get_GT_C17_path():
    #cfg = init.config()
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    path_file = os.path.join(path_info.config,stat_cfg.GT_file_C17)
    return  path_file

def get_VS_file_path():
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    file_name ="%s_%1.3lf.csv" %(stat_cfg.vs_file,init.get_positive_gate())
    path_file = os.path.join(path_info.outs,file_name)
    return  path_file

def get_result_info_path():
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    path_file = os.path.join(path_info.outs,stat_cfg.info_file)
    return  path_file

def get_kappa_file_path():
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    path_file = os.path.join(path_info.outs,stat_cfg.gate_kappa_file)
    return path_file

def get_pnstage_kappa_file_path():
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    path_file = os.path.join(path_info.outs,stat_cfg.patient_kappa_file)
    return  path_file

def get_pnstage_file_path():
    cfg = init.config()
    path_info = init.path_info()
    pnstage_file_name = "%s_%1.3lf.csv" % (cfg.result_csv_file, init.get_positive_gate())
    result_path = os.path.join(path_info.pns_info, pnstage_file_name)
    return  result_path


def get_slide_info_file_path():
    cfg = init.config()
    gate = init.get_positive_gate()
    path_info = init.path_info()
    file_name = "%s_%1.4lf.csv" %(cfg.slide_info_file,gate)
    path_file = os.path.join(path_info.slide_info,file_name)
    return path_file