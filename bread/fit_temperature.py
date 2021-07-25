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

#~ def func(x, a, b):
    #~ return a * (1. - np.exp(-x / b))
#~ func_display = "{} * (1 - np.exp(-x / {}))"

def func(x, a):
    return 16. * (1. - np.exp(-x / a))
func_display = "16. * (1 - np.exp(-x / {}))"


xdata = np.array([0, 10, 30, 60, 80, 120, 160, 180]) # Time (minutes)
ydata = np.array([6, 7.6, 12, 14, 14.3, 15, 15.8, 16.2]) # Temperature (celsius)

# Fit
popt, pcov = curve_fit(func, xdata, ydata)

yfunc = func(xdata, *popt)

# We prepare the plot
fig = pl.figure()
# We define a fake subplot that is in fact only the plot.
plot1 = fig.add_subplot(1, 1, 1)

plot1.grid(True)
plot1.set_xlabel("Time (min)")
plot1.set_ylabel("Temperature (Celsius)")
plot1.semilogy(xdata, ydata, 'r.', label="Measurements")
plot1.semilogy(xdata, yfunc, 'b-', label=func_display.format(*popt))
plot1.legend() # afficher la legende
pl.show()

#~ stop()

