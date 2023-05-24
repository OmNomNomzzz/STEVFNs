# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 17:41:01 2022
@author: aniq_
"""

# from __init__.py import *
import numpy as np
from ..Plotting import bar_chart_artist, stackplot_artist, twin_line_artist




def plot_asset_sizes(my_network, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the size of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_sizes_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_sizes_array)):
        asset_sizes_array[counter1] = my_network.assets[counter1].asset_size()
    og_df["Asset_Size"] = asset_sizes_array
    max_asset_size = np.max(asset_sizes_array)
    # Set minimum asset size to plot
    min_asset_size = max_asset_size * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Size"] >= min_asset_size
    og_df = og_df[con1]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_size = my_network.assets[asset_number].asset_size()
            # check if asset is too small
            if asset_size < min_asset_size:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_size = my_network.assets[asset_number].asset_size()
                # check if asset is too small
                if asset_size < min_asset_size:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_size]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Size (GWh)"
    my_artist.title = "Size of Assets in the System by Location and Location Pair \n Scenario: " + my_network.scenario_name
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return


def plot_asset_costs(my_network, bar_width = 1.0, bar_spacing = 3.0):
    # Plots the cost of assets in the system #
    
    # Find maximum asset size so that we can remove assets that are too small, i.e. size zero.
    og_df = my_network.system_structure_df.copy()
    asset_costs_array = np.zeros(og_df.shape[0])
    for counter1 in range(len(asset_costs_array)):
        asset_costs_array[counter1] = my_network.assets[counter1].cost.value
    og_df["Asset_Cost"] = asset_costs_array
    max_asset_cost = np.max(asset_costs_array)
    # Set minimum asset size to plot
    min_asset_cost = max_asset_cost * 1E-3
    # Remove all assets that are too small
    con1 = og_df["Asset_Cost"] >= min_asset_cost
    og_df = og_df[con1]
    
    # initialize bar data dictionary for plotting assets of a system#
    bar_data_dict = dict()
    asset_class_list = np.sort(og_df["Asset_Class"].unique())
    for counter1 in range(len(asset_class_list)):
        bar_data = dict({
            "x" : [],
            "height" : [],
            })
        bar_data_dict.update({
            asset_class_list[counter1] : bar_data
            })
    # Initialize x ticks dictionary
    x_ticks_data_dict = dict({
        "ticks" : [],
        "labels" : []
        })
    
    #fill bar data dictionary for assets at a location i.e. loc_1 = loc_2
    loc_1_array = np.sort(og_df["Location_1"].unique())
    x_current = 0.0
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        loc_2 = loc_1
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        con2 = t_df1["Location_2"] == loc_2
        t_df2 = t_df1[con2]
        x_tick_0 = x_current
        for counter2 in range(t_df2.shape[0]):
            asset_data = t_df2.iloc[counter2]
            #add size of asset in bar_data
            asset_number = asset_data["Asset_Number"]
            asset_cost = my_network.assets[asset_number].cost.value
            # check if asset is too small
            if asset_cost < min_asset_cost:
                continue
            bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
            #add x location of asset in bar_data
            bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
            #move to next asset
            x_current += bar_width
        #check if any asset was added to that location pair
        if x_current == x_tick_0:
            continue
        #add entry to x_ticks
        x_ticks_data_dict["labels"] += ["(" + str(loc_1) + ")"]
        x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
        #move to next location
        x_current += bar_spacing
    
    
    #fill bar data dictionary for assets between locations
    
    for counter1 in range(len(loc_1_array)):
        loc_1 = loc_1_array[counter1]
        con1 = og_df["Location_1"] == loc_1
        t_df1 = og_df[con1]
        loc_2_array = np.sort(t_df1["Location_2"].unique())
        for counter2 in range(len(loc_2_array)):
            loc_2 = loc_2_array[counter2]
            #check if asset is between locations
            if loc_2 == loc_1:
                continue
            con2 = t_df1["Location_2"] == loc_2
            t_df2 = t_df1[con2]
            x_tick_0 = x_current
            for counter3 in range(t_df2.shape[0]):
                asset_data = t_df2.iloc[counter3]
                #add size of asset in bar_data
                asset_number = asset_data["Asset_Number"]
                asset_cost = my_network.assets[asset_number].cost.value
                # check if asset is too small
                if asset_cost < min_asset_cost:
                    continue
                bar_data_dict[asset_data["Asset_Class"]]["height"] += [asset_cost]
                #add x location of asset in bar_data
                bar_data_dict[asset_data["Asset_Class"]]["x"] += [x_current + bar_width/2]
                #move to next asset
                x_current += bar_width
            #check if any asset was added to that location pair
            if x_current == x_tick_0:
                continue
            #add entry to x_ticks
            x_ticks_data_dict["labels"] += ["(" + str(loc_1) + "," + str(loc_2) + ")"]
            x_ticks_data_dict["ticks"] += [(x_tick_0 + x_current)/2]
            #move to next location
            x_current += bar_spacing
    
    #Make a bar chart artist and plot
    my_artist = bar_chart_artist()
    my_artist.bar_data_dict = bar_data_dict
    my_artist.x_ticks_data_dict = x_ticks_data_dict
    my_artist.ylabel = "Asset Cost (Billion USD)"
    my_artist.title = "Cost of Assets in the System by Location and Location Pair \n Scenario: " + my_network.scenario_name
    my_artist.text_data = {"x": 0.65, "y": 0.67, "s": "Total Cost = " + f"{my_network.cost.value: .5}" + " Bil USD"}
    my_artist.plot(bar_width = bar_width, bar_spacing = bar_spacing)
    return


def plot_SG_EL_output_flows(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "EL_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
        
    
    #Add flows and times for EL demand
    component_name = "EL_Demand"
    con2 = tdf1["Asset_Class"] == "EL_Demand"
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Charging
    asset_name = "BESS"
    component_name = "BESS_Charging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Charging"]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL to HTH
    component_name = "EL_to_HTH"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["EL_Demand"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy out of EL node at Singapore"
    my_artist.plot()
    return


def plot_SG_EL_input_flows(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "EL_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_network.assets[asset_number].source_node_times
        times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Discharging
    asset_name = "BESS"
    component_name = "BESS_Discharging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_asset = my_network.assets[asset_number]
    my_component = my_asset.assets_dictionary["Discharging"]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["BESS_Discharging"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy into EL node at Singapore"
    my_artist.plot()
    return


def plot_single_RE_EL_output_flows(my_network, RE_loc):
    #Plots the EL output flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport for locations less than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        component_name = "EL_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "EL_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Charging
    asset_name = "BESS"
    component_name = "BESS_Charging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Charging"]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["BESS_Charging"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy out of EL node at RE Location " + str(RE_loc)
    my_artist.plot()
    return


def plot_RE_EL_output_flows(my_network):
    #Plots the output EL flows for all RE locations. This is only for SG case study for my DPhil Thesis
    for counter1 in range(3):
        plot_single_RE_EL_output_flows(my_network, counter1+1)
    return


def plot_single_RE_EL_input_flows(my_network, RE_loc):
    #Plots the input EL flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport for locations less than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        component_name = "EL_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "EL_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Discharging
    asset_name = "BESS"
    component_name = "BESS_Disharging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Discharging"]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    ### Add flows and times for RE_PV ####
    component_name = "RE_PV"
    con2 = tdf1["Asset_Class"] == "RE_PV"
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = (my_component.flows * my_component.gen_profile).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.node_times
    times_dictionary[component_name] = component_times
    
    
    ### Add flows and times for RE_WIND ####
    component_name = "RE_WIND"
    con2 = tdf1["Asset_Class"] == "RE_WIND"
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = (my_component.flows * my_component.gen_profile).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.node_times
    times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["BESS_Disharging"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy into EL node at RE Location " + str(RE_loc)
    my_artist.plot()
    return


def plot_RE_EL_input_flows(my_network):
    #Plots the input EL flows for all RE locations. This is only for SG case study for my DPhil Thesis
    for counter1 in range(3):
        plot_single_RE_EL_input_flows(my_network, counter1 + 1)
    return


def plot_SG_NH3_output_flows(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 to HTH
    component_name = "NH3_to_HTH"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport assets
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "NH3_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_EL"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = flows_dictionary["NH3_to_EL"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_to_EL"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia out of NH3 node at Singapore"
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_SG_NH3_input_flows(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    temp_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    component_flows = np.zeros_like(temp_flows)
    component_flows[1:] = temp_flows[:-1]
    component_flows[0] = temp_flows[-1]
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_network.assets[asset_number].source_node_times
    times_dictionary[component_name] = component_times
    
    
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "NH3_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = flows_dictionary["EL_to_NH3"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["EL_to_NH3"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia into NH3 node at Singapore"
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_single_RE_NH3_output_flows(my_network, RE_loc):
    #Plots the EL output flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        component_name = "NH3_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_EL"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_to_EL"]
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "NH3_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_EL"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_to_EL"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_Storage"]/24
    my_artist.ylabel = "NH3 Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia out of NH3 node at RE Location " + str(RE_loc)
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Moved in Space or Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_RE_NH3_output_flows(my_network):
    for counter1 in range(3):
        plot_single_RE_NH3_output_flows(my_network, counter1 + 1)
    return


def plot_single_RE_NH3_input_flows(my_network, RE_loc):
    #Plots the input EL flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    temp_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    component_flows = np.zeros_like(temp_flows)
    component_flows[1:] = temp_flows[:-1]
    component_flows[0] = temp_flows[-1]
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_network.assets[asset_number].source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        component_name = "NH3_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_Storage"]
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "NH3_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_Storage"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_Storage"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia into NH3 node at RE Location " + str(RE_loc)
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Moved in Space or Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_RE_NH3_input_flows(my_network):
    for counter1 in range(3):
        plot_single_RE_NH3_input_flows(my_network, counter1 + 1)
    return


def plot_all(my_network):
    plot_asset_sizes(my_network)
    plot_asset_costs(my_network)
    plot_SG_EL_input_flows(my_network)
    plot_SG_EL_output_flows(my_network)
    plot_RE_EL_input_flows(my_network)
    plot_RE_EL_output_flows(my_network)
    plot_SG_NH3_input_flows(my_network)
    plot_SG_NH3_output_flows(my_network)
    plot_RE_NH3_input_flows(my_network)
    plot_RE_NH3_output_flows(my_network)
    return


############ Plots for BAU Scenario ######

def plot_SG_EL_input_flows_BAU(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "EL_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_network.assets[asset_number].source_node_times
        times_dictionary[component_name] = component_times
    
    
    # #Add flows and times for BESS Discharging
    asset_name = "BESS"
    component_name = "BESS_Discharging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_asset = my_network.assets[asset_number]
    my_component = my_asset.assets_dictionary["Discharging"]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    # #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["EL_Transport_1"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy into EL node at Singapore"
    my_artist.plot()
    return


def plot_SG_EL_output_flows_BAU(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        component_name = "EL_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
        
    
    #Add flows and times for EL demand
    component_name = "EL_Demand"
    con2 = tdf1["Asset_Class"] == "EL_Demand"
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.node_times
    times_dictionary[component_name] = component_times
    
    
    # #Add flows and times for BESS Charging
    asset_name = "BESS"
    component_name = "BESS_Charging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Charging"]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    # #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL to HTH
    component_name = "EL_to_HTH"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["EL_Demand"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy out of EL node at Singapore"
    my_artist.plot()
    return


def plot_single_RE_EL_input_flows_BAU(my_network, RE_loc):
    #Plots the input EL flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport for locations less than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        component_name = "EL_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "EL_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Discharging
    asset_name = "BESS"
    component_name = "BESS_Disharging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Discharging"]
    component_flows = my_component.conversion_fun(
        my_component.flows, 
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    if RE_loc == 3:
        #Add flows and times for NH3 to EL
        component_name = "NH3_to_EL"
        con2 = tdf1["Asset_Class"] == component_name
        asset_number = tdf1[con2]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        component_flows = my_component.conversion_fun(
            my_component.flows, 
            my_component.conversion_fun_params).value
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    ### Add flows and times for RE_PV ####
    component_name = "RE_PV"
    con2 = tdf1["Asset_Class"] == "RE_PV"
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = (my_component.flows * my_component.gen_profile).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.node_times
    times_dictionary[component_name] = component_times
    
    if RE_loc != 2:
        ### Add flows and times for RE_WIND ####
        component_name = "RE_WIND"
        con2 = tdf1["Asset_Class"] == "RE_WIND"
        asset_number = tdf1[con2]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        component_flows = (my_component.flows * my_component.gen_profile).value
        flows_dictionary[component_name] = component_flows
        component_times = my_component.node_times
        times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["BESS_Disharging"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy into EL node at RE Location " + str(RE_loc)
    my_artist.plot()
    return


def plot_RE_EL_input_flows_BAU(my_network):
    #Plots the input EL flows for all RE locations. This is only for SG case study for my DPhil Thesis
    for counter1 in range(3):
        plot_single_RE_EL_input_flows_BAU(my_network, counter1 + 1)
    return


def plot_single_RE_EL_output_flows_BAU(my_network, RE_loc):
    #Plots the EL output flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport for locations less than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    # for counter1 in range(RE_loc):
    for counter1 in range(1):
        component_name = "EL_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "EL_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "EL_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    #Add flows and times for BESS Charging
    asset_name = "BESS"
    component_name = "BESS_Charging"
    con2 = tdf1["Asset_Class"] == asset_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number].assets_dictionary["Charging"]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    if RE_loc == 3:
        #Add flows and times for EL to NH3
        component_name = "EL_to_NH3"
        con2 = tdf1["Asset_Class"] == component_name
        asset_number = tdf1[con2]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        component_flows = my_component.flows.value
        flows_dictionary[component_name] = component_flows
        component_times = my_component.source_node_times
        times_dictionary[component_name] = component_times
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["BESS_Charging"]/24
    my_artist.ylabel = "Electricity Flow (GWh)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Electrical Energy out of EL node at RE Location " + str(RE_loc)
    my_artist.plot()
    return


def plot_RE_EL_output_flows_BAU(my_network):
    #Plots the output EL flows for all RE locations. This is only for SG case study for my DPhil Thesis
    for counter1 in range(3):
        plot_single_RE_EL_output_flows_BAU(my_network, counter1+1)
    return


def plot_SG_NH3_input_flows_BAU(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    #Add flows and times for EL Transport assets
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    temp_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    component_flows = np.zeros_like(temp_flows)
    component_flows[1:] = temp_flows[:-1]
    component_flows[0] = temp_flows[-1]
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_network.assets[asset_number].source_node_times
    times_dictionary[component_name] = component_times
    
    
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        if counter1 !=2:
            continue
        component_name = "NH3_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = flows_dictionary["EL_to_NH3"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["EL_to_NH3"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia into NH3 node at Singapore"
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_SG_NH3_output_flows_BAU(my_network):
    #Plots the EL flows for loc_0, i.e. Singapore. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == 0
    tdf1 = my_network.system_structure_df[con1]
    
    
    # #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 to HTH
    component_name = "NH3_to_HTH"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport assets
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3):
        if counter1 !=2:
            continue
        component_name = "NH3_Transport_" + str(counter1 + 1)
        con3 = tdf2["Location_2"] == counter1 + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_HTH"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_to_HTH"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_to_HTH"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia out of NH3 node at Singapore"
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Stored or Moved in Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_single_RE_NH3_input_flows_BAU(my_network, RE_loc):
    #Plots the input EL flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for EL to NH3
    component_name = "EL_to_NH3"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    temp_flows = my_component.conversion_fun(
        my_component.flows,
        my_component.conversion_fun_params).value
    component_flows = np.zeros_like(temp_flows)
    component_flows[1:] = temp_flows[:-1]
    component_flows[0] = temp_flows[-1]
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_network.assets[asset_number].source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        if counter1 !=0:
            continue
        component_name = "NH3_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_Storage"]
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "NH3_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.conversion_fun(
            my_component.flows,
            my_component.conversion_fun_params).value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.target_node_times
        final_component_flows = np.zeros_like(flows_dictionary["EL_to_NH3"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_Storage"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_Storage"]/24
    my_artist.ylabel = "Ammonia Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia into NH3 node at RE Location " + str(RE_loc)
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Moved in Space or Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_RE_NH3_input_flows_BAU(my_network):
    for counter1 in range(3):
        plot_single_RE_NH3_input_flows_BAU(my_network, counter1 + 1)
    return


def plot_single_RE_NH3_output_flows_BAU(my_network, RE_loc):
    #Plots the EL output flows for RE_loc. This is only for SG case study for my DPhil Thesis
    #Initialize dictionary to store flows and times
    flows_dictionary = dict()
    twin_flows_dictionary = dict()
    times_dictionary = dict()
    
    
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    
    
    #Add flows and times for NH3 to EL
    component_name = "NH3_to_EL"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for NH3 Storage
    component_name = "NH3_Storage"
    con2 = tdf1["Asset_Class"] == component_name
    asset_number = tdf1[con2]["Asset_Number"].iloc[0]
    my_component = my_network.assets[asset_number]
    component_flows = my_component.flows.value
    twin_flows_dictionary[component_name] = component_flows
    component_times = my_component.source_node_times
    times_dictionary[component_name] = component_times
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_2"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(RE_loc):
        if counter1 != 0:
            continue
        component_name = "NH3_Transport_" + str(counter1)
        con3 = tdf2["Location_1"] == counter1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[int(total_length/2):]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_EL"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_to_EL"]
    
    
    #Add flows and times for EL Transport for locations more than RE_loc
    con1 = my_network.system_structure_df["Location_1"] == RE_loc
    tdf1 = my_network.system_structure_df[con1]
    con2 = tdf1["Asset_Class"] == "NH3_Transport"
    tdf2 = tdf1[con2]
    for counter1 in range(3-RE_loc):
        component_name = "NH3_Transport_" + str(counter1 + RE_loc + 1)
        con3 = tdf2["Location_2"] == counter1 + RE_loc + 1
        asset_number = tdf2[con3]["Asset_Number"].iloc[0]
        my_component = my_network.assets[asset_number]
        total_component_flows = my_component.flows.value
        total_length = len(total_component_flows)
        component_flows = total_component_flows[:int(total_length/2)]
        component_times = my_component.source_node_times
        final_component_flows = np.zeros_like(flows_dictionary["NH3_to_EL"])
        for counter2 in range(len(component_times)):
            final_component_flows[int(component_times[counter2])] = component_flows[counter2]
        twin_flows_dictionary[component_name] = final_component_flows
        times_dictionary[component_name] = times_dictionary["NH3_to_EL"]
    
    
    my_artist = stackplot_artist()
    my_artist.flows_dictionary = flows_dictionary
    my_artist.times = times_dictionary["NH3_Storage"]/24
    my_artist.ylabel = "NH3 Flow (Gg)"
    my_artist.xlabel = "Time (Days)"
    my_artist.title = "Flow of Ammonia out of NH3 node at RE Location " + str(RE_loc)
    # my_artist.plot()
    
    my_twin_artist = twin_line_artist()
    my_twin_artist.flows_dictionary = twin_flows_dictionary
    my_twin_artist.ylabel = "Ammonia Moved in Space or Time (Gg)"
    my_twin_artist.attach_artist(my_artist)
    my_twin_artist.plot()
    return


def plot_RE_NH3_output_flows_BAU(my_network):
    for counter1 in range(3):
        plot_single_RE_NH3_output_flows_BAU(my_network, counter1 + 1)
    return