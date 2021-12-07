#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 10:01:15 2021

@author: aniqahsan
"""

import numpy as np
import scipy as sp
import cvxpy as cp
import pandas as pd
import time



###### Define Functions ########
def load_solar_wind_profile(lat, lon, folder, RE_TYPE):
    """This function reads file and returns df with hourly RE output in W/Wp """
    filename = folder + RE_TYPE + r"/lat" + str(lat) + r"/" + RE_TYPE + r"_lat" + str(lat) + r"_lon" + str(lon) + r".csv"
    profile = np.loadtxt(filename)
    return profile


####### Load Files #######
data_folder = r"/Users/aniqahsan/Documents/Oxford_PhD/STEVFNs/Data/"


# #load network structure file
# network_structure_filename = data_folder + r"Scenario/Toy_Network_3_Node/Network_Structure/Network_Structure.csv"
# network_structure_df = pd.read_csv(network_structure_filename)

# #load network parameters file
# network_parameters_filename = data_folder + r"Scenario/Toy_Network_3_Node/Network_Parameters/Base_Parameters.csv"

#load electricity demand
electricity_demand_filename = data_folder + r"SG/demand/electricity/2019.csv"
electricity_demand_df = pd.read_csv(electricity_demand_filename) #electrical power demand in Watts

#load solar supply
solar_wind_folder = data_folder + r"WORLD/"
lat = 0.5 * 0
lon = 0.625 * 1
solar_df = load_solar_wind_profile(lat, lon, solar_wind_folder, "PVOUT")

#load wind supply
wind_df = load_solar_wind_profile(lat, lon, solar_wind_folder, "WINDOUT")


######## Define Parameters ###########
np.random.seed(0)
N = 3# number of nodes
T = 24 * 4# Number of timesteps
location_lat_lon_array = np.zeros((N,2))
for counter1 in range(N):
    location_lat_lon_array[counter1] = [0.5* 60 * (counter1-1), 0.625 * 100 * (counter1-1)]



### Build Electricity Demand Profiles ###
my_electricity_demand_parameters_list = []
for counter1 in range(N):
    my_electricity_demand_parameters_list += [cp.Parameter(shape = T, nonneg=1)]
    my_electricity_demand_values = np.array(electricity_demand_df[electricity_demand_df.columns[0]][
        counter1*T:(counter1+1)*T])
    my_electricity_demand_values = my_electricity_demand_values * 1E-9 * 1.0 #Convert from W to GWh
    my_electricity_demand_parameters_list[-1].value = my_electricity_demand_values


### Build solar and wind supply profiles ###
solar_gen_profile_list = []
wind_gen_profile_list = []
for counter1 in range(N):
    my_solar_gen_profile_array = load_solar_wind_profile(location_lat_lon_array[counter1,0], 
                                                location_lat_lon_array[counter1,1], solar_wind_folder, "PVOUT")[:T]
    solar_gen_profile_list += [cp.Parameter(nonneg = True, shape = T, value = my_solar_gen_profile_array)]
    my_wind_gen_profile_array = load_solar_wind_profile(location_lat_lon_array[counter1,0], 
                                                location_lat_lon_array[counter1,1], solar_wind_folder, "WINDOUT")[:T]
    wind_gen_profile_list += [cp.Parameter(nonneg = True, shape = T, value = my_wind_gen_profile_array)]

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
ALPHA_C = ALPHA * 0.1
ALPHA_C_MAX = ALPHA_C*10

ESS_storage_C_max = 0.3 * 0.1
ESS_storage_C = ESS_storage_C_max / (1E5)*0.0
ESS_charging_C_max = ESS_storage_C_max * 4
ESS_charging_C = ESS_charging_C_max / (8000)
ESS_discharging_C_max = ESS_storage_C_max * 2
ESS_discharging_C = ESS_discharging_C_max / (8000)
ESS_self_discharge_C = 0.99995
ESS_charging_eff_C = 0.95
ESS_discharging_eff_C = 0.95

H2_storage_C_max = 0.01
H2_storage_C = H2_storage_C_max / (1E5)*0.0
H2_charging_C_max = H2_storage_C_max * 4
H2_charging_C = H2_charging_C_max / (20000)
H2_discharging_C_max = H2_charging_C_max * 1
H2_discharging_C = H2_discharging_C_max / (20000)
H2_transport_C_max = 0.0
H2_transport_C = 1E-7
H2_self_discharge_C = 0.99995
H2_charging_eff_C = 0.7
H2_discharging_eff_C = 0.7
H2_transport_eff_C = 0.8



my_locations = np.arange(N)
my_type = "electricity"
my_type_battery = "battery"
my_type_hydrogen = "hydrogen"
my_type_HTH = "HTH"
my_times = np.arange(T)
my_times_2 = np.zeros_like(my_times)
my_times_2[:-1] = my_times[1:]
my_times_2[-1] = my_times[0]
my_hydrogen_transport_times = np.arange(0,T,24*1)
my_hydrogen_transport_times_2 = my_hydrogen_transport_times + 8
my_hydrogen_transport_times_2 = my_hydrogen_transport_times_2 % T


### Set CG Parameters ###


### Set Battery Parameters ###
my_battery_storage_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_storage_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = ESS_storage_C)}
my_battery_storage_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = ESS_self_discharge_C)}
my_battery_charging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_charging_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = ESS_charging_C)}
my_battery_charging_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = ESS_charging_eff_C)}
my_battery_discharging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = ESS_discharging_C)}
my_battery_discharging_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = ESS_discharging_eff_C)}



### Set Hydorgen Parameters ###
my_hydrogen_storage_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = H2_storage_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = H2_storage_C)}
my_hydrogen_storage_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = H2_self_discharge_C)}
my_hydrogen_charging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = H2_charging_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = H2_charging_C)}
my_hydrogen_charging_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = H2_charging_eff_C)}
my_hydrogen_discharging_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = H2_discharging_C_max),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = H2_discharging_C)}
my_hydrogen_discharging_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = H2_discharging_eff_C)}


### Set Electric heater Parameters ###
my_electric_heater_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = 0.01),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = 0.001)}
my_electric_heater_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = 1.0)}


### Set Hydrogen heater Parameters ###
my_hydrogen_heater_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = 0.01),
                                      "degradation_constant": cp.Parameter(nonneg=True, value = 0.001)}
my_hydrogen_heater_conversion_fun_params = {"C1": cp.Parameter(nonneg=True, value = 1.0)}