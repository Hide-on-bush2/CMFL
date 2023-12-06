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
        print('Using CMFL to Train')
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
        log_file_name = 'bflc_weight_attack_Selection_{:.2f}_learningRate_{:.3f}_CommitteeNode_{:.2f}_AggregationNode_{:.2f}_ActiveRate_{:.2f}_AttackMethod_{}_AttackNode_{:.2f}_AttackRange_{:.2f}_epoch_{:d}_{}.txt'.format(self.selection_strategy, self.learning_rate,self.committee_rate,self.aggregation_rate, self.active_rate,self.attack_method,self.attack_rate,self.attack_range,self.num_rounds,time.strftime("%Y-%m-%d-%X",time.localtime())) 
        logger = MyLogger(log_file_name)
        with open('../log/log_file_log/'+self.record_log,mode='a') as file:
            file.write(log_file_name)
            file.write('\n')
        
        '''Train using Committee Mechanism'''
        total_clients_num = len(self.clients)
        training_times = [0] *total_clients_num
        clients_list = range(total_clients_num)
        bad_list = random.sample(clients_list,k=int(total_clients_num * self.attack_rate))
        good_list = list(set(clients_list).difference(set(bad_list)))
        committee_list = random.sample(clients_list, k = int(total_clients_num * self.active_rate * self.committee_rate+0.5))
        committee_num = len(committee_list)
#         print(committee_list)
        rest_clients = list(set(clients_list).difference(set(committee_list)))
        training_list = random.sample(rest_clients, k=int(total_clients_num*self.active_rate*(1-self.committee_rate)+0.5))
        training_num = len(training_list)
        print('Training with {} workers ---'.format(training_num))
        
#         indices, selected_clients = self.select_clients(0, num_clients=self.clients_per_round)  # uniform sampling

        for i in range(self.num_rounds):
#             indices, selected_clients = self.select_clients(i, num_clients=self.clients_per_round)  # uniform sampling
#             np.random.seed(i)
#             active_clients = np.random.choice(selected_clients, round(self.clients_per_round * (1-self.drop_percent)), replace=False)
            training_param = []
            committee_param = []
            committee_clients = np.asarray(self.clients)[committee_list]
            training_clients = np.asarray(self.clients)[training_list]
            committee_bad = [i for i in committee_list if i in bad_list]
            training_bad = [i for i in training_list if i in bad_list]
            committee_bad_num = 0
            training_bad_num = 0
            
            localtraining_times = []
            scoring_times = []
        
            #Committe starts to train
            for idx, c in enumerate(committee_clients.tolist()):
#                 print("The {}-th committee client is training".format(idx))
                # communicate the latest model
                c.set_params(self.latest_model)

                # solve minimization locally
                localtraining_start_time = time.time()
                soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)
                localtraining_end_time = time.time()
                localtraining_time = localtraining_end_time - localtraining_start_time
                localtraining_times.append(localtraining_time)
                
                c_param = soln[1]
                c_id = committee_list[idx]
                if c_id in committee_bad:
                    committee_bad_num += 1
                    if self.attack_method == 1:
                        c_param = self.disturb(c_param,self.attack_range)
                    elif self.attack_method == 2:
                        c_param = self.all_0_gradient(c_param)
                    elif self.attack_method == 3:
                        c_param = self.all_1_gradient(c_param)
                    elif self.attack_method == 5:
                        c_param = self.gauss_disturb(c_param)
                    elif self.attack_method == 6:
                        c_param = self.gradient_steering(c_param)
                    elif self.attack_method == 7:
                        c_param = self.gradient_explosion(c_param)
#                     soln[1] = c_param

                # gather solutions from client
                committee_param.append(c_param)

                # track communication cost
                self.metrics.update(rnd=i, cid=c.id, stats=stats)
            
            
            for idx, c in enumerate(training_clients.tolist()):
#                 print("The {}-th training client is training".format(idx))
                # communicate the latest model
                c.set_params(self.latest_model)

                # solve minimization locally
                localtraining_start_time = time.time()
                soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)
                localtraining_end_time = time.time()
                localtraining_time = localtraining_end_time - localtraining_start_time
                localtraining_times.append(localtraining_time)
                
                t_param = soln[1]
                t_id = training_list[idx]
                
                if t_id in training_bad:
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
                
                #The committee assigns the score on each training clients
                scoring_start_time = time.time()
                score = self.committee_eval(t_param, committee_param) 
                scoring_end_time = time.time()
                scoring_time = scoring_end_time - scoring_start_time
                scoring_times.append(scoring_time)
                
                # gather solutions from client
                training_param.append([t_id,score,soln])

                # track communication cost
                self.metrics.update(rnd=i, cid=c.id, stats=stats)
            

#             csolns = []  # buffer for receiving client solutions

#             for idx, c in enumerate(active_clients.tolist()):  # simply drop the slow devices
#                 # communicate the latest model
#                 c.set_params(self.latest_model)

#                 # solve minimization locally
#                 soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)

#                 # gather solutions from client
#                 csolns.append(soln)

#                 # track communication cost
#                 self.metrics.update(rnd=i, cid=c.id, stats=stats)

            #some information
            print("malicious committee:{}, malicious training:{}".format(committee_bad_num,training_bad_num))

            #aggregation
            if self.selection_strategy == 1:
                sorted_gradients = sorted(training_param,key=lambda s : s[1], reverse=False) #selection strategy 1
            else:
                sorted_gradients = sorted(training_param,key=lambda s : s[1], reverse=True) #selection strategy 2
            update_list = [i[2] for i in sorted_gradients[0:int(total_clients_num * self.active_rate*self.aggregation_rate)]]
            aggregation_ids = [i[0] for i in sorted_gradients[0:int(total_clients_num * self.active_rate*self.aggregation_rate)]]
            aggregation_bad_num = 0
            for client_id in aggregation_ids:
                training_times[client_id] += 1 
                if client_id in bad_list:
                    aggregation_bad_num += 1
            
            
    
            # update models
            aggregation_start_time = time.time()
            self.latest_model = self.aggregate(update_list)
            aggregation_end_time = time.time()
            aggregation_time = aggregation_end_time - aggregation_start_time
            
            # replace the committee members
            committee_list = [i[0] for i in sorted_gradients[int(training_num/2-committee_num/2) : int(training_num/2 + committee_num/2)]]
#             print(committee_list)
            rest_clients = list(set(clients_list).difference(set(committee_list)))
            training_list = random.sample(rest_clients, k=int(total_clients_num*self.active_rate*(1-self.committee_rate) + 0.5))
        
            # test model
            if i % self.eval_every == 0:
                stats = self.test()  # have set the latest model for all clients
                stats_train = self.train_error_and_loss()

                tqdm.write('At round {} accuracy: {}'.format(i, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))  # testing accuracy
                tqdm.write('At round {} training accuracy: {}'.format(i, np.sum(stats_train[3]) * 1.0 / np.sum(stats_train[2])))
                tqdm.write('At round {} training loss: {}'.format(i, np.dot(stats_train[4], stats_train[2]) * 1.0 / np.sum(stats_train[2])))
                logger.log("SMALL, BIG: {}, {}".format(0, len(training_list)), display=True)  
                logger.log("traing clients: {}, malicious train nodes: {}, malicious committee nodes: {}, malicious average nodes: {}".format(len(training_list),training_bad_num, committee_bad_num, aggregation_bad_num), display=True)
                res = "\n[epoch {:d}, {:d} inst] Testing {} accuracy: {:.4f}, Loss: {:.4f}".format(
        i+1, 10000, 'model', np.sum(stats[3]) * 1.0 / np.sum(stats[2]), np.dot(stats_train[4], stats_train[2]) * 1.0 / np.sum(stats_train[2]))
                logger.log(res, display=True)
            average_training_time = np.mean(localtraining_times)
            average_scoring_time = np.sum(scoring_times) / len(committee_list) 
            print("Training Time:{}".format(average_training_time))
            print("Aggregation Time:{}".format(aggregation_time))
            print("Scoring Time:{}".format(average_scoring_time))

        # final test model
#         stats = self.test()
#         stats_train = self.train_error_and_loss()
        self.metrics.accuracies.append(stats)
        self.metrics.train_accuracies.append(stats_train)
#         tqdm.write('At round {} accuracy: {}'.format(self.num_rounds, np.sum(stats[3]) * 1.0 / np.sum(stats[2])))
#         tqdm.write('At round {} training accuracy: {}'.format(self.num_rounds, np.sum(stats_train[3]) * 1.0 / np.sum(stats_train[2])))
        test_ids, test_groups,test_num_samples,test_tot_correct = self.test()
        train_ids, train_groups, train_num_samples, train_tot_correct, train_losses = self.train_error_and_loss()
        for i in range(len(training_times)):
            logger.log("{} {} {} {}".format(training_times[i], test_tot_correct[i] * 1.0 / test_num_samples[i], train_tot_correct[i] * 1.0 / train_num_samples[i], train_losses[i]))
        res_mean = np.mean(training_times)
        res_var = np.var(training_times)
        logger.log("mean:{}, var:{}".format(res_mean,res_var))
