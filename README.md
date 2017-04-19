# Post process
Cameylon17 post process.
## 配置说明
    创建./input文件夹，文件夹中放置模型输出的csv文件
    配置文件：_init_all.py
    class config: 
        self.positive_gate = 0.88 #阴性阳性识别时的阈值设定
        self.transfer_gate = 0.80 #阳性识别后，进行转移尺寸识别时的阈值设定
        self.get_score_mode = 0  #获取输入评分的类型，设为0，0为从input中读取csv文件
        self.get_csv_mode = 0    #获取csv文件的类型，0：input中读取的csv为patient_xxx_node_xx.csv的形式(17测试集为该形式)， 1:从input中读取test_xxx.csv的csv文件（c16测试集为该形式）
        self.eva_mode = 0   #是否进行结果评估（kappa值计算），0：不进行结果评估 1：进行结果评估，进行结果评估值针对于C16测试集，含有ground truth
        self.output_heatmap_mode = 0 #是否输出热图, 0：不输出热图，1：输出热图 
        self.gate_loop_test_mode = 0 #是否进行循环阈值遍历， 0：不进行循环，1：循环的阈值遍历，阈值遍历范围为 self.gate_start 到self.gate_end  以self.gate_step 为step
        self.gate_start = 0.92  #循环阈值的开始值（self.gate_loop_test_mode = 1时有效）
        self.gate_end = 0.94    #循环阈值的结束值（self.gate_loop_test_mode = 1时有效）
        self.gate_step = 0.001  #循环阈值的变化step（self.gate_loop_test_mode = 1时有效）
        self.output_max_positive_region = 0 #是否输出阳性区域的形状（已经进行扩充后的形状） 0：不输出 1：输出
    
    class slide:
        self.start_id = 100  #patient的开始id， c17的测试集，start_id为100
        self.end_id = 200   #patient的结束id，如c17的测试集 end_id为200
        
## 用法

### Cameylon16测试与评估
    修改配置：（以Camelyon16的测试集，循环遍历阈值0.7~1.0 step为0.01，并对结果进行评估,不输出热图和阳性区域图）
    class config:
        self.get_score_mode = 0
        self.get_csv_mode = 1
        self.eva_mode = 1
        self.output_heatmap_mode = 0
        self.gate_loop_test_mode = 1
        self.gate_start = 0.7
        self.gate_end = 1.0
        self.gate_step = 0.01
        self.output_max_positive_region = 0
    class slide:
        self.start_id = 0
        self.end_id = 27  #c16测试集为1~130编号的slide图，换成5个slide一个patient，最大的patient_id为26，执行到27结束        
        
    运行脚本： python demo.py
   
    结果说明：
        ./heatmap: 生成的直方图
        ./outs kappa值和每个阈值下evaluate和ground truth的对比
        ./pN_stage 每个阈值下的pn-stage值
        ./slide_info 每个阈值下的slide的统计信息
        
        
    
### Cameylon17测试集
     修改配置：（以Camelyon17的测试集，阴性阳性判别阈值为:0.88,阳性区域转移大小设定阈值0.80，生成热力图，生成阳性区域图,不进行结果评估（c17无ground truth））
     class config:
        self.positive_gate = 0.88
        self.transfer_gate = 0.80
        self.get_csv_mode = 0 
        self.eva_mode = 0 
        self.output_heatmap_mode = 1
        self.gate_loop_test_mode = 0
        self.output_max_positive_region = 1
     class slide:
        self.start_id = 100
        self.end_id = 200 #c17测试集patient_id的范围为100~199
     
     运行脚本： python demo.py

    
 ### auc评估方式
    评估脚本为：evaluate_c16.py
    input中放置c16测试集生成的csv
    该方式是取slide中最大的几个score的平均值作为slide的评分
    MEAN_COUNT = 10 #设置slide的评分由最大的10个patch的均值作为slide的score值
    执行脚本： python evalute_c16.py
    
 
 