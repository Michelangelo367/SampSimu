# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:46:08 2020

@author: siavash tabrizian stabrizian@smu.edu
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

        
'''
   This class contains the subroutine for visualization using the sampling 
   and resampling classes.
   
   resampling input is an instance of resampling class from the resampling module
'''
class visualsamp():
    def __init__(self, resampling, loc):
        self.resample = resampling
        self.loc = loc
        if not os.path.exists(self.loc):
            os.makedirs(self.loc)
        self.figcount = 0
    
    #Visualization on law of large numbers 
    def lawlargevs(self, minssize = 10, maxssize = 100, \
                   increment = 10, samptype = ['SRS'], separate = False,\
                   title = 'Law of Large Numbers'):
        truemean = self.resample.sampling.dist.getmu()
        if separate == False:
            fig = plt.figure(num = self.figcount)
        for st in samptype:
            self.resample.samptype = st
            mean = []
            expnum = 0
            confupp = []
            confdwn = []
            mu = []
            x = []
            for sz in range(minssize,maxssize,increment):
                x.append(sz)
                self.resample.rssize = sz
                out = self.resample.monte_carlo()
                mean.append(out[0][0])
                mu.append(truemean)
                out = self.resample.getCI(out[0][0],out[0][1])
                confupp.append(out[0])
                confdwn.append(out[1])
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
        plt.fill_between(np.array(x),np.array(confupp),np.array(confdwn), alpha = 0.3)
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
        truemean = self.resample.sampling.dist.getmu()
        self.resample.samptype = samptype
        self.resample.rssize = ssize
        o = self.resample.monte_carlo()
        CI = self.resample.getCI(o[0][0],o[0][1])
        meanlist = []
        std = self.resample.sampling.dist.getsigma()
        for m in o1[1]:
            meanlist.append((m-truemean)/(std/np.sqrt(len(o1[1]))))
        n, bins, patches = plt.hist(np.array(meanlist), num_bins, density = True,\
                                    facecolor = 'blue', alpha = 0.5) 
        y = norm.pdf(bins,0.0,1.0)
        plt.plot(bins,y,'r--')
        plt.xlabel('mean estimates')
        plt.ylabel('probabilities')
        plt.title(title)
        plt.show
        plt.savefig(self.loc + '/central')
        
    
    #Comparing barcharts
    def barcompare(self, minssize = 10, maxssize = 100, \
                   increment = 10, samptype = ['SRS', 'LHS'], separate = False,\
                   title = 'Comparing sampling techniques'):
        std1 = []
        std2 = []
        xlabel = []
        for ss in range(minssize,maxssize, increment):
            self.resample.samptype = samptype[0]
            self.resample.rssize = ss
            o = self.resample.monte_carlo()
            CI = self.resample.getCI(o[0][0],o[0][1])
            std1.append(self.resample.std)
            self.resample.samptype = samptype[1]
            self.resample.rssize = ss
            o = self.resample.monte_carlo()
            CI = self.resample.getCI(o[0][0],o[0][1])
            std2.append(self.resample.std)
            xlabel.append(ss)
        width = 0.3
        fig, ax = subplots()
        x = np.arange(len(xlabel))
        rec1 = ax.bar(x - width/2, std1, width, label = samptype[0])
        rec1 = ax.bar(x - width/2, std2, width, label = samptype[1])
        ax.set_ylabel('standard deviation')
        ax.set_xlabel('sample size')
        ax.set_xticks(x)
        ax.set_xticklabels(xlabel)
        ax.legend
        fig.tightlayout()
        plt.show
        plt.savefig(self.loc + '/bar_'+samptype[0]+'_'+samptype[1])
            
            
