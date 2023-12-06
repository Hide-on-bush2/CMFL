import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator


def readNumFromFile(filename):
    res = []
    f = open(filename)
    line = f.readline()
    while line:
        num = int(line.replace('\n',''))
        res.append(num)
        line = f.readline()
    f.close()
    return res

def getTrainingTimesAndAccFromFile(filename):
    training_times = []
    accs = []
    f = open(filename)
    line = f.readline()
    while line:
        content = line.split()
        training_time = int(content[0])
        acc = float(content[1])
        training_times.append(training_time)
        accs.append(acc)
        line = f.readline()
    f.close()
    return training_times, accs

def drawBar(arr,imgName):
    plt.bar(range(len(arr)),arr)
    plt.savefig(imgName+'.png')

def calSplit(arr,max_val):
    res = []
    for i in range(max_val+1):
        tmp = [j for j in arr if j == i]
        res.append(len(tmp))
    return res

def calMax(arr):
    res = 0
    for item in arr:
        res = max(res,item)
    return res

def calMin(arr):
    res = arr[0]
    for item in arr:
        res = min(res,item)
    return res
    

def drawDoubleBar(arr1, arr2, label1,label2,imgName):
    width = 0.25
    x = np.arange(len(arr1))
    plt.bar(x-width/2,arr1,width,label=label1)
    plt.bar(x+width/2,arr2,width,label=label2)
    plt.xticks(x,label=range(len(arr1)))
    plt.legend()
    plt.savefig(imgName+'.png')
    
def drawTripleBar(arr1, arr2, arr3, label1,label2, label3, xlabel,ylabel,imgName, x_labels):
    print(x_labels)
    plt.rcParams['text.usetex']=True
    width = 0.7
#     x = np.arange(len(arr1))
    x_list = [i*3 for i in range(len(arr1))]
    x = np.array(x_list)
    plt.bar(x-width,arr1,width,label=label1)
    plt.bar(x,arr2,width,label=label2)
    plt.bar(x+width,arr3,width,label=label3)
    plt.xticks(x,x_labels,rotation=30)
    plt.xlabel(xlabel, fontsize=15)
#     x_major_locator=MultipleLocator(100)
#     #把x轴的刻度间隔设置为1，并存在变量里
#     ax=plt.gca()
#     #ax为两条坐标轴的实例
#     ax.xaxis.set_major_locator(x_major_locator)
    plt.ylabel(ylabel, fontsize=15)
    plt.legend()
    plt.savefig(imgName+'.png')

def drawTriplePlot(arr1, arr2, arr3, label1,label2, label3, xlabel, ylabel,imgName):
    plt.rcParams['text.usetex']=True
    width = 0.25
    x = range(len(arr1))
    plt.plot(x,arr1,label=label1)
    plt.plot(x,arr2,label=label2)
    plt.plot(x,arr3,label=label3)
    plt.xticks(x,label=range(len(arr1)))
    plt.xlabel(xlabel, fontsize=15)
    x_major_locator=MultipleLocator(10)
    #把x轴的刻度间隔设置为1，并存在变量里
    ax=plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    plt.ylabel(ylabel, fontsize=15)
    plt.legend()
    plt.savefig(imgName+'.png')
    
def splitAcc(accs):
    res = [0] * 5
    for acc in accs:
        if acc < 0.2:
            res[0] += 1
        elif acc < 0.4:
            res[1] += 1
        elif acc < 0.6:
            res[2] += 1
        elif acc < 0.8:
            res[3] += 1
        else:
            res[4] += 1
    return res
              

def drawTrainingtimesAcc(training_times_arr, accs_arr, max_val, groups_num):
    size = len(training_times_arr)
    length = len(training_times_arr[0])
    shift = (max_val+1) / groups_num
    split_accs_arr = []
    for i in range(size):
        curr_training_times_arr = training_times_arr[i]
        curr_accs_arr = accs_arr[i]
        split_accs = []
        for j in range(groups_num):
            curr_max_training_times = shift * (j+1)
            curr_min_training_times = shift * j
            satisfied_accs = [curr_accs_arr[k] for k in range(length) if curr_training_times_arr[k] > curr_min_training_times and curr_training_times_arr[k] <= curr_max_training_times]
            average_acc = np.sum(satisfied_accs) / len(satisfied_accs)
            split_accs.append(average_acc)
        split_accs_arr.append(split_accs)
    drawTripleBar(split_accs_arr[0],split_accs_arr[1],split_accs_arr[2],r"Strategy \uppercase\expandafter{\romannumeral1}",r"Strategy \uppercase\expandafter{\romannumeral2}","Typical FL", "Training Times","Accuracy","times_acc")
        
def drawAccTT(accs_arr,training_times_arr,groups_num):
    size = len(accs_arr)
    length = len(accs_arr[0])
    split_training_times_arr = []
    shift = 1.0 / groups_num
    for i in range(size):
        curr_training_times_arr = training_times_arr[i]
        curr_accs_arr = accs_arr[i]
        split_training_times = []
        for j in range(groups_num):
            curr_max_acc = shift * (j+1) * 1.0
            curr_min_acc = shift * j * 1.0
            satisfied_tt = [curr_training_times_arr[k] for k in range(length) if curr_accs_arr[k] > curr_min_acc and curr_accs_arr[k] <= curr_max_acc]
            average_tt = np.sum(satisfied_tt) * 1.0 / len(satisfied_tt)
            split_training_times.append(average_tt)
        split_training_times_arr.append(split_training_times)
    x_labels = ["({:.1f},{:.1f}]".format(i*shift,(i+1)*shift) for i in range(groups_num)] 
    drawTripleBar(split_training_times_arr[0],split_training_times_arr[1],split_training_times_arr[2],r"Strategy \uppercase\expandafter{\romannumeral1}",r"Strategy \uppercase\expandafter{\romannumeral2}","Typical FL", "Accuracy","Aggregation Times","acc_times",x_labels)
    


if __name__ == "__main__":
    training_times1, accs1 = getTrainingTimesAndAccFromFile("./cmfl_1_tt_loss.txt")
    training_times2, accs2 = getTrainingTimesAndAccFromFile("./cmfl_2_tt_loss.txt")
    training_times3, accs3 = getTrainingTimesAndAccFromFile("./fl_tt_loss.txt")
    
    max1 = calMax(training_times1)
    max2 = calMax(training_times2)
    max3 = calMax(training_times3)
    
    max_val = max(max1,max(max2,max3))
    
    res1 = calSplit(training_times1,max_val)
    res2 = calSplit(training_times2,max_val)
    res3 = calSplit(training_times3,max_val)

#     drawTriplePlot(res1,res2,res3,r"Strategy \uppercase\expandafter{\romannumeral1}",r"Strategy \uppercase\expandafter{\romannumeral2}","Typical FL", "Aggregation Times", "Number of Clients","distributed_map")
    
#     nonZeroAccs1 = [accs1[i] for i in range(len(accs1)) if training_times1[i] != 0]
#     nonZeroAccs2 = [accs2[i] for i in range(len(accs2)) if training_times2[i] != 0]
#     nonZeroAccs3 = [accs3[i] for i in range(len(accs3)) if training_times3[i] != 0]
    
#     splitedAcc1 = splitAcc(nonZeroAccs1)
#     splitedAcc2 = splitAcc(nonZeroAccs2)
#     splitedAcc3 = splitAcc(nonZeroAccs3)
#     x_labels = ["({:.1f},{:.1f}]".format(i*0.2,(i+1)*0.2) for i in range(5)]
#     drawTripleBar(splitedAcc1,splitedAcc2,splitedAcc3,r"Strategy \uppercase\expandafter{\romannumeral1}",r"Strategy \uppercase\expandafter{\romannumeral2}","Typical FL", "Accuracy","Number of Clients","acc_distributed",x_labels)
    
#     #draw Accuracy-TrainingTimes Histogram
#     training_times_arr = [training_times1, training_times2, training_times3]
#     accs_arr = [accs1, accs2, accs3]
#     drawTrainingtimesAcc(training_times_arr, accs_arr, max_val, 10)
    
    #draw TrainingTimes-Accuracy Histogram
    training_times_arr = [training_times1, training_times2, training_times3]
    accs_arr = [accs1, accs2, accs3]
    drawAccTT(accs_arr,training_times_arr,10)
    
    
    
    
    
    
    
    
        