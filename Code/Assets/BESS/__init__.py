#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
"""

import cvxpy as cp
import numpy as np
from ..Base_Assets import Asset_STEVFNs
from ..Base_Assets import Multi_Asset


class Charging_Asset(Asset_STEVFNs):
    """Class for battery charging"""
    asset_name = "Charging"
    source_node_type = "EL"
    target_node_type = "BESS"
    
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["charging_sizing_constant"]
        usage_constant_1 = params["charging_usage_constant"]
        
        return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
        
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["charging_conversion_factor"]
        return conversion_factor * flows
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"charging_sizing_constant": cp.Parameter(nonneg=True),
                          "charging_usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"charging_conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["charging_sizing_constant"].value = self.cost_fun_params["charging_sizing_constant"].value * NPV_factor
        return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["charging_usage_constant"].value = (self.cost_fun_params["charging_usage_constant"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        self._update_usage_constant()
        self._update_sizing_constant()
        return

class Discharging_Asset(Asset_STEVFNs):
    """Class for battery discharging"""
    asset_name = "Discharging"
    source_node_type = "BESS"
    target_node_type = "EL"
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["discharging_sizing_constant"]
        usage_constant_1 = params["discharging_usage_constant"]
        
        return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["discharging_conversion_factor"]
        return conversion_factor * flows
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"discharging_sizing_constant": cp.Parameter(nonneg=True),
                          "discharging_usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"discharging_conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["discharging_sizing_constant"].value = self.cost_fun_params["discharging_sizing_constant"].value * NPV_factor
        return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["discharging_usage_constant"].value = (self.cost_fun_params["discharging_usage_constant"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        self._update_usage_constant()
        self._update_sizing_constant()
        return

class Storage_Asset(Asset_STEVFNs):
    """Class for battery storage"""
    asset_name = "Storage"
    source_node_type = "BESS"
    target_node_type = "BESS"
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["storage_sizing_constant"]
        usage_constant_1 = params["storage_usage_constant"]
        # minimum_size = params["minimum_constant"]
        
        
        return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
        # return sizing_constant * cp.max(flows)
        
        # Setting a minimum size for the assets, Supergrid case study sensitivity analysis; uncomment minimum size for parameters
        # return cp.maximum(sizing_constant * cp.maximum(cp.max(flows), minimum_size),  usage_constant_1 * cp.sum(flows))
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["storage_conversion_factor"]
        return conversion_factor * flows
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"storage_sizing_constant": cp.Parameter(nonneg=True),
                          "storage_usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"storage_conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.target_node_times[-1] = self.source_node_times[0]
        self.target_node_times[:-1] = self.source_node_times[1:]
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["storage_sizing_constant"].value = self.cost_fun_params["storage_sizing_constant"].value * NPV_factor
        return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["storage_usage_constant"].value = (self.cost_fun_params["storage_usage_constant"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        self._update_usage_constant()
        self._update_sizing_constant()
        return

class BESS_Asset(Multi_Asset):
    """Class for Battery Energy Storage System"""
    asset_name = "BESS"
    assets_class_dictionary = {"Charging": Charging_Asset,
                               "Discharging": Discharging_Asset,
                               "Storage": Storage_Asset}
    
    @staticmethod
    def cost_fun(costs_dictionary, cost_fun_params):
        return cp.maximum(*costs_dictionary.values())
    
    
    def _update_assets(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset.update(self.parameters_df)
        return
    
    def asset_size(self):
        # Returns size of asset #
        effective_component_sizes = np.zeros(3)
        effective_component_sizes[0] = (self.assets_dictionary["Charging"].component_size() * 
                                        self.parameters_df["charging_sizing_constant"] / 
                                        self.parameters_df["storage_sizing_constant"])
        effective_component_sizes[1] = (self.assets_dictionary["Discharging"].component_size() * 
                                        self.parameters_df["discharging_sizing_constant"] / 
                                        self.parameters_df["storage_sizing_constant"])
        effective_component_sizes[2] = self.assets_dictionary["Storage"].component_size()
        asset_size = effective_component_sizes.max()
        return asset_size
    
    
    
    