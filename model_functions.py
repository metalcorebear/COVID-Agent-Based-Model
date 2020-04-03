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
from datetime import datetime

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
def infect(agent_1, agent_2, ptrans, psevere, reinfection_rate):
    was_infected = agent_2.was_infected
    if (agent_2.infected == False) and (agent_2.susceptible == True):
        if agent_1.infected == True:
            if agent_2.was_infected == False:
                agent_2.infected = coin_flip(ptrans)
                if agent_2.infected == True:
                    infected_bool = True
                    agent_2.severe = coin_flip(psevere)
                else:
                    infected_bool = False
                    agent_2.severe = False
            else:
                #agent_2.infected = coin_flip(reinfection_rate)
                agent_2.infected = coin_flip(ptrans)
                if agent_2.infected == True:
                    infected_bool = True
                    agent_2.severe = coin_flip(psevere)
                else:
                    infected_bool = False
                    agent_2.severe = False
        else:
            agent_2.infected = agent_2.infected
            infected_bool = False
    else:
        infected_bool = False
    return infected_bool, was_infected


#Instantiate social network
#Chaos parameter allows for variability in following social distancing recommendations.
def build_network(interactions, population, chaos = 0.001):
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
    total_susceptible = float(model.susceptible)
    return total_susceptible

def compute_infected(model):
    total_infected = float(model.infected)
    return total_infected

def compute_recovered(model):
    total_recovered = float(model.recovered)
    return total_recovered

def compute_dead(model):
    total_dead = float(model.dead)
    return total_dead

# Compute R0
def compute_R0(model):
    induced_infections = [a.induced_infections for a in model.schedule.agents if a.infected_others == True]
    if len(induced_infections) == 0:
        induced_infections = [0]
    #induced_infections_ = [value for value in induced_infections if value != 0]
    infection_array = np.array(induced_infections)
    R0 = np.average(infection_array)
    return R0

# Compute number of severe cases
def compute_severe(model):
    severe_infections_ = [1 for a in model.schedule.agents if a.severe == True]
    severe_infections = sum(severe_infections_)
    return severe_infections

# Compute daily deaths
def compute_daily_deaths(model):
    deaths = model.daily_deaths
    return deaths

# Plot output
def plot_SIR(df_out, output_path):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'SIR_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if (column != 'R0') and (column != 'severe_cases') and (column != 'daily_deaths'):
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - SIR')
    plt.xlabel('Day')
    plt.ylabel('Population')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()
    
def plot_R0(df_out, output_path):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'R0_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'R0':
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - R0')
    plt.xlabel('Day')
    plt.ylabel('R0')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()

def plot_severe(df_out, output_path):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'Severe_Cases_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'severe_cases':
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - Severe Cases')
    plt.xlabel('Day')
    plt.ylabel('Number of Severe Cases')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()

def plot_daily_deaths(df_out, output_path):
    today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')
    plot_name = 'Daily_Deaths_' + today + '_.png'
    ax = plt.subplot(111)
    for column in list(df_out.columns):
        if column == 'daily_deaths':
            ax.plot(df_out[column], label=column)
    plt.title('COVID ABM Model Output - Deaths per Day')
    plt.xlabel('Day')
    plt.ylabel('Number of Deaths')
    ax.legend()
    plt.savefig(os.path.join(output_path, plot_name), dpi=300)
    plt.close()