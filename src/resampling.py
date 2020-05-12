# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:45:32 2020

@author: siavash tabrizian stabrizian@smu.edu
"""
import numpy as np
import time
import random
import scipy.stats


# Runnig time decorator
def running_time(method):
    def runtime(*arg, **kwarg):
        t0 = time.time()
        result = method(*arg, **kwarg)
        t1 = time.time()
        print('running time of %r:  %2.2f ms' % (method.__name__,(t1 - t0)*1000))
        return [result,(t1 - t0)*1000]
    return runtime


'''
   This class complement the previous function which was just about
   taking a sample of fixed size.   
   The resampling class is simulate the process in different ways to 
   provides a better sense about the distributions
   
   samp_gen input should be an instance of samp_gen class from sampling module
'''
class resampling():
    def __init__(self, samp_gen, n_rep = 30, alpha = 0.025, samptype = 'SRS', rssize = 100):
        self.sampling = samp_gen
        self.n_rep = n_rep  #number of replications
        self.mean = None
        self.std  = None
        self.alpha = alpha
        self.confidence = []
        self.error = None
        self.samptype = samptype
        self.rssize = rssize  #resampling size
    
    @running_time
    def monte_carlo(self):
        mean = 0.0
        mean_list = []
        weight = 1.0/self.n_rep
        for rep in range(self.n_rep):
            [s, estim] = self.sampling.sample_gen(self, self.rssize, \
                          seed = rep, samptype = self.samptype)
            mean_list.append(estim)
            mean += weight * estim
        return [mean, mean_list]
            
    @running_time
    def bootstrap(self):
        mean = 0.0
        mean_list = []
        weight = 1.0/self.n_rep
        for rep in range(self.n_rep):
            sample = random.choices(self.sample, k = self.rssize)
            estim  = self.sampling._samp_mean(sample)
            mean_list.append(estim)
            mean += weight * estim
        return [mean, mean_list]
    
    @running_time
    def jacknife(self):
        mean = 0.0
        mean_list = []
        weight = 1.0/len(self.sample)
        for rep in range(len(self.sample)):
            sample = self.sample
            sample = sample.remove(self.sample[rep])
            estim  = self.sampling._samp_mean(sample)
            mean_list.append(estim)
            mean += weight * estim
        return [mean, mean_list]    
    
    #subroutine to get the confidence interval of a list of estimates and the mean
    def getCI(self,mean,mean_list):
        self.std = 0.0
        weight = 1/(len(mean_list)-1)
        for m in mean_list:
            self.std += weight * (m - mean)**2
        self.error = scipy.stats.norm(0,1).ppf(1-self.alpha)*\
                                  self.std/(np.sqrt(len(mean_list)))
        self.confidence = [mean - self.error, mean + self.error]
        return self.confidence
            
