
"""
@author: siavash tabrizian
"""


"""

        Format : RVs = [ [Var1], [Var2], ...] Var: random variable
        [Var1] = [[Values],[Probabilities]] : Mass function of the random
                                              variable 1
             

"""

# Python code to get the Cumulative sum of a list 
def Cumulative(lists): 
    cu_list = [] 
    length = len(lists) 
    cu_list = [sum(lists[0:x + 1]) for x in range(0, length)] 
    return cu_list 


# Finding the CDF of a mass funciton
def getCDF(RVs):
    CDF = []
    for i in range(len(RVs)):
          CDF.append([RVs[i][0],Cumulative(RVs[i][1])])
    
    return CDF
    