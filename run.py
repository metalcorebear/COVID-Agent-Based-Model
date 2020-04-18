# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:52:39 2020

@author: metalcorebear
"""

from model import COVID_model
import model_params
import argparse
import os
import numpy as np
from datetime import date as datemethod
from datetime import datetime
from mesa.batchrunner2 import BatchRunnerMP
import mesa_SIR.calculations_and_plots as c_p
from multiprocess import freeze_support


# Specify arguments
def get_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Enter the output path.', required=False)
    parser.add_argument('-br', '--BatchRunner', help="additional variable to run BatchRunner", required=False)
    args = vars(parser.parse_args())


    output_path = str(args['output'])
    if args["BatchRunner"] != None:
        batch = int(args["BatchRunner"])
    else:
        batch = None
    return output_path, batch


# Generate output file name parameters
output_path, batch = get_path()
today = datemethod.strftime(datetime.utcnow(), '%Y%m%dZ%H%M%S')

# Number of steps to run model.
steps = model_params.parameters['steps']

filename = 'COVID_output_' + today + '.csv'
output_file = os.path.join(output_path, filename)

# Instantiate model
if __name__ == "__main__":

    freeze_support()

    if isinstance(batch, int):
        print ("batch is running")
        variable_params = {"population": range(500,1000,500),
                           "I0": np.linspace(0.1,0.5, num=2),
                           "ptrans": np.linspace(0.1,0.5, num=2),
                           "interactions": range(1,10,4)}

        fixed_params = {"reinfection_rate" : model_params.parameters["reinfection_rate"],
                        "progression_sd": model_params.parameters["progression_sd"],
                        "progression_period": model_params.parameters["progression_period"],
                        "recovery_days": model_params.parameters["recovery_days"],
                        "recovery_sd": model_params.parameters["recovery_sd"],
                        "death_rate": model_params.parameters["death_rate"],
                        "severe": model_params.parameters["severe"]}

        # The variables parameters will be invoke along with the fixed parameters allowing
        # or either or both to be honored.
        batch_run = BatchRunnerMP(
            COVID_model,
            nr_processes=batch,
            max_steps=steps,
            variable_parameters=variable_params,
            fixed_parameters = fixed_params,
            iterations=2,
            model_reporters={"infected": [c_p.compute, [COVID_model, "infected"]],
                             "recovered": [c_p.compute, [COVID_model, 'recovered']],
                             "susceptible": [c_p.compute, [COVID_model, "susceptible"]],
                             "dead": [c_p.compute, [COVID_model, "dead"]],
                             "R0": [c_p.compute, [COVID_model, "R0"]],
                             "severe_cases": [c_p.compute, [COVID_model, "severe"]]})

        output_data =batch_run.run_all()
        #output_data = batch_run.get_model_vars_dataframe()

    else:
        print ("batch is not running")
        meme_model = COVID_model(reinfection_rate = model_params.parameters["reinfection_rate"],
                                 progression_sd= model_params.parameters["progression_sd"],
                                 progression_period= model_params.parameters["progression_period"],
                                 recovery_days= model_params.parameters["recovery_days"],
                                 recovery_sd= model_params.parameters["recovery_sd"],
                                 death_rate = model_params.parameters["death_rate"],
                                 severe= model_params.parameters["severe"],
                                 population = model_params.parameters["population"],
                                 I0= model_params.parameters["I0"],
                                 ptrans=model_params.parameters["ptrans"],
                                 interactions=model_params.parameters["interactions"])


        for i in range(steps):
            #print('Running step {}'.format(str(i)))
            meme_model.step()
        # Generate output
        output_data = meme_model.datacollector.get_model_vars_dataframe()



    for output in output_data.values():
        c_p.save_data(output_data, output_path=output_path, filename=filename)

        #print(output_data)
        #print('Filename:')
        #print(filename)

        print('Plotting...')
        title = 'COVID ABM Model Output'
        c_p.plot_SIR(output, title, output_path)
        c_p.plot_R0(output, title, output_path)
        c_p.plot_severe(output, title, output_path)

        print('You are great!!')
