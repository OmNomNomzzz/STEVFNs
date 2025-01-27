#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
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
    source_node_type_2 = "NULL"
    target_node_type_2 = "RE_WIND_Existing"
    period = 1
    transport_time = 0
    target_node_time_2 = 0
    
    @staticmethod
    def cost_fun(flows, params):
        return params["sizing_constant"] * cp.sum(flows)
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        self.asset_structure = asset_structure
        self.source_node_location = "NULL"
        self.target_node_location = asset_structure["Location_1"]
        self.source_node_location_2 = "NULL"
        self.target_node_location_2 = asset_structure["Location_1"]
        self.target_node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           self.period)
        self.number_of_edges = len(self.target_node_times)
        
        # EDITED: shape of profile to account for various years
        self.gen_profile = cp.Parameter(shape = (3 ,self.number_of_edges), nonneg=True)
        # set size of RE asset as array of sizes per horizon modeled
        self.flows = cp.Parameter(shape=(3,), value=[10, 20, 35])
        return
    
    def build_edge(self, edge_number):
        target_node_time = self.target_node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.target_node_location, self.target_node_type, target_node_time))
        # new_edge.flow = self.flows * self.gen_profile[edge_number]
        
        
        # NEWLY ADDED: Needs to relate to the loop in main.py so the asset size updates
        # According to the iteration and not just internally here.
        for year_number in range(0, 3):
            new_edge.flow = self.flows[year_number] * self.gen_profile[year_number][edge_number]
        return
    
    def get_plot_data(self):
        # NEWLY ADDED: getting flows data for each year's capacity
        return self.gen_profile.T.value * self.flows.value
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["sizing_constant"].value = self.parameters_df["sizing_constant"] * NPV_factor
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Update cost parameters based on NPV#
        self._update_sizing_constant()
        self._load_RE_profile()
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
        for counter1 in range(n_sets):
            old_loc_0 = offset + gap*counter1
            old_loc_1 = old_loc_0 + set_size
            new_loc_0 = set_size * counter1
            new_loc_1 = new_loc_0 + set_size
            new_profile[new_loc_0 : new_loc_1] = full_profile[old_loc_0 : old_loc_1]
        # self.gen_profile.value = new_profile[:self.number_of_edges]
        
        '''Below testing for mpc updates for a set of years in prediction horizon'''
        # Get the profile added the same number of times as prediction_horizon to
        # multiply by the flows array. Currently hard coded for five 
        self.gen_profile.value = np.tile(new_profile[:self.number_of_edges], (3, 1))
        return
    
    def size(self):
        # The sizes of Existing assets is pre-defined by the previously installed and their lifetimes
        return self.flows
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_" + self.parameters_df["RE_type"] + r"_location_" + str(self.target_node_location)
        return {asset_identity: asset_size}
    