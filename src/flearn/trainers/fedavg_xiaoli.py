import numpy as np
from tqdm import trange, tqdm
import tensorflow as tf
import copy
import heapq
import math

from .fedbase import BaseFedarated
from flearn.utils.tf_utils import process_grad


class Server(BaseFedarated):
    def __init__(self, params, learner, dataset):
        print('Using Federated avg to Train')
        self.inner_opt = tf.train.GradientDescentOptimizer(params['learning_rate'])
        super(Server, self).__init__(params, learner, dataset)

    def train(self):
        '''Train using Federated Proximal'''
        print('Training with {} workers ---'.format(self.clients_per_round))
        lastselectclients =  []
        allselectedclients = [0] * len(self.clients)
        
        

        for i in range(self.num_rounds):
            # test model
            if i % self.eval_every == 0:
                ids, groups, num_test, num_correct_test = self.test() # have set the latest model for all clients
                #num_train, num_correct_train = self.train_error() 
                ids, groups, num_train, num_correct_train, loss = self.train_error_and_loss()
                newloss = np.dot(loss, num_train) * 1.0 / np.sum(num_train)
                
               
                tqdm.write('At round {} loss: {}'.format(i, np.dot(loss, num_train) * 1.0 / np.sum(num_train)))
                tqdm.write('At round {} testing accuracy: {}'.format(i, np.sum(np.array(num_correct_test)) * 1.0 / np.sum(np.array(num_test))))
                tqdm.write('At round {} training accuracy: {}'.format(i, np.sum(np.array(num_correct_train)) * 1.0 / np.sum(np.array(num_train))))
              

            model_len = process_grad(self.latest_model).size
            global_grads = np.zeros(model_len)
            client_grads = np.zeros(model_len)
            num_samples = []
            local_grads = []
            

            indices, selected_clients = self.select_clients(i, num_clients=self.clients_per_round)  # uniform sampling
            #np.random.seed(i)
            #active_clients = np.random.choice(selected_clients, round(self.clients_per_round * (1-self.drop_percent)), replace=False)



            #selected_clients = np.asarray(self.clients)[indices]
            
            active_clients = []
            np.random.seed(i)
            #active_clients = np.random.choice(selected_clients, round(self.clients_per_round * (1-self.drop_percent)), replace=False)
            
            active_clients_list = np.random.choice(indices, round(self.clients_per_round * (1 - self.drop_percent)), replace=False)
            active_clients_list2= set(active_clients_list)
            #print("active_clients_list",active_clients_list)
            active = list(zip(indices,selected_clients))
            for t in active:
                if t[0] in active_clients_list2:
                    active_clients.append(t[1])
            #print("active_clients",active_clients)
            
            lastselectclients = active_clients_list.tolist()
            print("lastselectclients",lastselectclients)
            for k in lastselectclients:
                allselectedclients[k] +=  1

            csolns = []  # buffer for receiving client solutions

            for idx, c in enumerate(active_clients):  # simply drop the slow devices
                # communicate the latest model
                c.set_params(self.latest_model)

                # solve minimization locally
                soln, stats = c.solve_inner(num_epochs=self.num_epochs, batch_size=self.batch_size)

                # gather solutions from client
                csolns.append(soln)

                # track communication cost
                self.metrics.update(rnd=i, cid=c.id, stats=stats)

            # update models
            self.latest_model = self.aggregate(csolns)


        # final test model
        
    
        


