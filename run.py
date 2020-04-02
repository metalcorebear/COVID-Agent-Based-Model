# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:52:39 2020

@author: metalcorebear
"""

from model import COVID_model
import model_params
import argparse
import os
from datetime import date as datemethod
from datetime import datetime
import mesa_SIR.calculations_and_plots as c_p

# Specify arguments
def get_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Enter the output path.', required=False)
    args = vars(parser.parse_args())
    print (args)
    output_path = str(args['output'])
    return output_path

# Generate output file name parameters
output_path = get_path()

today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')

# Number of steps to run model.
steps = model_params.parameters['steps']

filename = 'COVID_output_' + today + '.csv'
output_file = os.path.join(output_path, filename)

# Instantiate model
meme_model = COVID_model()

for i in range(steps):
    print('Running step {}'.format(str(i)))
    meme_model.step()

# Generate output    
output_data = meme_model.datacollector.get_model_vars_dataframe()
c_p.save_data(output_data, output_path = output_path, filename =filename)

print (output_data)
print('Filename:')
print(filename)

print('Plotting...')
title = 'COVID ABM Model Output'
c_p.plot_SIR(output_data, title, output_path)
c_p.plot_R0(output_data, title, output_path)
c_p.plot_severe(output_data, title, output_path)

print('You are great!!')


