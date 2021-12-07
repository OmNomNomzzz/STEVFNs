#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:25:54 2021

@author: aniqahsan
"""

import numpy as np
import cvxpy as cp
import pandas as pd
import os
from ..Base_Assets import Asset_STEVFNs
from ...Network import Edge_STEVFNs


class HTH_Demand_Asset(Asset_STEVFNs):
    """Class of High Temperature Heat Demand Asset"""
    asset_name = "HTH_Demand"
    node_type = "HTH"
    def __init__(self):
        super().__init__()
        return
    
    def define_structure(self, asset_structure):
        self.node_location = asset_structure["Location_1"]
        self.node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           asset_structure["Period"])
        self.number_of_edges = len(self.node_times)
        self.flows = cp.Parameter(shape = self.number_of_edges, nonneg=True)
        return
    
    def build_costs(self):
        self.cost = cp.Constant(0)
        return
        
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_source_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows[edge_number]
        return
    
    def _update_parameters(self):
        profile_filename = self.parameters_df["profile_filename"] + r".csv"
        profile_filename = os.path.join(self.parameters_folder, "profiles", profile_filename)
        profile_df = pd.read_csv(profile_filename)
        full_profile = np.array(profile_df["Demand"])
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
        self.flows.value = new_profile[:self.number_of_edges]
        return
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_location_" + str(self.node_location)
        return {asset_identity: asset_size}
