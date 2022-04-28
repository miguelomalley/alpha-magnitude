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
    tval=np.logspace(start,stop,numstep)
    
    pers=am.alphacomplexpersget(filename)
    amag=am.pool_magsum(pers, tval)
    
    cloud=np.loadtxt(filename, delimiter=',')
    savename=str(len(cloud))+'_'+os.path.basename(filename)
    savename.replace('.txt', '_alphamag.txt')
    am.filer(tval, amag, savename)
