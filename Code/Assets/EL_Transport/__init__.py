#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
"""

import cvxpy as cp
from ..Base_Assets import Asset_STEVFNs
import numpy as np
from ...Network import Edge_STEVFNs


class EL_Transport_Asset(Asset_STEVFNs):
    """Class of EL transport asset"""
    asset_name = "EL_Transport"
    source_node_type = "EL"
    target_node_type = "EL"
    
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["sizing_constant"]
        usage_constant = params["usage_constant"]
        return sizing_constant * cp.max(flows) + usage_constant * cp.sum(flows)
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["conversion_factor"]
        return conversion_factor * flows
    
    def _update_distance(self):
        #Function that calculates the distance between the source and target nodes#
        lat_lon_0 = self.network.lat_lon_df.iloc[int(self.source_node_location)]
        lat_lon_1 = self.network.lat_lon_df.iloc[int(self.target_node_location)]
        lat_0 = lat_lon_0["lat"]/180 * np.pi
        lat_1 = lat_lon_1["lat"]/180 * np.pi
        lon_d = (lat_lon_1["lon"] - lat_lon_0["lon"])/180 * np.pi
        a = np.sin((lat_1 - lat_0)/2)**2 + np.cos(lat_0) * np.cos(lat_1) * np.sin(lon_d/2)**2
        c = 2 * np.arctan2(a**0.5, (1-a)**0.5)
        R = 6.371 # in Mm radius of the earth
        self.distance = R * c # in Mm
        return
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True),
                          "usage_constant": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_times = self.target_node_times + asset_structure["Transport_Time"]
        self.target_node_times = self.target_node_times % asset_structure["End_Time"]
        self.flows = cp.Variable(self.number_of_edges*2, nonneg = True)
        return
    
    def build_edge_opposite(self, edge_number):
        source_node_time = self.source_node_times[edge_number]
        target_node_time = self.target_node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_source_node(self.network.extract_node(
            self.target_node_location, self.target_node_type, source_node_time))
        new_edge.attach_target_node(self.network.extract_node(
            self.source_node_location, self.source_node_type, target_node_time))
        new_edge.flow = self.flows[self.number_of_edges + edge_number]
        new_edge.conversion_fun = self.conversion_fun
        new_edge.conversion_fun_params = self.conversion_fun_params
        return
    
    def build_edges(self):
        super().build_edges()
        for counter1 in range(self.number_of_edges):
            self.build_edge_opposite(counter1)
        return
    
    
    def _update_parameters(self):
        #update distance#
        self._update_distance()
        #update parameters using self.parameters_df and self.distance#
        for parameter_name, parameter in self.cost_fun_params.items():
            parameter.value = (self.parameters_df[parameter_name + r"_1"] + 
                               self.parameters_df[parameter_name + r"_2"] * self.distance)
        for parameter_name, parameter in self.conversion_fun_params.items():
            parameter.value = 1 - (self.parameters_df[parameter_name + r"_1"] + 
                               self.parameters_df[parameter_name + r"_2"] * self.distance)
        #Set Usage Parameters Based on Usage assuming 30 years operation#
        self.cost_fun_params["usage_constant"].value = (self.cost_fun_params["usage_constant"].value * 
                                                        self.network.usage_factor)
        return

