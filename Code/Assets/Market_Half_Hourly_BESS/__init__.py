#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
"""

import cvxpy as cp
import numpy as np
import pandas as pd
from ..Base_Assets import Asset_STEVFNs
from ..Base_Assets import Multi_Asset
import os


class Import_Asset(Asset_STEVFNs):
    """Class for battery charging from half hourly market"""
    asset_name = "Import"
    source_node_type = "NULL"
    target_node_type = "EL"
    target_node_type_list = ["EL", "BESS_Import"]
    
    
    @staticmethod
    def cost_fun(flows, params):
        usage_constant = params["import_prices"]
        
        return cp.sum(cp.multiply(usage_constant, flows))
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"import_prices": cp.Parameter()}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        self.cost_fun_params["import_prices"] = cp.Parameter(shape = self.number_of_edges)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return  
    
    def build(self):
        for counter1 in range(2):
            self.target_node_type = self.target_node_type_list[counter1]
            self.build_edges()
            self.build_cost()
            self._prevent_curtailment()
        return
    
    def _prevent_curtailment(self):
        for edge_number in range(self.number_of_edges):
            target_node_type = self.target_node_type_list[1]
            target_node_time = self.target_node_times[edge_number]
            target_node_location = self.source_node_location
            node = self.network.extract_node(target_node_location, target_node_type, target_node_time)
            node.curtailment = False
        return
    
    def _update_parameters(self):
        profile_filename = self.parameters_df["profile_filename"] + r".csv"
        profile_filename = os.path.join(self.parameters_folder, "profiles", profile_filename)
        profile_df = pd.read_csv(profile_filename)
        full_profile = np.array(profile_df["Import Price"])
        full_profile = np.append(full_profile, full_profile)
        start_index = self.parameters_df["initial_timestep"]
        end_index = start_index + self.number_of_edges
        final_profile = full_profile[start_index:end_index]
        
        #Add impact of asset period (timestep)
        final_profile = final_profile * self.asset_structure["Period"]
        
        # #Add impact of NPV for simulated times
        # r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        # N_array = np.floor(np.arange(self.number_of_edges) * 
        #              self.asset_structure["Period"] / 8760.0)
        # NPV_factor_array = (r**N_array)
        # final_profile = final_profile * NPV_factor_array
        
        # #Add impact of NPV for lifetime of project
        # simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        # N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        # NPV_factor = (1-r**N)/(1-r)
        # final_profile = final_profile * NPV_factor * simulation_factor
        
        # self.cost_fun_params["charging_usage_constant"].value = (self.cost_fun_params["charging_usage_constant"].value * 
        #                                                 NPV_factor * simulation_factor)
        
        self.cost_fun_params["import_prices"].value = final_profile
        
        return

class Export_Asset(Asset_STEVFNs):
    """Class for battery discharging from half hourly market"""
    asset_name = "Export"
    source_node_type = "EL"
    target_node_type = "NULL"
    source_node_type_list = ["EL", "BESS_Export"]
    
    
    @staticmethod
    def cost_fun(flows, params):
        usage_constant = params["export_prices"]
        
        return -cp.sum(cp.multiply(usage_constant, flows))
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"export_prices": cp.Parameter()}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        self.cost_fun_params["export_prices"] = cp.Parameter(shape = self.number_of_edges)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return  
    
    def build(self):
        for counter1 in range(2):
            self.source_node_type = self.source_node_type_list[counter1]
            self.build_edges()
            self.build_cost()
            self._prevent_curtailment()
        return
    
    def _prevent_curtailment(self):
        for edge_number in range(self.number_of_edges):
            target_node_type = self.target_node_type_list[1]
            target_node_time = self.target_node_times[edge_number]
            target_node_location = self.source_node_location
            node = self.network.extract_node(target_node_location, target_node_type, target_node_time)
            node.curtailment = False
        return
    
    def _update_parameters(self):
        profile_filename = self.parameters_df["profile_filename"] + r".csv"
        profile_filename = os.path.join(self.parameters_folder, "profiles", profile_filename)
        profile_df = pd.read_csv(profile_filename)
        full_profile = np.array(profile_df["Export Price"])
        full_profile = np.append(full_profile, full_profile)
        start_index = self.parameters_df["initial_timestep"]
        end_index = start_index + self.number_of_edges
        self.cost_fun_params["export_prices"].value = self.asset_structure["Period"] * full_profile[start_index:end_index]
        return



class Market_Half_Hourly_BESS_Asset(Multi_Asset):
    """Class for Battery Energy Storage System"""
    asset_name = "Market_Half_Hourly_BESS"
    assets_class_dictionary = {"Import": Import_Asset,
                               "Export": Export_Asset}
    
    @staticmethod
    def cost_fun(costs_dictionary, cost_fun_params):
        return cp.sum(list(costs_dictionary.values()))
    
    
    def _update_assets(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset.parameters_folder = self.parameters_folder
            asset.update(self.parameters_df)
        return
    
    def asset_size(self):
        # Returns size of asset #
        effective_component_sizes = np.zeros(2)
        effective_component_sizes[0] = self.assets_dictionary["Import"].component_size()
        effective_component_sizes[1] = self.assets_dictionary["Export"].component_size()
        asset_size = effective_component_sizes.max()
        return asset_size
    
    
    
    