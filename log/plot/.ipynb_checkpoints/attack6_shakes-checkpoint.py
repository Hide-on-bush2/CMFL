from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    # 攻击范围：5
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_0_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-09-02:10:16.txt")
    legends.append("FL")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_1_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-09-18:42:13.txt")
    legends.append("MEDIAN")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_2_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-10-11:38:54.txt")
    legends.append("TRIMMED")
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_3_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-11-03:57:03.txt")
    legends.append("KRUM")
    
    
    logs.append("../log/fl_attack_learningRate_0.050_ActiveRate_0.10_MergeMethod_4_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_500_2022-08-11-21:14:06.txt")
    legends.append("MULTIKRUM")
    
    logs.append("../log/bflc_weight_attack_Selection_1.00_learningRate_0.050_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_epoch_500_2022-08-07-16:27:16.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral1}")
    logs.append("../log/bflc_weight_attack_Selection_2.00_learningRate_0.050_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_6_AttackNode_0.10_AttackRange_0.00_epoch_500_2022-08-08-08:50:37.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral2}")
    
    
#     logs.append("./log/FL_attack_BigModelRate_1.00_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_MergeMethod_MULKRUM_epoch_600_2021-06-05-15:49:18.txt")
#     legends.append("multikrum")
    
    
#     _plot('accuracy',logs,legends,0,500,1,"shakes_attack6_acc")
    _plot('loss',logs,legends,0,500,1,"shakes_attack6_loss")