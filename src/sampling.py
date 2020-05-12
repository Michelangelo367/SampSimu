
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
             

"""


import numpy as np
from itertools import permutations



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


# sampling class contains subroutines associated with different 
#ProbDist inut should be an instance of ProbDist class in distribution module      
# sampling techniques
class samp_gen():
      def __init__(self, ProbDist,seed = 0):
            self.dist = ProbDist
            self.RVs = ProbDist.RVs
            self.rv_num = len(self.RVs)
            self.CDF = self.getCDF(self.RVs)
            self.newdist = self.RVs
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
                  estim += self.weight[s] * self.dist.evaluate(self.sample[s])   
              self.estimate = estim
              return estim
      
      #Estimate based on the generated input sample
      def _samp_mean(self, sample):
          estim = 0
          weight = 1.0/len(sample)
          for s in range(len(sample)):
              estim += weight * self.dist.evaluate(sample[s])   
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
              
                
            


                
            
      

