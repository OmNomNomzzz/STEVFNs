#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:49:50 2023

@author: mnsgsty
"""

import pandas as pd


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
            
            
        elif name == 'RE_PV_Rooftop_Lim' or name == 'RE_PV_Openfield_Lim' or name == 'RE_WIND_Onshore_Lim' or name == 'RE_WIND_Offshore_Lim':
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