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
# case_study_name = "Autarky_Case_Study"
# case_study_name = "Xlinks_Case_Study" 
case_study_name = "Xlinks_EXT_Case_Study"


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


for counter1 in range(len(scenario_folders_list)):
# for counter1 in range(1):
    ### Read Input Files ###
    scenario_folder = scenario_folders_list[counter1]
    asset_parameters_filename = os.path.join(scenario_folder, "Asset_Parameters.csv")
    location_parameters_filename = os.path.join(scenario_folder, "Location_Parameters.csv")
    system_parameters_filename = os.path.join(scenario_folder, "System_Parameters.csv")
    
    asset_parameters_df = pd.read_csv(asset_parameters_filename)
    location_parameters_df = pd.read_csv(location_parameters_filename)
    system_parameters_df = pd.read_csv(system_parameters_filename)
    
    
    ### Update Network Parameters ###
    start_time = time.time()
    
    
    my_network.update(location_parameters_df, asset_parameters_df, system_parameters_df)
    
    
    end_time = time.time()
    print(case_study_name)
    print("Time taken to update network = ", end_time - start_time, "s")
    
    ### Run Simulation ###
    start_time = time.time()
    
    
    # my_network.solve_problem()
    my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=10000, ignore_dpp=True)
    
    end_time = time.time()
    
    ### Plot Results ############
    print("Time taken to solve problem = ", end_time - start_time, "s")
    print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD, in scenario:", scenario_folders_list[counter1])
    # DPhil_Plotting.plot_all(my_network)
    DPhil_Plotting.plot_asset_sizes(my_network)
    DPhil_Plotting.plot_asset_costs(my_network)
    # DPhil_Plotting.plot_AUT_EL_input_flows(my_network)
    # DPhil_Plotting.plot_AUT_EL_output_flows(my_network)
    DPhil_Plotting.plot_XlinkEXT_EL_input_flows(my_network)
    DPhil_Plotting.plot_XlinkEXT_EL_output_flows(my_network)
    
    
    # DPhil_Plotting.plot_single_RE_EL_output_flows(my_network, 0)
    
    

    for counter2 in range(len(my_network.assets)):
        print(my_network.assets[counter2], 'size:', my_network.assets[counter2].asset_size())
        print(my_network.assets[counter2], 'cost:', my_network.assets[counter2].cost.value)

