# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 14:28:12 2022

@author: migue
"""

import numpy as np
import gudhi as gd
from multiprocessing import Pool as pl

def magsum(pers, *args): #Takes persistence, optional scale factor t, returns alternating sum. 
    if len(args)>0: #If scale factor t is provided, scales intervals by t. Else, t is taken to be 1.
        t=args[0]
    else:
        t=1
    """
    Alternating sum of persistence intervals of form l=(dimension, (birth,death)).
    Sum of terms (-1)^dim*(e^(-t*birth)-exp^(-t*death)) across total persistence.
    """
    p=[((-1)**(l[0]))*(np.exp(-t*l[1][0])-np.exp(-t*l[1][1])) for l in pers]
    p=np.sum(p)
    return p

def alphacomplexpersget(path, normalize=False, **kwargs): #Takes a file path or pointcloud, returns the alpha complex
    if type(path) is str:
        cloud=np.loadtxt(path, delimiter=',', dtype='float64')
    else:
        cloud=path
    if np.ndim(cloud)==1:
        Z=np.zeros_like(cloud)
        cloud=np.c_[cloud,Z]    
    a_com=gd.AlphaComplex(points=cloud) 
    simplex_tree = a_com.create_simplex_tree()
    per=simplex_tree.persistence()
    pers=[[p[0],tuple(np.sqrt(p[1]))] for p in per] #By default, has squared values. This takes the root.
    return pers

def filer(tval, amag, filename):
    out=np.transpose(np.vstack((tval,amag)))
    np.savetxt(filename, out, delimiter=',' , fmt='%1.10f')
    
def cloud_divider(path, numdivs, mindiv): #takes a file path or pointcloud, number of point clouds to return log spaced and a smallest point cloud size
    if type(path) is str:
        cloud=np.loadtxt(path, delimiter=',', dtype='float64')
    else:
        cloud=path
    if np.ndim(cloud)==1:
        Z=np.zeros_like(cloud)
        cloud=np.c_[cloud,Z]
    ptsval=np.logspace(mindiv, np.log10(len(cloud)), num=numdivs, dtype='int') #Creates the log spacing
    clouds=[cloud[0:t,:] for t in ptsval] #takes the subsamples from the original. If the original is not randomly sampled, this may produce degenerate results!
    return clouds

def pool_magsum(pers, tval): #takes list tval, returns magsums for each scaling in tval of pers
    pool=pl(processes=8)
    out=[pool.apply(magsum, args=(pers,t)) for t in tval]
    pool.close()
    return out

def alpha_magnitude_at_cards(path_or_cloud, start, steps, *args): #takes cloud or filepath cloud as pathorclour, returns 2xn array of cardinalities and alpha magnitudes
    if type(path_or_cloud) is str:
        cloud=np.loadtxt(path_or_cloud, delimiter=',', dtype='float64')
    else:
        cloud=path_or_cloud
    if len(args)>0: #If scale factor t is provided, scales intervals by t. Else, t is taken to be 1.
         t=args[0]
    else:
         t=1
    cards=np.logspace(start,np.log10(len(cloud)),steps, dtype='int')
    out=[[l,magsum(alphacomplexpersget(cloud[0:l,:], t))] for l in cards]
    savename=str(input('Save list as: '))
    np.savetxt(savename, out, delimiter=',')
    
def magsum_dim0(pers, *args): #Runs magsum but just dim 0 bars 
    if len(args)>0: #If scale factor t is provided, scales intervals by t. Else, t is taken to be 1.
        t=args[0]
    else:
        t=1
    pers=[p for p in pers if p[0]==0]
    p=[((-1)**(l[0]))*(np.exp(-t*l[1][0])-np.exp(-t*l[1][1])) for l in pers]
    p=np.sum(p)
    return p
    
def pool_magsum_dim0(pers, tval): #pooled magsum for dim 0
    pool=pl(processes=8)
    out=[pool.apply(magsum_dim0, args=(pers,t)) for t in tval]
    pool.close()
    return out