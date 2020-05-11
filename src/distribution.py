
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
                                              
        abstract method evaluate is the function for evaluation of an observation
        The reason that this method is abstract is that based on different 
        application there are different ways of evaluating an observation
             

"""

import itertools
from abc import ABC, abstractmethod 

class Eval(ABC):
    def evaluate(self, obs): #abstract method for evaluating an observation
        pass
    def approxeval(self, obs): #abstract method for approximate evaluation 
        pass                           # an obsrvation
        

'''
combine funcions from: 
    https://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists
'''
combinations = []
def combine(terms, accum):
    last = (len(terms) == 1)
    n = len(terms[0])
    for i in range(n):
        item = accum + [terms[0][i]]
        if last:
            combinations.append(item)
        else:
            combine(terms[1:], item)
    return combinations

combinations2 = []
def combine2(terms, accum):
    last = (len(terms) == 1)
    n = len(terms[0])
    for i in range(n):
        item = accum * terms[0][i]
        if last:
            combinations2.append(item)
        else:
            combine2(terms[1:], item)
    return combinations2


class ProbDist(Eval):
    def __init__(self, RVs, totsamp = None, totprob = None, mu = None):
        self.RVs = RVs
        self.rvnum = len(RVs)
        self.rvsizes = [len(r[0]) for r in RVs]
        self.totsamp = totsamp
        self.totprob = totprob
        self.mu = mu
        
    # Python code to get the Cumulative sum of a list 
    def Cumulative(self, lists): 
        self.cu_list = [] 
        length = len(lists) 
        self.cu_list = [sum(lists[0:x + 1]) for x in range(0, length)] 
        return self.cu_list 
    
    
    # Finding the CDF of a mass funciton
    def getCDF(self):
        self.CDF = []
        for i in range(len(self.RVs)):
              self.CDF.append([self.RVs[i][0],self.Cumulative(self.RVs[i][1])])
        
        return self.CDF
    

    #get the total possible outcomes of the distribution and their weights
    def gettot(self):
        combinations = []
        combinations2 = []
        if self.totsamp == None:
            vals = [rv[0] for rv in self.RVs]
            probs = [rv[1] for rv in self.RVs]
            self.totsamp = combine(vals,[])
            self.totprob = combine2(probs,1.0)
        else:
            return [self.totsamp, self.totprob]
    
    #Finding the original mean of the population \mu
    #This mean depends on the evaluation function which is abstract 
    #and should be defined by the user
    def getmu(self):
        if self.mu == None:
            evalval = 0.0
            for s in range(len(self.totsamp)):
                evalval += self.totprob[s] * self.evaluate(self.totsamp[s])
            self.mu = evalval
            return evalval                
        else:
            return self.mu 

    