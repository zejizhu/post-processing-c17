import os
import _init_all as init
import gen_name as gname
import  evaluate as eva

def stat_slide_info(gt_type,eva_type):
    stat_cfg = init.stat_config()
    path_info = init.path_info()
    outs_path = os.path.join(path_info.outs,stat_cfg.info_file)
    vs_file = gname.get_VS_file_path()
    files = open(vs_file, "r")
    fd_outs = open(outs_path,"ab+")
    #print  "type: %d %d "%(gt_type,eva_type)
    if stat_cfg.gt_itc_mode == 0:
        GtStr = stat_cfg.GT_str16
    else:
        GtStr = stat_cfg.GT_str17

    match_cnt = 0
    match_id_str = ""
    for line in files:
        st = line.split(",")
        #print "[%s %s] [%s %s]" %(st[0],GtStr[gt_type],st[1],stat_cfg.eva_str[eva_type])
        if str(st[0]) == str(GtStr[gt_type]):
            if str(st[1]) == str(stat_cfg.eva_str[eva_type]):
                match_cnt += 1
                match_id_str = "%s,%d"%(match_id_str,int(st[2]))
    context = "%s,%s,%d,%s\n"%(GtStr[gt_type],stat_cfg.eva_str[eva_type],match_cnt,match_id_str)
    fd_outs.write(context)
    fd_outs.close()
    files.close()
    return  match_cnt

def write_kappa_score(rate,kappa):
    stat_cfg = init.stat_config()
    #path_info = init.path_info()
    #outs_path = os.path.join(path_info.outs,stat_cfg.info_file)
    outs_path = gname.get_result_info_path()
    fd_outs = open(outs_path,"ab+")
    gate = init.get_positive_gate()
    context = "Threshold:,%lf\n"%(gate)
    context = context + "Kappa:,%1.5lf\n" %(kappa)
    context = context + "\n\n"
    context = context + "#,#,#,#,#,#,#,#,#,#,#,#,#,#\n"
    fd_outs.write(context)
    fd_outs.close()
    outs_path = gname.get_kappa_file_path()
    fd_outs = open(outs_path,"ab+")
    context = "%1.4lf,%lf,%lf\n"%(gate,kappa,rate)
    fd_outs.write(context)
    fd_outs.close()



def write_stat_sum(cnt):
    val_all = sum(cnt) * 1.0
    match_cnt = cnt[0] + cnt[1] + cnt[2] + cnt[3] + 0.0
    rate = match_cnt / val_all
    outs_path = gname.get_result_info_path()
    fd_outs = open(outs_path, "ab+")
    context = "All:,%d\n" % (val_all)
    context = context + "match:,%d\n" % (match_cnt)
    context = context + "match rate:%1.5lf\n" % (rate)
    fd_outs.write(context)
    fd_outs.close()
    return rate


def write_stat_info(kappa):
    stat_cfg = init.stat_config()
    vs_file = gname.get_VS_file_path()
    cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if os.path.exists(vs_file):
        #files = open(vs_file,"r")
        if stat_cfg.gt_itc_mode == 0:
            cnt[0]= stat_slide_info( 0, 0)  # negative #negative
            cnt[1]= stat_slide_info( 1, 2)  # micro  #micro
            cnt[2] = stat_slide_info( 2, 3)  # macro #macro

            cnt[3] =stat_slide_info( 0, 1)  # negative #itc
            cnt[4] =stat_slide_info( 0, 2)  # negative #micro
            cnt[5] =stat_slide_info( 0, 3)  # negative #macro
            cnt[6] =stat_slide_info( 1, 3)  # micro  #macro

            cnt[7] =stat_slide_info( 2, 2)  # macro #micro
            cnt[8] =stat_slide_info( 2, 1)  # macro #itc
            cnt[9] =stat_slide_info( 2, 0)  # macro #negative

            cnt[10] =stat_slide_info( 1, 1)  # micro  #itc
            cnt[11] =stat_slide_info( 1, 0)  # micro  #negative
        #files.close()
        elif stat_cfg.gt_itc_mode == 1:
            cnt[0]= stat_slide_info( 0, 0)  # negative #negative
            cnt[1]= stat_slide_info( 1, 1)  # itc  #itc
            cnt[2] = stat_slide_info( 2, 2)  # micro #micro

            cnt[3] =stat_slide_info( 3, 3)  # macro #macro
            cnt[4] =stat_slide_info( 0, 1)  # negative #itc
            cnt[5] =stat_slide_info( 0, 2)  # negative #micro
            cnt[6] =stat_slide_info( 0, 3)  # negative  #macro

            cnt[7] =stat_slide_info( 1, 0)  # itc #negative
            cnt[8] =stat_slide_info( 1, 2)  # itc #micro
            cnt[9] =stat_slide_info( 1, 3)  # itc #macro

            cnt[10] =stat_slide_info( 2, 0)  # micro  #negative
            cnt[11] =stat_slide_info( 2, 1)  # micro  #itc
            cnt[12] =stat_slide_info( 2, 3)  # micro  #macro
            cnt[13] =stat_slide_info( 3, 0)  # macro  #negative
            cnt[14] =stat_slide_info( 3, 1)  # macro  #itc
            cnt[15] =stat_slide_info( 3, 2)  # macro  #micro

        rate = write_stat_sum(cnt)

        write_kappa_score(rate ,kappa)

    else:
        print "cannot find file :%s "%(vs_file)



def write_pn_stage_kappa():
    path_info = init.path_info()
    stat_cfg = init.stat_config()
    gate = init.get_positive_gate()
    c17_gt_path = os.path.join(path_info.config,stat_cfg.c17_pnstage)
    c17_eva_path = gname.get_pnstage_file_path()
    kappa_score = eva.pnstage_kappa(c17_eva_path,c17_gt_path)
    file_path = gname.get_pnstage_kappa_file_path()
    result_pnstage_kappa = open(file_path,"ab+")
    context_str = "%lf,%lf\n" %(gate,kappa_score)
    result_pnstage_kappa.write(context_str)
    result_pnstage_kappa.close()

