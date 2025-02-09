#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
@contributor: Mónica Sagastuy Breña (c) 2024-2025
"""

import os
import numpy as np
import cvxpy as cp
from ..Base_Assets import Asset_STEVFNs
from ...Network import Edge_STEVFNs


class RE_WIND_Existing_Asset(Asset_STEVFNs):
    """Class of Renewable Energy Sources """
    asset_name = "RE_WIND_Existing"
    target_node_type = "EL"
    period = 1
    transport_time = 0
    
    
    @staticmethod
    def cost_fun(flows, params):
        return params["costs"] @ flows # element wise dot product
        
    def __init__(self):
        super().__init__()
        # NEW ADDITION: Initialize attributes for multi year modeling
        self.year_change_indices = []
        self.power_flows = []
        
        # Initialize number of years in prediction horizon - currently hard coded, needs review
        self.num_years = 2
        
        # EDITED: Parameter shape to fit control horizon in length, and initialize cost projection list
        self.cost_fun_params = {"costs": cp.Parameter(shape=(self.num_years,), nonneg=True) }
        self.cost_projections = []
        return
    
    def define_structure(self, asset_structure):
        self.asset_structure = asset_structure
        self.source_node_location = "NULL"
        self.target_node_location = asset_structure["Location_1"]
        self.target_node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           self.period)
        self.number_of_edges = len(self.target_node_times)
        self.gen_profile = cp.Parameter(shape = (self.number_of_edges), nonneg=True)
        # NEW ADDITION: Determine how many years in control horizon from system params
        # self.num_years = self.network.system_parameters_df.loc["project_life", "value"] / 8760
        self.num_years = 2 # Hard-coded it for 2 years, need to figure out how to properly update with params
        # EDITED: set size of RE asset as array of sizes per horizon modeled
        self.flows = cp.Variable(shape=(self.num_years,), nonneg=True)
        return
    
    def build_edge(self, edge_number):
        target_node_time = self.target_node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.target_node_location, self.target_node_type, target_node_time))
        # EDITED: Build power flows first with single capacity (first element in Parameter)
        index_number = 0
        new_edge.flow = self.flows[index_number] * self.gen_profile[edge_number]
        return
    
    def build_edges(self):
        self.edges = []
        for counter1 in range(self.number_of_edges):
            self.build_edge(counter1)
        return
    
    def _update_flows(self):
        # NEW FUNCTION: Allows powerflow update for multi-year modeling for RE assets
        index_number = 0
        edge_counter = 0
        for edge in self.edges:
            if edge_counter >= self.year_change_indices[index_number]:
                if index_number < self.num_years-1:
                    if edge_counter == self.year_change_indices[index_number+1]:
                        index_number += 1
                edge.flow = self.flows[index_number] * self.gen_profile[edge_counter]
                edge_counter += 1
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        
        # EDITED: Update costs with NPV Factor in the cost projections list. 
        # TO-DO: Needs exception for single-year modeling to use one value alone
        # TO-DO: Needs NPV factor update per year as it advances.
        for counter in range(self.num_years):
            self.cost_fun_params["costs"].value[counter] = self.cost_projections[counter] * NPV_factor

        return
    
    def _update_parameters(self):
        # Convert cost projections input into list if given, otherwise update single input value
        for parameter_name, parameter in self.cost_fun_params.items():
            costs_values = self.parameters_df[parameter_name]
            if isinstance(costs_values, str): 
                self.cost_projections = costs_values.split(",")
                for counter in range(len(self.cost_projections)):
                    self.cost_projections[counter] = float(self.cost_projections[counter])
                parameter.value = self.cost_projections
            else: 
                parameter.value = costs_values
        # Update costs and RE profile
        self._update_sizing_constant()
        self._load_RE_profile()
        if self.num_years > 1:
            self._update_flows()
        return
    
    def _load_RE_profile(self):
        """This function reads file and updates self.gen_profile """
        lat_lon_df = self.network.lat_lon_df.iloc[self.target_node_location]
        lat = lat_lon_df["lat"]
        lat = np.int64(np.round((lat) / 0.5)) * 0.5
        lat = min(lat,90.0)
        lat = max(lat,-90.0)
        LAT = "{:0.1f}".format(lat)
        lon = lat_lon_df["lon"]
        lon = np.int64(np.round((lon) / 0.625)) * 0.625
        lon = min(lon, 179.375)
        lon = max(lon, -180.0)
        LON = str(lon)
        RE_TYPE = self.parameters_df["RE_type"]
        profile_folder = os.path.join(self.parameters_folder, "profiles", RE_TYPE, r"lat"+LAT)
        profile_filename = RE_TYPE + r"_lat" + LAT + r"_lon" + LON + r".csv"
        profile_filename = os.path.join(profile_folder, profile_filename)
        full_profile = np.loadtxt(profile_filename)
        set_size = self.parameters_df["set_size"]
        set_number = self.parameters_df["set_number"]
        n_sets = int(np.ceil(self.number_of_edges/set_size))
        gap = int(len(full_profile) / (n_sets * set_size)) * set_size
        offset = set_size * set_number
        new_profile = np.zeros(int(n_sets * set_size))
        # NEW ADDITION: Initialize indices and variables to Build multi-year profiles
        self.year_indexes = [0] # Initialize a list with first element 0 to indicate first year
        hour_counter = 1
        missing_val = 0
        # --
        for counter1 in range(n_sets):
            old_loc_0 = offset + gap*counter1
            old_loc_1 = old_loc_0 + set_size
            new_loc_0 = set_size * counter1
            new_loc_1 = new_loc_0 + set_size
            new_profile[new_loc_0 : new_loc_1] = full_profile[old_loc_0 : old_loc_1]
            # -- NEW ADDITION: Get indices for change in year when day sampling
            if old_loc_0 > (hour_counter * 8759) + missing_val:
                 self.year_change_indices.append(new_loc_0)
                 hour_counter += 1
                 missing_val += 1
        self.gen_profile.value = new_profile[:self.number_of_edges]
        return
    
    def get_plot_data(self):
        # NEWLY ADDITION: getting complete power flows for plotting
        for edge_counter in range(self.number_of_edges):
            self.power_flows += [self.edges[edge_counter].flow.value]
        return self.power_flows
    
    def size(self):
        return self.flows.value
    
    def asset_size(self):
        # Returns size of asset for Exsiting RE, which is a vector #
        return self.flows.value
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_" + self.parameters_df["RE_type"] + r"_location_" + str(self.target_node_location)
        return {asset_identity: asset_size}