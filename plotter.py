# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 09:09:31 2022

@author: migue
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog as fd

if __name__=="__main__":
    root = tk.Tk()
    root.iconify()
    filename=fd.askopenfilename()
    root.destroy()
    
    points=np.loadtxt(filename, dtype='float64', delimiter=',')
    
    if points.dtype==complex:
        points=np.c_[points.real, points.imag]
    
    plt.figure(num=1, figsize=(8,6), dpi=100)
    ax=plt.gca()
    plt.grid(False, linestyle='--')
    plt.scatter(points[:,0], points[:,1], s=1)
    
    plt.legend()
    plt.draw()