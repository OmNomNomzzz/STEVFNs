#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 11:17:12 2021

@author: aniqahsan
"""

import cvxpy as cp

####### Define Classes #######

class __Node:
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


class __Edge:
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


class Edge_STEVFNs(__Edge):
    """STEVFNs Edge Class"""
    conversion_fun = staticmethod(lambda flow,params:flow)
    def __init__(self):
        super().__init__()
        self.flow = cp.Constant(0)
        self.conversion_fun_params = dict()
        return
    
    def extract_flow(self):
        return self.conversion_fun(self.flow, self.conversion_fun_params)


class Node_STEVFNs(__Node):
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
    
