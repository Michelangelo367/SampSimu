# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:17:00 2020

@author: siavash tabrizian stabrizian@smu.edu
"""


from distribution import ProbDist
from sampling import samp_gen
from resampling import resampling
from sampvisual import visualsamp


var1 = [[0.0,1.0,2.0],[0.1,0.4,0.5]]
var2 = [[1.5,2.5,3.5,4.5,8.0],[0.05,0.05,0.2,0.4,0.3]]
var3 = [[0.1,7.0],[0.05,0.95]]
var4 = [[0.0,0.05,0.07,0.9,0.4],[0.2,0.2,0.5,0.05,0.05]]

RVs =[var1,var2,var3,var4]


def evalfunc(obs):
    out = 0.0
    out += 10*obs[0]*obs[1]
    out += 100*obs[2]
    out += (10*obs[3])**2
    return out

dist = ProbDist(RVs, evalfunc) #instance of the distribution with its evaluation function

sampl = samp_gen(dist)

resampl = resampling(sampl)

visual = visualsamp(resampl,'Res/')

visual.lawlargevs()

resampl.n_rep = 150
visual.centlimit()
    