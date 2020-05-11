
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
             

"""

from distribution import ProbDist
import numpy as np
from itertools import permutations
import time

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
    def __init__(self, n_rep = 30, alpha = 0.05, samptype = 'SRS', ssize = 100):
        self.n_rep = n_rep #number of replications
        self.mean = None
        self.std  = None
        self.alpha = alpha
        self.confidence = []
        self.error = None
        self.samptype = samptype
        self.ssize = ssize
    
    @running_time
    def monte_carlo(self):
        mean = 0.0
        mean_list = []
        weight = 1.0/self.n_rep
        for rep in range(self.n_rep):
            [s, estim] = self.sample_gen(self, self.ssize, \
                          seed = rep, samptype = self.samptype)
            mean_list.append(weight * estim)
            mean += weight * estim
            
    @running_time
    def bootstrap(self):
        mean = 0.0
        mean_list = []
        weight = 1.0/self.n_rep
        for rep in range(self.n_rep):
            [s, estim] = self.sample_gen(self, self.ssize, \
                          seed = rep, samptype = self.samptype)
            mean_list.append(weight * estim)
            mean += weight * estim
            
        
      

