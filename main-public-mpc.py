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
from Code.Results import GMPA_Results

#### Define Input Files ####
case_study_name = "Autarky_IN_TRIAL_MPC"

### Define Input Data Paths ###
base_folder = os.path.dirname(__name__) #prev: __file__
data_folder = os.path.join(base_folder, "Data")
case_study_folder = os.path.join(data_folder, "Case_Study", case_study_name)
scenario_folders_list = [x[0] for x in os.walk(case_study_folder)][1:]
network_structure_filename = os.path.join(case_study_folder, "Network_Structure.csv")
results_filename = os.path.join(case_study_folder, "total_data.csv")
unrounded_results_filename = os.path.join(case_study_folder, "total_data_unrounded.csv")


### Read Input Files ###
network_structure_df = pd.read_csv(network_structure_filename)
prediction_horizon = int(network_structure_df['End_Time'].max())
prediction_horizon
control_horizon = prediction_horizon


### Build Network ###
start_time = time.time()
my_network = Network_STEVFNs()
my_network.build(network_structure_df)
end_time = time.time()
print("Time taken to build network = ", end_time - start_time, "s")

### Initialize results DataFrame ###
total_df = pd.DataFrame()
total_df_1 = pd.DataFrame() 
results_df = pd.DataFrame() #  NEWLY ADDED - for intermediate results every prediction horizon


### Loop through scenarios ###
for counter1 in range(len(scenario_folders_list)):
    ### Read Input Files ###
    scenario_folder = scenario_folders_list[-1-counter1]
    asset_parameters_filename = os.path.join(scenario_folder, "Asset_Parameters.csv")
    location_parameters_filename = os.path.join(scenario_folder, "Location_Parameters.csv")
    system_parameters_filename = os.path.join(scenario_folder, "System_Parameters.csv")
    
    asset_parameters_df = pd.read_csv(asset_parameters_filename)
    location_parameters_df = pd.read_csv(location_parameters_filename)
    system_parameters_df = pd.read_csv(system_parameters_filename)
    
    
    my_network.scenario_name = os.path.basename(scenario_folder)
    project_life = int(system_parameters_df[system_parameters_df['parameter']=='project_life']['value'].values[0])
    print("===================== Scenario: ", my_network.scenario_name, "=====================") 
    print("Project Life:", project_life, "| Prediction Horizon:", prediction_horizon, "| Control Horizon:", control_horizon)
    print()
    
    for t in range(0, project_life, control_horizon):
        
        ### define optimization horizon ###
        end_t = min(t + int(prediction_horizon), project_life) 
        print("Start time:", t, "End time:", end_t)
        
        ### Update network parameters ###
        start_time = time.time()
        my_network.update(location_parameters_df, asset_parameters_df, system_parameters_df)    
        end_time = time.time()
        print("Time taken to update network = ", end_time - start_time, "s")
        
        
        ### Run Simulation ###
        start_time = time.time()
        # my_network.solve_problem()
        my_network.problem.solve(solver = cp.CLARABEL, warm_start=True, verbose=False,
                                ignore_dpp=True,# Uncomment to disable DPP. DPP will make the first scenario run slower, but subsequent scenarios will run significantly faster.
                                )
        # my_network.problem.solve(solver = cp.CLARABEL, warm_start=True, max_iters=10000, verbose=False,
        #                         ignore_dpp=True,# Uncomment to disable DPP. DPP will make the first scenario run slower, but subsequent scenarios will run significantly faster.
        #                         )
        # my_network.problem.solve(solver = cp.ECOS, warm_start=True, max_iters=10000, feastol=1e-5, reltol=1e-5, abstol=1e-5, ignore_dpp=True, verbose=False)
        # my_network.problem.solve(solver = cp.SCS, warm_start=True, max_iters=10000, ignore_dpp=True, verbose=False)
        end_time = time.time()
        print("Time taken to solve problem = ", end_time - start_time, "s")
        
        
        ### Plot Results ###
        print("problem solution status:", my_network.problem.solution.status)
        if my_network.problem.value == float("inf"):
            continue
        
        print("---------- Objective Values ----------")
        print("Total cost to satisfy all demand = ", my_network.problem.value, " Billion USD")
        co2_budget_index = [i for i in range(len(my_network.assets)) if my_network.assets[i].asset_name == 'CO2_Budget'][0]
        print("Total emissions = ", my_network.assets[co2_budget_index].asset_size(), "MtCO2e")
        
        print("---------- Assets Summary ----------")
        rows = []
        for asset in my_network.assets:
            print("-----", asset.asset_name, "-----")
            print("Size:", asset.asset_size(), "Cost:", asset.cost.value)
            rows.append({
                    "Scenario": my_network.scenario_name,
                    "Start Time": t,
                    "End Time": end_t,
                    "Asset Name": asset.asset_name,
                    "Asset Size": asset.asset_size(),
                    "Asset Cost": asset.cost.value
                })
            
            try:
                for sub_asset_name, sub_asset in asset.assets_dictionary.items():
                    print("=", sub_asset_name, "=")
                    print("Size:", sub_asset.asset_size(), "Cost:",sub_asset.cost.value )
                    print("No. of flow:", len(sub_asset.get_plot_data()), "Data Type of flow:", type(sub_asset.get_plot_data()))
                    rows.append({
                        "Scenario": my_network.scenario_name,
                        "Start Time": t,
                        "End Time": end_t,
                        "Asset Name": asset.asset_name + '-' + sub_asset_name,
                        "Asset Size": sub_asset.asset_size(),
                        "Asset Cost": sub_asset.cost.value
                    })
                    
            except:
                continue
        df = pd.DataFrame(rows)
        results_df = pd.concat([results_df, df], ignore_index = True)
            
    
        print()
        
        ##############################################################
        ###### TODO: Update asset parameters for the next window #####
        ##############################################################
        
        # Create new assets for the updated existing capacity
        # Update asset_parameters_df for the next loop
        
    print("="*100)
results_df
        
        
        
    
    





