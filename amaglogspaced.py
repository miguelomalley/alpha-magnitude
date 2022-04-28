# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 15:12:02 2022

@author: migue
"""

import numpy as np
import alphamagnitude as am
import tkinter as tk
from tkinter import filedialog as fd
import os

if __name__=='__main__':
    root = tk.Tk()
    root.iconify()
    filename=fd.askopenfilename()
    root.destroy()
    
    start=float(input("t lower bound? "))
    stop=float(input("t upper bound? "))
    numstep=int(input("Steps? "))
    startpts=int(input("Least number of points? (log) "))
    numpts=int(input("Point Steps? "))
    
    clouds=am.cloud_divider(filename, numpts, startpts)
    tval=np.logspace(start, stop, numstep)
    pers=[am.alphacomplexpersget(c) for c in clouds]
    amag=[am.pool_magsum(p, tval) for p in pers]
    
    l=len(np.loadtxt(filename, delimiter=','))
    ptsval=np.logspace(startpts, np.log10(l), num=numpts, dtype='int')
    legnamesone=[str(p)+"_"+os.path.basename(filename) for p in ptsval]
    legnames=[f.replace(".txt","_alphmag.txt") for f in legnamesone]
    
    k=0
    for a in amag:
        am.filer(tval, a, legnames[k])
        k+=1