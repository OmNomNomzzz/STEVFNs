#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 18:09:22 2021

@author: aniqahsan
"""
from STEVFNs_Classes import *
from STEVFNs_Functions import *
from STEVFNs_Parameters import *


    

########### Testing area #######

# Build 3 node toy network #

####Build Network #####
start_time = time.time()


toy_network = Network_SETVFNs()



for counter1 in range(N):
    my_location = my_locations[counter1]
    #add conventional generator
    my_CG_cost_params = {"sizing_constant": cp.Parameter(nonneg=1, value=C_G_max[counter1]),
                          "usage_constant_1": cp.Parameter(nonneg=1, value=C_G[counter1]),
                          "usage_constant_2": cp.Parameter(nonneg=1, value=C_G2[counter1])}
    my_cg = Conventional_Generator(my_location, my_type, my_times, 
                                    conventional_generator_cost_fun, my_CG_cost_params)
    toy_network.add_asset(my_cg)
    # if counter1 ==0:
    #     toy_network.add_asset(my_dg)
    
    #add electrical demand
    my_electricity_demand = Demand_Asset(my_location, my_type, my_times, my_electricity_demand_parameters_list[counter1])
    toy_network.add_asset(my_electricity_demand)
    # if counter1 == 0:
    #     toy_network.add_asset(my_electricity_demand)
    
    #add HTH demand
    my_HTH_demand_values = list(P_D[counter1] * np.random.rand(len(my_times)))
    my_HTH_demand_values = cp.Parameter(shape = len(my_times), nonneg=1, 
                                    value = my_HTH_demand_values)
    my_HTH_demand = Demand_Asset(my_location, my_type_HTH, my_times, my_HTH_demand_values)
    toy_network.add_asset(my_HTH_demand)
    # if counter1 == 0:
    #     toy_network.add_asset(my_HTH_demand)
    
    #add Solar supply
    my_solar_gen_profile = solar_gen_profile_list[counter1]
    my_solar_cost_params = {"C1": cp.Parameter(value = RE_C1[counter1], nonneg = True)}
    my_solar_asset = RE_Asset(my_location, my_type, my_times, my_solar_gen_profile, 
                            linear_fun, my_solar_cost_params)
    toy_network.add_asset(my_solar_asset)
    # if counter1 == 0:
    #     toy_network.add_asset(my_solar_asset)
    
    #add Wind supply
    my_wind_gen_profile = wind_gen_profile_list[counter1]
    my_wind_cost_params = {"C1": cp.Parameter(value = RE_C1[counter1], nonneg = True)}
    my_wind_asset = RE_Asset(my_location, my_type, my_times, my_wind_gen_profile, 
                           linear_fun, my_wind_cost_params)
    toy_network.add_asset(my_wind_asset)
    # if counter1 == 0:
    #     toy_network.add_asset(my_wind_asset)
    
    #add Battery
    my_battery = ESS_Asset(battery_cost_fun, my_location, my_type_battery, my_type, my_times, 
                            my_times_2, battery_storage_cost_fun, my_battery_storage_cost_fun_params, linear_fun, 
                            my_battery_storage_conversion_fun_params, battery_charging_cost_fun, 
                            my_battery_charging_cost_fun_params, linear_fun, my_battery_charging_conversion_fun_params,
                            battery_discharging_cost_fun, my_battery_discharging_cost_fun_params, linear_fun,
                            my_battery_discharging_conversion_fun_params )
    
    toy_network.add_asset(my_battery)
    
    #add Hydrogen    
    my_hydrogen = ESS_Asset(hydrogen_cost_fun, my_location, my_type_hydrogen, my_type, my_times, 
                            my_times_2, hydrogen_storage_cost_fun, my_hydrogen_storage_cost_fun_params, linear_fun, 
                            my_hydrogen_storage_conversion_fun_params, hydrogen_charging_cost_fun, 
                            my_hydrogen_charging_cost_fun_params, linear_fun, my_hydrogen_charging_conversion_fun_params,
                            hydrogen_discharging_cost_fun, my_hydrogen_discharging_cost_fun_params, linear_fun,
                            my_hydrogen_discharging_conversion_fun_params )
    
    toy_network.add_asset(my_hydrogen)
    
    #add Electric heater
    my_electric_heater = Transport_Asset(my_location, my_type, my_times, my_location, my_type_HTH, my_times, 
                                         electric_heater_cost_fun, my_electric_heater_cost_fun_params, linear_fun, 
                                         my_electric_heater_conversion_fun_params )
    toy_network.add_asset(my_electric_heater)
    
    #add Hydrogen heater
    my_hydrogen_heater = Transport_Asset(my_location, my_type_hydrogen, my_times, my_location, my_type_HTH, my_times, 
                                         hydrogen_heater_cost_fun, my_hydrogen_heater_cost_fun_params, linear_fun, 
                                         my_hydrogen_heater_conversion_fun_params )
    toy_network.add_asset(my_hydrogen_heater)
    

### Add electricity lines ###
for counter1 in range(N):
    my_location = my_locations[counter1]
    for counter2 in range(N):
        if counter1 == counter2:
            continue
        my_location_2 = my_locations[counter2]
        #add electricity line
        electricity_line_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = ALPHA_C_MAX[counter1, counter2]),
                            "degradation_constant": cp.Parameter(nonneg=True, value = ALPHA_C[counter1, counter2])}
        electricity_line_conversion_fun_params= {"C1": cp.Parameter(
            value = ALPHA[counter1, counter2], nonneg =True)}
        my_electricity_line = Transport_Asset(my_location, my_type, my_times, 
                                my_location_2, my_type, my_times, electricity_line_cost_fun, 
                                electricity_line_cost_fun_params,linear_fun, electricity_line_conversion_fun_params)
        toy_network.add_asset(my_electricity_line)
        
        #add hydrogen transport
        my_hydrogen_transport_cost_fun_params = {"sizing_constant": cp.Parameter(nonneg=True, value = H2_transport_C_max),
                                                 "degradation_constant": cp.Parameter(nonneg=True, value = H2_transport_C)}
        my_hydrogen_transport_conversion_fun_param = {"C1": cp.Parameter(nonneg=True, value = H2_transport_eff_C)}
        my_hydrogen_transport = Transport_Asset(my_location, my_type_hydrogen, my_hydrogen_transport_times, 
                                my_location_2, my_type_hydrogen, my_hydrogen_transport_times_2, hydrogen_transport_cost_fun, 
                                my_hydrogen_transport_cost_fun_params,linear_fun, my_hydrogen_transport_conversion_fun_param)
        toy_network.add_asset(my_hydrogen_transport)


end_time = time.time()
print("Time taken to build network = ", end_time - start_time)


###### Build Problem ####
start_time = time.time()

toy_network.build_problem()

end_time = time.time()
print("Time taken to build problem = ", end_time - start_time)



### Solve Problem ###
# my_tol = 1E-8
start_time = time.time()

toy_network.solve_problem()
# toy_network.problem.solve(solver = cp.ECOS, verbose = True, abstol = my_tol, reltol = my_tol, feastol = my_tol)

end_time = time.time()
print("Time taken to solve = ", end_time - start_time)

print("Cost Value = ", toy_network.problem.value)

print("Solar Sizes:")
print(toy_network.assets[3].flows.value)
print(toy_network.assets[12].flows.value)
print(toy_network.assets[21].flows.value)
print("Wind Sizes:")
print(toy_network.assets[4].flows.value)
print(toy_network.assets[13].flows.value)
print(toy_network.assets[22].flows.value)
print("Battery storage sizes:")
print(toy_network.assets[5].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[14].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[23].assets_dictionary["storage"].flows.value.max())
print("Hydrogen storage sizes:")
print(toy_network.assets[6].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[15].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[24].assets_dictionary["storage"].flows.value.max())


my_multiple_artists_2 = multiple_artists()

electricity_node_locations_1 = [31, 27, 29]
electricity_node_locations_2 = [35, 37, 33]
electricity_node_names_1 = [2,1,1]
electricity_node_names_2 = [3,3,2]

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Conventional Generator", toy_network.assets[0 + counter1 * 9])
    my_line_graph_artist.add_asset("Solar Energy", toy_network.assets[3 + counter1 * 9])
    my_line_graph_artist.add_asset("Wind Energy", toy_network.assets[4 + counter1 * 9])
    my_line_graph_artist.add_asset("Battery", toy_network.assets[5 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("electricity line Node "+ str(electricity_node_names_1[counter1]), 
                                   toy_network.assets[electricity_node_locations_1[counter1]])
    my_line_graph_artist.add_asset("electricity line Node "+str(electricity_node_names_2[counter1]),
                                   toy_network.assets[electricity_node_locations_2[counter1]])
    my_line_graph_artist.plot()
    my_multiple_artists_2.add_artist("Node "+str(counter1+1), my_line_graph_artist)

# my_multiple_artists_2.plot()


my_multiple_artists_3 = multiple_artists()

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Hydrogen Storage", toy_network.assets[6 + counter1 * 9].assets_dictionary["storage"])
    
    my_multiple_artists_3.add_artist("Node "+str(counter1+1), my_line_graph_artist)

my_multiple_artists_3.plot()

my_bar_chart_artist = bar_chart_artist(title = "Base Scenario")

for counter1 in range(N):
    my_bar_chart_artist.add_group("Node " + str(counter1 + 1))
    my_bar_chart_artist.add_asset("Solar", toy_network.assets[3 + counter1*9])
    my_bar_chart_artist.add_asset("Wind", toy_network.assets[4 + counter1*9])
    my_bar_chart_artist.add_asset("Battery", toy_network.assets[5 + counter1*9].assets_dictionary["storage"])
    my_bar_chart_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1*9].assets_dictionary["storage"])

my_bar_chart_artist.plot()

###### Change and Solve Problem ######

### Reduce solar cost ###
print("\n Reduce Solar Cost and slightly change profile")
# my_tol = 1E-8
toy_network.assets[3].cost_fun_params["C1"].value = toy_network.assets[3].cost_fun_params["C1"].value * 0.7
toy_network.assets[3].gen_profile.value = toy_network.assets[3].gen_profile.value * (0.9 + 0.2 * np.random.rand(T))
# toy_network.assets[0].cost_fun_params["usage_constant_1"].value = toy_network.assets[0].cost_fun_params["usage_constant_1"].value * 0.1
start_time = time.time()

toy_network.solve_problem()
# toy_network.problem.solve(solver = cp.ECOS, verbose = True, abstol = my_tol, reltol = my_tol, feastol = my_tol)

end_time = time.time()
print("Time taken to re-solve = ", end_time - start_time)

print("New Cost Value = ", toy_network.problem.value)

print("Solar Sizes:")
print(toy_network.assets[3].flows.value)
print(toy_network.assets[12].flows.value)
print(toy_network.assets[21].flows.value)
print("Wind Sizes:")
print(toy_network.assets[4].flows.value)
print(toy_network.assets[13].flows.value)
print(toy_network.assets[22].flows.value)
print("Battery storage sizes:")
print(toy_network.assets[5].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[14].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[23].assets_dictionary["storage"].flows.value.max())
print("Hydrogen storage sizes:")
print(toy_network.assets[6].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[15].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[24].assets_dictionary["storage"].flows.value.max())


my_multiple_artists_2 = multiple_artists()

electricity_node_locations_1 = [31, 27, 29]
electricity_node_locations_2 = [35, 37, 33]
electricity_node_names_1 = [2,1,1]
electricity_node_names_2 = [3,3,2]

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Conventional Generator", toy_network.assets[0 + counter1 * 9])
    my_line_graph_artist.add_asset("Solar Energy", toy_network.assets[3 + counter1 * 9])
    my_line_graph_artist.add_asset("Wind Energy", toy_network.assets[4 + counter1 * 9])
    my_line_graph_artist.add_asset("Battery", toy_network.assets[5 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("electricity line Node "+ str(electricity_node_names_1[counter1]), 
                                   toy_network.assets[electricity_node_locations_1[counter1]])
    my_line_graph_artist.add_asset("electricity line Node "+str(electricity_node_names_2[counter1]),
                                   toy_network.assets[electricity_node_locations_2[counter1]])
    my_line_graph_artist.plot()
    my_multiple_artists_2.add_artist("Node "+str(counter1+1), my_line_graph_artist)

# my_multiple_artists_2.plot()


my_multiple_artists_3 = multiple_artists()

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Hydrogen Storage", toy_network.assets[6 + counter1 * 9].assets_dictionary["storage"])
    
    my_multiple_artists_3.add_artist("Node "+str(counter1+1), my_line_graph_artist)

my_multiple_artists_3.plot()

my_bar_chart_artist = bar_chart_artist(title = "Cheaper, intermittent Node 1 Solar")

for counter1 in range(N):
    my_bar_chart_artist.add_group("Node " + str(counter1 + 1))
    my_bar_chart_artist.add_asset("Solar", toy_network.assets[3 + counter1*9])
    my_bar_chart_artist.add_asset("Wind", toy_network.assets[4 + counter1*9])
    my_bar_chart_artist.add_asset("Battery", toy_network.assets[5 + counter1*9].assets_dictionary["storage"])
    my_bar_chart_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1*9].assets_dictionary["storage"])

my_bar_chart_artist.plot()

### Reduce hydrogen cost ###
print("\n Reduce Hydrogen Cost")
# my_tol = 1E-8
toy_network.assets[6].assets_dictionary["storage"].cost_fun_params["sizing_constant"].value = toy_network.assets[6].assets_dictionary["storage"].cost_fun_params["sizing_constant"].value * 0.7
toy_network.assets[6].assets_dictionary["storage"].cost_fun_params["degradation_constant"].value = toy_network.assets[6].assets_dictionary["storage"].cost_fun_params["degradation_constant"].value * 0.7
toy_network.assets[6].assets_dictionary["charging"].cost_fun_params["sizing_constant"].value = toy_network.assets[6].assets_dictionary["charging"].cost_fun_params["sizing_constant"].value * 0.7
toy_network.assets[6].assets_dictionary["charging"].cost_fun_params["degradation_constant"].value = toy_network.assets[6].assets_dictionary["charging"].cost_fun_params["degradation_constant"].value * 0.7
toy_network.assets[6].assets_dictionary["discharging"].cost_fun_params["sizing_constant"].value = toy_network.assets[6].assets_dictionary["discharging"].cost_fun_params["sizing_constant"].value * 0.7
toy_network.assets[6].assets_dictionary["discharging"].cost_fun_params["degradation_constant"].value = toy_network.assets[6].assets_dictionary["discharging"].cost_fun_params["degradation_constant"].value * 0.7

start_time = time.time()

toy_network.solve_problem()
# toy_network.problem.solve(solver = cp.ECOS, verbose = True, abstol = my_tol, reltol = my_tol, feastol = my_tol)

end_time = time.time()
print("Time taken to re-solve = ", end_time - start_time)

print("New Cost Value = ", toy_network.problem.value)

print("Solar Sizes:")
print(toy_network.assets[3].flows.value)
print(toy_network.assets[12].flows.value)
print(toy_network.assets[21].flows.value)
print("Wind Sizes:")
print(toy_network.assets[4].flows.value)
print(toy_network.assets[13].flows.value)
print(toy_network.assets[22].flows.value)
print("Battery storage sizes:")
print(toy_network.assets[5].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[14].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[23].assets_dictionary["storage"].flows.value.max())
print("Hydrogen storage sizes:")
print(toy_network.assets[6].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[15].assets_dictionary["storage"].flows.value.max())
print(toy_network.assets[24].assets_dictionary["storage"].flows.value.max())


my_multiple_artists_2 = multiple_artists()

electricity_node_locations_1 = [31, 27, 29]
electricity_node_locations_2 = [35, 37, 33]
electricity_node_names_1 = [2,1,1]
electricity_node_names_2 = [3,3,2]

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Conventional Generator", toy_network.assets[0 + counter1 * 9])
    my_line_graph_artist.add_asset("Solar Energy", toy_network.assets[3 + counter1 * 9])
    my_line_graph_artist.add_asset("Wind Energy", toy_network.assets[4 + counter1 * 9])
    my_line_graph_artist.add_asset("Battery", toy_network.assets[5 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1 * 9].assets_dictionary["discharging"])
    my_line_graph_artist.add_asset("electricity line Node "+ str(electricity_node_names_1[counter1]), 
                                   toy_network.assets[electricity_node_locations_1[counter1]])
    my_line_graph_artist.add_asset("electricity line Node "+str(electricity_node_names_2[counter1]),
                                   toy_network.assets[electricity_node_locations_2[counter1]])
    my_line_graph_artist.plot()
    my_multiple_artists_2.add_artist("Node "+str(counter1+1), my_line_graph_artist)

# my_multiple_artists_2.plot()


my_multiple_artists_3 = multiple_artists()

for counter1 in range(N):
    my_line_graph_artist = line_graph_artist()
    my_line_graph_artist.add_asset("Hydrogen Storage", toy_network.assets[6 + counter1 * 9].assets_dictionary["storage"])
    
    my_multiple_artists_3.add_artist("Node "+str(counter1+1), my_line_graph_artist)

my_multiple_artists_3.plot(figure_title = "Hydrogen Storage")



my_bar_chart_artist = bar_chart_artist(title = "Cheaper Hydrogen")

for counter1 in range(N):
    my_bar_chart_artist.add_group("Node " + str(counter1 + 1))
    my_bar_chart_artist.add_asset("Solar", toy_network.assets[3 + counter1*9])
    my_bar_chart_artist.add_asset("Wind", toy_network.assets[4 + counter1*9])
    my_bar_chart_artist.add_asset("Battery", toy_network.assets[5 + counter1*9].assets_dictionary["storage"])
    my_bar_chart_artist.add_asset("Hydrogen", toy_network.assets[6 + counter1*9].assets_dictionary["storage"])

my_bar_chart_artist.plot()




# plt.plot(toy_network.problem.variables()[8].value, label = "electric heater")
# plt.plot(toy_network.problem.variables()[9].value, label = "hydrogen heater")
# plt.legend()
# plt.show()
# plt.plot(toy_network.problem.variables()[5].value)
# plt.show()



### Plot some results ###

# my_stackplot_artist_1 = stackplot_artist()
# my_stackplot_artist_1.add_asset("Conventional Generator", toy_network.assets[0])
# my_stackplot_artist_1.add_asset("Renewable Energy", toy_network.assets[3])
# my_stackplot_artist_1.add_asset("Battery", toy_network.assets[4].assets_dictionary["discharging"])
# my_stackplot_artist_1.add_asset("Hydrogen", toy_network.assets[5].assets_dictionary["discharging"])
# my_stackplot_artist_1.add_asset("electricity line Node 1", toy_network.assets[28])
# my_stackplot_artist_1.add_asset("electricity line Node 2", toy_network.assets[32])

# my_stackplot_artist_1.plot()


# my_line_graph_artist_1 = line_graph_artist()
# my_line_graph_artist_1.add_asset("Conventional Generator", toy_network.assets[0])
# my_line_graph_artist_1.add_asset("Renewable Energy", toy_network.assets[3])
# my_line_graph_artist_1.add_asset("Battery", toy_network.assets[4].assets_dictionary["discharging"])
# my_line_graph_artist_1.add_asset("Hydrogen", toy_network.assets[5].assets_dictionary["discharging"])
# my_line_graph_artist_1.add_asset("electricity line Node 1", toy_network.assets[28])
# my_line_graph_artist_1.add_asset("electricity line Node 2", toy_network.assets[32])

# my_line_graph_artist_1.plot()

# my_multiple_artists_1 = multiple_artists()
# my_multiple_artists_1.add_artist("Stackplot", my_stackplot_artist_1)
# my_multiple_artists_1.add_artist("Line Graph", my_line_graph_artist_1)

# my_multiple_artists_1.plot()