# Post process
Cameylon17 post process.
## ����˵��
    ����./input�ļ��У��ļ����з���ģ�������csv�ļ�
    �����ļ���_init_all.py
    class config: 
        self.positive_gate = 0.88 #��������ʶ��ʱ����ֵ�趨
        self.transfer_gate = 0.80 #����ʶ��󣬽���ת�Ƴߴ�ʶ��ʱ����ֵ�趨
        self.get_score_mode = 0  #��ȡ�������ֵ����ͣ���Ϊ0��0Ϊ��input�ж�ȡcsv�ļ�
        self.get_csv_mode = 0    #��ȡcsv�ļ������ͣ�0��input�ж�ȡ��csvΪpatient_xxx_node_xx.csv����ʽ(17���Լ�Ϊ����ʽ)�� 1:��input�ж�ȡtest_xxx.csv��csv�ļ���c16���Լ�Ϊ����ʽ��
        self.eva_mode = 0   #�Ƿ���н��������kappaֵ���㣩��0�������н������ 1�����н�����������н������ֵ�����C16���Լ�������ground truth
        self.output_heatmap_mode = 0 #�Ƿ������ͼ, 0���������ͼ��1�������ͼ 
        self.gate_loop_test_mode = 0 #�Ƿ����ѭ����ֵ������ 0��������ѭ����1��ѭ������ֵ��������ֵ������ΧΪ self.gate_start ��self.gate_end  ��self.gate_step Ϊstep
        self.gate_start = 0.92  #ѭ����ֵ�Ŀ�ʼֵ��self.gate_loop_test_mode = 1ʱ��Ч��
        self.gate_end = 0.94    #ѭ����ֵ�Ľ���ֵ��self.gate_loop_test_mode = 1ʱ��Ч��
        self.gate_step = 0.001  #ѭ����ֵ�ı仯step��self.gate_loop_test_mode = 1ʱ��Ч��
        self.output_max_positive_region = 0 #�Ƿ���������������״���Ѿ�������������״�� 0������� 1�����
    
    class slide:
        self.start_id = 100  #patient�Ŀ�ʼid�� c17�Ĳ��Լ���start_idΪ100
        self.end_id = 200   #patient�Ľ���id����c17�Ĳ��Լ� end_idΪ200
        
## �÷�

### Cameylon16����������
    �޸����ã�����Camelyon16�Ĳ��Լ���ѭ��������ֵ0.7~1.0 stepΪ0.01�����Խ����������,�������ͼ����������ͼ��
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
        self.end_id = 27  #c16���Լ�Ϊ1~130��ŵ�slideͼ������5��slideһ��patient������patient_idΪ26��ִ�е�27����        
        
    ���нű��� python demo.py
   
    ���˵����
        ./heatmap: ���ɵ�ֱ��ͼ
        ./outs kappaֵ��ÿ����ֵ��evaluate��ground truth�ĶԱ�
        ./pN_stage ÿ����ֵ�µ�pn-stageֵ
        ./slide_info ÿ����ֵ�µ�slide��ͳ����Ϣ
        
        
    
### Cameylon17���Լ�
     �޸����ã�����Camelyon17�Ĳ��Լ������������б���ֵΪ:0.88,��������ת�ƴ�С�趨��ֵ0.80����������ͼ��������������ͼ,�����н��������c17��ground truth����
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
        self.end_id = 200 #c17���Լ�patient_id�ķ�ΧΪ100~199
     
     ���нű��� python demo.py

    
 ### auc������ʽ
    �����ű�Ϊ��evaluate_c16.py
    input�з���c16���Լ����ɵ�csv
    �÷�ʽ��ȡslide�����ļ���score��ƽ��ֵ��Ϊslide������
    MEAN_COUNT = 10 #����slide������������10��patch�ľ�ֵ��Ϊslide��scoreֵ
    ִ�нű��� python evalute_c16.py
    
 
 