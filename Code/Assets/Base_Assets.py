#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:33:27 2021

@author: aniqahsan
"""

import cvxpy as cp
import numpy as np
import pandas as pd
import os
from ..Network import Edge_STEVFNs
import matplotlib.pyplot as plt

####### Define Classes #######

class Asset_STEVFNs:
    """Base Class of assets"""
    asset_name = "Asset_STEVFNs"
    source_node_type = "NULL"
    target_node_type = "NULL"
    cost_fun = staticmethod(lambda flows, params: cp.Constant(0))
    conversion_fun = staticmethod(lambda flow, params: flow)
    def __init__(self):
        self.cost_fun_params = dict()
        self.conversion_fun_params = dict()
        return
    
    def build_cost(self):
        self.cost = self.cost_fun(self.flows, self.cost_fun_params)
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
        new_edge.conversion_fun_params = self.conversion_fun_params
        return
    
    def build_edges(self):
        self.edges = []
        for counter1 in range(self.number_of_edges):
            self.build_edge(counter1)
        return
    
    def get_plot_data(self):
        return self.flows.value
    
    def build(self):
        self.build_edges()
        self.build_cost()
        return
    
    def define_structure(self, asset_structure):
        self.asset_structure = asset_structure
        self.source_node_location = asset_structure["Location_1"]
        self.source_node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           asset_structure["Period"])
        self.target_node_location = asset_structure["Location_2"]
        self.target_node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           asset_structure["Period"])
        self.number_of_edges = len(self.source_node_times)
        self.flows = cp.Constant(np.zeros(self.number_of_edges))
        return
    
    def _load_parameters_df(self, asset_type):
        self.parameters_folder = os.path.join(self.network.base_folder, "Code", "Assets", 
                                           self.asset_name)
        parameters_filename = os.path.join(self.parameters_folder, "parameters.csv")
        self.parameters_df = pd.read_csv(parameters_filename).iloc[asset_type]
        return
    
    def _load_historic_capacity_params(self):
        ## NEW FUNCTION
        """Loads historic capacity parameters if the file exists."""
        country = self.parameters_df["location_name"]
        historic_filename = os.path.join(self.parameters_folder, "capacities", f"{country}_capacity_params.csv")
        if os.path.exists(historic_filename):
            self.historic_capacity_df = pd.read_csv(historic_filename)
        else:
            self.historic_capacity_df = None  # Optionally set to None to indicate no file
        return

    
    def _update_parameters(self):
        for parameter_name, parameter in self.cost_fun_params.items():
            parameter.value = self.parameters_df[parameter_name]
        for parameter_name, parameter in self.conversion_fun_params.items():
            parameter.value = self.parameters_df[parameter_name]
        return
    
    def update(self, asset_type):
        self._load_parameters_df(asset_type)
        self._update_parameters()
        return
    
    def size(self):
        return self.flows.value.max()
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_location_" + str(self.source_node_location)
        return {asset_identity: asset_size}
    
    def plot_asset_usage(self):
        plt.plot(self.flows.value)
        plt.show()
        return
    
    def component_size(self):
        # Returns size of component (i.e. asset) #
        return self.flows.value.max()
    
    def asset_size(self):
        # Returns size of asset #
        return self.component_size()
    
    def get_component_size(self):
        # Returns the size of component as a dict #
        component_size = self.component_size()
        component_identity = self.asset_name
        return {component_identity: component_size}
    
    def get_component_sizes(self):
        # Returns the size of components of the asset as a dict #
        return self.get_component_size()
    
    def get_asset_size(self):
        # Returns the size of asset as a dict #
        asset_size = self.asset_size()
        asset_identity = self.asset_name
        return {asset_identity: asset_size}

            
class Multi_Asset(Asset_STEVFNs):
    """Class that contains multiple assets"""
    asset_name = "Multi_Asset"
    cost_fun = staticmethod(lambda costs_dictionary, cost_fun_params: cp.Constant(0))
    assets_class_dictionary = dict()#dictionary that contains assetclasses
    def __init__(self):
        super().__init__()
        self.assets_dictionary = dict()
        self._generate_assets()
        self.costs_dictionary = dict()
        return
    
    def _generate_assets(self):
        for asset_name, asset_class in self.assets_class_dictionary.items():
            self.assets_dictionary[asset_name] = self.assets_class_dictionary[asset_name]()
        return
    
    def build(self):
        self._build_assets()
        self.build_cost()
        return
    
    def build_cost(self):
        for asset_name, asset in self.assets_dictionary.items():
            self.costs_dictionary[asset_name] = asset.cost
        self.cost = self.cost_fun(self.costs_dictionary, self.cost_fun_params)
        return
    
    def _build_assets(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset.build()
        return
    
    def define_structure(self, asset_structure):
        self.asset_structure = asset_structure
        self._define_asset_structures()
        return
    
    def _define_asset_structures(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset.network = self.network
            asset.define_structure(self.asset_structure)
        return
    
    def update(self, asset_type):
        super().update(asset_type)
        self._update_assets()
        return
    
    def _update_assets(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset_type = self.parameters_df[asset_name + "_asset_type"]
            asset.update(asset_type)
        return
    
    def get_plot_data(self):
        flow_dictionary = dict()
        for asset_name, asset in self.assets_dictionary.items():
            flow_dictionary[asset_name] = asset.get_plot_data()
        return flow_dictionary
    
    def size(self):
        asset_sizes_dictionary = dict()
        for asset_name, asset in self.assets_dictionary.items():
            asset_sizes_dictionary[asset_name] = asset.size()
        return asset_sizes_dictionary
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        assets_sizes_dict = dict()
        for asset_name, asset in self.assets_dictionary.items():
            assets_sizes_dict.update(asset.get_asset_sizes())
        new_assets_sizes_dict = dict()
        for asset_identity, asset_size in assets_sizes_dict.items():
            new_asset_identity = self.asset_name + r"_" + asset_identity
            new_assets_sizes_dict[new_asset_identity] = asset_size
        return new_assets_sizes_dict
    
    def get_component_sizes(self):
        # Returns the size of components of the asset as a dict #
        component_sizes_dict = dict()
        for component_name, component in self.assets_dictionary.items():
            component_sizes_dict.update(component.get_component_size())
        new_component_sizes_dict = dict()
        for component_identity, component_size in component_sizes_dict.items():
            new_component_identity = self.asset_name + r"_" + component_identity
            new_component_sizes_dict[new_component_identity] = component_size
        return new_component_sizes_dict
    
    def asset_size(self):
        # Returns size of asset #
        component_size_df = self.get_component_sizes()
        asset_size = np.array(list(component_size_df.values())).max()
        return asset_size
    
    def get_asset_size(self):
        # Returns the size of asset as a dict #
        asset_identity = self.asset_name
        asset_size = self.asset_size()
        return {asset_identity : asset_size}