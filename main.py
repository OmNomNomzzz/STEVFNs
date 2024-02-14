#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:38:43 2021

@author: aniqahsan
"""

import pandas as pd
import time
import os
import cvxpy as cp


from Code.Network.Network import Network_STEVFNs
from Code.Plotting import DPhil_Plotting


#### Define Input Files ####
case_study_name = "SG_Case_Study"


base_folder = os.path.dirname(__file__)
data_folder = os.path.join(base_folder, "Data")
case_study_folder = os.path.join(data_folder, "Case_Study", case_study_name)
scenario_folders_list = [x[0] for x in os.walk(case_study_folder)][1:]
network_structure_filename = os.path.join(case_study_folder, "Network_Structure.csv")

### Read Input Files ###

network_structure_df = pd.read_csv(network_structure_filename)



### Build Network ###
start_time = time.time()


my_network = Network_STEVFNs()
my_network.build(network_structure_df)


end_time = time.time()
print("Time taken to build network = ", end_time - start_time, "s")
total_df = pd.DataFrame()
total_df_1 = pd.DataFrame()



for counter1 in range(len(scenario_folders_list)):
# for counter1 in range(1):
    # Read Input Files ###
    scenario_folder = scenario_folders_list[-1-counter1]
    asset_parameters_filename = os.path.join(scenario_folder, "Asset_Parameters.csv")
    location_parameters_filename = os.path.join(scenario_folder, "Location_Parameters.csv")
    system_parameters_filename = os.path.join(scenario_folder, "System_Parameters.csv")
    
    asset_parameters_df = pd.read_csv(asset_parameters_filename)
    location_parameters_df = pd.read_csv(location_parameters_filename)
    system_parameters_df = pd.read_csv(system_parameters_filename)
    
    
    ### Update Network Parameters ###
    start_time = time.time()
    
    
    my_network.update(location_parameters_df, asset_parameters_df, system_parameters_df)
    my_network.scenario_name = os.path.basename(scenario_folder)
    
    
    end_time = time.time()
    print("Time taken to update network = ", end_time - start_time, "s")
    
    ### Run Simulation ###
    start_time = time.time()
    
    
    # my_network.solve_problem()
    my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=10000, verbose=False,
                              ignore_dpp=True,# Uncomment to disable DPP. DPP will make the first scenario run slower, but subsequent scenarios will run significantly faster.
                             )
    end_time = time.time()

    
    ### Plot Results ############
    print("Scenario: ", my_network.scenario_name)
    print("Time taken to solve problem = ", end_time - start_time, "s")
    print(my_network.problem.solution.status)
    if my_network.problem.value == float("inf"):
        continue
    print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
    # DPhil_Plotting.plot_all(my_network) # Uncomment to plot all flows. Only works for SG_Case_Study at the moment. Will not work if network structure is changed.
    DPhil_Plotting.plot_asset_sizes(my_network)
    DPhil_Plotting.plot_asset_costs(my_network)
    


   