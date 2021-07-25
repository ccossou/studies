#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute the amount of water needed to dilute a given alcool to the desired
concentration of alcool

"""

from pdb import set_trace as stop
import numpy as np

def get_box_size(surface, height, nb=1):
    """
    Given the desired total surface and the height, compute the needed
    square section. If needed, can be splitted in a given number of boxes
    
    In short, we want a wood surface for the alcool. We are limited by
    the section of the bottle. 
    
    The total surface of a box of height h and square section lxl is:
    4 x (h x l) + 2 x l^2
    
    the equation is:
    2*l^2 + 4h * s - surface = 0
    
    
    Parameters
    ----------
    surface: float
        total surface needed in cm2
    height: float
        height [cm] of the boxes we want to make
    nb: int
        number of boxes we want to make
    
    """

    sol = np.roots([2, 4*height, -surface/float(nb)])
    
    width = [x for x in sol if np.isreal(x) and x > 0]
    
    if (len(width) > 1):
        stop()
    else:
        width = width[0]
    
    print("Surface {:.2f} cm^2 with {} boxes".format(surface, nb))
    print("Box size: {:.2f} cm x {:.2f} cm x {:.2f} cm".format(height, width, width))
    
    

get_box_size(150, 11.6)
get_box_size(150, 10.7)
get_box_size(150, 11.6, 2)
get_box_size(150, 10.7, 2)

