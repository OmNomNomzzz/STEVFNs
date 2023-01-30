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
        self.conserved_flows_types = set()
        self.curtailed_flows_types = set()
        self.net_output_flows_conserved = cp.Constant(0)
        self.net_output_flows_curtailed = cp.Constant(0)
        self.eq_cons = []#Equality constraints
        self.ieq_cons = []#Inequality constraints
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

class Edge:
    conversion_fun = staticmethod(lambda flows_x ,params: flows_x)
    def __init__(self):
        self.source_node = False
        self.target_node = False
        self.flows_x = cp.Constant(0)
        self.flows_types_x = ["NULL"]
        self.flows_types_y = ["NULL"]
        self.conversion_fun_params = dict()
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
    
    def build_flows_y(self):
        self.flows_y = self.conversion_fun(self.flows_x, self.conversion_fun_params)
        return
    
    def build_flows_dictionary(self):
        self.flows_x_dict = {self.flows_types_x[i] : self.flows_x[i] for i in range(len(self.flows_types_x))}
        self.flows_y_dict = {self.flows_types_y[i] : self.flows_y[i] for i in range(len(self.flows_types_y))}
        return
    
    def build(self):
        self.build_flows_y()
        self.build_flows_dictionary()
        return




