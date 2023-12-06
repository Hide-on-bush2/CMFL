from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    # 攻击范围：5
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_0_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-05-02-01:11:09.txt")
    legends.append("FL")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_1_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-05-03-02:00:31.txt")
    legends.append("MEDIAN")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_2_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-05-04-05:12:07.txt")
    legends.append("TRIMMED")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_3_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-05-05-05:50:53.txt")
    legends.append("KRUM")
    
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_4_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-05-06-06:42:30.txt")
    legends.append("MULTIKRUM")
    
    logs.append("../log/bflc_weight_attack_Selection_1.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_epoch_2000_2022-04-29-19:11:22.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral1}")
    logs.append("../log/bflc_weight_attack_Selection_2.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_epoch_2000_2022-04-30-22:01:29.txt")
    legends.append(r"CMFL\uppercase\expandafter{\romannumeral2}")
    
    
#     logs.append("./log/FL_attack_BigModelRate_1.00_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_MergeMethod_MULKRUM_epoch_600_2021-06-05-15:49:18.txt")
#     legends.append("multikrum")
    
    
    _plot('accuracy',logs,legends,0,2000,1,"sent140_attack_method_acc_2_2000round")
#     _plot('loss',logs,legends,0,2000,1,"new_sent140_attack_method_loss_2_2000round")