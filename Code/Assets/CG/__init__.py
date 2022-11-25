#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:25:54 2021

@author: aniqahsan
"""

import numpy as np
import cvxpy as cp
from ..Base_Assets import Asset_STEVFNs
from ...Network import Edge_STEVFNs



class CG_Asset(Asset_STEVFNs):
    """Class of Conventional Generators"""
    asset_name = "CG"
    node_type = "EL"
    
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["sizing_constant"]
        usage_constant_1 = params["usage_constant_1"]
        usage_constant_2 = params["usage_constant_2"]
        return (sizing_constant * cp.max(flows) + usage_constant_1 * cp.sum(flows) 
                + usage_constant_2 * cp.sum(cp.power(flows,2)))
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True),
                          "usage_constant_1": cp.Parameter(nonneg=True),
                          "usage_constant_2": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        self.node_location = asset_structure["Location_1"]
        self.node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           asset_structure["Period"])
        self.number_of_edges = len(self.node_times)
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
        
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows[edge_number]
        return
    
    def _update_sizing_constant(self):
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/self.parameters_df["lifespan"])
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**(-self.parameters_df["lifespan"]/8760)
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["sizing_constant"].value = self.cost_fun_params["sizing_constant"].value * NPV_factor
        return
    
    def _update_usage_constants(self):
        simulation_factor = 8760/self.network.system_structure_properties["simulated_timesteps"]
        N = np.ceil(self.network.system_parameters_df.loc["project_life", "value"]/8760)
        r = (1 + self.network.system_parameters_df.loc["discount_rate", "value"])**-1
        NPV_factor = (1-r**N)/(1-r)
        self.cost_fun_params["usage_constant_1"].value = (self.cost_fun_params["usage_constant_1"].value * 
                                                        NPV_factor * simulation_factor)
        self.cost_fun_params["usage_constant_2"].value = (self.cost_fun_params["usage_constant_2"].value * 
                                                        NPV_factor * simulation_factor)
        return
    
    def _update_parameters(self):
        for parameter_name, parameter in self.cost_fun_params.items():
            parameter.value = self.parameters_df[parameter_name]
        #Update cost parameters based on NPV#
        self._update_sizing_constant()
        self._update_usage_constants()
        return
    
    def get_asset_sizes(self):
        # Returns the size of the asset as a dict #
        asset_size = self.size()
        asset_identity = self.asset_name + r"_location_" + str(self.node_location)
        return {asset_identity: asset_size}
