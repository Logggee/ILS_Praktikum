# coding: utf-8
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np, scipy.stats
import matplotlib.pyplot as plt
#import tkinter
import ivisit as iv
from ivisit.matplotlib import *

from GaussDataGeneration import *

# *************************************************************************************************************
# (I) IVISIT GUI elements
# *************************************************************************************************************

#@IVISIT:SIMULATION & ivisit_LinearClassifiers 

#@IVISIT:SLIDER     & seed            & [200,1] & [0,100,5,1]        & seed            & -1 & int   & 0      # Seed for reproducible results

#@IVISIT:DICTSLIDER & Class1-GaussData-Parameters & [200,20,-1,2,10] & par_GaussData1 & 0                    # class1 data parameters
#@IVISIT:DICTSLIDERITEM  & N          & [0,200, 3,1]    & N        & int   & 10 
#@IVISIT:DICTSLIDERITEM  & mu_1       & [-5, 5, 3,0.1]  & mu_1     & float & 2 
#@IVISIT:DICTSLIDERITEM  & mu_2       & [-5, 5, 3,0.1]  & mu_2     & float & 1.0 
#@IVISIT:DICTSLIDERITEM  & Sigma_11   & [0, 5, 3,0.1]   & Sigma_11 & float & 1.0
#@IVISIT:DICTSLIDERITEM  & Sigma_22   & [0, 5, 3,0.1]   & Sigma_22 & float & 2.0
#@IVISIT:DICTSLIDERITEM  & Sigma_12   & [-5, 5, 3,0.1]  & Sigma_12 & float & 0.1

#@IVISIT:DICTSLIDER & Class2-GaussData-Parameters & [200,20,-1,2,10] & par_GaussData2 & 0                    # class2 data parameters
#@IVISIT:DICTSLIDERITEM  & N          & [0,200, 3,1]    & N        & int   & 10 
#@IVISIT:DICTSLIDERITEM  & mu_1       & [-5, 5, 3,0.1]  & mu_1     & float & 2 
#@IVISIT:DICTSLIDERITEM  & mu_2       & [-5, 5, 3,0.1]  & mu_2     & float & 1.0 
#@IVISIT:DICTSLIDERITEM  & Sigma_11   & [0, 5, 3,0.1]   & Sigma_11 & float & 1.0
#@IVISIT:DICTSLIDERITEM  & Sigma_22   & [0, 5, 3,0.1]   & Sigma_22 & float & 2.0
#@IVISIT:DICTSLIDERITEM  & Sigma_12   & [-5, 5, 3,0.1]  & Sigma_12 & float & 0.1

#@IVISIT:IMAGE       & Data Vectors   & 1.0     & [0,255]          & im_results      & int                   # image for displaying data


# *************************************************************************************************************
# (II) Auxiliary Data and Functions 
# *************************************************************************************************************

font = {'family' : 'normal',
        'weight' : 'normal', #'bold',
        'size'   : 16}
plt.rc('font', **font)


# *************************************************************************************************************
# (III) IVISIT Classes for Parameters, Data, and Simulation  
# *************************************************************************************************************

# (III.1) define parameters to be controlled by IVisit
class SimParameters(iv.IVisit_Parameters):
    seed = 14           # seed of random generator (to be able to reproduce results)
    par_GaussData1={'N':10,           # number of data points
                    'mu_1':-1.0,      # expectation (component 1)
                    'mu_2':1.0,       # expectation (component 2)
                    'Sigma_11':1.0,   # variance (component 1)
                    'Sigma_22':2.0,   # variance (component 2)
                    'Sigma_12':0.1    # covariance (between components 1 and 2)
    }
    par_GaussData2={'N':15,          # number of data points
                    'mu_1':1.0,       # expectation (component 1)
                    'mu_2':-1.0,      # expectation (component 2)
                    'Sigma_11':2.0,   # variance (component 1)
                    'Sigma_22':1.0,   # variance (component 2)
                    'Sigma_12':0.2    # covariance (between components 1 and 2)
    }
    xmin,xmax,ymin,ymax = -8,8,-8,8   # axis limits
    
# (III.2) define simulation data to be displayed by IVisit
class SimData(iv.IVisit_Data):
    im_results  = np.array([[0,0,0]])  # image of data vectors

# (III.3) define Simulation Class
class Sim(iv.IVisit_Simulation):
    def __init__(self,name_arg="ivisit_GaussDataGeneration.py"):
        iv.IVisit_Simulation.__init__(self,name_arg,SimParameters,SimData)

    def getGaussData2D(N,mu1,mu2,Sig11,Sig22,Sig12,t=0,C=2,flagOneHot=0):
            """
            generate random data matrix X of 2D Gaussian data and corresponding target matrix T
            :param N: number of Gaussian data vectors
            :param mu1: mean of component 1
            :param mu2: mean of component 2
            :param Sig11: component Sigma(1,1) of covariance matrix Sigma (=variance of first component of random vectors)
            :param Sig22: component Sigma(2,2) of covariance matrix Sigma (=variance of second component of random vectors)
            :param Sig12: component Sigma(1,2)=Sigma(2,1) of covariance matrix Sigma (=covariance between two components of random vectors)
            :param t: target value (=class index) to be stored in T (integer between 0 and C-1)
            :param C: number of different classes
            :param flagOneHot: If >1 then each line of T is a one-hot-vector; ELSE T is 1D array containing t
            :return X: data matrix of size NxD for dimension D=2
            :return T: target matrix of size NxC containing N one-hot-vectors (if flagOneHot>0) or simply 1D array of size N (if flagOneHot=0) containing t
            """
            mu=np.array([mu1,mu2])                            # define expectation vector of Gaussian
            Sig=np.array([[Sig11,Sig12],[Sig12,Sig22]])       # define covariance matrix of Gaussian
            X = np.random.multivariate_normal(mu, Sig, N)     # genarate random gausian distributed 2D Vectors
            if flagOneHot:
                T=np.zeros(N,nClasses)                        # allocate target matrix
                T[:,t]=1;                                     # set one-hot-entry of current class to 1
            else:
                T=np.zeros(N)                                 # allocate target vector
                T[:]=t                                        # set to target value
            return X,T                                        # return data matrix and target matrix

    def step(self):
        p = SimParameters    # short hand to simulation parameters
        d = SimData          # short hand to simulation data arrays

        # (i) generate data
        np.random.seed(p.seed)                               # set seed of random generator (to be able to regenerate data)
        dp=p.par_GaussData1                                  # reference to data parameters for class 1
        X1,T1=getGaussData2D(dp['N'],
                             dp['mu_1'],dp['mu_2'],
                             dp['Sigma_11'], dp['Sigma_22'], dp['Sigma_12'],
                             t=1,C=2,flagOneHot=0)           # create data for class 1
        dp=p.par_GaussData2                                  # reference to data parameters for class 2
        X2,T2=getGaussData2D(dp['N'],
                             dp['mu_1'],dp['mu_2'],
                             dp['Sigma_11'], dp['Sigma_22'], dp['Sigma_12'],
                             t=2,C=2,flagOneHot=0)           # create data for class 2
        X = np.concatenate((X1,X2))
        T = np.concatenate((T1,T2))

        # (ii) plot data
        fig = getMatplotlibFigure(figsize=(6,5))                 # create figure
        ax1 = fig.add_subplot(111)                               # create axis for contour plot of posterior distribution
        ax1.scatter(X1[:,0],X1[:,1],c='r',marker='x',s=20)                              # plot data from class 1
        ax1.scatter(X2[:,0],X2[:,1],marker='o',s=20, facecolors='none', edgecolors='b') # plot data from class 2
        ax1.set_xlabel('x1'); ax1.set_ylabel('x2')               # labels on x/y-axis
        ax1.grid(which='both')                                   # draw a grid
        ax1.set_xlim((p.xmin,p.xmax))                            # limits for axis
        ax1.set_ylim((p.ymin,p.ymax))                            # limits for axis
        d.im_results = getMatplotlibImage(fig)                   # send matplotlib image to ivisit image

        
# *************************************************************************************************************
# Main Program: Just start IVISIT simulation
# *************************************************************************************************************

sim=Sim()
sim.main_init()
sim.init()
sim.step()

iv.IVisit_main(sim=sim)
