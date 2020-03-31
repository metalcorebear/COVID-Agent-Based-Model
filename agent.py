# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: metalcorebear
"""

from mesa import Agent
import model_functions
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
            self.was_infected = True
        else:
            self.susceptible = False
            self.model.infected += 1
            self.was_infected = False
        self.alive = True
        self.day = 0
        self.induced_infections = 0
        
    def step(self):
        if self.alive == True:
            for neighbor in self.model.grid.get_neighbors(self.pos):
                neighbor_obj = self.model.schedule.agents[neighbor]
                infected_bool, was_infected = model_functions.infect(self, neighbor_obj, model_params.parameters['ptrans'], model_params.parameters['reinfection_rate'])
                if infected_bool == True:
                    self.model.infected += 1
                    neighbor_obj.susceptible = False
                    self.induced_infections += 1
                    self.model.susceptible -= 1
                    if was_infected == True:
                        self.model.recovered -+ 1
            
            if self.infected == True:
                self.susceptible = False
                if self.day >= model_params.parameters['progression_period']:
                    self.alive = model_functions.coin_flip((1-model_params.parameters['death_rate']))
                    if self.alive == False:
                        self.model.dead += 1
                        self.model.infected -= 1
                        self.was_infected = True
                    elif self.alive == True:
                        recovered = model_functions.coin_flip(model_params.parameters['recovery_rate'])
                        if recovered == True:
                            self.infected = False
                            self.model.infected -= 1
                            self.model.recovered += 1
                            self.was_infected = True
                            self.susceptible = True
            
            self.day += 1


