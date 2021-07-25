#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute the amount of water needed to dilute a given alcool to the desired
concentration of alcool

v1.1: Now can be called in command lines with arguments (v, ci and cf)

Run with: 
python dilution.py -v 750 -ci 62.5 -cf 40

"""

from pdb import set_trace as stop
import numpy as np

import argparse

# Default values
volume_in = 750.  # mL
concentration = 62.5 # ° alcool (vol)
final_concentration = 40.  # ° alcool (vol)

def get_dilution(volume_in, concentration, final_concentration):
    volume_in           = float(volume_in)
    concentration       = float(concentration)
    final_concentration = float(final_concentration)
    
    total_volume_needed = volume_in * concentration / final_concentration

    added_water = total_volume_needed - volume_in
    
    print("To dilute {} mL ({:.0f}% vol) into {:.0f}% vol, add {:.1f} mL of water (total volume: {:.1f} mL)".format(volume_in, concentration, final_concentration, added_water, total_volume_needed))
    
    #~ return added_water

parser = argparse.ArgumentParser(description='How much water is needed to dilute a given quantity of alcohol (e.g from 50° to 40°)')
parser.add_argument("-v", "--volume", help="Initial volume in mL", type=float)
parser.add_argument("-ci", "--initial-concentration", help="Initial alcohol concentration in %% vol", type=float)
parser.add_argument("-cf", "--final-concentration", help="Final alcohol concentration in %% vol", type=float)

args = parser.parse_args()

if (args.volume and args.initial_concentration and args.final_concentration):
    get_dilution(args.volume, args.initial_concentration, args.final_concentration)
else:
    #Default conversion
    print("No arguments, using default conversion")
    get_dilution(volume_in, concentration, final_concentration)
    get_dilution(640, 50, 40)
