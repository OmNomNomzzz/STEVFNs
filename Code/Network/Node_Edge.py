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
        self.net_output_flows = cp.Constant(0)
        self.eq_cons = []#Equality constraints
        self.ieq_cons = []#Inequality constraints
        self.net_output_flows_conserved = dict()
        self.net_output_flows_curtailed = dict()
        return

class Edge:
    def __init__(self):
        self.source_node = False
        self.target_node = False
        self.x_flows = dict()
        self.y_flows = dict()
        return




