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
    source_note_type = "NULL"
    target_node_type = "CO2_Budget"
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
        self.source_node_times = np.arange(asset_structure["Start_Time"], 
                                           asset_structure["End_Time"], 
                                           self.period)
        self.target_node_location = 0
        self.target_node_times = np.arange(asset_structure["Start_Time"] + self.transport_time, 
                                           asset_structure["End_Time"] + self.transport_time, 
                                           self.period)
        self.number_of_edges = len(self.source_node_times)
        self.flows = cp.Constant(np.zeros(self.number_of_edges))
        return
    
    def get_plot_data(self):
        return self.flows.value * self.gen_profile.value
    
    
    def component_size(self):
        # Returns size of component (i.e. asset) #
        return self.conversion_fun_params["maximum_budget"].value
    