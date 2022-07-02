#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 17:38:43 2021

@author: aniqahsan
"""

import pandas as pd
import time
import os


from Code.Network.Network import Network_STEVFNs



#### Define Input Files ####
base_folder = os.path.dirname(__file__)
data_folder = os.path.join(base_folder, "Data")

scenario_folder = os.path.join(data_folder, "Scenario", "SG_Case_Study")
network_structure_filename = os.path.join(scenario_folder, "Network_Structure_test.csv")
asset_parameters_filename = os.path.join(scenario_folder, r"Asset_Parameters", r"Parameters_1.csv")
location_parameters_filename = os.path.join( scenario_folder, r"Location_Parameters", r"Parameters_1.csv")
asset_parameters_filename_2 = os.path.join( scenario_folder, r"Asset_Parameters", r"Parameters_2.csv")
location_parameters_filename_2 = os.path.join( scenario_folder, r"Location_Parameters", r"Parameters_2.csv")




### Read Input Files ###

network_structure_df = pd.read_csv(asset_parameters_filename)
asset_parameters_df = pd.read_csv(asset_parameters_filename)
location_parameters_df = pd.read_csv(location_parameters_filename)
asset_parameters_2_df = pd.read_csv(asset_parameters_filename_2)
location_parameters_2_df = pd.read_csv(location_parameters_filename_2)


### Import Dictionary of Assets ###



### Build Network ###
start_time = time.time()


my_network = Network_STEVFNs()
my_network.build(network_structure_df)


end_time = time.time()
print("Time taken to build network = ", end_time - start_time, "s")

### Update Network Parameters ###
start_time = time.time()


my_network.update(location_parameters_df, asset_parameters_df)


end_time = time.time()
print("Time taken to update network = ", end_time - start_time, "s")

### Run Simulation ###
start_time = time.time()


my_network.solve_problem()


end_time = time.time()

### Plot Results ############
print("Time taken to solve problem = ", end_time - start_time, "s")
print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
# my_network.print_asset_sizes()
my_network.plot_asset_sizes()
my_network.plot_asset_costs()
my_network.plot_SG_EL_output_flows()
my_network.plot_SG_EL_input_flows()
my_network.plot_RE_EL_output_flows()
my_network.plot_RE_EL_input_flows()


### Update Network Parameters ###
start_time = time.time()


my_network.update(location_parameters_2_df, asset_parameters_2_df)


end_time = time.time()
print("Time taken to reupdate network = ", end_time - start_time, "s")
### Rerun Simulation ###
start_time = time.time()


my_network.solve_problem()


end_time = time.time()

### Plot Results ############
print("Time taken to resolve problem = ", end_time - start_time, "s")
print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
# my_network.print_asset_sizes()
my_network.plot_asset_sizes()
my_network.plot_asset_costs()
my_network.plot_SG_EL_output_flows()
my_network.plot_SG_EL_input_flows()
my_network.plot_RE_EL_output_flows()
my_network.plot_RE_EL_input_flows()


