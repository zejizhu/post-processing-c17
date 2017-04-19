import sys
import os
import _init_all as init
import gen_slide_data as slide_run
import gen_name as gname
import draw
import positive_check
import metastasis_check
import pnstage_result as result
import evaluate_mete as eva
import statistics_info as statinfo
import gen_positive_xml as positive_xml

def demo_init():
    if init.all_dir_check():
        print ("The folder Check fail")
        return 1
    return 0

def draw_heatmap_img(slide_score,patient_id, node_id, step):
    cfg = init.config()
    path_info =init.path_info()
    gate = init.get_positive_gate()
    if slide_score.shape[0] == 100:
        if slide_score.shape[1] == 100:
            return 0
    if cfg.output_heatmap_mode == 1:
    #draw raw_heatmap
        file_name = gname.gen_raw_heatmap_img_name(patient_id, node_id,step)
        dat_path = os.path.join(path_info.heatmap, file_name)
        draw.drae_raw_heatmap(slide_score,dat_path)

    #draw heatmap1
        file_name = gname.gen_heatmap_img_name(patient_id, node_id,step, gate)
        dat_path = os.path.join(path_info.heatmap, file_name)
        draw.draw_heatmap(slide_score, gate, dat_path)
        #heatmap
        '''
        file_name = gname.gen_heatmap_img_name(patient_id, node_id,step,cfg.positive_gate_map1)
        dat_path = os.path.join(path_info.heatmap, file_name)
        draw.draw_heatmap(slide_score, cfg.positive_gate_map1, dat_path)
        file_name = gname.gen_heatmap_img_name(patient_id, node_id,step,cfg.positive_gate_map2)
        dat_path = os.path.join(path_info.heatmap, file_name)
        draw.draw_heatmap(slide_score, cfg.positive_gate_map2, dat_path)
        '''
    else:
        print "skip output heatmap"



def loop_patient(bar_img,gate):
    slide_info = init.slide()
    path_info = init.path_info()
    cfg=init.config()
    patient_info = ["", "", "", "", ""]

    init.set_positive_gate(gate)
    ## patients loop
    for patient_id in range(slide_info.start_id,slide_info.end_id):
        print "###################  Patient:%d  Gate:%1.4lf ###################" %(patient_id,gate)
        for node_id in range(slide_info.node_num):
            print ">>>Patient:%d Node:%d"%(patient_id,node_id)
            #get score
            slide_score = slide_run.gen_slide_score(patient_id,node_id)

            #generate heatmap
            draw_heatmap_img(slide_score, patient_id, node_id, cfg.step)

            #positive check
            if bar_img == 1:
                gate_cnt = positive_check.section_stat(slide_score)
                positive_check.section_bar_img(gate_cnt,(patient_id,node_id))
            positive_flag,mask_dat = positive_check.positive_find(slide_score,gate)
            if positive_flag:
                mask_dat =  positive_check.transfer_find(slide_score,mask_dat)
                positive_xml.gen_xml(mask_dat,patient_id,node_id,gate)
                print("patient:"+str(patient_id)+" node:"+str(node_id)+" is Positive!")
                #mask_dat = positive_check.slide_mask(slide_score,cfg.positive_gate)
                #metastasis_check.get_positive_count(mask_dat)
                slide_type_str = metastasis_check.get_slide_type(patient_id, node_id,mask_dat)
                patient_info[node_id] = slide_type_str
            else:
                patient_info[node_id] = cfg.slide_type[0]
                if (slide_score.shape[0] != 100) & (slide_score.shape[1] != 100):
                    metastasis_check.save_slide_info(patient_id,node_id,0,0,patient_info[node_id])

        #pnstage_file_name = "%s_%1.3lf.csv" %(cfg.result_csv_file,init.get_positive_gate())
        #result_path = os.path.join(path_info.pns_info,pnstage_file_name)
        result_path = gname.get_pnstage_file_path()
        #print "patient :%d "%(patient_id)
        print patient_info
        result.result(patient_info,result_path,patient_id)
    if cfg.eva_mode == 1:
        val_kappa = eva.evaluate_main()
        statinfo.write_stat_info(val_kappa)
        print "Threshold:%1.3lf Kappa:%1.5lf" %(cfg.positive_gate,val_kappa)
        stat_cfg = init.stat_config()
        if stat_cfg.pnstage_kappa_mode == 1:
            statinfo.write_pn_stage_kappa()



def patient_test_once():
    cfg=init.config()
    loop_patient(1,cfg.positive_gate)


def patient_test_gate_loop():
    slide_info = init.slide()
    path_info = init.path_info()
    cfg=init.config()
    patient_info = ["","","","",""]
    gate_loop_cnt = 0
    for gate_num in range(int((cfg.gate_end-cfg.gate_start)/cfg.gate_step)):

        ## patients loop
        gate_tmp = cfg.gate_start + gate_num*cfg.gate_step
        gate_loop_cnt += 1
        loop_patient(gate_loop_cnt,gate_tmp)

def main():
    if demo_init():
        sys.exit()
    cfg=init.config()
    if cfg.gate_loop_test_mode == 0:
        patient_test_once()
    else:
        patient_test_gate_loop()

if __name__ == "__main__":
    main()
