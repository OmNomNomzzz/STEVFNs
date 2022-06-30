#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 10:19:15 2021

@author: aniqahsan
"""

### Import Packages ###

import os
import pandas as pd
import cvxpy as cp
import numpy as np
from . import Node_STEVFNs
from ..Assets.Assets_Dictionary import ASSET_DICT
from ..Plotting import bar_chart_artist

class Network_STEVFNs:
    """This is the NETWORK class of STEVFNs"""
    def __init__(self):
        self.lat_lon_df = pd.DataFrame(columns = ["lat", "lon"])
        self.assets = []
        self.costs = []
        self.constraints = []
        self.nodes_df = pd.Series([], index = pd.MultiIndex.from_tuples([], names = ["location", "type", "time"]))
        self.base_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return
    
    def set_usage_factor(self, discount_rate, timesteps):
        discount_factor = 1 / (1+discount_rate)
        NPV_factor = (1-discount_factor**30)/(1-discount_factor)#Assume the asset will be used for 30 years
        yearly_factor = 365.0*24 / timesteps
        self.usage_factor = NPV_factor * yearly_factor
        return
    
    def generate_node(self, node_location, node_type, node_time):
        new_node = Node_STEVFNs()
        node_df = pd.Series([new_node], 
                            index = pd.MultiIndex.from_tuples([(node_location, node_type, node_time)], 
                                    names = ["location", "type", "time"]))
        self.nodes_df = self.nodes_df.append(node_df)
        return
    
    def extract_node(self, node_location, node_type, node_time):
        if not((node_location, node_type, node_time) in self.nodes_df.index):
            self.generate_node(node_location, node_type, node_time)
        return self.nodes_df[node_location, node_type, node_time]
    
    def add_asset(self, asset):
        asset.network = self
        self.assets += [asset]
        return
    
    def build_assets(self):
        self.costs = []
        for counter1 in range(len(self.assets)):
            self.assets[counter1].build()
            self.costs += [self.assets[counter1].cost]
    
    def build_constraints(self):
        self.constraints = []
        for counter1 in range(self.nodes_df.size):
            node = self.nodes_df.iloc[counter1]
            node.build_constraints()
            self.constraints += node.constraints
        return
    
    def build_cost(self):
        self.cost = cp.sum(self.costs)
        return
    
    def build_problem(self):
        self.build_assets()
        self.build_cost()
        self.build_constraints()
        self.objective = cp.Minimize(self.cost)
        self.problem = cp.Problem(self.objective, self.constraints)
        return
    
    def solve_problem(self):
        # self.problem.solve()
        # self.problem.solve(warm_start=True)# This can sometimes use OSQP solver that sometimes gives errors.
        self.problem.solve(solver = cp.ECOS, warm_start=True)
        # self.problem.solve(solver = cp.OSQP, warm_start=True)
        # self.problem.solve(solver = cp.CVXOPT, warm_start=True)
        # self.problem.solve(solver = cp.SCS, warm_start=True)
        return
    
    def satisfy_net_loads(self):
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            if type(asset).__name__ == "Conventional_Generator":
                asset.satisfy_net_load()
        return
    
    def generate_asset(self, asset_structure):
        asset_class_name = asset_structure["Asset_Class"]
        my_asset = ASSET_DICT[asset_class_name]()
        self.add_asset(my_asset)
        my_asset.define_structure(asset_structure)
        return
    
    def build(self, network_structure_df):
        #Set System Structure#
        self.system_structure_df = network_structure_df[["Asset_Number", "Asset_Class", "Location_1", "Location_2"]]
        #Generate Assets#
        for counter1 in range(len(network_structure_df)):
            self.generate_asset(network_structure_df.iloc[counter1])
        self.set_usage_factor(discount_rate = 0.05, timesteps = network_structure_df["End_Time"].max())
        #Build Problem#
        self.build_problem()
        return
    
    def update(self, location_parameters_df, asset_parameters_df):
        #Update Location lat,lon#
        for counter1 in range(len(location_parameters_df)):
            location = location_parameters_df.iloc[counter1]["Location"]
            self.lat_lon_df.loc[location, "lat"] = location_parameters_df.iloc[counter1]["lat"]
            self.lat_lon_df.loc[location, "lon"] = location_parameters_df.iloc[counter1]["lon"]
        #update Assets#
        for counter1 in range(len(asset_parameters_df)):
            asset_number = asset_parameters_df.iloc[counter1]["Asset_Number"]
            asset_type = asset_parameters_df.iloc[counter1]["Asset_Type"]
            self.assets[asset_number].update(asset_type)
        return
    
    def print_asset_sizes(self):
        #Plot some stuff#
        print("")
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            print("Size of ", asset.asset_name, ":")
            print(asset.size())
        print("")
        return
    
    def get_asset_sizes(self):
        # Returns dictionary of asset sizes #
        asset_sizes_dict = dict()
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            asset_sizes_dict.update(asset.get_asset_sizes())
        return asset_sizes_dict
    
    def plot_asset_usage(self):
        # Plot the flows in each asset #
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            asset.plot_asset_usage()
        return
    
    def get_asset_number_by_locations(self, loc_1, loc_2):
        # Returns list of Asset_Number of assets at the specific loc_1 and loc_2 #
        con_1 = self.system_structure_df["Location_1"] == loc_1
        con_2 = self.system_structure_df["Location_2"] == loc_2
        t_con = con_1 & con_2
        return list(self.system_structure_df[t_con]["Asset_Number"])
    
    def plot_asset_sizes(self, bar_width = 1.0, bar_spacing = 3.0):
        # Plots the size of assets in the system #
        
        # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
        og_df = self.system_structure_df.copy()
        asset_sizes_array = np.zeros(og_df.shape[0])
        for counter1 in range(len(asset_sizes_array)):
            asset_sizes_array[counter1] = self.assets[counter1].asset_size()
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
                asset_size = self.assets[asset_number].asset_size()
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
                    asset_size = self.assets[asset_number].asset_size()
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
        my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
        return
    
    def plot_asset_costs(self, bar_width = 1.0, bar_spacing = 3.0):
        # Plots the cost of assets in the system #
        
        # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
        og_df = self.system_structure_df.copy()
        asset_costs_array = np.zeros(og_df.shape[0])
        for counter1 in range(len(asset_costs_array)):
            asset_costs_array[counter1] = self.assets[counter1].cost.value
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
                asset_cost = self.assets[asset_number].cost.value
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
                    asset_cost = self.assets[asset_number].cost.value
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
        my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
        return
        
        
