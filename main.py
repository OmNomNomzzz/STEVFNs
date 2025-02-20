#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:38:43 2021

@author: aniqahsan
"""

import pandas as pd
import time
import os
from os.path import normpath, basename
import cvxpy as cp


from Code.Network.Network import Network_STEVFNs
from Code.Plotting import DPhil_Plotting
from Code.Results import GMPA_Results


#### Define Input Files ####
# case_study_name = "BAU_No_Action"
# case_study_name = "Autarky_CL"
# case_study_name = "KH-BN_Autarky"
# case_study_name = "KH-BN_Collab"
# case_study_name = "VN-MY-LA_Autarky"
case_study_name = "VN-MY-LA_Collab"
# case_study_name = "SG-KH-VN-ID_Autarky"
# case_study_name = "SG-KH-VN-ID_Collab"

base_folder = os.path.dirname(__file__)
data_folder = os.path.join(base_folder, "Data")
case_study_folder = os.path.join(data_folder, "Case_Study", case_study_name)
scenario_folders_list = [x[0] for x in os.walk(case_study_folder)][1:]
network_structure_filename = os.path.join(case_study_folder, "Network_Structure.csv")
results_filename = os.path.join(case_study_folder, "total_data.csv")
unrounded_results_filename = os.path.join(case_study_folder, "total_data_unrounded.csv")
capacities_filename = os.path.join(case_study_folder, "capacities_total_data.csv")


### Read Input Files ###

network_structure_df = pd.read_csv(network_structure_filename)



### Build Network ###
start_time0 = time.time()


my_network = Network_STEVFNs()
my_network.build(network_structure_df)


end_time = time.time()
print("Time taken to build network = ", end_time - start_time0, "s")
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
    # my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=100000000, verbose=True,
                              # ignore_dpp=True,# Uncomment to disable DPP. DPP will make the first scenario run slower, but subsequent scenarios will run significantly faster.
                              # )
    my_network.problem.solve(solver = cp.CLARABEL, max_iter=10000)
    # my_network.problem.solve(solver = cp.SCS, warm_start=True, max_iters=100000, ignore_dpp=True, verbose=False)
    # my_network.problem.solve(solver = cp.MOSEK)
    end_time = time.time()

    
    ### Plot Results ############
    print("Scenario: ", my_network.scenario_name)
    print("Time taken to solve problem = ", end_time - start_time, "s")
    print(my_network.problem.solution.status)
    if my_network.problem.value == float("inf"):
        continue
    # print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
    # print("Total emissions = ", my_network.assets[0].asset_size(), "MtCO2e")
    # DPhil_Plotting.plot_all(my_network)
    # DPhil_Plotting.plot_asset_sizes(my_network)
    # DPhil_Plotting.plot_asset_costs(my_network)

    
    ### Export cost results to pandas dataframe per scenario and concat all scenarios
    t_df = GMPA_Results.export_total_data(my_network, location_parameters_df, asset_parameters_df)
    t1_df = GMPA_Results.export_total_data_not_rounded(my_network, location_parameters_df, asset_parameters_df)
    capacities_df = GMPA_Results.export_total_data_capacities(my_network, location_parameters_df, asset_parameters_df)
    if counter1 == 0:
        total_df = t_df
        total_df_1 = t1_df
        total_cap_df = capacities_df
    else:
        total_df = pd.concat([total_df, t_df], ignore_index=True)
        total_df_1 = pd.concat([total_df_1, t1_df], ignore_index=True)
        total_cap_df = pd.concat([total_cap_df, capacities_df], ignore_index=True)
        
# #### Save Result
total_df.to_csv(results_filename, index=False, header=True)
total_df_1.to_csv(unrounded_results_filename, index=False, header=True)
total_cap_df.to_csv(capacities_filename, index=False, header=True)
    
        
final_time = time.time()
print("Time to build network, run all scenarios, and export data", (final_time - start_time0)/60, "min")
   