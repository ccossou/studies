#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to compute ideal time for bread, depending on temperature and quantity of yeast

Equation is of the form:
\log(\mathrm{GT}) &= a + bT + cT^2
where GT (Generation Time) is the required time to double the population

For the saccharomyces cerevisiae family (AB1), following this article:
"Growth of Saccharomyces cerevisiae and Saccharomyces uvarum in a temperature gradient incubator" (R. M. Walsh et P. A. Martin, 11 octobre 1976, Journal of the Institute of Brewing)

The formulae is:
log(GT) = 2.747 - 0.1865 * T + 0.00413 T**2

"""

from pdb import set_trace as stop
import numpy as np
import pylab as pl
from matplotlib.ticker import FormatStrFormatter


def generation_time(T):
    """
    Given the temperature in Celsius, provide the generation time, 
    unit not yet known but possibly hours
    
    For the saccharomyces cerevisiae family (AB1), following this article:
"Growth of Saccharomyces cerevisiae and Saccharomyces uvarum in a temperature gradient incubator" (R. M. Walsh et P. A. Martin, 11 octobre 1976, Journal of the Institute of Brewing)
    
    Example of values from the article, for calibration purposes:
    Engauge-digitizer was use on figure 3 of the paper cited above
    GT(6°C) ~ 60.9314
    GT(8°C) ~ 32.4341
    GT(10°C) ~ 18.8922
    GT(12°C) ~ 12.8832
    GT(14°C) ~ 8.68711
    GT(16°C) ~ 6.78103
    GT(18°C) ~ 5.53702
    GT(20°C) ~ 4.78307
    GT(22°C) ~ 4.32212
    
    x = [6 , 8 , 10 , 12 , 14 , 16 , 18 , 20 , 22]
    y = [60.9314 , 32.4341 , 18.8922 , 12.8832 , 8.68711 , 6.78103 , 5.53702 , 4.78307 , 4.32212]
    """
    
    log_GT = 2.747 - 0.1865 * T + 0.00413 * T**2
    
    GT = 10**log_GT
    
    return GT

def exponential_growth(N, t, GT):
    """
    Compute the new population given the following parameters
    
    Parameters
    ~~~~~~~~~~
    N: float
        Initial population (usually in gram of fresh yeast)
    t: float
        time in hours
    GT: float
        in hours, Generation Time, time for doubling the population
    
    Return
    ~~~~~~
    New population (in gram equivalent yeast in the preparation)
    """
    N_new = N * np.exp(t * np.log(2) / GT)
    
    return N_new

def test_GT():
    """Comparison of the function to the points defined in the article"""
    x = np.array([6 , 8 , 10 , 12 , 14 , 16 , 18 , 20 , 22])
    y_ref = np.array([60.9314 , 32.4341 , 18.8922 , 12.8832 , 8.68711 , 6.78103 , 5.53702 , 4.78307 , 4.32212])
    
    #~ y = [generation_time(xi) for xi in x]
    y = generation_time(x)
        
    import pylab as pl
    
    # We prepare the plot
    fig = pl.figure()
    # We define a fake subplot that is in fact only the plot.
    plot1 = fig.add_subplot(1, 1, 1)
    
    plot1.grid(True)
    plot1.set_xlabel("Temperature (Celsius)")
    plot1.set_ylabel("Generation Time (h)")
    plot1.semilogy(x, y_ref, 'r.', label="Article points")
    plot1.semilogy(x, y, 'b-', label="Formulae")
    plot1.legend() # afficher la legende
    pl.show()

def get_temperature(t):
    """
    give the temperature solely as a function of time
    
    Between 0 and t_fridge, temperature is T_0
    Between t_fridge and t_fridge+2h, temperature linearly increase from T_0 to T_1
    after t_fridge + 2h, temperature is T_1
    
    Parameter
    ~~~~~~~~~
    t: float
        time in hours. Must be positive
    
    Return
    ~~~~~~
    temperature in celsius
    """
    
    if (t<0.):
        raise ValueError("Time must be a positive float (hours)")
    
    t_fridge = 12. # hours
    delta_t = 2. # hours. Time estimated for warm up before the cold preparation reach room temperature
    
    T_0 = 6. # Celsius degree
    T_1 = 18. # Celsius degree
    
    
    
    if (t < t_fridge):
        temperature = T_0
    elif (t > (t_fridge + delta_t)):
        temperature = T_1
    else:
        temperature = T_0 + (T_1 - T_0) * (t - t_fridge) / 2. # Linear increase of the temperature from T_0 to T_1
    
    return temperature

def test_temperature():
    """test of the function get_temperature"""
    
    fig2 = pl.figure()
    temp = [get_temperature(ti) for ti in time]
    # We define a fake subplot that is in fact only the plot.
    plot1 = fig2.add_subplot(1, 1, 1)

    plot1.grid(True)
    plot1.set_xlabel("Time (h)")
    plot1.set_ylabel("Temperature (Celsius)")
    plot1.plot(time, temp, label="Temperature evolution")
    
    pl.show()

def get_population(delta_t, N0, t0):
    """Given time only, will provide the population
    In this function, time evolution of temperature is not a free parameter
    but rather constrained directly into the code. 
    
    Then, from the temperature, we compute the generation time
    then from the generation time we increase the population
    
    Parameter
    ~~~~~~~~~
    delta_t: float
        time in hours of population evolution, related to t0 (we get N(t0+delta_t)
    t0: float
        time in hours for N0 (N0 = N(t0)).
    N0: population (in g of fresh yeast)
    
    Return
    ~~~~~~
    N(t), population at t
    
    """
    
    T = get_temperature(t0 + delta_t) # Temperature function need the absolute time, not the relative one
    pop = exponential_growth(N0, delta_t, generation_time(T))
    
    return pop

def get_new_time(N1, t1, T1, N2, T2):
    """
    Given the initial population, temperature and total growth time
    will return the required time needed to achieve the same with another initial population and temperature
    
    Parameter
    ~~~~~~~~~
    N1: float
        Initial population of case 1
    t1: float
        growth time in hours of case 1
    T1: float
        temperature in Celsius of case 1
    N2: float
        Initial population of case 2
    T2: float
        temperature in Celsius of case 2
    
    Return
    ~~~~~~
    return t2, growth time needed in case 2
    """
    
    GT1 = generation_time(T1)
    GT2 = generation_time(T2)
    
    t2 = GT2 * (t1 / GT1 - np.log(N1 / N2) / np.log(2))
    
    return t2

def displayTime(time):
    """Will format the given time in seconds to display hours and minutes if needed. 
    
    Hence, 1200 seconds will display as 20 min
    
    Input:
    time: number of seconds
    
    Output: string formating of the given time, using hours and minutes if needed"""

    time = float(time)
    
    nb_hours = int(time)
    time = time - nb_hours
    
    nb_minutes = int(round(time * 60))
    
    # We construct the string
    str_time = ''
    if (nb_hours != 0):
        str_time += "%dh " % nb_hours
    if (nb_minutes != 0):
        str_time += "%dmin " % nb_minutes
    return str_time

#~ stop()

# We assume from now on that yeast population scale linearly. i.e, if we start with half of the initial population, we have to increase the time accordingly. 

# Tradition_PL.pdf (for 500g of flour)
# 3.11g of fresh yeast, 2h45-3h15, 24°C)
#~ print(exponential_growth(3.11, 3., generation_time(24.)))

# My bread (for 500g of flour)
# 2.5g of dry yeast, 12h at 6°C then 4h at 18°C (slow increase of time)
#~ step1 = exponential_growth(2.5, 12., generation_time(6.))
#~ step2 = exponential_growth(2.5, 12., generation_time(6.))
#~ print(exponential_growth(3.11, 3., generation_time(24.)))

#~ dry_yeast = 2. # g
t_start = 0. # hours
t_stop = 16. # hours

#~ time = np.linspace(t_start, t_stop, 1000)
#~ time = np.linspace(t_start, t_stop, 1000)
nb_points = 1000
delta_t = (t_stop - t_start) / float(nb_points)

time = []
population = []

t_prev = t_start - delta_t
pop_prev = 3.11 #g
for i in range(nb_points):
    ti = t_start + delta_t * i
    popi = get_population(delta_t, pop_prev, t_prev)
    
    if popi == None:
        stop()
    
    time.append(ti)
    population.append(popi)
    t_prev = ti
    pop_prev = popi

time = np.array(time)

pop_low = exponential_growth(3.11, time, generation_time(6.)) # Population evolution at 6 degree celsius
#~ pop_high = exponential_growth(dry_yeast*2, time, generation_time(20.)) # Population evolution at 20 degree celsius

# Tradition_PL.pdf (for 500g of flour)
# 3.11g of fresh yeast, 2h45-3h15, 24°C)
#~ print(exponential_growth(3.11, 3., generation_time(24.)))
time_ref = np.linspace(0., 3.25, 1000)
pop_ref = exponential_growth(3.15, time_ref, generation_time(24.)) # Reference from professionnal

# We prepare the plot
fig = pl.figure()
# We define a fake subplot that is in fact only the plot.
plot1 = fig.add_subplot(1, 1, 1)

myyfmt = FormatStrFormatter("%.3g")

plot1.xaxis.grid(True,which='minor', color='#666666')
plot1.yaxis.grid(True,which='minor', color='#666666')
plot1.xaxis.grid(True,which='major', color='#222222')
plot1.yaxis.grid(True,which='major', color='#222222')
plot1.set_xlabel("Temperature (Celsius)")
plot1.set_ylabel("Yeast population (g)")
plot1.yaxis.set_major_formatter(myyfmt)
plot1.yaxis.set_minor_formatter(myyfmt)

plot1.semilogy(time, population, label="Ma recette")
plot1.semilogy(time, pop_low, label="T=6 degree")
#~ plot1.semilogy(time, pop_high, label="T=20 degree")
plot1.semilogy(time_ref, pop_ref, label="Professionnal")
plot1.legend() # afficher la legende

# evolution of growth time with respect to temperature
#~ temperatures = np.arange(6, 25)
#~ growth_time = [get_new_time(N1=3.11, t1=3.25, T1=24., N2=3.11, T2=ti) for ti in temperatures]

#~ print("Temperature (Celsius) & Growth time (h)\\\\\\hline")
#~ for (Ti, ti) in zip(temperatures, growth_time):
    #~ print("{} & {}\\\\\\hline".format(Ti, displayTime(ti)))

#~ fig2 = pl.figure()
#~ # We define a fake subplot that is in fact only the plot.
#~ plot1 = fig2.add_subplot(1, 1, 1)

#~ myyfmt = FormatStrFormatter("%.3g")

#~ plot1.xaxis.grid(True,which='minor', color='#666666')
#~ plot1.yaxis.grid(True,which='minor', color='#666666')
#~ plot1.xaxis.grid(True,which='major', color='#222222')
#~ plot1.yaxis.grid(True,which='major', color='#222222')
#~ plot1.set_xlabel("Temperature (Celsius)")
#~ plot1.set_ylabel("Growth time (h)")
#~ plot1.yaxis.set_major_formatter(myyfmt)
#~ plot1.yaxis.set_minor_formatter(myyfmt)

#~ plot1.plot(temperatures, growth_time)


pl.show()

#~ pl.draw()
#~ pl.waitforbuttonpress(0) # this will wait for indefinite time

# temperature dependance of the heating part of the growth (when out of the fridge up to the ambiant temperature)
# (t0 + 0.5*(t1 - t0)*x