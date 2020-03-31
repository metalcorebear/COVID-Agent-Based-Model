# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 14:36:25 2020

@author: metalcorebear
"""

import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import date as datemethod

#Random output generator
def coin_flip(ptrue):
    test = random.uniform(0.0,1.0)
    if ptrue == 0:
        out = False
    elif test < ptrue:
        out = True
    else:
        out = False
    return out


# Determine if infection is transmitted
def infect(agent_1, agent_2, ptrans, reinfection_rate):
    was_infected = agent_2.was_infected
    if (agent_2.infected == False) and (agent_2.susceptible == True):
        if agent_1.infected == True:
            if agent_2.was_infected == False:
                agent_2.infected = coin_flip(ptrans)
                if agent_2.infected == True:
                    infected_bool = True
                else:
                    infected_bool = False
            else:
                agent_2.infected = coin_flip(reinfection_rate)
                if agent_2.infected == True:
                    infected_bool = True
                else:
                    infected_bool = False
        else:
            agent_2.infected = agent_2.infected
            infected_bool = False
    else:
        infected_bool = False
    return infected_bool, was_infected


#Instantiate social network
#Chaos parameter allows for variability in following social distancing recommendations.
def build_network(interactions, population, chaos = 0.01):
    G = nx.Graph()
    G.add_nodes_from(range(population))
    nodes_list = list(G.nodes())
    edge_set = set()
    top_row = 0
    for node_1 in nodes_list:
        top_row += 1
        for node_2 in range(top_row):
            if (G.degree(node_2) < interactions) and (G.degree(node_1) < interactions):
                edge = (node_1, node_2)
                if ((edge[0],edge[1])) and ((edge[1],edge[0])) not in edge_set:
                    if not coin_flip(chaos):
                        G.add_edge(*edge)
                        edge_set.add(edge)
            else:
                if coin_flip(chaos):
                    edge = (node_1, node_2)
                    if ((edge[0],edge[1])) and ((edge[1],edge[0])) not in edge_set:
                        G.add_edge(*edge)
                        edge_set.add(edge)
    return G


#Compute SIR and dead at any point in time
def compute_susceptible(model):
    N = float(model.num_agents)
    total_susceptible = float(model.susceptible)
    susceptible_rate = total_susceptible/N
    return susceptible_rate

def compute_infected(model):
    N = float(model.num_agents)
    total_infected = float(model.infected)
    infected_rate = total_infected/N
    return infected_rate

def compute_recovered(model):
    N = float(model.num_agents)
    total_recovered = float(model.recovered)
    recovered_rate = total_recovered/N
    return recovered_rate

def compute_dead(model):
    N = float(model.num_agents)
    total_dead = float(model.dead)
    death_rate = total_dead/N
    return death_rate

# Compute R0
def compute_R0(model):
    induced_infections = [agent.induced_infections for agent in model.schedule.agents]
    #induced_infections_ = [value for value in induced_infections if value != 0]
    infection_array = np.array(induced_infections)
    R0 = np.average(infection_array)
    return R0


# Plot output
def plot_SIR(df_out, output_path):
    today = datemethod.strftime(datemethod.today(), '%Y-%m-%d')
    plot_name = today + 'SIR_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column != 'R0':
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - SIR')
    plt.xlabel('Step')
    plt.ylabel('Population Fraction')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()
    
def plot_R0(df_out, output_path):
    today = datemethod.strftime(datemethod.today(), '%Y-%m-%d')
    plot_name = today + 'R0_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'R0':
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - R0')
    plt.xlabel('Step')
    plt.ylabel('R0')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()