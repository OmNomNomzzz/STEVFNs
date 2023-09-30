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


class CO2_Budget_Asset(Asset_STEVFNs):
    """Class of Renewable Energy Sources """
    asset_name = "CO2_Budget"
    source_node_type = "NULL"
    source_node_time = 0
    target_node_type = "CO2_Budget"
    target_node_time = 0
    period = 1
    transport_time = 0
    
    @staticmethod
    def conversion_fun(flows, params):
        return params["maximum_budget"]
    
    def __init__(self):
        super().__init__()
        self.conversion_fun_params = {"maximum_budget": cp.Parameter(nonneg=True)}
        return
        
    
    def define_structure(self, asset_structure):
        self.source_node_location = 0
        self.source_node_times = np.array([self.source_node_time])
        self.target_node_location = 0
        self.number_of_edges = 1
        self.target_node_times = np.array([self.target_node_time])
        self.flows = cp.Constant(np.zeros(self.number_of_edges))
        return
    
    def get_plot_data(self):
        return self.flows.value
    
    
    def component_size(self):
        # Returns size of component (i.e. asset) #
        return (self.edges[0].target_node.net_output_flows + self.conversion_fun_params["maximum_budget"]).value
    