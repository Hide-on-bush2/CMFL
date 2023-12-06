import os, sys
import re
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib import rcParams
from mpl_toolkits.axisartist.axislines import Subplot

matplotlib.rc('xtick', labelsize=17) 
matplotlib.rc('ytick', labelsize=17) 


def parse_log(file_name):
    rounds = []
    accu = []
    loss = []

    for line in open(file_name, 'r'):
#         print(line)
        search_round = re.search(r'\[epoch (.*), 10000 inst\] Testing model',line, re.M|re.I)
        search_metric = re.search(r'Testing model accuracy: (.*), Loss: (.*)',line, re.M|re.I)
        if search_round:
            rounds.append(int(search_round.group(1)))
        if search_metric:
            accu.append(float(search_metric.group(1)))
            loss.append(float(search_metric.group(2))) 
    
    return rounds, loss, accu

def parse_log2(file_name):
    rounds = []
    accu = []
    loss = []

    for line in open(file_name, 'r'):
        search_round = re.search(r'\[epoch (.*), 10000 inst\] Testing B-Model',line, re.M|re.I)
        search_metric = re.search(r'Testing B-Model accuracy: (.*), Loss: (.*)',line, re.M|re.I)
        if search_round:
            rounds.append(int(search_round.group(1)))
        if search_metric:
            accu.append(float(search_metric.group(1)))
            loss.append(float(search_metric.group(2))) 
    return rounds, loss, accu

def parse_log3(file_name):
    rounds = []
    malicious_train_clients = []
    malicious_committee_clients = []
    malicious_average_clients = []
    for line in open(file_name, 'r'):
        search_round = re.search(r'\[epoch (.*), 10000 inst\] Testing model',line, re.M|re.I)
        search_metric = re.search(r'malicious train nodes: (.*), malicious committee nodes: (.*), malicious average nodes: (.*)', line, re.M|re.I)
        if search_round:
            rounds.append(int(search_round.group(1)))
        if search_metric:
            malicious_train_clients.append(float(search_metric.group(1)))
            malicious_committee_clients.append(float(search_metric.group(2)))
            malicious_average_clients.append(float(search_metric.group(3)))
            
             
    return malicious_train_clients, malicious_committee_clients, malicious_average_clients

def _plot3(logs,x_des,img_name):
    colors = ["red","blue","green","black","gray","brown","darkred"]
    idx = 0
    f = plt.figure(1)
    
    log_size = len(logs)
    ax2 = ax.twinx()
    malicious_train_clients = []
    malicious_committee_clients = []
    malicious_average_clients = []
    acc = []
    
    for i in range(log_size):
        t_malicious_train_clients, t_malicious_committee_clients, t_malicious_average_clients = parse_log3(logs[i])
        malicious_train_clients.append(np.mean(t_malicious_train_clients))
        malicious_committee_clients.append(np.mean(t_malicious_committee_clients))
        malicious_average_clients.append(np.mean(t_malicious_average_clients))
        t_rounds, t_loss, t_acc = parse_log(logs[i])
        acc.append(sum(t_acc[-5:])/5)
        
    
    ax.plot(np.asarray(x_des), np.asarray(malicious_train_clients), linewidth=1.0, label=r"$N_1$", color="red", linestyle='-')
    ax.plot(np.asarray(x_des), np.asarray(malicious_committee_clients), linewidth=1.0, label=r"$N_2$", color="blue", linestyle='-')
    ax.plot(np.asarray(x_des), np.asarray(malicious_average_clients), linewidth=1.0, label=r"$N_3$", color="green", linestyle='-')
    
    ax2.plot(np.asarray(x_des), np.asarray(acc), linewidth=1.0, label="Accuracy", color="gray", linestyle='--')
    
    plt.tick_params(labelsize=18)
    ax.set_ylabel('Client Number', fontsize=20)
    ax2.set_ylabel('Performance', fontsize=20)
    
#     if idx == 4:
#         plt.legend(fontsize=22)
    ax.legend()
    ax2.legend()
    plt.tight_layout()
    plt.savefig("./img/" + img_name + ".png")
    plt.show()

def _plot(typ,logs,description,begin_pos,end_pos,skip_points,img_name):
    colors = ['black', 'red', 'violet', 'indigo', 'blue', 'green', 'orange']
    plt.rcParams['text.usetex']=True
    idx = 0
    f = plt.figure(1)
    
#     ax = plt.subplot()
    log_size = len(logs)
    rounds = []
    losses = []
    test_accuracies = []
    for log in logs:
        t_rounds, t_losses, t_test_accuracies = parse_log(log)
        # cut off
        t_rounds = t_rounds[begin_pos:end_pos]
        t_losses = t_losses[begin_pos:end_pos]
        t_test_accuracies = t_test_accuracies[begin_pos:end_pos]
        #     skip some points
        t_rounds = [t_rounds[i] for i in range(len(t_rounds)) if i % skip_points == 0]
        t_test_accuracies = [t_test_accuracies[i] for i in range(len(t_test_accuracies)) if i % skip_points == 0]
        t_losses = [t_losses[i] for i in range(len(t_losses)) if i % skip_points == 0]
        rounds.append(t_rounds)
        losses.append(t_losses)
        test_accuracies.append(t_test_accuracies)
        
    
    if typ == 'loss':
        for i in range(log_size):
            plt.plot(np.asarray(rounds[i]), np.asarray(losses[i]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    
    elif typ == 'accuracy':
        for i in range(log_size):
            plt.plot(np.asarray(rounds[i]), np.asarray(test_accuracies[i]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    plt.tick_params(labelsize=18)
    plt.xlabel("Rounds", fontsize=20)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend()

    if typ == 'loss':
        plt.ylabel('Loss', fontsize=20)
    elif typ == 'accuracy':
        plt.ylabel('Accuracy', fontsize=20)


    plt.tight_layout()
    lgd = plt.legend(bbox_to_anchor=(1.02, 0), loc=3, borderaxespad=0)
    plt.savefig("./img/" + img_name + ".png", bbox_extra_artists=(lgd,), bbox_inches='tight')
#     plt.savefig("./img/" + img_name + ".png")
    plt.show()
    
def _plot2(typ,logs,description,begin_pos,end_pos,img_name):
    colors = ["red","blue","green","black","gray","brown","darkred"]
    plt.rcParams['text.usetex']=True
    idx = 0
    f = plt.figure(1)
    
    log_size = len(logs)
    rounds = []
    losses = []
    test_accuracies = []
    for log in logs:
        t_rounds, t_losses, t_test_accuracies = parse_log2(log)
        rounds.append(t_rounds)
        losses.append(t_losses)
        test_accuracies.append(t_test_accuracies)
    
    if typ == 'loss':
        for i in range(log_size):
            plt.plot(np.asarray(rounds[i][begin_pos:end_pos]), np.asarray(losses[i][begin_pos:end_pos]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    
    elif typ == 'accuracy':
        for i in range(log_size):
            plt.plot(np.asarray(rounds[i][begin_pos:end_pos]), np.asarray(test_accuracies[i][begin_pos:end_pos]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    plt.tick_params(labelsize=18)
    plt.xlabel("Rounds", fontsize=20)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend()

    if typ == 'loss':
        plt.ylabel('Loss', fontsize=20)
    elif typ == 'accuracy':
        plt.ylabel('Accuracy', fontsize=20)
    plt.tight_layout()
    plt.savefig("./img/" + img_name + ".png")
    plt.show()
    
def _realtime_plot(typ,logs,total_times,description,begin_pos,end_pos,img_name):
    print(len(logs))
    print(len(description))
    colors = ["red","blue","green","black","gray","brown","darkred"]
    plt.rcParams['text.usetex']=True
    idx = 0
    f = plt.figure(1)
    
    log_size = len(logs)
    rounds = []
    losses = []
    test_accuracies = []
    for log in logs:
        t_rounds, t_losses, t_test_accuracies = parse_log(log)
        rounds.append(t_rounds)
        losses.append(t_losses)
        test_accuracies.append(t_test_accuracies)
    real_time = []
    for i in range(log_size):
        curr_real_time = [item*total_times[i] for item in rounds[i]]
        real_time.append(curr_real_time)
    
    if typ == 'loss':
        for i in range(log_size):
            plt.plot(np.asarray(real_time[i][begin_pos:end_pos]), np.asarray(losses[i][begin_pos:end_pos]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    
    elif typ == 'accuracy':
        for i in range(log_size):
            plt.plot(np.asarray(real_time[i][begin_pos:end_pos]), np.asarray(test_accuracies[i][begin_pos:end_pos]), linewidth=1.0, label=description[i], color=colors[i], linestyle='-')
    plt.tick_params(labelsize=18)
    plt.xlabel("Time", fontsize=20)
    plt.xticks(fontsize=17)
    plt.yticks(fontsize=17)
    plt.legend()

    if typ == 'loss':
        plt.ylabel('Loss', fontsize=20)
    elif typ == 'accuracy':
        plt.ylabel('Accuracy', fontsize=20)
    plt.tight_layout()
    plt.savefig("./img/" + img_name + ".png")
    plt.show()
    
    