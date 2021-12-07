#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 18:02:21 2021

@author: aniqahsan
"""

# from .Network import *
# from .Assets import *
# from .Plotting import *
# from .STEVFNs_Functions import *
# from .STEVFNs_Parameters import *

# ### Import Packages ###

# import os
# import pandas as pd
# import cvxpy as cp
# from Network import Node_STEVFNs
# from Assets.Assets_Dictionary import ASSET_DICT

# class Network_STEVFNs:
#     """This is the NETWORK class of STEVFNs"""
#     def __init__(self):
#         self.lat_lon_df = pd.DataFrame(columns = ["Lat", "Lon"])
#         self.assets = []
#         self.costs = []
#         self.constraints = []
#         self.nodes_df = pd.Series([], index = pd.MultiIndex.from_tuples([], names = ["location", "type", "time"]))
#         self.base_folder = os.path.dirname(os.path.dirname(__file__))
#         return
    
#     def generate_node(self, node_location, node_type, node_time):
#         new_node = Node_STEVFNs()
#         node_df = pd.Series([new_node], 
#                             index = pd.MultiIndex.from_tuples([(node_location, node_type, node_time)], 
#                                     names = ["location", "type", "time"]))
#         self.nodes_df = self.nodes_df.append(node_df)
#         return
    
#     def extract_node(self, node_location, node_type, node_time):
#         if not((node_location, node_type, node_time) in self.nodes_df.index):
#             self.generate_node(node_location, node_type, node_time)
#         return self.nodes_df[node_location, node_type, node_time]
    
#     def add_asset(self, asset):
#         asset.network = self
#         self.assets += [asset]
#         return
    
#     def build_assets(self):
#         self.costs = []
#         for counter1 in range(len(self.assets)):
#             self.assets[counter1].build()
#             self.costs += [self.assets[counter1].cost]
    
#     def build_constraints(self):
#         self.constraints = []
#         for counter1 in range(self.nodes_df.size):
#             node = self.nodes_df.iloc[counter1]
#             node.build_constraints()
#             self.constraints += node.constraints
#         return
    
#     def build_cost(self):
#         self.cost = cp.sum(self.costs)
#         return
    
#     def build_problem(self):
#         self.build_assets()
#         self.build_cost()
#         self.build_constraints()
#         self.objective = cp.Minimize(self.cost)
#         self.problem = cp.Problem(self.objective, self.constraints)
#         return
    
#     def solve_problem(self):
#         # self.problem.solve()
#         # self.problem.solve(warm_start=True)# This can sometimes use OSQP solver that sometimes gives errors.
#         self.problem.solve(solver = cp.ECOS, warm_start=True)
#         # self.problem.solve(solver = cp.SCS, warm_start=True)
#         return
    
#     def satisfy_net_loads(self):
#         for counter1 in range(len(self.assets)):
#             asset = self.assets[counter1]
#             if type(asset).__name__ == "Conventional_Generator":
#                 asset.satisfy_net_load()
#         return
    
#     def generate_asset(self, asset_structure):
#         asset_class_name = asset_structure["Asset_Class"]
#         my_asset = ASSET_DICT[asset_class_name]()
#         my_asset.define_structure(asset_structure)
#         return my_asset
    
#     def build(self, network_structure_df):
#         #Generate Assets#
#         for counter1 in range(len(network_structure_df)):
#             my_asset = self.generate_asset(network_structure_df.iloc[counter1])
#             self.add_asset(my_asset)
#         #Build Problem#
#         self.build_problem()
#         return
    
#     def update(self, location_parameters_df, asset_parameters_df):
#         #Update Location lat,lon#
#         for counter1 in range(len(location_parameters_df)):
#             location = location_parameters_df.iloc[counter1]["Location"]
#             self.lat_lon_df.loc[location, "Lat"] = location_parameters_df.iloc[counter1]["Lat"]
#             self.lat_lon_df.loc[location, "Lon"] = location_parameters_df.iloc[counter1]["Lon"]
#         #update Assets#
#         for counter1 in range(len(asset_parameters_df)):
#             asset_number = asset_parameters_df.iloc[counter1]["Asset_Number"]
#             asset_type = asset_parameters_df.iloc[counter1]["Asset_Type"]
#             self.assets[asset_number].update(asset_type)
#         return
    
#     def plot(self):
#         #Plot some stuff#
#         return
