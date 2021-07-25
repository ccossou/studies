#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fitting yeast growth from 

"""

from pdb import set_trace as stop


import numpy as np
from scipy.optimize import curve_fit
import pylab as pl

def compare_fit(xdata, ydata, func, constants):
    """
    Display in the same plot the original data as points and the fitted curve as a line
    
    Parameters
    ~~~~~~~~~~
    xdata: np.array
        x axis
    ydata: np.array
        original y data
    func: function object
        first argument must be x, all the remainings are constants
    constants: list of constants
        fit results given by curve_fit
    
    """
    try:
        yfunc = func(xdata, *constants, verbose=True)
    except:
        stop()
        
    # We prepare the plot
    fig = pl.figure()
    # We define a fake subplot that is in fact only the plot.
    plot1 = fig.add_subplot(1, 1, 1)
    
    plot1.grid(True)
    plot1.set_xlabel("Temperature (Celsius)")
    plot1.set_ylabel("Generation Time (h)")
    plot1.semilogy(xdata, ydata, 'r.', label="Article points")
    plot1.semilogy(xdata, yfunc, 'b-', label="Formulae")
    plot1.legend() # afficher la legende
    pl.show()

def func(x, a, b, c):
    return a * np.exp(-b * x) + c
func_display = "{} * np.exp(-{} * x) + {}"



xdata = np.array([6 , 8 , 10 , 12 , 14 , 16 , 18 , 20 , 22])
ydata = np.array([60.9314 , 32.4341 , 18.8922 , 12.8832 , 8.68711 , 6.78103 , 5.53702 , 4.78307 , 4.32212])

# Fit
popt, pcov = curve_fit(func, xdata, ydata)

yfunc = func(xdata, *popt)

# We prepare the plot
fig = pl.figure()
# We define a fake subplot that is in fact only the plot.
plot1 = fig.add_subplot(1, 1, 1)

plot1.grid(True)
plot1.set_xlabel("Temperature (Celsius)")
plot1.set_ylabel("Generation Time (h)")
plot1.semilogy(xdata, ydata, 'r.', label="Article points")
plot1.semilogy(xdata, yfunc, 'b-', label=func_display.format(popt))
plot1.legend() # afficher la legende
pl.show()

#~ stop()

