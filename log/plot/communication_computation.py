import numpy as np
import matplotlib.pyplot as plt



labels = ["FedAvg","BrainTorrent","GossipFL", "CMFL"]  # x值取默认值

training_time = 0.05
cmfl_aggregation_time = 0.025
fl_aggregation_time = 0.04
scoring_time = 0.026
single_transmission_time = 0.02 #0.002
committee_num = 43 #43
#     multikrum_aggregation_time = 3.5
activated_client_num = 65 #65

fl_communication_time = single_transmission_time*2*1000
fl_computation_time = (training_time + fl_aggregation_time)*1000

cmfl_communication_time = single_transmission_time * (committee_num+1)*1000
cmfl_computation_time = (training_time + scoring_time + cmfl_aggregation_time)*1000

braintorrent_communication_time = single_transmission_time*activated_client_num*1000
braintorrent_computation_time = (training_time+fl_aggregation_time)*1000

gossip_communication_time = single_transmission_time*(activated_client_num-1)*1000
gossip_computation_time = (training_time+fl_aggregation_time)*1000



men_means = [fl_computation_time,braintorrent_computation_time,gossip_computation_time,cmfl_computation_time]
women_means = [fl_communication_time, braintorrent_communication_time, gossip_communication_time, cmfl_communication_time]

width = 0.35       # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots()
ax.bar(labels, men_means, width,label='Computation')
ax.bar(labels, women_means, width, bottom=men_means,label='Communication')

ax.legend()
#ax.text(.87,-.08,'\nVisualization by DataCharm',transform = ax.transAxes,
        #ha='center', va='center',fontsize = 5,color='black',fontweight='bold',family='Roboto Mono')

plt.ylabel('Time (sec)')
plt.savefig('./img/communication_computation_sent140_1.png', dpi=300, bbox_inches = 'tight')
