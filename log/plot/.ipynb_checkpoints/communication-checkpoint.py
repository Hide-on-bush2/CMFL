from Plot import _realtime_plot

if __name__ == "__main__":
    #画图
    logs = []
    legends = []
    
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.04_MergeMethod_0_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-09-21:30:45.txt")
    legends.append("Typical FL")
    
#     logs.append("../log/bflc_weight_distance_big_0.25_client_0.10_k_20_epoch_600_2021-04-30-15:10:43.txt")
#     legends.append(r"Strategy \uppercase\expandafter{\romannumeral1}")
    
    logs.append("../log/bflc_weight_attack_Selection_2.00_learningRate_0.005_CommitteeNode_0.40_AggregationNode_0.40_ActiveRate_0.10_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_epoch_1000_2022-04-10-07:57:43.txt")
    legends.append("CMFL")
    
#     logs.append("../MajorRevisionLog/FL_attack_BigModelRate_1.00_ActiveRate_0.02_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_MergeMethod_MULKRUM_epoch_600_2022-04-23-21:47:01.txt")
#     legends.append("FL-MultiKrum")
    
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.04_MergeMethod_0_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-04-09-21:30:45.txt")
    legends.append("BrainTorrent")
    logs.append("../log/fl_attack_learningRate_0.005_ActiveRate_0.05_MergeMethod_0_AttackMethod_0_AttackNode_0.00_AttackRange_0.00_AggregationRate_0.4_epoch_1000_2022-05-05-18:06:33.txt")
    legends.append("Gossip")
    
    
    
    
    training_time = 0.05
    cmfl_aggregation_time = 0.025
    fl_aggregation_time = 0.04
    scoring_time = 0.026
    single_transmission_time = 0.02 #0.002
    committee_num = 43 #43
#     multikrum_aggregation_time = 3.5
    activated_client_num = 65 #65
#     braintorrent_communication_time_one_round = 1
#     for i in range(1,activated_client_num+1):
#         braintorrent_communication_time_one_round = braintorrent_communication_time_one_round * i
    
    total_time_oneround_cmfl = training_time + single_transmission_time * committee_num + scoring_time + cmfl_aggregation_time + single_transmission_time
    total_time_oneround_fl = training_time + single_transmission_time + fl_aggregation_time + single_transmission_time
#     total_time_onround_multikrum = training_time + single_transmission_time + multikrum_aggregation_time + single_transmission_time
    total_time_onround_braintorrent = training_time + single_transmission_time*activated_client_num + fl_aggregation_time
    total_time_onround_gossip = training_time + single_transmission_time*(activated_client_num-1) + fl_aggregation_time
    
    total_times = [total_time_oneround_fl,total_time_oneround_cmfl,total_time_onround_braintorrent,total_time_onround_gossip]
    
    _realtime_plot('accuracy',logs,total_times,legends,0,1000,"communication_sent140_1")
    
    
    
    
    
    