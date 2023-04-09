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
import numpy as np


from Code.Network.Network import Network_STEVFNs
from Code.Plotting import DPhil_Plotting



#### Define Input Files ####
case_study_name = "BESS_Arbitrage_Case_Study"


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
    my_network.scenario_name = os.path.basename(scenario_folder)
    
    
    end_time = time.time()
    print("Time taken to update network = ", end_time - start_time, "s")
    
    ### Run Simulation ###
    start_time = time.time()
    
    
    # my_network.solve_problem()
    my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=1000, ignore_dpp=False)
    
    end_time = time.time()
    
    ### Plot Results ############
    print("Time taken to solve problem = ", end_time - start_time, "s")
    print("Total cost to satisfy all demand = ", my_network.problem.value, " Million USD")
    # DPhil_Plotting.plot_all(my_network)
    DPhil_Plotting.plot_asset_sizes(my_network)
    DPhil_Plotting.plot_asset_costs(my_network)
    
# ##### Plot flows for BAU scenario ######
# DPhil_Plotting.plot_SG_EL_input_flows_BAU(my_network)
# DPhil_Plotting.plot_SG_EL_output_flows_BAU(my_network)
# DPhil_Plotting.plot_RE_EL_input_flows_BAU(my_network)
# DPhil_Plotting.plot_RE_EL_output_flows_BAU(my_network)

# DPhil_Plotting.plot_SG_NH3_input_flows_BAU(my_network)
# DPhil_Plotting.plot_SG_NH3_output_flows_BAU(my_network)
# DPhil_Plotting.plot_RE_NH3_input_flows_BAU(my_network)
# DPhil_Plotting.plot_RE_NH3_output_flows_BAU(my_network)

######### Perform Model Predictive Control ###########
#Total number of half hours to simulate
N_times = 1096*48

final_BESS_charging = np.zeros(N_times)
final_BESS_discharging = np.zeros(N_times)
market_half_hourly_imports = np.zeros(N_times)
market_half_hourly_exports = np.zeros(N_times)
market_daily_imports = np.zeros(N_times)
market_daily_exports = np.zeros(N_times)

initial_storage = 0.0

BESS_asset =  my_network.assets[0]
market_half_hourly_asset = my_network.assets[1]
market_daily_asset = my_network.assets[2]

for counter1 in range(1095):
    
    ### Update Network Parameters ###
    start_time = time.time()
    
    day_number = counter1
    half_hour_number = counter1*48
    #Update BESS#
    BESS_asset.parameters_df["initial_storage"] = initial_storage
    BESS_asset._update_assets()
    
    #Update half hourly market#
    market_half_hourly_asset.parameters_df["initial_timestep"] = half_hour_number
    market_half_hourly_asset._update_assets()
    
    #Update daily market#
    market_daily_asset.parameters_df["initial_timestep"] = day_number
    market_daily_asset._update_assets()
    
    end_time = time.time()
    # print("Time taken to update network = ", end_time - start_time, "s")
    
    ### Run Simulation ###
    start_time = time.time()
    
    
    # my_network.solve_problem()
    my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=1000, ignore_dpp=False)
    
    end_time = time.time()
    # print("Time taken to solve problem = ", end_time - start_time, "s")
    
    #Store Results
    final_BESS_charging[half_hour_number: half_hour_number+48] = BESS_asset.assets_dictionary["Charging"].flows.value[:48]
    final_BESS_discharging[half_hour_number: half_hour_number+48] = BESS_asset.assets_dictionary["Discharging"].flows.value[:48]
    market_half_hourly_imports[half_hour_number: half_hour_number+48] = market_half_hourly_asset.assets_dictionary["Import"].flows.value[:48]
    market_half_hourly_exports[half_hour_number: half_hour_number+48] = market_half_hourly_asset.assets_dictionary["Export"].flows.value[:48]
    market_daily_imports[half_hour_number: half_hour_number+48] = market_daily_asset.assets_dictionary["Import"].flows.value[0]
    market_daily_exports[half_hour_number: half_hour_number+48] = market_daily_asset.assets_dictionary["Export"].flows.value[0]
    
    #Update soc
    initial_storage = BESS_asset.assets_dictionary["Storage"].flows[47].value
    


