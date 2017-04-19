import numpy as np
import os
import draw
import _init_all as init
import gen_name as gname
from scipy import ndimage as nd
from skimage import measure

def get_positive_count(data):
    dat_arr = np.array(data)
    print (dat_arr.shape)

def gen_mask_data(dat):
    #cfg = init.config()
    #dat_mask = dat> cfg.transfer_gate
    dat_mask = dat > 0.2
    return dat_mask

def matrix_inflate(mask):
    arr = np.array(mask)
    new_arr =np.zeros((arr.shape[0]*2 , arr.shape[1]*2),dtype="uint")
    #print arr.shape
    #print new_arr.shape
    for x in range(arr.shape[1]):
        for y in range(arr.shape[0]):
            new_arr[2*y][2*x] = arr[y][x]
            new_arr[2*y+1][2*x]=arr[y][x]
            new_arr[2*y][2*x+1] =arr[y][x]
            new_arr[2*y+1][2*x+1] =arr[y][x]
    return new_arr

def draw_region_heatmap(evaluation_mask,(patient_id,node_id)):
    path_info = init.path_info()
    #max_label = np.amax(evaluation_mask)
    arr_mask = evaluation_mask >=1
    score_arr = arr_mask * 1.0
    file_name = "Patient_%03d_Node_%d_positive_region.jpg"%(patient_id,node_id)
    img_path = os.path.join(path_info.heatmap,file_name)
    draw.draw_score_map(score_arr,img_path)

def draw_region_heatmap_with_hole(arr,(patient_id,node_id)):
    path_info = init.path_info()
    #max_label = np.amax(evaluation_mask)
    if arr.shape[0] == 1:
        return
    #arr_mask = (raw_score or eva_score)
    score_arr = arr * 1.0
    file_name = "Patient_%03d_Node_%d_hole_positive_region.jpg"%(patient_id,node_id)
    img_path = os.path.join(path_info.heatmap,file_name)
    draw.draw_score_map(score_arr,img_path)


def draw_max_region_heatmap(shape,coords,(patient_id,node_id)):
    path_info = init.path_info()
    arr = np.zeros(shape)
    arr_coords = np.array(coords)
    for cnt in range(arr_coords.shape[0]):
        arr[arr_coords[cnt][0]][arr_coords[cnt][1]] = 0.99
    file_name = "Patient_%03d_Node_%d_max_positive_region.jpg"%(patient_id,node_id)
    img_path = os.path.join(path_info.heatmap,file_name)
    draw.draw_score_map(arr,img_path)

def calc_slide_max_len_and_max_area(mask_dat,(patient_id,node_id)):
    cfg = init.config()
    #arr_mask = np.array(mask_dat)
    #print "metastasis check shape: %s"%(str(arr_mask.shape))
    #print "input:"
    #print mask_dat
    Threshold = cfg.expand_size *(cfg.inflate_level + 1) / (cfg.gap_size * cfg.step * 2)
    if Threshold >= 1.0:
        reverse = 1 - mask_dat
        distance = nd.distance_transform_edt(reverse)
        binary = distance < Threshold
        #sum_arr = (binary or mask_dat)
        filled_image = nd.morphology.binary_fill_holes(binary)
    else:
        #sum_arr = 0
        filled_image =mask_dat*1
    #print filled_image
    evaluation_mask = measure.label(filled_image, connectivity=2)

    #print evaluation_mask
    #print "label out:"
    #print evaluation_mask
    max_label = np.amax(evaluation_mask)
    properties = measure.regionprops(evaluation_mask)
    max_axis_len = 0
    max_area = 0
    max_area_perimeter = 0
    max_coords_len = 0
    max_i = 0

    for i in range(max_label):
        if properties[i].major_axis_length > max_axis_len:
            max_i = i
            max_axis_len = properties[i].major_axis_length
            coot = properties[i].coords.T
            min_coo = min(coot[0])
            max_coo = max(coot[0])
            tmp_coords_len1 = 1 + max_coo - min_coo
            min_coo = min(coot[1])
            max_coo = max(coot[1])
            tmp_coords_len2 = 1 + max_coo - min_coo
            if tmp_coords_len2 > tmp_coords_len1:
                max_coords_len = tmp_coords_len2
            else:
                max_coords_len = tmp_coords_len1
        if properties[i].area > max_area:
            max_area = properties[i].area
            max_area_perimeter =  int(properties[i].perimeter)
    #print max_area_perimeter
    #print int(1+Threshold/2)
    if cfg.output_max_positive_region:
        draw_region_heatmap(evaluation_mask, (patient_id, node_id))
        #draw_region_heatmap_with_hole(sum_arr,(patient_id,node_id))
        draw_max_region_heatmap(mask_dat.shape,properties[max_i].coords,(patient_id,node_id))
    max_area = max_area - (max_area_perimeter - int(1 + Threshold/2))*int(Threshold)
    print "axis_len: %3.2lf coords_len:%3.2lf "%(max_axis_len,max_coords_len)
    return max_axis_len,max_area


def calc_slide_type(max_len,max_area):
    '''
    :param max_len:The biggest axis len in positive regions
    :param max_area:The biggest area in positive regions
    :return:sort type
            0: negative
            1:ITC
            2:Micro
            3:Macro
    '''
    cfg = init.config()
    positive_size = max_len *cfg.gap_size*cfg.step/(cfg.inflate_level+1)
    positive_cell_cnt = max_area * cfg.patch_tumor_cell_cnt/(pow((cfg.inflate_level+1),2))
    print "max patch count:%3.2lf , max axis distance is :%4.2lf um"%(max_len,positive_size)
    if  positive_size == 0:
        #negative
        return 0
    elif positive_size < 275.0:
        if cfg.sort_mode == 0:
            if positive_cell_cnt > 200:
                # Micro
                return 2
            else:
                # ITC
                return 1
        else:
            #ITC
            return 1
    elif positive_size < 2075.0:
        # Micro
        return 2
    else:
        #Macro
        return 3


def get_slide_type_str(slide_type):
    cfg = init.config()
    if slide_type > 3:
        print "ERR: slide type fail!"
    return cfg.slide_type[slide_type]

def save_slide_info(patient_id,node_id,max_len,max_area,slide_type_str):
    cfg = init.config()
    axis_size = max_len*cfg.gap_size*cfg.step/(cfg.inflate_level+1)
    #gate = init.get_positive_gate()
    #path_info = init.path_info()
    #file_name = "%s_%1.4lf.csv" %(cfg.slide_info_file,gate)
    #path_file = os.path.join(path_info.slide_info,file_name)
    path_file = gname.get_slide_info_file_path()
    positive_cell_cnt = max_area * cfg.patch_tumor_cell_cnt / (pow((cfg.inflate_level + 1), 2))
    if os.path.exists(path_file):
        fd_file = open(path_file,'ab+')
    else:
        fd_file = open(path_file,'ab+')
        fd_file.write("Patient_id,Node_id,Axis_patch_cnt,Axis_size(um),Region_area,Cell_cnt,Slide_type\n")
    write_context = "%d,%d,%3.2lf,%lf,%d,%d,%s\n"%(patient_id,node_id,max_len,axis_size,max_area,int(positive_cell_cnt),slide_type_str)
    fd_file.write(write_context)
    fd_file.close()

def get_slide_type(patient_id,node_id,score):
    #gen mask array
    mask_score = gen_mask_data(score)
    inflate_mask = matrix_inflate(mask_score)
    #get the max axis len, max area
    max_len, max_area = calc_slide_max_len_and_max_area(inflate_mask,(patient_id,node_id))
    #calculate the slide type
    slide_type = calc_slide_type(max_len,max_area)
    slide_type_str = get_slide_type_str(slide_type)
    # save the slide information into a csv file
    save_slide_info(patient_id,node_id,max_len,max_area,slide_type_str)
    print "Classification type :%s " %(slide_type_str)
    return slide_type_str

