#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:36:27 2021

@author: aniqahsan
"""

import cvxpy as cp
from ..Base_Assets import Asset_STEVFNs


class EL_to_H2_Asset(Asset_STEVFNs):
    """Class of EL to H2 conversion asset"""
    asset_name = "EL_to_H2"
    source_node_type = "EL"
    target_node_type = "H2"
    
    @staticmethod
    def cost_fun(flows, params):
        sizing_constant = params["sizing_constant"]
        # usage_constant_1 = params["usage_constant_1"]
        # return sizing_constant * cp.max(flows) + usage_constant_1 * cp.sum(flows)
        return sizing_constant * cp.max(flows)
    
    @staticmethod
    def conversion_fun(flows, params):
        conversion_factor = params["conversion_factor"]
        return conversion_factor * flows
    
    def __init__(self):
        super().__init__()
        self.cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True),
                          "usage_constant_1": cp.Parameter(nonneg=True)}
        self.conversion_fun_params = {"conversion_factor": cp.Parameter(nonneg=True)}
        return
    
    def define_structure(self, asset_structure):
        super().define_structure(asset_structure)
        self.target_node_location = self.source_node_location
        self.flows = cp.Variable(self.number_of_edges, nonneg = True)
        return
    
    def _update_parameters(self):
        super()._update_parameters()
        #Set Usage Parameters Based on Usage assuming 30 years operation#
        self.cost_fun_params["usage_constant_1"].value = (self.cost_fun_params["usage_constant_1"].value * 
                                                          self.network.usage_factor)
        return

