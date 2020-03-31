# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:21:34 2020

@author: metalcorebear
"""

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import agent
import model_functions
import model_params

class COVID_model(Model):
    
    def __init__(self):
        super().__init__(Model)
        
        self.susceptible = 0
        self.dead = 0
        self.recovered = 0
        self.infected = 0
        interactions = model_params.parameters['interactions']
        population = model_params.parameters['population']
        
        self.num_agents = population
        
        G = model_functions.build_network(interactions, population)
        self.grid = NetworkGrid(G)
        self.schedule = RandomActivation(self)
        
        self.running = True
    
        for node in range(population):
            new_agent = agent.human(self.next_id(), node, self)
            self.grid.place_agent(new_agent, node)
            self.schedule.add(new_agent)
    
        #self.meme = 0
        self.datacollector = DataCollector(model_reporters={"infected_fraction": model_functions.compute_infected, 
                                                            "recovered_fraction": model_functions.compute_recovered, 
                                                            "susceptible_fraction": model_functions.compute_susceptible, 
                                                            "dead_fraction": model_functions.compute_dead, 
                                                            "R0": model_functions.compute_R0})
        self.datacollector.collect(self)
    
    def step(self):
        self.schedule.step()
        
        self.datacollector.collect(self)
        
        if self.dead == self.schedule.get_agent_count():
            self.running = False
        else:
            self.running = True


