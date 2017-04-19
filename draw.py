#!/usr/bin/env python
import _init_all as init
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as mpcm
from  pyheatmap.heatmap import HeatMap
import gen_slide_data as gen_data


def heatmap_draw(data, path):
    #draw heatmap
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    heatmap = ax.pcolor(data, cmap = plt.cm.jet)
    plt.axis('off')
    #plt.subplots_adjust(right=0.99, left=0.125, bottom=0.14, top=0.975)
    plt.draw()
    name_str = "/"
    plt.title(path[path.rfind(name_str)+1:])
    s_sharp = np.array(data).shape
    lenx = 2.0*(s_sharp[1]/100.0)
    leny = 2.0*(s_sharp[0]/100.0)
    #leny = lenx * (s_sharp[0]/s_sharp[1])
    #print leny,lenx
    #save heatmap
    fig.set_size_inches(lenx,leny)
    plt.savefig(path, dpi = 300)
    plt.clf() #close image
    plt.cla()  #clean axis
    plt.close() #close windows




def data_process(data, thread):
    #line = len(data)
    #rank = len(data[0])
    cfg = init.config()

    thresh1 = thread
    thresh2 = cfg.cell_gate
    '''
    for i in range(0, line):
        for j in range(0, rank):
            if data[i][j] < thresh2:
                data[i][j] = 0
            else :
                if data[i][j] < thresh1:
                    data[i][j] = 0.1
    #print data
    '''
    arr = np.array(data)
    arr[arr < thresh2] = 0
    arr[arr < thresh1] = cfg.cell_gate
    return arr

def draw_heatmap(data, thread, path):
    arr=data_process(data, thread)
    heatmap_draw(arr, path)

def drae_raw_heatmap(data,path):
    heatmap_draw(data,path)

def draw_slide_heatmap(dat_score,path):
    dat_num = (dat_score * 255)%256
    dat_u8 = np.array(dat_num,dtype=np.uint8)
    #print(dat_u8.dtype)
    #print(dat_u8.shape)
    imgdat_1 = dat_u8[:,:]
    cmap = mpcm.jet
    #plt.figure(figsize=(dat_u8.shape[0]/10,dat_u8.shape[1]/10))
    plt.imshow(imgdat_1,cmap=cmap)
    #plt.title("image title")
    #hot:heatmap
    #plt.set_cmap('hot')
    plt.axis('off')
    plt.savefig(path)
    #plt.show()
    plt.clf() #close image
    plt.cla()  #clean axis
    plt.close() #close windows



def draw_score_map(data,path):
    return heatmap_draw(data,path)

def test_raw_input():
    score = gen_data.gen_slide_score_from_np_matrix(8,2)

    arr_score =np.array(score)>0.0 # (score > 0.0)
    draw_slide_heatmap(arr_score,"p4n2_raw_data_image.jpg")


if __name__ == "__main__":
    test_raw_input()