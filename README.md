# COVID Infection Model

(C) 2020 Mark M. Bailey

## About
This repository contains an agent-based model simulating COVID transmission within social networks using Mesa.  Model parameters can be set in the 'model_params.py" file.  Produces a dataframe output over quasi-time (steps).

This is a work in progress and is intended for research purposes only.<br />

Several parameters were taken from the following report:<br />
https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-College-COVID19-symptom-progression-11-03-2020.pdf

## Model Description
This is an SIR (susceptible, infected, recovered) model for COVID.  Model parameters can be set to simulate the changes in these three variables, as well as the reproduction number (R0) and number of severe cases, over time.  An R0 less than 1 would indicate that the epidemic is becoming extinguished.  This can be used to simulate the effects of social distancing.

## Model Parameters
* ptrans = Transmission probability.
* population = Total population within all containers.
* progression_period = Average number of days until a patient seeks treatment.
* progression_sd = Standard deviation of progression_period.
* interactions = Average number of interactions per person per day (decreases with social distancing).
* reinfection_rate = Probability of becoming susceptible again after recovery.
* I0 = Initial probability of being infected.
* death_rate = Probability of dying after being infected after progression_period and before recovery_days.
* recovery_days = Average number of days until recovery.
* recovery_sd = Standard deviation of recovery_days.
* severe = Probability of developing severe, symptomatic disease.
* steps = number of days in simulation.<br /><br />
* chaos (in model_functions.py 'build_network' function) = Adjusting this parameter allows for social distancing compliance uncertainty.

## Instructions for Use
* Update parameters in the 'model_params.py' file.<br />
* Execute the 'run.py' script.<br />
`python run.py -o <output_path>`
