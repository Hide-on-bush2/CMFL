import numpy as np
from tqdm import trange, tqdm
import random, time
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from .fedbase import BaseFedarated
from flearn.utils.tf_utils import process_grad
from log import MyLogger


class Server(BaseFedarated):
    def __init__(self, params, learner, dataset):
        print('Using Federated avg to Train')
        self.inner_opt = tf.train.GradientDescentOptimizer(params['learning_rate'])
        super(Server, self).__init__(params, learner, dataset)
        
    def committee_eval(self, train_param, committee_param):
        distance = []
        for W_c in committee_param:
            dis = 0
            for w_c,w_k in zip(W_c, train_param):  #逐层参数求二范数，距离相加
                dis += np.linalg.norm(w_k-w_c)
            distance.append(dis)
    #     score = np.median(np.array(distance,dtype = np.float32))
        score = np.sum(distance)
        return score
    
    # Attack1:gradient scaling attack
    def disturb(self, param, attack_range):  
        for i,weight in enumerate(param):
            shape = weight.shape
            base_disturb = np.zeros(shape)
            base_disturb.fill(attack_range)
            disturb = base_disturb + (1-attack_range)*np.random.random(shape)
    #         print(disturb)
            param[i] *= disturb
        return param
    #attack2：全0梯度
    def all_0_gradient(self, param):
        for i,weight in enumerate(param):
            shape = weight.shape
            param[i] = np.zeros(shape)
        return param

    #attack3：全1梯度
    def all_1_gradient(self, param):
        for i,weight in enumerate(param):
            shape = weight.shape
            param[i] = np.ones(shape)
        return param


    #attack5：扰动
    def gauss_disturb(self, param):
        for i,weight in enumerate(param):
            shape = weight.shape
            base_disturb = np.random.normal(0, ATTACK_RANGE, shape)
            param[i] += base_disturb
        return param

    #attack6：梯度转向
    def gradient_steering(self, param):
        for i,weight in enumerate(param):
            shape = weight.shape
            base_disturb = np.zeros(shape)
            base_disturb.fill(-1)
            param[i] *= base_disturb
        return param

    #attack7：随机给个很大的梯度
    def gradient_explosion(self, param):
        for i,weight in enumerate(param):
            shape = weight.shape
            base_disturb = np.zeros(shape)
            base_disturb.fill(100)
            random_disturb = np.random.random(shape)
            param[i] = base_disturb * random_disturb 
        return param
    

    def train(self):
        '''Log setting'''
        log_file_name = "fl_attack_learningRate_{:.3f}_ActiveRate_{:.2f}_MergeMethod_{}_AttackMethod_{}_AttackNode_{:.2f}_AttackRange_{:.2f}_AggregationRate_{}_epoch_{:d}_{}.txt".format(self.learning_rate,self.active_rate,self.merge_method,self.attack_method,self.attack_rate,self.attack_range,self.aggregation_rate,self.num_rounds,time.strftime("%Y-%m-%d-%X",time.localtime()))
        logger = MyLogger(log_file_name)
        print(log_file_name)
        with open('./log_file_log/'+self.record_log,mode='a') as file:
            file.write(log_file_name)
            file.write('\n')
            
        total_clients_num = len(self.clients)
        clients_list = range(total_clients_num)
        training_times = [0] *total_clients_num
        bad_list = random.sample(clients_list,k=int(total_clients_num*self.attack_rate))
        good_list = list(set(clients_list).difference(set(bad_list)))
        training_list = random.sample(clients_list,k=int(total_clients_num*self.active_rate+0.5))
        
        
        '''Train using Federated Proximal'''
        print('Training with {} workers ---'.format(self.clients_per_round))
#         np.random.seed(1)
        for i in range(self.num_rounds):
            # test model

#             indices, selected_clients = self.select_clients(i, num_clients=self.clients_per_round)  # uniform sampling
#             np.random.seed(i+1)
#             active_clients = np.random.choice(selected_clients, round(self.clients_per_round * (1-self.drop_percent)), replace=False)
            training_list = random.sample(clients_list,k=int(total_clients_num*self.active_rate+0.5))
            print_list = sorted(training_list)
            print(print_list)
            print(training_list)
            for client_id in training_list:
                training_times[client_id] += 1
            active_clients = np.asarray(self.clients)[training_list]
            training_bad = [i for i in training_list if i in bad_list]
            training_bad_num = 0
            

            csolns = []  # buffer for receiving client solutions

            for idx, c in enumerate(active_clients.tolist()):  # simply drop the slow devices
                # communicate the latest model
                c.set_params(self.latest_model)

                # solve minimization locally
                soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)
                t_id = training_list[idx]
                
                #attack
                if t_id in training_bad:
                    t_param = soln[1]
                    training_bad_num += 1
                    if self.attack_method == 1:
                        t_param = self.disturb(t_param,self.attack_range)
                    elif self.attack_method == 2:
                        t_param = self.all_0_gradient(t_param)
                    elif self.attack_method == 3:
                        t_param = self.all_1_gradient(t_param)
                    elif self.attack_method == 5:
                        t_param = self.gauss_disturb(t_param)
                    elif self.attack_method == 6:
                        t_param = self.gradient_steering(t_param)
                    elif self.attack_method == 7:
                        t_param = self.gradient_explosion(t_param)
                    # transfer tuple to list and then transfer it back to tuple
                    soln = list(soln)
                    soln[1] = t_param #update soln
                    soln = tuple(soln)
                
                # gather solutions from client
                csolns.append(soln)
                # track communication cost
                self.metrics.update(rnd=i, cid=c.id, stats=stats)

            # update models
            if self.merge_method == 0: #normal
                self.latest_model = self.aggregate(csolns)
            elif self.merge_method == 1: #median
                self.latest_model = self.median(csolns)
            elif self.merge_method == 2: #trimmed_mean
                self.latest_model = self.trimmed_mean(csolns)
            elif self.merge_method == 3:#krum
                self.latest_model = self.krum(csolns,len(training_bad))
            elif self.merge_method == 4:#multi-krum
                self.latest_model = self.multi_krum(csolns,len(training_bad),int(total_clients_num*self.active_rate*self.aggregation_rate+0.5))
            
            
            if i % self.eval_every == 0:
                stats = self.test()  # have set the latest model for all clients
                stats_train = self.train_error_and_loss()

                tqdm.write('At round {} accuracy: {}'.format(i, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))  # testing accuracy
                tqdm.write('At round {} training accuracy: {}'.format(i, np.sum(stats_train[3]) * 1.0 / np.sum(stats_train[2])))
                tqdm.write('At round {} training loss: {}'.format(i, np.dot(stats_train[4], stats_train[2]) * 1.0 / np.sum(stats_train[2])))
                logger.log("SMALL, BIG: {}, {}".format(0, len(training_list)), display=True)  
                logger.log("traing clients: {}, malicious train nodes: {}".format(len(training_list),training_bad_num), display=True)
                res = "\n[epoch {:d}, {:d} inst] Testing {} accuracy: {:.4f}, Loss: {:.4f}".format(
        i+1, 10000, 'model', np.sum(stats[3]) * 1.0 / np.sum(stats[2]), np.dot(stats_train[4], stats_train[2]) * 1.0 / np.sum(stats_train[2]))
                logger.log(res, display=True)

        # final test model
#         stats = self.test()
#         stats_train = self.train_error_and_loss()
        self.metrics.accuracies.append(stats)
        self.metrics.train_accuracies.append(stats_train)
#         tqdm.write('At round {} accuracy: {}'.format(self.num_rounds, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))
#         tqdm.write('At round {} training accuracy: {}'.format(self.num_rounds, np.sum(stats_train[3]) * 1.0 / np.sum(stats_train[2])))
        ids, groups,num_samples,tot_correct = self.test()
        for i in range(len(training_times)):
            logger.log("{} {}".format(training_times[i], tot_correct[i] * 1.0 / num_samples[i]))
        res_mean = np.mean(training_times)
        res_var = np.var(training_times)
        logger.log("mean:{}, var:{}".format(res_mean,res_var))
        
