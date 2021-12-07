#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:59:27 2021

@author: aniqahsan
"""

import numpy as np
import cvxpy as cp
from .Base_Assets import *
from ..Network import *

####### Define Classes #######

class _Conventional_Generator(Asset_STEVFNs):
    """Class of Conventional Generators"""
    def __init__(self, node_location, node_type, node_times, cost_fun= False, 
                 cost_fun_params = False):
        super().__init__()
        self.node_location = node_location
        self.node_type = node_type
        self.node_times = node_times
        if cost_fun != False:
            self.cost_fun = cost_fun
        if cost_fun_params != False:
            self.cost_fun_params = cost_fun_params
        self.number_of_edges = len(node_times)
        self.flows = cp.Variable(self.number_of_edges, nonneg = True, 
                                 value = np.zeros(self.number_of_edges))
        return
        
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows[edge_number]
        return
    
    def satisfy_net_load(self):
        net_load = np.zeros(self.number_of_edges)
        for counter1 in range(self.number_of_edges):
            node_time = self.node_times[counter1]
            node = self.network.extract_node(self.node_location, self.node_type, node_time)
            net_load[counter1] = node.net_output_flows.value
        self.flows.value = net_load
        return


class _Demand_Asset(Asset_STEVFNs):
    """Class of Demand Asset"""
    def __init__(self, node_location, node_type, node_times, demand_values):
        super().__init__()
        self.node_location = node_location
        self.node_type = node_type
        self.node_times = node_times
        self.number_of_edges = len(node_times)
        self.flows = demand_values#this is a cp.Parameter
        return
    
    def build_costs(self):
        self.cost = cp.Constant(0)
        return
        
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_source_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows[edge_number]
        return

    
class _Transport_Asset(Asset_STEVFNs):
    """Class of Transport Asset"""
    def __init__(self, source_node_location, source_node_type, source_node_times,
                 target_node_location, target_node_type, target_node_times,
                 cost_fun = False, cost_fun_params = False, conversion_fun = False, 
                 conversion_fun_params = False):
        super().__init__()
        self.source_node_location = source_node_location
        self.source_node_type = source_node_type
        self.source_node_times = source_node_times
        self.target_node_location = target_node_location
        self.target_node_type = target_node_type
        self.target_node_times = target_node_times
        if cost_fun != False:
            self.cost_fun = cost_fun
        if cost_fun_params != False:
            self.cost_fun_params = cost_fun_params
        if conversion_fun != False:
            self.conversion_fun = conversion_fun
        if conversion_fun_params != False:
            self.conversion_fun_params = conversion_fun_params
        self.number_of_edges = len(source_node_times)
        self.flows = cp.Variable(self.number_of_edges, nonneg = True, 
                                 value = np.zeros(self.number_of_edges))
        return

    def build_edge(self, edge_number):
        source_node_time = self.source_node_times[edge_number]
        target_node_time = self.target_node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_source_node(self.network.extract_node(
            self.source_node_location, self.source_node_type, source_node_time))
        new_edge.attach_target_node(self.network.extract_node(
            self.target_node_location, self.target_node_type, target_node_time))
        new_edge.flow = self.flows[edge_number]
        new_edge.conversion_fun = self.conversion_fun
        new_edge.conversion_fun_params = self.conversion_fun_params
        return


class _RE_Asset(Asset_STEVFNs):
    """Class of Renewable Energy Sources """
    def __init__(self, node_location, node_type, node_times, gen_profile,
                 cost_fun= False, cost_fun_params = False):
        super().__init__()
        self.node_location = node_location
        self.node_type = node_type
        self.node_times = node_times
        self.gen_profile = gen_profile#this is a cp.Parameter
        if cost_fun != False:
            self.cost_fun = cost_fun
        if cost_fun_params != False:
            self.cost_fun_params = cost_fun_params
        self.number_of_edges = len(node_times)
        self.flows = cp.Variable(nonneg = True)#size of RE asset
        return
    
    def build_edge(self, edge_number):
        node_time = self.node_times[edge_number]
        new_edge = Edge_STEVFNs()
        self.edges += [new_edge]
        new_edge.attach_target_node(self.network.extract_node(
            self.node_location, self.node_type, node_time))
        new_edge.flow = self.flows * self.gen_profile[edge_number]
        return
    
    def get_plot_data(self):
        return self.flows.value * self.gen_profile.value


class _ESS_Asset(Multi_Asset):
    """Class for Storage"""
    def __init__(self, cost_fun=False , node_location = False, node_type_0 = False, node_type_1 = False, 
                 node_times_0 = False, node_times_1 = False, storage_cost_fun = False, storage_cost_fun_params = False, 
                 storage_conversion_fun = False, storage_conversion_fun_params = False,
                 charging_cost_fun = False, charging_cost_fun_params = False, charging_conversion_fun = False, 
                 charging_conversion_fun_params = False, discharging_cost_fun = False, discharging_cost_fun_params = False,
                 discharging_conversion_fun = False, discharging_conversion_fun_params = False):
        super().__init__(cost_fun=cost_fun , cost_fun_params=False)
        self.node_location = node_location
        self.node_type_0 = node_type_0 #this is the type of the storage, i.e. ESS for example "battery"
        self.node_type_1 = node_type_1 #this is the type of the energy that ESS charges from/ discharges to, e.g. "electricity"
        self.node_times_0 = node_times_0
        self.node_times_1 = node_times_1
        self.attach_storage(storage_cost_fun, storage_cost_fun_params, storage_conversion_fun, storage_conversion_fun_params)
        self.attach_charging(charging_cost_fun, charging_cost_fun_params, 
                             charging_conversion_fun, charging_conversion_fun_params)
        self.attach_discharging(discharging_cost_fun, discharging_cost_fun_params, 
                                discharging_conversion_fun, discharging_conversion_fun_params)
        return
    
    def attach_storage(self, cost_fun, cost_fun_params, conversion_fun, conversion_fun_params):
        my_storage_asset = _Transport_Asset(self.node_location, self.node_type_0, self.node_times_0,
                                           self.node_location, self.node_type_0, self.node_times_1,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("storage", my_storage_asset)
        return
    
    def attach_charging(self, cost_fun, cost_fun_params, conversion_fun, conversion_fun_params):
        my_storage_asset = _Transport_Asset(self.node_location, self.node_type_1, self.node_times_0,
                                           self.node_location, self.node_type_0, self.node_times_0,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("charging", my_storage_asset)
        return
    
    def attach_discharging(self, cost_fun, cost_fun_params, conversion_fun, conversion_fun_params):
        my_storage_asset = _Transport_Asset(self.node_location, self.node_type_0, self.node_times_0,
                                           self.node_location, self.node_type_1, self.node_times_0,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("discharging", my_storage_asset)
        return



