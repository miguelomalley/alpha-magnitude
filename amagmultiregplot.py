# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 12:21:45 2022

@author: migue
"""

import numpy as np
import gudhi as gd
import rotcal
from multiprocessing import Pool as pl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog as fd
import os

if __name__=="__main__":
    root = tk.Tk()
    root.iconify()
    filenames=fd.askopenfilenames()
    root.destroy()
    
    plt.figure(num=1, figsize=(8,6), dpi=100)
    ax=plt.gca()
    k=1
    for filename in filenames:
        p='0'
        for s in os.path.splitext(os.path.basename(filename))[0]:
            if s=='_':
                break
            else:
                p=p+s
        p=int(p)
        pers=np.loadtxt(filename, delimiter=',')
        perss=np.log10(pers)
        persss=perss[perss[:,0] >= 1.75]
        persss=persss[persss[:,0] <= np.log10(p)-2]
        color=next(ax._get_lines.prop_cycler)['color']
        if len(persss)>0:
            m,c=np.polyfit(persss[:,0], persss[:,1], 1)
            L=[((10**c))*(p**m) for p in pers[:,0]]
            L=np.log10(L)
            plt.plot(perss[:,0], L, 'm--', label='slope='+str(m))
            plt.axvline(1.75,  color='k', linestyle='dashed')
            plt.axvline(np.log10(p)-2, color=color, linestyle='dashed')
        
        plt.plot(perss[:,0], perss[:,1], label= r'$\log |tX $'+str(k)+r'$|_\alpha,\,$' + '#X'+str(k)+'='+str(p), color=color)
        k+=1
  
    plt.xlabel(r'$\log t$', fontsize=15)
    plt.ylabel(r'$\log |tX_n|_{\alpha}$', fontsize=15)
    plt.grid(True, linestyle='--')
    
    plt.legend()
    plt.savefig('tempfig.png')
    plt.draw()
    print(m)


    
    