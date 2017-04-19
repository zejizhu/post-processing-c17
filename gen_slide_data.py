import _init_all as init
import os
import math
import numpy as np
import draw
import gen_name as gname
import matplotlib.image as mpimg
import test_task
import openslide


def gen_sction_info(patient_id,node_id,section_x,section_y,step,score):
    x_pixel =section_x*step
    y_pixel =section_y*step
    str_info ="patient_"+str(patient_id)+"_node_"+str(node_id)+"_L00_X"+str(x_pixel)+"_Y"+str(y_pixel)+".jpg  :"+str(score)+"\n"
    return str_info

def gen_section_img_name(patient_id,node_id,section_x,section_y):
    cfg = init.config()
    step = cfg.step
    x_pixel = section_x * step
    y_pixel = section_y * step
    file_name = "patient_"+str(patient_id).zfill(3)+"_node_"+str(node_id)+"_L00_X"+str(x_pixel).zfill(6)+"_Y"+str(y_pixel).zfill(6)+".jpg"
    return file_name


def get_section_score(patient_id,node_id,section_x,section_y):
    path_info = init.path_info()
    file_name = gen_section_img_name(patient_id,node_id,section_x,section_y)
    file_path = os.path.join(path_info.input,file_name)
    if os.path.exists(file_path):
        return test_task.get_section_score(file_path)
    else:
        return test_task.gen_maan_score(patient_id,node_id,section_x,section_y)

'''generate the score'''

def gen_slide_score_random(patient_id,node_id):
    #slide_info = init.slide()
    cfg = init.config()
    path_info = init.path_info()
    slide_size = init.get_patient_img_param(patient_id,node_id)
    x_cnt = slide_size[2]/cfg.step
    y_cnt = slide_size[3]/cfg.step

    '''generate score from the test_task'''
    file_name = gname.gen_section_score_txt_name(patient_id,node_id,cfg.step)
    txt_path = os.path.join(path_info.raw_score,file_name)
    fd_txt =open(txt_path,'w+')
    print("File name is :"+txt_path)
    file_name = gname.gen_section_score_dat_name(patient_id,node_id,cfg.step)
    dat_path = os.path.join(path_info.raw_score, file_name)
    fd_dat = open(dat_path, 'w+')
    print("File name is :" + dat_path)
    arr_score= np.zeros((y_cnt,x_cnt))
    for section_y in range(y_cnt):
        for section_x in range(x_cnt):
            #section_score = test_task.gen_section_score(patient_id,node_id,section_x,section_y)
            section_score = get_section_score(patient_id,node_id,section_x,section_y)
            str_txt = gen_sction_info(patient_id,node_id,section_x,section_y,cfg.step,section_score)
            fd_txt.write(str_txt)
            arr_score[section_y][section_x] = section_score
            fd_dat.write(str(section_score))
            if section_x != (x_cnt -1):
                fd_dat.write(",")
        fd_dat.write("\n")
    fd_txt.close()
    fd_dat.close()
    return arr_score

def gen_slide_score_from_img(patient_id,node_id):
    #cfg = init.config()
    path_info = init.path_info()
    img_name = "test_%02d_%d.jpg"%(patient_id,node_id)
    file_path = os.path.join(path_info.config,img_name)
    imgdat = mpimg.imread(file_path)
    newdat = imgdat[:,:,1]
    print np.array(newdat).shape
    slide_score = newdat/256.0
    return  slide_score


def matrix_deflate(inarr_mask,level=1):
    mask_arr =np.array(inarr_mask)
    #if 255 in arr:
    #    mask_arr =(arr >1)
    #if 1 in arr:
    #    mask_arr = (arr==1)
    step = pow(2,level)
    sum_gate = 0.4*pow(step,2)
    out_arr = np.zeros((int(mask_arr.shape[0]/step),int(mask_arr.shape[1]/step)))
    for y_cnt in range(int(mask_arr.shape[0]/step)):
        for x_cnt in range(int(mask_arr.shape[1]/step)):
            mask_sum = sum(sum(mask_arr[y_cnt*step:(y_cnt+1)*step,x_cnt*step:(x_cnt+1)*step]))
            if mask_sum > sum_gate:
                out_arr[y_cnt][x_cnt] = 1
            else:
                out_arr[y_cnt][x_cnt] = 0
    return out_arr


def gen_slide_score_from_mask_img(patient_id,node_id):
    cfg = init.config()
    path_info = init.path_info()
    if cfg.get_csv_mode ==0:
        mask_name = "patient_%03d_node_%d_mask.tif" % (patient_id, node_id)
    elif cfg.get_csv_mode == 1:
        test_cnt = patient_id*5+node_id
        mask_name = "test_%03d_mask.tif"%test_cnt
    else:
        print "get raw score mode fail!"
        mask_name = "null"

    file_path = os.path.join(path_info.mask_dir,mask_name)
    if os.path.exists(file_path):
        print "open mask image :%s" %(file_path)
        slide = openslide.open_slide(file_path)
        level_real = int(math.log(cfg.step, 2))
        if slide.level_count > level_real:
            level = level_real
        else:
            level = slide.level_count -1

        dims = slide.level_dimensions[level]
        pixelarray = np.zeros(dims[0]*dims[1], dtype=np.int8)
        pixelarray = np.array(slide.read_region((0,0), level, dims)) # read all image to pixelarry

        diff_level = level_real - level
        #np.save("patient_%d_node_%d_array_npsave.npy"%(patient_id,node_id),pixelarray[:,:,0])
        '''
        if 1 in pixelarray[:,:0]:
            pixel_mask = (pixelarray[:,:,0] == 1)
            print "1 in mask image"
        else:
            pixel_mask = (pixelarray[:,:,0] > 10)
            print  "1 not in mask image"
        '''
        pixel_mask = pixelarray[:,:,0] > 100
        if 1 in pixel_mask:
            print "the mask image : 0-255"
        else:
            pixel_mask = (pixelarray[:, :, 0] == 1)
            print "positive region is label 1"

        if diff_level != 0:
            outs_arr = matrix_deflate(pixel_mask,diff_level)
        else:
            #outs_arr = pixelarray[:,:,1]/256.0
            outs_arr = pixel_mask
        #print "this mask image shape:%s"%(str(outs_arr.shape))
        #slide_score = pixelarray[:, :, 1] / 256.0
        slide_score = outs_arr*1.0
    else:
        step = cfg.step
        pat_param = init.get_patient_img_param(patient_id,node_id)
        x_cnt = int(pat_param[cfg.pst_xsize] / step)
        y_cnt = int(pat_param[cfg.pst_ysize] / step)
        slide_score = np.zeros((y_cnt,x_cnt))
    return slide_score

def gen_slide_score_form_csv(patient_id,node_id):
    path_info = init.path_info()
    cfg = init.config()
    step =cfg.step
    max_x = 0
    max_y = 0
    if cfg.get_csv_mode == 0:
        file_name = gname.gen_slide_score_file_name(patient_id,node_id,step)
        if file_name != "null":
            max_x = int(file_name[29:32])
            max_y = int(file_name[34:37])

    elif cfg.get_csv_mode == 1:
        file_name = gname.get_slide_score_test_csv_name(patient_id,node_id,step)
        if file_name != "null":
            max_x = int(file_name[19:22])
            max_y = int(file_name[24:27])
            #max_x = int(file_name[19:23])
            #max_y = int(file_name[25:29])

    else:
        print "get the csv file fail!"
        file_name = "xxx"

    dat_path = os.path.join(path_info.input,file_name)
    if os.path.exists(dat_path):
        print "Read csv [patient:%d node:%d] %s "%(patient_id,node_id,dat_path)
        score_data = np.loadtxt(dat_path,delimiter=',',usecols=(0,1,2))
        # get the max size from the input csv
        if (max_x + max_y) == 0:
            max_x = 1 + int(max(score_data.T[0])/cfg.step)
            max_y = 1 + int(max(score_data.T[1])/cfg.step)
        #print  "max is :%d %d \n" %(max_x,max_y)
    else:
        max_x = 100
        max_y = 100
        score_data = np.zeros((max_y,max_x))

    '''
    # get the image size from the config
    slide_cfg = init.get_patient_img_param(patient_id,node_id)
    slide_cfg_arr = np.array(slide_cfg)

    #print slide_cfg_arr
    if slide_cfg_arr[0] != patient_id:
        print "cannot find patient: %03d node:%02d config."%(patient_id,node_id)
    # get the max size from the config file
    x_cnt = int(slide_cfg_arr[cfg.pst_xsize]/step)
    y_cnt = int(slide_cfg_arr[cfg.pst_ysize]/step)
    '''
    x_cnt = max_x
    y_cnt = max_y

    slide_score = np.zeros((y_cnt,x_cnt))
    #print "this image shape is :[%d * %d]"%(y_cnt,x_cnt)
    for num_id in range(score_data.shape[0]):
        x_pst = int(score_data[num_id][0]/step)
        y_pst = int(score_data[num_id][1]/step)
        if y_pst >= y_cnt:
            print  "y:max:%d real:%d "%(y_cnt,y_pst)
        if x_pst >= x_cnt:
            print  "x:max:%d real:%d "%(x_cnt,x_pst)
        slide_score[y_pst][x_pst] =score_data[num_id][2]
    file_name = gname.gen_section_score_npy_name(patient_id,node_id,step)
    file_path = os.path.join(path_info.raw_score,file_name)
    np.save(file_path,slide_score)
    return  slide_score

def gen_slide_score_from_np_matrix(patient_id,node_id):
    cfg = init.config()
    path_info = init.path_info()
    step =cfg.step
    file_name = gname.gen_section_score_npy_name(patient_id,node_id,step)
    file_path = os.path.join(path_info.raw_score,file_name)
    slide_score = np.load(file_path)
    return slide_score


def gen_slide_score(patient_id,node_id):
    cfg = init.config()
    if cfg.get_score_mode == 0:
        slide_score = gen_slide_score_form_csv(patient_id,node_id)
    elif cfg.get_score_mode == 1:
        slide_score = gen_slide_score_from_np_matrix(patient_id,node_id)
    elif cfg.get_score_mode == 2:
        slide_score = gen_slide_score_from_img(patient_id,node_id)
    elif cfg.get_score_mode == 3:
        slide_score = gen_slide_score_random(patient_id, node_id)
    else:
        slide_score = gen_slide_score_from_mask_img(patient_id, node_id)
    return  slide_score

def test_gen_img_score():
    gen_slide_score_from_img(1,1)


def test():
    print (gname.gen_section_score_txt_name(10,15,256))
    print (gname.gen_section_score_dat_name(10,15,128))
    if 1:
        patient_id =1
        node_id  = 2
        path_info = init.path_info()
        arr_score = gen_slide_score(patient_id,node_id)
        #arr_score = test_gen_img_score()
        #draw.draw_slide_heatmap(arr_score)
        file_name = gname.gen_heatmap_img_name(patient_id,node_id, 256, 0.2)
        dat_path = os.path.join(path_info.heatmap,file_name)
        draw.draw_heatmap(arr_score,0.2,dat_path)
        file_name = gname.gen_heatmap_img_name(patient_id,node_id,256,0.7)
        dat_path = os.path.join(path_info.heatmap,file_name)
        draw.draw_heatmap(arr_score,0.7,dat_path)
    else:
        #gen_section_img_name(0,0,0,0)
        #gen_section_img_name(1,2,10,32)
        gen_slide_score(1,2)


def read_save_image(patient_id,node_id):
    score =  gen_slide_score_from_img(patient_id,node_id)


if __name__  ==  "__main__":
    #test()
    #slide_core = test_gen_img_score()
    init.all_dir_check()
    test()

