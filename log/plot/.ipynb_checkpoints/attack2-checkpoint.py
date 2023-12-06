from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    # 攻击范围：5
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_0_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-16-07:59:21.txt")
    legends.append("FL")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_1_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-16-18:53:43.txt")
    legends.append("MEDIAN")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_2_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-17-05:52:28.txt")
    legends.append("TRIMMED")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_3_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-22-03:01:52.txt")
    legends.append("KRUM")
    
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.10_MergeMethod_4_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-17-16:11:13.txt")
    legends.append("MULTIKRUM")
    
    logs.append("../log/bflc_weight_attack_Selection_1.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_epoch_1000_2022-04-15-21:57:37.txt")
    legends.append("CMFL1")
#     logs.append("../MajorRevisionLog/bflc_weight_attack2_BigModelRate_1.00_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_1_AttackNode_0.10_AttackRange_0.50_epoch_600_2022-03-18-15:45:19.txt")
#     legends.append("CMFL2")
    
    
#     logs.append("./log/FL_attack_BigModelRate_1.00_ActiveRate_0.10_AttackMethod_2_AttackNode_0.10_AttackRange_0.00_MergeMethod_MULKRUM_epoch_600_2021-06-05-15:49:18.txt")
#     legends.append("multikrum")
    
    
#     _plot('accuracy',logs,legends,0,1000,"sent140_attack_method_acc_2")
    _plot('loss',logs,legends,0,1000,"new_sent140_attack_method_loss_2")