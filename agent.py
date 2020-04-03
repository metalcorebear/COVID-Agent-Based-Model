# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: metalcorebear
"""

from mesa import Agent
import model_functions
import numpy as np
import model_params

#Agent class
class human(Agent):
    
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.infected = model_functions.coin_flip(model_params.parameters['I0'])
        if self.infected == False:
            self.susceptible = True
            self.model.susceptible += 1
            self.severe = False
        else:
            self.susceptible = False
            self.model.infected += 1
            self.severe = model_functions.coin_flip(model_params.parameters['severe'])
        self.was_infected = False
        self.alive = True
        self.day = 0
        self.induced_infections = 0
        self.infected_others = False
        
    def step(self):
        if self.alive == True:
            for neighbor in self.model.grid.get_neighbors(self.pos):
                neighbor_obj = self.model.schedule.agents[neighbor]
                infected_bool, was_infected = model_functions.infect(self, neighbor_obj, model_params.parameters['ptrans'], model_params.parameters['severe'], model_params.parameters['reinfection_rate'])
                if infected_bool == True:
                    self.model.infected += 1
                    neighbor_obj.susceptible = False
                    neighbor_obj.day = 0
                    self.induced_infections += 1
                    self.infected_others = True
                    self.model.susceptible -= 1
                    if was_infected == True:
                        self.model.recovered -= 1
            
            if self.infected == True:
                self.susceptible = False
                progression_threshold = int(np.random.normal(model_params.parameters['progression_period'],model_params.parameters['progression_sd']))
                if self.day >= progression_threshold:
                    if self.severe == True:
                        self.alive = model_functions.coin_flip((1-model_params.parameters['death_rate']))
                        if self.alive == False:
                            self.model.daily_deaths += 1
                            self.susceptible = False
                            self.model.dead += 1
                            self.severe = False
                            self.model.infected -= 1
                            self.was_infected = True
                if self.alive == True:
                    recovery_threshold = int(np.random.normal(model_params.parameters['recovery_days'],model_params.parameters['recovery_sd']))
                    if self.day >= recovery_threshold:
                        self.infected = False
                        self.severe = False
                        self.model.infected -= 1
                        if model_functions.coin_flip(model_params.parameters['reinfection_rate']):
                            self.susceptible = True
                            self.model.susceptible += 1
                        else:
                            self.model.recovered += 1
                            self.susceptible = False
                        self.was_infected = True
                        self.day = 0
            
            self.day += 1


