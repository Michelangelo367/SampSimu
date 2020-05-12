
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
             

"""

import os
from distribution import ProbDist
import numpy as np
from itertools import permutations
import time
import random
import scipy.stats
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

# draw from 0-1 interval
def draw(lo,hi, seed):
      np.random.seed(seed)
      return np.random.uniform(lo,hi,1).tolist()[0]

# mapping the zero one interval to the valure of the true distribution
def getVal(RV, zone):
      val = RV[0]
      prob = RV[1]
      draw = [val[i] for i in range(len(RV[1])) if prob[i] >= zone]
      return draw[0]

# Runnig time decorator
def running_time(method):
    def runtime(*arg, **kwarg):
        t0 = time.time()
        result = method(*arg, **kwarg)
        t1 = time.time()
        print('running time of %r:  %2.2f ms' % (method.__name__,(t1 - t0)*1000))
        return [result,(t1 - t0)*1000]
    return runtime

# sampling class contains subroutines associated with different 
# sampling techniques
class samp_gen(ProbDist):
      def __init__(self, RVs,seed = 0):
            self.RVs = RVs
            self.rv_num = len(RVs)
            self.CDF = self.getCDF(RVs)
            self.newdist = RVs
            self.sample  = []
            self.weight  = []
            self.estimate = None
            self.sample_u = [] #the sample from the [0,1] interval
            self.unit     = [] #each sample is associated with a list of units
            self.seed     = seed
            self.bias     = None
      
      #Funcion for simple random smapling - independent sampling
      def _SRS(self, n, seed = None):
            self.sample = []
            self.weight = []
            self.sample_u = []
            self.unit = []
            if seed != None:
                  self.seed = seed 
            
            np.random.seed(self.seed)
            for s in range(n):                
                zone = np.random.uniform(0.0,1.0,self.rv_num).tolist()
                self.sample_u.append(zone)
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
                self.weight.append(1/n)
            
            return self.sample
      
      #Function for antithetic sampling - dependent sampling
      def _antithetic(self, n, seed = None):
            self.sample = []
            self.weight = []
            self.sample_u = []
            self.unit = []
            if seed != None:
                  self.seed = seed 
            
            np.random.seed(self.seed)
            for s in range(round(float(n)/2.0)):                
                zone = np.random.uniform(0.0,1.0,self.rv_num).tolist()
                self.sample_u.append(zone)
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
                zone1 = [1.0 - z for z in zone]
                samp = [getVal(self.CDF[r], zone1[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
                self.weight.append(1/n)
            
            return self.sample      
      
      #Function for Latin Hypercube sampling - dependent sampling
      def _LHS(self, n, seed = None):
            self.sample = []
            self.weight = []
            self.sample_u = []
            self.unit = []
            if seed != 0:
                  self.seed = seed 
            
            interval = 1.0/float(n)
            self.permute = [np.random.permutation(n).tolist() for r in range(self.rv_num)]
            np.random.seed(self.seed)
            for s in range(n):                
                zone = []
                for i in range(self.rv_num):
                      lo = max(0.0, (self.permute[i][s]-1) * interval )
                      hi = self.permute[i][s] * interval 
                      zone.append(np.random.uniform(lo,hi,1).tolist()[0])
                      self.sample_u.append(zone)
                      self.unit.append([lo,hi])
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
                self.weight.append(1/n)
            return self.sample
              
      #Estimate based on the generated sample in self.sample
      def _estim_calc(self):
          estim = 0
          if self.sample == None:
              print('Error: the sample does not exist!')
              raise
          else:
              for s in range(len(self.sample)):
                  estim += self.weight[s] * self.evaluate(self.sample[s])   
              self.estimate = estim
              return estim
      
      #Estimate based on the generated input sample
      def _samp_mean(self, sample):
          estim = 0
          weight = 1.0/len(sample)
          for s in range(len(sample)):
              estim += weight * self.evaluate(sample[s])   
          return estim      

      #Sample generation method - for generating a sample of size n 
      #with the sample mthod of samptype
      def sample_gen(self, n, seed = 0, samptype = 'SRS'):
          sample = []
          estim = 0.0
          if samptype == 'SRS':
              sample = self._SRS(self, n, seed)
              estim = self._estim_calc()
          elif samptype == 'LHS':
              sample = self._LHS(self, n, seed)
              estim = self._estim_calc()
          elif samptype == 'antithetic':
              sample = self._antithetic(self, n, seed)
              estim = self._estim_calc()
          else:
              print('Error: Sampling technique does not exist!')
              raise
          return [sample, estim]
              
                
            
'''
   This class complement the previous function which was just about
   taking a sample of fixed size.   
   The resampling class is simulate the process in different ways to 
   provides a better sense about the distributions
'''
class resampling(samp_gen):
    def __init__(self, n_rep = 30, alpha = 0.025, samptype = 'SRS', rssize = 100):
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
            [s, estim] = self.sample_gen(self, self.rssize, \
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
            estim  = self._samp_mean(sample)
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
            estim  = self._samp_mean(sample)
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
            
        
'''
   This class contains the subroutine for visualization using the sampling 
   and resampling classes.
'''
class visualsamp(resampling):
    def __init__(self, loc):
        self.loc = loc
        if not os.path.exists(self.loc):
            os.makedirs(self.loc)
        self.figcount = 0
    
    #Visualization on law of large numbers 
    def lawlargevs(self, minssize = 10, maxssize = 100, \
                   increment = 10, samptype = ['SRS'], separate = False,\
                   title = 'Law of Large Numbers'):
        truemean = self.getmu()
        if separate == False:
            fig = plt.figure(num = self.figcount)
        for st in samptype:
            self.samptype = samptype
            mean = []
            expnum = 0
            confupp = []
            confdwn = []
            x = []
            for sz in range(minssize,maxssize,increment):
                x.append(sz)
                self.rssize = sz
                [o1,o2] = self.monte_carlo()
                mean.append(o1)
                mu.append(truemean)
                [o1, o2] = self.getCI(o1,o2)
                confupp.append(o1)
                confdwn.append(o2)
                expnum += 1
            if separate == True:
                self.figcount += 1
                fig = plt.figure()
                plt.plot(np.array(x),np.array(mean))
                plt.plot(np.array(x),np.array(mu))
                plt.fill_between(np.array(x),np.array(confupp),np.array(confdwn), alpha = 0.3)
                plt.xlabel('Number of observations --->')
                plt.ylabel('Estimation value --->')
                plt.title(title)
                plt.grid(True)
                plt.savefig(self.loc + '/lawlarge' + samptype)
                plt.show()
            else:
                plt.plot(np.array(x),np.array(mean))           
        plt.plot(np.array(x),np.array(mu))
        plt.xlabel('Number of observations --->')
        plt.ylabel('Estimation value --->')
        plt.title(title)
        plt.grid(True)
        plt.savefig(self.loc + '/lawlarge')
        plt.show()
    
    #Histogram representation of the sampling method comparing to normal dist
    #This is experimenting the central limit theorem
    def centlimit(self, ssize = 100, \
                   samptype = 'SRS', separate = False,\
                   num_bins =20, title = 'Central limit theorem'):
        truemean = self.getmu()
        self.samptype = samptype
        self.rssize = ssize
        [o1,o2] = self.monte_carlo()
        mean = o1
        meanlist = []
        x = []
        std = self.std
        for m in o2:
            meanlist.append((m-mean)/(std/np.sqrt(len(o2))))
        n, bins, patches = plt.hist(np.array(meanlist), num_bins, normed = 1, \
                                    facecolor = 'blue', alpha = 0.5) 
        y = mlab.normpdf(bins,0.0,1.0)
        plt.plot(bins,y,'r--')
        plt.xlabel('mean estimates')
        plt.ylabel('probabilities')
        plt.title(title)
        plt.show
        plt.savefig(self.loc + '/central')

                
            
      

