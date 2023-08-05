#!usr/bin/python 3.7
#-*-coding:utf-8-*-

'''
@file: fcm.py, fuzzy c-means algorithm
@Author: Jing Wang (jingw2@foxmail.com)
@Date: 06/06/2020
@paper: Clustering with Size Constraints
@github reference: https://github.com/omadson/fuzzy-c-means/blob/master/fcmeans/fcm.py
'''

from scipy.spatial.distance import cdist
import numpy as np 
from scipy.linalg import norm
import sys 
import os 
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path)
import base

class FCM(base.Base):
    
    def __init__(self, n_clusters, \
        max_iters=1000, m=2, 
        epsilon=1e-5,
        random_state=42, 
        distance_func=cdist):
        '''
        Args:
            n_clusters (int): number of clusters 
            max_iters (int): maximum iterations
            m (float): membership order, in general it is 2 
            epsilon (float): 1e-5
            random_state (int): random seed
            distance_func (callable function/None), default is Euclidean distance
        '''
        super(FCM, self).__init__(n_clusters, max_iters, distance_func)
        assert m > 1
        assert epsilon > 0
        self.m = m 
        self.epsilon = epsilon
        self.random_state = random_state
        self.u, self.cluster_centers_ = None, None

    def fit(self, X):
        '''
        Args:
            X (array like): shape is (n_samples, n_dimensions)
        '''
        np.random.seed(self.random_state)
        n_samples, n_dimensions = X.shape

        # initialize mu 
        self.u = np.random.random(size=(n_samples, self.n_clusters))
        self.u /= np.sum(self.u, axis=1).reshape((-1, 1))

        # initialize centers
        itr = 0
        while True:
            last_u = self.u.copy()
            # update centers
            self.cluster_centers_ = self.update_centers(X) 
            # update membership
            self.u = self.update_membership(X)
            if norm(self.u - last_u) < self.epsilon or itr >= self.max_iters:
                break 
            itr += 1
        
        self.labels_ = np.argmax(self.u, axis=1)

    def update_centers(self, X):
        '''
        Update centers based new u
        '''
        um = np.power(self.u, self.m) # (n_samples, n_clusters)
        centers = (X.T.dot(um)).T / np.sum(um, axis=0).reshape((-1, 1))
        return centers

    def update_membership(self, X):
        power = 2. / (self.m - 1)
        n_samples, n_dimensions = X.shape
        dist = self.distance_func(X, self.cluster_centers_)
        dist = np.power(dist, power)
        u = dist * np.sum(1. / dist, axis=1).reshape((-1, 1))
        u = 1. / u
        # normalize
        u /= np.sum(u, axis=1).reshape((-1, 1))
        return u
    
    def predict(self, X):
        u = self.update_membership(X)
        labels = np.argmax(u, axis=1)
        return labels
