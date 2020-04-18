# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:37:10 2020

@author: metalcorebear
"""

# ptrans = Transmission probability.
# population = Total population within all containers.
# progression_period = Average number of days until a patient seeks treatment.
# progression_sd = Standard deviation of progression_period.
# interactions = Average number of interactions per person per day (decreases with social distancing).
# reinfection_rate = Probability of becoming susceptible again after recovery.
# I0 = Initial probability of being infected.
# death_rate = Probability of dying after being infected after progression_period and before recovery_days.
# recovery_days = Average number of days until recovery.
# recovery_sd = Standard deviation of recovery_days.
# severe = Probability of developing severe, symptomatic disease.
# steps = number of days in siimulation.

parameters = {'I0':0.01, 'ptrans':0.25, 'progression_period':3, 
              'progression_sd':2, 'population':100, 'interactions':6,
              'reinfection_rate':0.00, 'death_rate':0.0193, 
              'recovery_days':21, 'recovery_sd':7, 'severe':0.18, 'steps':20}
