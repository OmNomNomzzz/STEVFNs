#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 14:32:48 2021

@author: aniqahsan
"""
############ Import packages #######
import numpy as np
import scipy as sp
import cvxpy as cp
import pandas as pd
import matplotlib.pyplot as plt
import time


####### Define Classes #######

class Node:
    """Basic Node Class"""
    def __init__(self):
        self.input_edges = set()
        self.output_edges = set()
        return
    
    def attach_input_edge(self, input_edge):
        self.input_edges.add(input_edge)
        if input_edge.target_node == self:
            return
        input_edge.attach_target_node(self)
        return
    
    def attach_output_edge(self, output_edge):
        self.output_edges.add(output_edge)
        if output_edge.source_node == self:
            return
        output_edge.attach_source_node(self)
        return


class Edge:
    """Basic Directed Edge Class"""
    def __init__(self):
        self.source_node = False
        self.target_node = False
        return
    
    def attach_source_node(self, source_node):
        self.source_node = source_node
        if source_node == False:
            return
        if self in source_node.output_edges:
            return
        source_node.attach_output_edge(self)
        return
    
    def attach_target_node(self, target_node):
        self.target_node = target_node
        if target_node == False:
            return
        if self in target_node.input_edges:
            return
        target_node.attach_input_edge(self)
        return


class Edge_STEVFNs(Edge):
    """STEVFNs Edge Class"""
    def __init__(self):
        super().__init__()
        self.flow = cp.Constant(0)
        self.conversion_fun_params = dict()
        self.conversion_fun = lambda flow,params:flow
        return
    
    def extract_flow(self):
        return self.conversion_fun(self.flow, self.conversion_fun_params)


class Node_STEVFNs(Node):
    def __init__(self):
        super().__init__()
        self.curtailment = True
        self.net_output_flows = cp.Constant(0)
        self.constraints = []
        return
    
    def build_constraints(self):
        total_output_flows = self.calculate_total_output_flows()
        total_input_flows = self.calculate_total_input_flows()
        if (total_input_flows.sign == "ZERO"):
            if (total_output_flows.sign == "ZERO"):
                self.net_output_flows = cp.Constant(0)
                self.constraints = []
                return
            else:
                self.net_output_flows = total_output_flows
        else:
            if (total_output_flows.sign == "ZERO"):
                self.net_output_flows = -total_input_flows
            else:
                self.net_output_flows = total_output_flows - total_input_flows
        if self.curtailment == True:
            self.constraints = [self.net_output_flows <= 0]
        else:
            self.constraints = [self.net_output_flows == 0]
        return
    
    def calculate_total_output_flows(self):
        total_output_flows = cp.Constant(0)
        for output_edge in self.output_edges:
            if total_output_flows.sign == "ZERO":
                total_output_flows = output_edge.flow
            else:
                total_output_flows += output_edge.flow
        return total_output_flows
    
    def calculate_total_input_flows(self):
        total_input_flows = cp.Constant(0)
        for input_edge in self.input_edges:
            if total_input_flows.sign == "ZERO":
                total_input_flows = input_edge.extract_flow()
            else:
                total_input_flows += input_edge.extract_flow()
        return total_input_flows
    

class Network_SETVFNs:
    """This is the NETWORK calss of STEVFNs"""
    def __init__(self):
        self.assets = []
        self.costs = []
        self.constraints = []
        self.cost = cp.Constant(0)
        self.nodes_df = pd.Series([], index = pd.MultiIndex.from_tuples([], names = ["location", "type", "time"]))
        return
    
    def generate_node(self, node_location, node_type, node_time):
        new_node = Node_STEVFNs()
        node_df = pd.Series([new_node], 
                            index = pd.MultiIndex.from_tuples([(node_location, node_type, node_time)], 
                                    names = ["location", "type", "time"]))
        self.nodes_df = self.nodes_df.append(node_df)
        # self.add_node(new_node)
        return
    
    def extract_node(self, node_location, node_type, node_time):
        if not((node_location, node_type, node_time) in self.nodes_df.index):
            self.generate_node(node_location, node_type, node_time)
        return self.nodes_df[node_location, node_type, node_time]
    
    def add_asset(self, asset):
        asset.network = self
        self.assets += [asset]
        return
    
    def build_assets(self):
        self.costs = []
        for counter1 in range(len(self.assets)):
            # self.assets[counter1].build_edges()
            # self.assets[counter1].build_cost()
            self.assets[counter1].build()
            self.costs += [self.assets[counter1].cost]
    
    def build_constraints(self):
        self.constraints = []
        for counter1 in range(self.nodes_df.size):
            node = self.nodes_df.iloc[counter1]
            node.build_constraints()
            self.constraints += node.constraints
        return
    
    def build_cost(self):
        self.cost = cp.sum(self.costs)
        return
    
    def build_problem(self):
        self.build_assets()
        self.build_cost()
        self.build_constraints()
        self.objective = cp.Minimize(self.cost)
        self.problem = cp.Problem(self.objective, self.constraints)
        return
    
    def solve_problem(self):
        # self.problem.solve()
        # self.problem.solve(warm_start=True)# This can sometimes use OSQP solver that sometimes gives errors.
        self.problem.solve(solver = cp.ECOS, warm_start=True)
        # self.problem.solve(solver = cp.SCS, warm_start=True)
        return
    
    def satisfy_net_loads(self):
        for counter1 in range(len(self.assets)):
            asset = self.assets[counter1]
            if type(asset).__name__ == "Conventional_Generator":
                asset.satisfy_net_load()
        return


class Asset_STEVFNs:
    """Base Class of assets"""
    def __init__(self):
        self.network = False
        self.edges = []
        self.cost = cp.Constant(0)
        self.number_of_edges = 0
        self.flows = cp.Constant(0)
        self.cost_fun = False
        self.cost_fun_params = dict()
        return
    
    def build_cost(self):
        if (self.cost_fun == False) or (self.flows.sign == "ZERO"):
            self.cost = cp.Constant(0)
            return
        self.cost = self.cost_fun(self.flows, self.cost_fun_params)
        return
    
    def build_edge(self, node_number):
        return
    
    def build_edges(self):
        for counter1 in range(self.number_of_edges):
            self.build_edge(counter1)
        return
    
    def get_plot_data(self):
        return self.flows.value
    
    def build(self):
        self.build_edges()
        self.build_cost()
        return
            
        
class Conventional_Generator(Asset_STEVFNs):
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


class Demand_Asset(Asset_STEVFNs):
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

    
class Transport_Asset(Asset_STEVFNs):
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


class RE_Asset(Asset_STEVFNs):
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


class Multi_Asset(Asset_STEVFNs):
    """Class that contains multiple assets"""
    def __init__(self, cost_fun=False , cost_fun_params=False):
        super().__init__()
        self.assets_dictionary = dict()
        self.costs_dictionary = dict()
        if cost_fun != False:
            self.cost_fun = cost_fun
        if cost_fun_params != False:
            self.cost_fun_params = cost_fun_params
        return
 
    def build_edges(self):
        for asset_name, asset in self.assets_dictionary.items():
            asset.network = self.network
            asset.build_edges()
        return
    
    def build_cost(self):
        if self.cost_fun == False:
            self.cost = cp.Constant(0)
            return
        for asset_name, asset in self.assets_dictionary.items():
            asset.build_cost()
            self.costs_dictionary[asset_name] = asset.cost
        self.cost = self.cost_fun(self.costs_dictionary, self.cost_fun_params)
        return
    
    def add_asset(self, asset_name, asset):
        self.assets_dictionary[asset_name] = asset
        return
    
    def get_plot_data(self):
        flow_dictionary = dict()
        for asset_name, asset in self.assets_dictionary.items():
            flow_dictionary[asset_name] = asset.get_plot_data()
        return flow_dictionary


class ESS_Asset(Multi_Asset):
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
        my_storage_asset = Transport_Asset(self.node_location, self.node_type_0, self.node_times_0,
                                           self.node_location, self.node_type_0, self.node_times_1,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("storage", my_storage_asset)
        return
    
    def attach_charging(self, cost_fun, cost_fun_params, conversion_fun, conversion_fun_params):
        my_storage_asset = Transport_Asset(self.node_location, self.node_type_1, self.node_times_0,
                                           self.node_location, self.node_type_0, self.node_times_0,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("charging", my_storage_asset)
        return
    
    def attach_discharging(self, cost_fun, cost_fun_params, conversion_fun, conversion_fun_params):
        my_storage_asset = Transport_Asset(self.node_location, self.node_type_0, self.node_times_0,
                                           self.node_location, self.node_type_1, self.node_times_0,
                                           cost_fun, cost_fun_params, conversion_fun, conversion_fun_params)
        self.add_asset("discharging", my_storage_asset)
        return


class stackplot_artist:
    """Class that takes assets and draws a stackplot """
    def __init__(self):
        self.flows_dictionary = dict()
        return
    
    def add_asset(self, asset_name, asset):
        self.flows_dictionary[asset_name] = asset.get_plot_data()
        return
    
    def set_times(self, times):
        self.times = times
        return
    
    def plot(self, show = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        if not(hasattr(self, "times")):
            self.times = np.arange(self.flows_dictionary[list(self.flows_dictionary)[0]].size)
        self.ax.stackplot(self.times, self.flows_dictionary.values(), labels = self.flows_dictionary.keys())
        self.ax.legend()
        if show == 1:
            plt.show()
        return


class bar_chart_artist:
    """Class that takes assets and draws a bar graph"""
    def __init__(self, title = None):
        self.bars_dictionary = dict()
        self.group_names_list = []
        if title != None:
            self.title = title
        return
    
    def add_asset(self, asset_name, asset):
        if asset_name in self.bars_dictionary:
            self.bars_dictionary[asset_name] += [asset.flows.value.max()]
        else:
            self.bars_dictionary[asset_name] = [asset.flows.value.max()]
        return
    
    def add_group(self, group_name):
        self.group_names_list += [group_name] # list of group names
        return
    
    def plot(self, show =1, show_legend = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        width = 0.35
        asset_names_list = list(self.bars_dictionary.keys())
        N_assets = len(asset_names_list)
        N_groups = len(self.group_names_list)
        x = np.arange(N_groups)
        width = 1.0/(N_assets + 1)
        bars_list = []
        for counter1 in range(N_assets):
            asset_name = asset_names_list[counter1]
            bars_list += [self.ax.bar(x + width * (counter1-(N_assets-1)*0.5), 
                                      self.bars_dictionary[asset_name][:N_groups],
                                      width,
                                      label = asset_name)]
            # self.ax.bar_label(bars_list[counter1], padding=3)
            
        ### add some labels ###
        if hasattr(self, "title"):
            self.ax.set_title(self.title)
        self.ax.set_ylabel("Asset Size")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.group_names_list)
        self.ax.legend()
        
        self.fig.tight_layout()
        plt.show()
        return
        

class line_graph_artist:
    """Class that takes assets and draws a line graph"""
    def __init__(self):
        self.flows_dictionary = dict()
        return
    
    def add_asset(self, asset_name, asset):
        self.flows_dictionary[asset_name] = asset.get_plot_data()
        return
    
    def set_times(self, times):
        self.times = times
        return
    
    def plot(self, show = 1, show_legend = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        if not(hasattr(self, "times")):
            self.times = np.arange(self.flows_dictionary[list(self.flows_dictionary)[0]].size)
        for flow_name, flow in self.flows_dictionary.items():
            self.ax.plot(self.times, flow, label = flow_name)
        if show_legend == 1:
            self.ax.legend()
        if show == 1:
            plt.show()
        return


class multiple_artists:
    """Class that takes assets and draws multiple graphs"""
    def __init__(self):
        self.artist_dictionary = dict()
        return
    
    def add_artist(self, artist_name, artist):
        self.artist_dictionary[artist_name] = artist
        return
    
    def plot(self, figure_title = None, show_legend = 1):
        N_artists = len(self.artist_dictionary)
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots(len(self.artist_dictionary), 1, figsize=(6.4, 4.8))
        artist_names = list(self.artist_dictionary.keys())
        for counter1 in range(N_artists):
            artist_name = artist_names[counter1]
            artist = self.artist_dictionary[artist_name]
            artist.fig = self.fig
            artist.ax = self.ax[counter1]
            artist.plot(show = 0, show_legend = 1)
            artist.ax.set_title(artist_name)
        if figure_title != None:
            self.fig.suptitle(figure_title, y=1.03)
        self.fig.tight_layout()
        plt.show()
        return


