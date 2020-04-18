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
from mesa_SIR import SIR
import model_params
import mesa_SIR.calculations_and_plots as c_p

class COVID_model(Model):
    
    def __init__(self, interactions, population, ptrans, reinfection_rate, I0, severe, progression_period,
                        progression_sd, death_rate, recovery_days, recovery_sd):
        super().__init__(Model)
        
        self.susceptible = 0
        self.dead = 0
        self.recovered = 0
        self.infected = 0
        interactions = interactions
        self.population = population
        self.SIR_instance = SIR.Infection(self, ptrans = ptrans,
                                          reinfection_rate = reinfection_rate,
                                          I0=I0,
                                          severe=severe,
                                          progression_period=progression_period,
                                          progression_sd=progression_sd,
                                          death_rate=death_rate,
                                          recovery_days=recovery_days,
                                          recovery_sd=recovery_sd)
        G = SIR.build_network(interactions, self.population)
        self.grid = NetworkGrid(G)
        self.schedule = RandomActivation(self)
        self.dead_agents = []
        self.running = True
    
        for node in range(self.population):
            new_agent = agent.human(node, self)
            self.grid.place_agent(new_agent, node)
            self.schedule.add(new_agent)

        #self.meme = 0
        self.datacollector = DataCollector(model_reporters={"infected": [c_p.compute, [self,'recovered']],
                                                            "recovered": [c_p.compute, [self,'recovered']],
                                                            "susceptible": [c_p.compute, [self,"susceptible"]],
                                                            "dead": [c_p.compute, [self, "dead"]],
                                                            "R0": [c_p.compute, [self, "R0"]],
                                                            "severe_cases": [c_p.compute, [self,"severe"]]})
        self.datacollector.collect(self)
    
    def step(self):

        self.schedule.step()
        
        self.datacollector.collect(self)

        if self.dead == self.schedule.get_agent_count():
            self.running = False
        else:
            self.running = True


