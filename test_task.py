import random

def gen_rand_score(id_1,id_2,x,y):
    return random.random()

def gen_maan_score_abs(id_1,id_2,x,y):
    rate = (abs(x-190)*abs(y-430))/90000.0
    return rate
def gen_maan_score(id_1,id_2,x,y):
    rate = (x*y)/360000.0
    return rate

def gen_section_score(id_1,id_2,x,y):
    return gen_maan_score(id_1,id_2,x,y)

def get_section_score(file_path):
    print ("path:"+file_path)
    return  gen_rand_score(0,0,0,0)

