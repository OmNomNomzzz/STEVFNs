#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:49:50 2023

@author: mnsgsty
"""

import pandas as pd
import numpy as np


def export_results(my_network):
    '''Class to export all results, generalized for all case studies'''
    
    sizes_df = pd.DataFrame()
    costs_df = pd.DataFrame()
    number_assets = len(my_network.assets)
    
    
    for asset in range(1, number_assets):

        name = my_network.assets[asset].asset_name
        
        ### Exceptions in formatting or extracting results per type of asset ###
        if name == 'BESS' or name == 'NH3_Storage':
            loc1 = my_network.assets[asset].asset_structure["Location_1"]
            costs_df.insert(0, f'{name}_{loc1}_G$', [my_network.assets[asset].cost.value])
            sizes_df.insert(0, f'{name}_{loc1}_GWh', [my_network.assets[asset].asset_size()])
            
            
        elif name == 'RE_PV_Rooftop_Lim' or name == 'RE_PV_Openfield_Lim' or name == 'RE_WIND_Onshore_Lim' or name == 'RE_WIND_Offshore_Lim' or name == 'RE_WIND_Onshore_BAU' or name == 'RE_PV_Openfield_BAU':
            loc1 = my_network.assets[asset].target_node_location
            costs_df.insert(0, f'{name}_{loc1}_G$', [my_network.assets[asset].cost.value])
            sizes_df.insert(0, f'{name}_{loc1}_GW', [my_network.assets[asset].asset_size()])

        elif name == 'EL_Demand' or name == 'HTH_Demand':
            loc1 = my_network.assets[asset].node_location
            costs_df.insert(0, f'{name}_{loc1}_G$', [my_network.assets[asset].cost.value])
            sizes_df.insert(0, f'{name}_{loc1}_GWh', [my_network.assets[asset].asset_size()])
            
        elif name == 'EL_Transport' or name == 'NH3_Transport':
            loc1 = my_network.assets[asset].asset_structure["Location_1"]
            loc2 = my_network.assets[asset].asset_structure["Location_2"]
            costs_df.insert(0, f'{name}_{loc1}-{loc2}_G$', [my_network.assets[asset].cost.value])
            sizes_df.insert(0, f'{name}_{loc1}-{loc2}_GW', [my_network.assets[asset].asset_size()])
        
        
        
        ### The rest of the assets, in general ###
        else:
            loc1 = my_network.assets[asset].asset_structure["Location_1"]
            costs_df.insert(0, f'{name}_{loc1}_G$', [my_network.assets[asset].cost.value])
            sizes_df.insert(0, f'{name}_{loc1}_GW', [my_network.assets[asset].asset_size()])
                
    
    
    costs_df.insert(0, 'Total_System_Cost', [my_network.problem.value])
    sizes_df.insert(0, 'CO2_Budget_GgCO2',  [my_network.assets[0].asset_size()])    
    

    ## hardcoded for better format output 
    index = list(range(number_assets))
               
    costs_df = costs_df.T
    costs_df['Number'] = index
    costs_df['Asset Name'] = costs_df.index
    costs_df = costs_df.set_index(costs_df['Number'])
    costs_df = costs_df.drop('Number', axis=1)
    costs_df = costs_df.rename(columns={0: "Costs"})
    
    
    sizes_df = sizes_df.T
    sizes_df['Number'] = index
    sizes_df['Asset Name'] = sizes_df.index
    sizes_df = sizes_df.set_index(sizes_df['Number'])
    sizes_df = sizes_df.drop('Number', axis=1)
    sizes_df = sizes_df.rename(columns={0: "Sizes"})
    
    costs_df = pd.concat([costs_df, sizes_df], axis=1)
    
    return(costs_df)

def export_total_data(my_network, location_parameters_df, asset_parameters_df):
    ''' Function to export results, generalized for all case studies'''
    
    location_names = list(location_parameters_df["location_name"])
    loc_names_set_list = list(set(asset_parameters_df["Location_1"]).union(set(asset_parameters_df["Location_2"])))
    loc_names_list = ["",]*4
    for counter1 in range(len(loc_names_set_list)):
        loc_names_list[counter1] = location_names[loc_names_set_list[counter1]]
    
    total_data_columns = ["country_1",
                  "country_2",
                  "country_3",
                  "country_4",
                  "collaboration_emissions",
                  "technology_cost",
                  "technology_name",]
    total_data_df = pd.DataFrame(columns = total_data_columns)
    
    collaboration_emissions =  my_network.assets[0].asset_size()
    loc_names_set = set()
    
    for counter1 in range(1,len(my_network.assets)):
        asset = my_network.assets[counter1]
        name = asset.asset_name
        
        ### Exceptions in formatting or extracting results per type of asset ###
        if name == 'BESS' or name == 'NH3_Storage':
            loc1 = asset.asset_structure["Location_1"]
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
            
        elif name == 'RE_PV_Rooftop_Lim' or name == 'RE_PV_Openfield_Lim' or name == 'RE_WIND_Onshore_Lim' or name == 'RE_WIND_Offshore_Lim' or name == 'RE_WIND_Onshore_BAU' or name == 'RE_PV_Openfield_BAU':
            loc1 = asset.target_node_location
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost =  asset.cost.value

        elif name == 'EL_Demand' or name == 'HTH_Demand':
            loc1 = asset.node_location
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
            
        elif name == 'EL_Transport' or name == 'NH3_Transport':
            loc1 = asset.asset_structure["Location_1"]
            loc2 = asset.asset_structure["Location_2"]
            loc_name_1 = location_names[loc1]
            loc_name_2 = location_names[loc2]
            loc_names_set.add(loc_name_1)
            loc_names_set.add(loc_name_1)
            technology_name = name + r"_[" + loc_name_1 + r"-" + loc_name_2 + r"]"
            technology_cost = asset.cost.value
        
        
        
        ### The rest of the assets, in general ###
        else:
            loc1 = asset.asset_structure["Location_1"]
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
        
        N = np.ceil(my_network.system_parameters_df.loc["project_life", "value"]/8760) #number of years for the project
        t_df = pd.DataFrame({"country_1": [loc_names_list[0]],
                             "country_2": [loc_names_list[1]],
                             "country_3": [loc_names_list[2]],
                             "country_4": [loc_names_list[3]],
                             "collaboration_emissions": [round(collaboration_emissions/N, 1)],# Number is annualized, number is converted from ktCO2e to MtCO2e
                             "technology_cost": [round(technology_cost/N, 1)],# Number is annualized
                             "technology_name": [technology_name],
            })
        total_data_df = pd.concat([total_data_df, t_df], ignore_index=True)
    return total_data_df


def export_total_data_not_rounded(my_network, location_parameters_df, asset_parameters_df):
    ''' Function to export results, generalized for all case studies'''
    
    location_names = list(location_parameters_df["location_name"])
    loc_names_set_list = list(set(asset_parameters_df["Location_1"]).union(set(asset_parameters_df["Location_2"])))
    loc_names_list = ["",]*4
    for counter1 in range(len(loc_names_set_list)):
        loc_names_list[counter1] = location_names[loc_names_set_list[counter1]]
    
    total_data_columns = ["country_1",
                  "country_2",
                  "country_3",
                  "country_4",
                  "collaboration_emissions",
                  "technology_cost",
                  "technology_name",]
    total_data_df = pd.DataFrame(columns = total_data_columns)
    
    collaboration_emissions =  my_network.assets[0].asset_size()
    loc_names_set = set()
    
    for counter1 in range(1,len(my_network.assets)):
        asset = my_network.assets[counter1]
        name = asset.asset_name
        
        ### Exceptions in formatting or extracting results per type of asset ###
        if name == 'BESS' or name == 'NH3_Storage':
            loc1 = asset.asset_structure["Location_1"]
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
            
        elif name == 'RE_PV_Rooftop_Lim' or name == 'RE_PV_Openfield_Lim' or name == 'RE_WIND_Onshore_Lim' or name == 'RE_WIND_Offshore_Lim' or name == 'RE_WIND_Onshore_BAU' or name == 'RE_PV_Openfield_BAU':
            loc1 = asset.target_node_location
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost =  asset.cost.value

        elif name == 'EL_Demand' or name == 'HTH_Demand':
            loc1 = asset.node_location
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
            
        elif name == 'EL_Transport' or name == 'NH3_Transport':
            loc1 = asset.asset_structure["Location_1"]
            loc2 = asset.asset_structure["Location_2"]
            loc_name_1 = location_names[loc1]
            loc_name_2 = location_names[loc2]
            loc_names_set.add(loc_name_1)
            loc_names_set.add(loc_name_1)
            technology_name = name + r"_[" + loc_name_1 + r"-" + loc_name_2 + r"]"
            technology_cost = asset.cost.value
        
        
        
        ### The rest of the assets, in general ###
        else:
            loc1 = asset.asset_structure["Location_1"]
            loc_name = location_names[loc1]
            loc_names_set.add(loc_name)
            technology_name = name + r"_[" + loc_name + r"]"
            technology_cost = asset.cost.value
        
        N = np.ceil(my_network.system_parameters_df.loc["project_life", "value"]/8760) #number of years for the project
        t_df = pd.DataFrame({"country_1": [loc_names_list[0]],
                             "country_2": [loc_names_list[1]],
                             "country_3": [loc_names_list[2]],
                             "country_4": [loc_names_list[3]],
                             "collaboration_emissions": [collaboration_emissions/N],# Number is annualized, number is converted from ktCO2e to MtCO2e
                             "technology_cost": [technology_cost/N],# Number is annualized
                             "technology_name": [technology_name],
            })
        total_data_df = pd.concat([total_data_df, t_df], ignore_index=True)
    return total_data_df

