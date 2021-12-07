#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 09:54:49 2021

@author: aniqahsan
"""

import cvxpy as cp

def linear_fun(flow, params):
    return params["C1"] * flow


def quad_fun(flow, params):
    return params["C1"] * flow + params["C2"] * cp.power(flow, 2)


def conventional_generator_cost_fun(flows, params):
    sizing_constant = params["sizing_constant"]
    usage_constant_1 = params["usage_constant_1"]
    usage_constant_2 = params["usage_constant_2"]
    return sizing_constant * cp.max(flows) + usage_constant_1 * cp.sum(flows) + usage_constant_2 * cp.sum(cp.power(flows,2))

def linear_sizing_deg_cost_fun(flows, params):
    sizing_constant = params["sizing_constant"]
    degradation_constant = params["degradation_constant"]
    sizing_cost = sizing_constant * cp.max(flows)
    degradation_cost = degradation_constant * cp.sum(flows)
    return cp.maximum(sizing_cost, degradation_cost)

def battery_cost_fun(cost_dict, params):
    cost_storage = cost_dict["storage"]
    cost_charging = cost_dict["charging"]
    cost_discharging = cost_dict["discharging"]
    return cp.maximum(cost_storage, cost_charging, cost_discharging)

def hydrogen_cost_fun(cost_dict, params):
    cost_storage = cost_dict["storage"]
    cost_charging = cost_dict["charging"]
    cost_discharging = cost_dict["discharging"]
    return cp.sum([cost_storage, cost_charging, cost_discharging])

electricity_line_cost_fun = linear_sizing_deg_cost_fun
battery_charging_cost_fun = linear_sizing_deg_cost_fun
battery_discharging_cost_fun = linear_sizing_deg_cost_fun
battery_storage_cost_fun = linear_sizing_deg_cost_fun
hydrogen_charging_cost_fun = linear_sizing_deg_cost_fun
hydrogen_discharging_cost_fun = linear_sizing_deg_cost_fun
hydrogen_storage_cost_fun = linear_sizing_deg_cost_fun
hydrogen_transport_cost_fun = linear_sizing_deg_cost_fun
hydrogen_transport_cost_fun = linear_sizing_deg_cost_fun
electric_heater_cost_fun = linear_sizing_deg_cost_fun
hydrogen_heater_cost_fun = linear_sizing_deg_cost_fun