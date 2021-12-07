#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:09:22 2021

@author: aniqahsan
"""
from STEVFNs_Classes import *
import matplotlib.pyplot as plt


######## Functions #########

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

electricity_line_cost_fun = linear_sizing_deg_cost_fun
battery_charging_cost_fun = linear_sizing_deg_cost_fun
battery_discharging_cost_fun = linear_sizing_deg_cost_fun
battery_storage_cost_fun = linear_sizing_deg_cost_fun


    

########### Testing area #######

# Build 3 node toy network #

######## Define Parameters ###########
np.random.seed(0)
N = 3# number of nodes
T = 1000# Number of timesteps
C_G =  np.array([1.,0.8,0.6])# np.random.rand(3)#
C_G2 = np.array([0.1,0.2,0.3])*0.1# np.random.rand(3) * 0.1
C_G_max = np.array([0.1, 0.1, 0.1])
Z = np.array([[0.,1,1],[0,0,1],[0,0,0]])
V_min = np.array([0.9, 0.9, 0.9])
V_max = np.array([1.1, 1.1, 1.1])
P_D = np.array([0.1, 0.2, 0.3])
P_G_max = np.array([3.,3,3])
P_G_min = np.array([0.,0,0])
P_MAX = np.array([[0.,1,1],[0,0,1],[0,0,0]])
ALPHA = np.array([[0.,0.9,0.9],[0,0,0.9],[0,0,0]])
V0 = 100.
RE_C1 = np.array([0.5, 0.3, 0.4])*0.1

RE_profile = np.sin(np.arange(T) * 2 * np.pi / 24.0)

P_MAX = P_MAX + P_MAX.T
ALPHA = ALPHA + ALPHA.T
ALPHA_C = ALPHA * 0.01
ALPHA_C_MAX = ALPHA_C*10

ESS_storage_C_max = 0.3
ESS_storage_C = ESS_storage_C_max / (1E5)*0.0
ESS_charging_C_max = ESS_storage_C_max * 4
ESS_charging_C = ESS_charging_C_max / (8000)
ESS_discharging_C_max = ESS_storage_C_max * 2
ESS_discharging_C = ESS_discharging_C_max / (8000)


ESS_self_discharge_C = 0.99995
ESS_charging_eff_C = 0.95
ESS_discharging_eff_C = 0.95
####Build Network #####
start_time = time.time()


toy_network = Network_SETVFNs()

### build DG ###

### Add demand and DGs ###
my_locations = np.arange(N)
my_type = "electricity"
my_type_battery = "battery"
my_times = np.arange(T)
my_times_2 = np.zeros_like(my_times)
my_times_2[:-1] = my_times[1:]
my_times_2[-1] = my_times[0]
for counter1 in range(N):
    my_location = my_locations[counter1]
    #add dg
    # my_cost_params = {"sizing_constant": cp.Parameter(nonneg=1, value=C_G_max[counter1]),
    #                      "usage_constant_1": cp.Parameter(nonneg=1, value=C_G[counter1]),
    #                      "usage_constant_2": cp.Parameter(nonneg=1, value=C_G2[counter1])}
    # my_dg = Conventional_Generator(my_location, my_type, my_times, 
    #                                 conventional_generator_cost_fun, my_cost_params)
    # toy_network.add_asset(my_dg)
    # if counter1 ==0:
    #     toy_network.add_asset(my_dg)
    
    #add demand
    # my_demand_values = list(P_D[counter1] * np.random.rand(len(my_times)))
    # my_demand_values = cp.Parameter(shape = len(my_times), nonneg=1, 
    #                                 value = my_demand_values)
    # my_electrical_demand = Demand_Asset(my_location, my_type, my_times, my_demand_values)
    # toy_network.add_asset(my_electrical_demand)
    if counter1 == 0:
        my_demand_values = list(P_D[counter1] * np.random.rand(len(my_times)))
        my_demand_values = cp.Parameter(shape = len(my_times), nonneg=1, 
                                        value = my_demand_values)
        my_electrical_demand = Demand_Asset(my_location, my_type, my_times, my_demand_values)
        toy_network.add_asset(my_electrical_demand)
    
    #add RE supply
    # my_RE_profile = np.cos((np.arange(T) + counter1*4) * 2 * np.pi / 24.0)/2.0 + 0.5
    # my_RE_profile = cp.Parameter(nonneg = True, shape = T, value = my_RE_profile)
    # my_RE_cost_params = {"C1": cp.Parameter(value = RE_C1[counter1], nonneg = True)}
    # my_RE_asset = RE_Asset(my_location, my_type, my_times, my_RE_profile, 
    #                        linear_fun, my_RE_cost_params)
    # toy_network.add_asset(my_RE_asset)
    if counter1 == 1:
        my_RE_profile = np.cos((np.arange(T) + counter1*4) * 2 * np.pi / 24.0)/2.0 + 0.5
        my_RE_profile = cp.Parameter(nonneg = True, shape = T, value = my_RE_profile)
        my_RE_cost_params = {"C1": cp.Parameter(value = RE_C1[counter1], nonneg = True)}
        my_RE_asset = RE_Asset(my_location, my_type, my_times, my_RE_profile, 
                               linear_fun, my_RE_cost_params)
        toy_network.add_asset(my_RE_asset)
    
    #add Battery
    # my_battery = Multi_Asset(battery_cost_fun)
    # my_battery_storage_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_storage_C_max),
    #                                       "degradation_constant": cp.Parameter(nonneg=True, value = ESS_storage_C)}
    # my_battery_storage_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_self_discharge_C)}
    # my_battery_storage = Transport_Asset(my_location, my_type_battery, my_times, 
    #                             my_location, my_type_battery, my_times_2, battery_storage_cost_fun, 
    #                             my_battery_storage_cost_fun_params,linear_fun, my_battery_storage_conversion_fun_param)
    # my_battery.add_asset("storage", my_battery_storage)
    # my_battery_charging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_charging_C_max),
    #                                       "degradation_constant": cp.Parameter(nonneg=True, value = ESS_charging_C)}
    # my_battery_charging_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_charging_eff_C)}
    # my_battery_charging = Transport_Asset(my_location, my_type, my_times, 
    #                             my_location, my_type_battery, my_times, battery_charging_cost_fun, 
    #                             my_battery_charging_cost_fun_params,linear_fun, my_battery_charging_conversion_fun_param)
    # my_battery.add_asset("charging", my_battery_charging)
    # my_battery_discharging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C_max),
    #                                       "degradation_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C)}
    # my_battery_discharging_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_discharging_eff_C)}
    # my_battery_discharging = Transport_Asset(my_location, my_type_battery, my_times, 
    #                             my_location, my_type, my_times, battery_discharging_cost_fun, 
    #                             my_battery_discharging_cost_fun_params,linear_fun, my_battery_discharging_conversion_fun_param)
    # my_battery.add_asset("discharging", my_battery_discharging)
    # toy_network.add_asset(my_battery)
    if counter1 == 0:
        my_battery = Multi_Asset(battery_cost_fun)
        my_battery_storage_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_storage_C_max),
                                          "degradation_constant": cp.Parameter(nonneg=True, value = ESS_storage_C)}
        my_battery_storage_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_self_discharge_C)}
        my_battery_storage = Transport_Asset(my_location, my_type_battery, my_times, 
                                my_location, my_type_battery, my_times_2, battery_storage_cost_fun, 
                                my_battery_storage_cost_fun_params,linear_fun, my_battery_storage_conversion_fun_param)
        my_battery.add_asset("storage", my_battery_storage)
        my_battery_charging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_charging_C_max),
                                          "degradation_constant": cp.Parameter(nonneg=True, value = ESS_charging_C)}
        my_battery_charging_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_charging_eff_C)}
        my_battery_charging = Transport_Asset(my_location, my_type, my_times, 
                                my_location, my_type_battery, my_times, battery_charging_cost_fun, 
                                my_battery_charging_cost_fun_params,linear_fun, my_battery_charging_conversion_fun_param)
        my_battery.add_asset("charging", my_battery_charging)
        my_battery_discharging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C_max),
                                          "degradation_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C)}
        my_battery_discharging_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = ESS_discharging_eff_C)}
        my_battery_discharging = Transport_Asset(my_location, my_type_battery, my_times, 
                                my_location, my_type, my_times, battery_discharging_cost_fun, 
                                my_battery_discharging_cost_fun_params,linear_fun, my_battery_discharging_conversion_fun_param)
        my_battery.add_asset("discharging", my_battery_discharging)
        toy_network.add_asset(my_battery)
    

### Add electricity lines ###
for counter1 in range(2):
    my_location = my_locations[counter1]
    for counter2 in range(2):
        if counter1 == counter2:
            continue
        my_location_2 = my_locations[counter2]
        my_cost_params_2 = {"sizing_constant": cp.Parameter(nonneg=True, value = ALPHA_C_MAX[counter1, counter2]),
                            "degradation_constant": cp.Parameter(nonneg=True, value = ALPHA_C[counter1, counter2])}
        my_conversion_fun_params_2= {"C1": cp.Parameter(
            value = ALPHA[counter1, counter2], nonneg =True)}
        my_electricity_line = Transport_Asset(my_location, my_type, my_times, 
                                my_location_2, my_type, my_times, electricity_line_cost_fun, 
                                my_cost_params_2,linear_fun, my_conversion_fun_params_2)
        toy_network.add_asset(my_electricity_line)



end_time = time.time()
print("Time taken to build network = ", end_time - start_time)


###### Build Problem ####
start_time = time.time()

toy_network.build_problem()

end_time = time.time()
print("Time taken to build problem = ", end_time - start_time)



### Solve Problem ###
my_tol = 1E-8
start_time = time.time()

toy_network.solve_problem()
# toy_network.problem.solve(solver = cp.ECOS, verbose = True, abstol = my_tol, reltol = my_tol, feastol = my_tol)

end_time = time.time()
print("Time taken to solve = ", end_time - start_time)

print("Cost Value = ", toy_network.problem.value)

print("Asset Sizes:")
print(toy_network.assets[1].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[2].flows.value.max())
print(toy_network.assets[4].flows.value.max())
# print(toy_network.assets[3].flows.value)
# print(toy_network.assets[5].flows.value)

### Change and Solve Problem ###
my_tol = 1E-8
toy_network.assets[2].cost_fun_params["C1"].value = toy_network.assets[2].cost_fun_params["C1"].value * 1.0
toy_network.assets[2].gen_profile.value = toy_network.assets[2].gen_profile.value * (0.9 + 0.2 * np.random.rand(T))
# toy_network.assets[4].cost_fun_params["degradation_constant"].value = toy_network.assets[4].cost_fun_params["degradation_constant"].value * 0.8
start_time = time.time()

toy_network.solve_problem()
# toy_network.problem.solve(solver = cp.ECOS, verbose = True, abstol = my_tol, reltol = my_tol, feastol = my_tol)

end_time = time.time()
print("Time taken to re-solve = ", end_time - start_time)

print("New Cost Value = ", toy_network.problem.value)

print("Asset Sizes:")
print(toy_network.assets[1].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[2].flows.value.max())
print(toy_network.assets[4].flows.value.max())
# print(toy_network.assets[3].flows.value)
# print(toy_network.assets[5].flows.value)