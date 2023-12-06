from Plot import _plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    
    logs.append("../log/fl_attack_ActiveRate_0.04_MergeMethod_0_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-02-02:31:46.txt")
    legends.append("Typical FL")
    
#     logs.append("../log/bflc_weight_attack_Selection_1.00_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_epoch_1000_2022-04-01-01:16:19.txt")
#     legends.append(r"Strategy \uppercase\expandafter{\romannumeral1}")
    
    logs.append("../log/bflc_weight_attack_Selection_2.00_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_epoch_1000_2022-04-01-14:39:08.txt")
    legends.append(r"Strategy \uppercase\expandafter{\romannumeral2}")
    
    
    

#     _plot('loss',logs,legends,0,1000,"FL_CMFL_strategy_loss_0.01")
    _plot('accuracy',logs,legends,0,1000,"FL_CMFL_strategy_acc_0.01")