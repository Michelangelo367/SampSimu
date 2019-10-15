
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



class samp_gen:
      def __init__(self,RVs):
            self.RVs = RVs
            self.CDF = getCDF(RVs)

