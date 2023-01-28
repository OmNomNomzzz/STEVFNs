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
from ..Base_Assets import Multi_Asset



class EL_Demand_Component(Asset_STEVFNs):
    """Class of Electricity Demand Component"""
    asset_name = "EL_Demand_Component"
    source_node_type = "NULL"
    target_node_type = "Net_EL_Demand"
    
    @staticmethod
    def conversion_fun(flows, params):
        return params["demand"]
    
    def __init__(self):
        super().__init__()
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.conversion_fun_params = {
            "demand_profile": cp.Parameter( self.number_of_edges, nonneg = True)}
        return
    
    def build_edge(self, edge_number):
        source_node_time = self.source_node_times[edge_number]
        target_node_time = self.target_node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        if self.source_node_type != "NULL":
            new_edge.attach_source_node(self.network.extract_node(
                self.source_node_location, self.source_node_type, source_node_time))
        if self.target_node_type != "NULL":
            new_edge.attach_target_node(self.network.extract_node(
                self.target_node_location, self.target_node_type, target_node_time))
        new_edge.flow = self.flows[edge_number]
        new_edge.conversion_fun = self.conversion_fun
        new_edge.conversion_fun_params = {
            "demand": self.conversion_fun_params["demand_profile"][edge_number]}
        new_edge.target_node.curtailment = False
        return

class Net_EL_Demand_Component(Asset_STEVFNs):
    """Class of Net Electricity Demand Component"""
    asset_name = "Net_EL_Demand_Component"
    source_node_type = "Net_EL_Demand"
    target_node_type = "EL"
    
    @staticmethod
    def conversion_fun(flows, params):
        return -flows
    
    def __init__(self):
        super().__init__()
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.flows = cp.Variable(self.number_of_edges, nonneg=True)
        return
    

class Unmet_EL_Demand_Component(Asset_STEVFNs):
    """Class of Total Unmet Electricity Demand Component"""
    asset_name = "Unmet_EL_Demand_Component"
    source_node_type = "Unmet_EL_Demand"
    target_node_type = "Net_EL_Demand"
    
    @staticmethod
    def conversion_fun(flows, params):
        return -flows
    
    def __init__(self):
        super().__init__()
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.source_node_times = np.zeros(self.number_of_edges)
        self.flows = cp.Variable(self.number_of_edges, nonneg=True)
        return

class Total_Unmet_EL_Demand_Component(Asset_STEVFNs):
    """Class of Total Unmet Electricity Demand Component"""
    asset_name = "Total_Unmet_EL_Demand_Component"
    source_node_type = "NULL"
    target_node_type = "Unmet_EL_Demand"
    
    @staticmethod
    def conversion_fun(flows, params):
        return params["total_unmet_demand"]
    
    def __init__(self):
        super().__init__()
        self.conversion_fun_params =  {"total_unmet_demand": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        self.asset_structure = asset_structure
        self.source_node_location = asset_structure["Location_1"]
        self.source_node_times = np.zeros(1)
        self.target_node_location = asset_structure["Location_2"]
        self.target_node_times = np.zeros(1)
        self.number_of_edges = len(self.source_node_times)
        self.flows = cp.Constant(np.zeros(self.number_of_edges))
        return

class EL_Demand_UM_Asset(Multi_Asset):
    """Class of Electricity Demand Asset"""
    asset_name = "EL_Demand_UM"
    
    def __init__(self):
        super().__init__()
        self.parameters_dict = dict()
        return
    
    assets_class_dictionary = {"EL_Demand": EL_Demand_Component,
                               "Net_EL_Demand": Net_EL_Demand_Component,
                               "Unmet_EL_Demand": Unmet_EL_Demand_Component,
                               "Total_Unmet_EL_Demand": Total_Unmet_EL_Demand_Component}
    
    def build(self):
        super().build()
        self.number_of_edges = self.assets_dictionary["EL_Demand"].number_of_edges
        return
    
    def update(self, asset_type):
        self._load_parameters_df(asset_type)
        self._update_parameters()
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
        demand_profile = new_profile[:self.number_of_edges]
        total_unmet_demand = demand_profile.sum() * self.parameters_df["unmet_fraction"]
        self.assets_dictionary["EL_Demand"].conversion_fun_params["demand_profile"].value = demand_profile
        self.assets_dictionary["Total_Unmet_EL_Demand"].conversion_fun_params["total_unmet_demand"].value = total_unmet_demand
        return
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.assets_dictionary["EL_Demand"].size()
        asset_identity = self.asset_name + r"_location_" + str(self.node_location)
        return {asset_identity: asset_size}
 
