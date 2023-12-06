from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.04_MergeMethod_0_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_AggregationRate_0.4_epoch_2000_2022-07-09-00:22:59.txt")
    legends.append("Typical FL")
    
    logs.append("../log/bflc_weight_attack_Selection_1.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_epoch_2000_2022-07-14-00:33:45.txt")
    legends.append(r"Strategy \uppercase\expandafter{\romannumeral1}")
    
    logs.append("../log/bflc_weight_attack_Selection_2.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_epoch_2000_2022-07-10-20:00:10.txt")
    legends.append(r"Strategy \uppercase\expandafter{\romannumeral2}")
    
    
    
#     _plot('loss',logs,legends,0,2000, 1,"FL_CMFL_strategy_loss_shakes")
    _plot('accuracy',logs,legends,0,2000,1,"FL_CMFL_strategy_acc_shakes")