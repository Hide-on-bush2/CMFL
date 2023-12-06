from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    # 攻击范围：5
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_0_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-08-04-05:36:55.txt")
    legends.append("FL")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_1_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-05-10:48:33.txt")
    legends.append("MEDIAN")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_2_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-06-05:21:57.txt")
    legends.append("TRIMMED")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_3_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-06-21:38:12.txt")
    legends.append("KRUM")
    
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_4_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-07-29-09:41:59.txt")
    legends.append("MULTIKRUM")
    
    logs.append("../log/bflc_weight_attack_Selection_1.00_learningRate_0.050_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_epoch_1000_2022-07-31-10:13:50.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral1}")
    logs.append("../log/bflc_weight_attack_Selection_2.00_learningRate_0.050_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_1_AttackNode_0.10_AttackRange_0.00_epoch_1000_2022-08-02-11:11:35.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral2}")
    
    
#     logs.append("./log/FL_attack_BigModelRate_1.00_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_MergeMethod_MULKRUM_epoch_600_2021-06-05-15:49:18.txt")
#     legends.append("multikrum")
    
    
#     _plot('accuracy',logs,legends,0,500,1,"shakes_attack1_acc")
    _plot('loss',logs,legends,0,500,1,"shakes_attack1_loss")