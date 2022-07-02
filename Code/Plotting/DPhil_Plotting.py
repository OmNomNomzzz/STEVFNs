# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 17:41:01 2022

@author: aniq_
"""

# from __init__.py import *
import numpy as np
from ..Plotting import *




def plot_asset_sizes(my_network, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the size of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_sizes_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_sizes_array)):
        asset_sizes_array[counter1] = my_network.assets[counter1].asset_size()
    og_df["Asset_Size"] = asset_sizes_array
    max_asset_size = np.max(asset_sizes_array)
    # Set minimum asset size to plot
    min_asset_size = max_asset_size * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Size"] >= min_asset_size
    og_df = og_df[con1]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_size = my_network.assets[asset_number].asset_size()
            # check if asset is too small
            if asset_size < min_asset_size:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_size = my_network.assets[asset_number].asset_size()
                # check if asset is too small
                if asset_size < min_asset_size:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Size (GWh)"
    my_artist.title = "Size of Assets in the System by Location and Location Pair"
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return

def plot_asset_costs(my_network, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the cost of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_costs_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_costs_array)):
        asset_costs_array[counter1] = my_network.assets[counter1].cost.value
    og_df["Asset_Cost"] = asset_costs_array
    max_asset_cost = np.max(asset_costs_array)
    # Set minimum asset size to plot
    min_asset_cost = max_asset_cost * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Cost"] >= min_asset_cost
    og_df = og_df[con1]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_cost = my_network.assets[asset_number].cost.value
            # check if asset is too small
            if asset_cost < min_asset_cost:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_cost = my_network.assets[asset_number].cost.value
                # check if asset is too small
                if asset_cost < min_asset_cost:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Cost (Billion USD)"
    my_artist.title = "Cost of Assets in the System by Location and Location Pair"
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return




