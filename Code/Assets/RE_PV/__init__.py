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


class RE_PV_Asset(Asset_STEVFNs):
    """Class of Renewable Energy Sources """
    asset_name = "RE_PV"
    node_type = "EL"
    
    @staticmethod
    def cost_fun(flows, params):
        return params["sizing_constant"] * flows
        # for minimum size assets in Supergrid case study:
        # return params["sizing_constant"] * cp.maximum(flows, minimum_size)
        
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True)}
        
        # Uncomment below to add minimum size asset to dictionary, and comment above 
        # self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True),
        #                         "minimum_constant": cp.Parameter(nonneg=True)}
        return
        
    
    def define_structure(self, asset_structure):
        self.node_location = asset_structure["Location_1"]
        self.node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           asset_structure["Period"])
        self.number_of_edges = len(self.node_times)
        self.gen_profile = cp.Parameter(shape = self.number_of_edges, nonneg=True)
        self.flows = cp.Variable(nonneg = True)#size of RE asset
        return
    
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows * self.gen_profile[edge_number]
        return
    
    def get_plot_data(self):
        return self.flows.value * self.gen_profile.value
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["sizing_constant"].value = self.parameters_df["sizing_constant"] * NPV_factor
        return
    
    def _update_parameters(self):
        for parameter_name, parameter in self.cost_fun_params.items():
            parameter.value = self.parameters_df[parameter_name]
        #Update cost parameters based on NPV#
        self._update_sizing_constant()
        self._load_RE_profile()
        return
    
    def _load_RE_profile(self):
        """This function reads file and updates self.gen_profile """
        lat_lon_df = self.network.lat_lon_df.iloc[self.node_location]
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
        new_profile = np.zeros(n_sets * set_size)
        for counter1 in range(n_sets):
            old_loc_0 = offset + gap*counter1
            old_loc_1 = old_loc_0 + set_size
            new_loc_0 = set_size * counter1
            new_loc_1 = new_loc_0 + set_size
            new_profile[new_loc_0 : new_loc_1] = full_profile[old_loc_0 : old_loc_1]
        self.gen_profile.value = new_profile[:self.number_of_edges]
        return
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_" + self.parameters_df["RE_type"] + r"_location_" + str(self.node_location)
        return {asset_identity: asset_size}
    