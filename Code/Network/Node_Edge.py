# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 19:19:16 2023

@author: aniq_
"""

import cvxpy as cp

class Node:
    """Node Class"""
    def __init__(self):
        self.input_edges = set()
        self.output_edges = set()
        self.eq_cons = []#Equality constraints
        self.ieq_cons = []#Inequality constraints
        self.net_output_flows_conserved = cp.Constant(0)
        self.net_output_flows_curtailed = cp.Constant(0)
        self.conserved_flows_types = []
        self.curtailed_flows_types = []
        return

class Edge:
    def __init__(self):
        self.source_node = False
        self.target_node = False
        self.flows_x = cp.Constant(0)
        self.flows_types_x = []
        self.flows_types_y = []
        return




