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
from ...Network import Edge_STEVFNs


class Charging_Asset(Asset_STEVFNs):
    """Class for battery charging"""
    asset_name = "Charging"
    source_node_type = "EL"
    target_node_type = "BESS"
    source_node_type_list = ["EL", "NULL", "NULL"]
    target_node_type_list = ["BESS", "BESS_Max_Charging", "BESS_Import"]
    
    
    @staticmethod
    def cost_fun(flows, params):
        # sizing_constant = params["charging_sizing_constant"]
        usage_constant_1 = params["charging_usage_constant"]
        
        # return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
        return usage_constant_1 * cp.sum(flows)
    
    @staticmethod
    def cost_fun1(flows, params):
        # sizing_constant = params["charging_sizing_constant"]
        usage_constant_1 = params["charging_usage_constant"]
        
        # return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
        return usage_constant_1 * cp.sum(flows)
    
    @staticmethod
    def cost_fun2(flows, params):
        return 0.0
        
    cost_fun_list = [cost_fun1, cost_fun2, cost_fun2]
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["charging_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun1(flows, params):
        conversion_factor = params["charging_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun2(flows, params):
        max_power = params["charging_max"]
        return max_power - flows
    
    @staticmethod
    def conversion_fun3(flows, params):
        return - flows
    
    conversion_fun_list = [conversion_fun1.__get__(object),
                           conversion_fun2.__get__(object),
                           conversion_fun3.__get__(object)]
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"charging_sizing_constant": cp.Parameter(nonneg=True),
                          "charging_usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"charging_conversion_factor": cp.Parameter(nonneg=True),
                                      "charging_max": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return
    
    # def _update_sizing_constant(self):
    #     N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
    #     r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
    #     NPV_factor = (1-r**N)/(1-r)
    #     self.cost_fun_params["charging_sizing_constant"].value = self.cost_fun_params["charging_sizing_constant"].value * NPV_factor
    #     return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["charging_usage_constant"].value = (self.cost_fun_params["charging_usage_constant"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_charging_max(self):
        self.conversion_fun_params["charging_max"].value = (self.conversion_fun_params["charging_max"].value * 
                                                            self.asset_structure["Period"])
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        self._update_usage_constant()
        # self._update_sizing_constant()
        self._update_charging_max()
        return
    
    def build(self):
        for counter1 in range(3):
            self.source_node_type = self.source_node_type_list[counter1]
            self.target_node_type = self.target_node_type_list[counter1]
            self.conversion_fun = self.conversion_fun_list[counter1]
            self.build_edges()
            self.build_cost()
        return

class Discharging_Asset(Asset_STEVFNs):
    """Class for battery discharging"""
    asset_name = "Discharging"
    source_node_type = "BESS"
    target_node_type = "EL"
    source_node_type_list = ["BESS", "NULL", "NULL"]
    target_node_type_list = ["EL", "BESS_Max_Discharging", "BESS_Export"]
    @staticmethod
    def cost_fun(flows, params):
        # sizing_constant = params["discharging_sizing_constant"]
        usage_constant_1 = params["discharging_usage_constant"]
        
        # return cp.maximum(sizing_constant * cp.max(flows),  usage_constant_1 * cp.sum(flows))
        return usage_constant_1 * cp.sum(flows)
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["discharging_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun1(flows, params):
        conversion_factor = params["discharging_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun2(flows, params):
        max_power = params["discharging_max"]
        return max_power - flows
    
    @staticmethod
    def conversion_fun3(flows, params):
        return flows
    
    conversion_fun_list = [conversion_fun1.__get__(object),
                           conversion_fun2.__get__(object),
                           conversion_fun3.__get__(object)]
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"discharging_sizing_constant": cp.Parameter(nonneg=True),
                          "discharging_usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"discharging_conversion_factor": cp.Parameter(nonneg=True),
                                      "discharging_max": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _load_parameters_df(self, parameters_df):
        self.parameters_df = parameters_df
        return
    
    # def _update_sizing_constant(self):
    #     N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
    #     r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
    #     NPV_factor = (1-r**N)/(1-r)
    #     self.cost_fun_params["discharging_sizing_constant"].value = self.cost_fun_params["discharging_sizing_constant"].value * NPV_factor
    #     return
    
    def _update_usage_constant(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["discharging_usage_constant"].value = (self.cost_fun_params["discharging_usage_constant"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_discharging_max(self):
        self.conversion_fun_params["discharging_max"].value = (self.conversion_fun_params["discharging_max"].value * 
                                                            self.asset_structure["Period"])
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        self._update_usage_constant()
        # self._update_sizing_constant()
        self._update_discharging_max()
        return
    
    def build(self):
        for counter1 in range(3):
            self.source_node_type = self.source_node_type_list[counter1]
            self.target_node_type = self.target_node_type_list[counter1]
            self.conversion_fun = self.conversion_fun_list[counter1]
            self.build_edges()
            self.build_cost()
        return

class Storage_Asset(Asset_STEVFNs):
    """Class for battery storage"""
    asset_name = "Storage"
    source_node_type = "BESS"
    target_node_type = "BESS"
    source_node_type_list = ["BESS", "NULL"]
    target_node_type_list = ["BESS", "BESS_Max_Storage"]
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["storage_sizing_constant"]
        return sizing_constant
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["storage_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun1(flows, params):
        conversion_factor = params["storage_conversion_factor"]
        return conversion_factor * flows
    
    @staticmethod
    def conversion_fun2(flows, params):
        storage_max = params["storage_max"]
        return storage_max - flows
    
    conversion_fun_list = [conversion_fun1.__get__(object), 
                           conversion_fun2.__get__(object)]
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"storage_sizing_constant": cp.Parameter(nonneg=True),
                          "storage_max": cp.Parameter(nonneg=True),
                          "lifespan": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"storage_conversion_factor": cp.Parameter(nonneg=True),
                                      "storage_max": cp.Parameter(nonneg=True),
                                      "initial_storage": cp.Parameter(nonneg=True)}
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
        # self.cost_fun_params["storage_sizing_constant"].value = self.cost_fun_params["storage_sizing_constant"].value * NPV_factor
        sizing_constant = self.cost_fun_params["storage_sizing_constant"].value
        storage_max = self.cost_fun_params["storage_max"]
        # lifespan = self.cost_fun_params["lifespan"]
        # lifespan_price = sizing_constant * storage_max / lifespan #Loss of lifespan per half hour
        # lifespan_cost = lifespan_price * self.network.system_structure_properties["simulated_timesteps"]
        replacement_cost = sizing_constant * storage_max * NPV_factor
        # self.cost_fun_params["storage_sizing_constant"].value = lifespan_cost.value
        self.cost_fun_params["storage_sizing_constant"].value = replacement_cost
        return
    
    # def _update_usage_constant(self):
    #     simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
    #     N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
    #     r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
    #     NPV_factor = (1-r**N)/(1-r)
    #     self.cost_fun_params["storage_usage_constant"].value = (self.cost_fun_params["storage_usage_constant"].value * 
    #                                                     NPV_factor * simulation_factor)
    #     return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on NPV#
        # self._update_usage_constant()
        self._update_sizing_constant()
        return
    
    def build(self):
        for counter1 in range(2):
            self.source_node_type = self.source_node_type_list[counter1]
            self.target_node_type = self.target_node_type_list[counter1]
            self.conversion_fun = self.conversion_fun_list[counter1]
            self.build_edges()
            self.build_cost()
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
        if edge_number == (self.number_of_edges-1):
            new_edge.flow = self.conversion_fun_params["initial_storage"]
        else:
            new_edge.flow = self.flows[edge_number]
            new_edge.conversion_fun = self.conversion_fun
            new_edge.conversion_fun_params = self.conversion_fun_params
        return

class BESS_Market_Asset(Multi_Asset):
    """Class for Battery Energy Storage System"""
    asset_name = "BESS_Market"
    assets_class_dictionary = {"Charging": Charging_Asset,
                               "Discharging": Discharging_Asset,
                               "Storage": Storage_Asset}
    
    @staticmethod
    def cost_fun(costs_dictionary, cost_fun_params):
        return cp.maximum(*costs_dictionary.values())
        # return cp.sum(list(costs_dictionary.values()))*0.5
    
    
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
    
    
    
    