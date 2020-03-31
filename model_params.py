# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:37:10 2020

@author: metalcorebear
"""

# ptrans = Transmission probability.
# population = Total population within all containers.
# progression_period = Average number of days until disease outcome (death or recovery).
# interactions = Average number of interactions per person per day (decreases with social distancing).
# reinfection_rate = Probability of becoming reinfected after recovery.
# I0 = Initial probability of being infected.
# death_rate = Probability of dying after being infected for number of days in progession period.
# recovery_rate = Probability of recovering after being infected for number of days in progession period.
# steps = number of days to simulate the model.

parameters = {'I0':0.02, 'ptrans':0.5, 'progression_period':30, 
              'population':100, 'interactions':6, 'reinfection_rate':0.00, 
              'death_rate':0.0193, 'recovery_rate':0.01, 'steps':120}
