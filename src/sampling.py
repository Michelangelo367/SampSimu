
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
             

"""

from distribution import getCDF
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
      #print(val)
      #print(prob)
      #print(zone)
      draw = [val[i] for i in range(len(RV[1])) if prob[i] >= zone]
      #print(draw)
      return draw[0]

# sampling class contains subroutines associated with different 
# sampling techniques
class samp_gen:
      def __init__(self,RVs,seed = 0):
            self.RVs = RVs
            self.rv_num = len(RVs)
            self.CDF = getCDF(RVs)
            self.newdist = RVs
            self.sample  = []
            self.seed    = seed
            
      def monte_samp(self, n, seed = 0):
            if seed != 0:
                  self.seed = seed 
            
            np.random.seed(self.seed)
            for s in range(n):                
                zone = np.random.uniform(0.0,1.0,self.rv_num).tolist()
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
            
            return self.sample
      
      def antithetic(self, n, seed = 0):
            if seed != 0:
                  self.seed = seed 
            
            np.random.seed(self.seed)
            for s in range(round(float(n)/2.0)):                
                zone = np.random.uniform(0.0,1.0,self.rv_num).tolist()
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
                zone1 = 1.0 - zone
                samp = [getVal(self.CDF[r], zone1[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
            
            return self.sample      

      def lhs(self, n, seed = 0):
            if seed != 0:
                  self.seed = seed 
            
            interval = 1.0/float(n)
            self.permute = [np.random.permutation(n).tolist() for r in range(self.rv_num)]
            np.random.seed(self.seed)
            for s in range(n):                
                zone = []
                for i in range(self.rv_num):
                      lo = max(0.0, (self.permute[i]-1) * interval )
                      hi = self.permute[i] * interval 
                      zone.append(np.random.uniform(lo,hi,1).tolist()[0])
                samp = [getVal(self.CDF[r], zone[r]) for r in range(len(self.CDF))]
                self.sample.append(samp)
            
            return self.sample
            
      
      
      
      

