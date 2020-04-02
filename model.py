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
    
    def __init__(self):
        super().__init__(Model)
        
        self.susceptible = 0
        self.dead = 0
        self.recovered = 0
        self.infected = 0
        interactions = model_params.parameters['interactions']
        self.population = model_params.parameters['population']
        self.SIR_instance = SIR.Infection(self, ptrans = model_params.parameters['ptrans'],
                                          reinfection_rate = model_params.parameters['reinfection_rate'],
                                          I0= model_params.parameters["I0"],
                                          severe = model_params.parameters["severe"],
                                          progression_period = model_params.parameters["progression_period"],
                                          progression_sd = model_params.parameters["progression_sd"],
                                          death_rate = model_params.parameters["death_rate"],
                                          recovery_days = model_params.parameters["recovery_days"],
                                          recovery_sd = model_params.parameters["recovery_sd"])


        G = SIR.build_network(interactions, self.population)
        self.grid = NetworkGrid(G)
        self.schedule = RandomActivation(self)
        self.dead_agents = []
        self.running = True
    
        for node in range(self.population):
            new_agent = agent.human(node, self) #what was self.next_id()
            self.grid.place_agent(new_agent, node)
            self.schedule.add(new_agent)

        #self.meme = 0
        self.datacollector = DataCollector(model_reporters={"infected": lambda m: c_p.compute(m,'infected'),
                                                            "recovered": lambda m: c_p.compute(m,'recovered'),
                                                            "susceptible": lambda m: c_p.compute(m,"susceptible"),
                                                            "dead": lambda m: c_p.compute(m, "dead"),
                                                            "R0": lambda m: c_p.compute(m, "R0"),
                                                            "severe_cases": lambda m: c_p.compute(m,"severe")})
        self.datacollector.collect(self)
    
    def step(self):
        self.schedule.step()
        
        self.datacollector.collect(self)
        '''
        for a in self.schedule.agents:
            if a.alive == False:
                self.schedule.remove(a)
                self.dead_agents.append(a.unique_id)
        '''

        if self.dead == self.schedule.get_agent_count():
            self.running = False
        else:
            self.running = True


