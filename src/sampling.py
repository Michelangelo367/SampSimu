
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
            
            for s in range(n):
                zone = np.random.uniform(0.0,1.0,self.rv_num).tolist()[0]
                samp = [getVal(rv, self.seed) for rv in RVs]
                self.sample.append(samp)
            
            return self.sample

