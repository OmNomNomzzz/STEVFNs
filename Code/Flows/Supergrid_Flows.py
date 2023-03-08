#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 10:03:55 2023

@author: laorie4253
"""

import pandas as pd

        

def export_AUT_Flows(my_network):
    
    flows = pd.DataFrame()
    ### Unmet demand asset
    demand = pd.DataFrame(my_network.assets[3].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM"])
    
    ### BESS ###
    BESS_ch = pd.DataFrame(my_network.assets[2].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging"])
    BESS_disch = pd.DataFrame(my_network.assets[2].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging"])

    ### RE ###
    PV = pd.DataFrame(my_network.assets[0].get_plot_data(), columns = ['PV'])
    Wind = pd.DataFrame(my_network.assets[1].get_plot_data(), columns = ['Wind'])
    
    ### Export to .csv in case study folder
    flows = pd.concat ([flows, demand, BESS_ch, BESS_disch, PV, Wind], axis=1)
    return(flows)
    
def export_Xlinks_Flows(my_network):

    flows = pd.DataFrame()
    demand_0 = pd.DataFrame(my_network.assets[3].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM_GB"])
    demand_1 = pd.DataFrame(my_network.assets[7].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM_loc1"])

    BESS_ch_0 = pd.DataFrame(my_network.assets[2].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging_GB"])
    BESS_disch_0 = pd.DataFrame(my_network.assets[2].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging_GB"])
    BESS_ch_1 = pd.DataFrame(my_network.assets[6].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging_loc1"])
    BESS_disch_1 = pd.DataFrame(my_network.assets[6].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging_loc1"])
    
    PV_0 = pd.DataFrame(my_network.assets[0].get_plot_data(), columns = ['PV_GB'])
    Wind_0 = pd.DataFrame(my_network.assets[1].get_plot_data(), columns = ['Wind_GB'])
    PV_1 = pd.DataFrame(my_network.assets[4].get_plot_data(), columns = ['PV_loc1'])
    Wind_1 = pd.DataFrame(my_network.assets[5].get_plot_data(), columns = ['Wind_loc1'])
    
    HVDC_out = pd.DataFrame(my_network.assets[8].flows.value[0:8760], columns = ['HVDC_GB-loc1'])
    HVDC_in = pd.DataFrame(my_network.assets[8].flows.value[8760:17520], columns = ['HVDC_loc1-GB'])

    flows = pd.concat ([flows, demand_0, demand_1, BESS_ch_0, BESS_disch_0, BESS_ch_1, BESS_disch_1,
    PV_0, Wind_0, PV_1, Wind_1, HVDC_out, HVDC_in], axis = 1)
    return(flows)

def export_XlinksEXT_Flows(my_network):
    
    flows = pd.DataFrame()
    demand_0 = pd.DataFrame(my_network.assets[3].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM_GB"])
    demand_1 = pd.DataFrame(my_network.assets[7].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM_MA"])
    demand_2 = pd.DataFrame(my_network.assets[11].assets_dictionary['Net_EL_Demand'].flows.value, columns = ["EL_Demand_UM_ZA"])
    
    BESS_ch_0 = pd.DataFrame(my_network.assets[2].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging_GB"])
    BESS_disch_0 = pd.DataFrame(my_network.assets[2].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging_GB"])
    BESS_ch_1 = pd.DataFrame(my_network.assets[6].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging_MA"])
    BESS_disch_1 = pd.DataFrame(my_network.assets[6].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging_MA"])
    BESS_ch_2 = pd.DataFrame(my_network.assets[10].assets_dictionary['Charging'].flows.value, columns = ["BESS_Charging_ZA"])
    BESS_disch_2 = pd.DataFrame(my_network.assets[10].assets_dictionary['Discharging'].flows.value, columns = ["BESS_Discharging_ZA"])
    
    PV_0 = pd.DataFrame(my_network.assets[0].get_plot_data(), columns = ['PV_GB'])
    Wind_0 = pd.DataFrame(my_network.assets[1].get_plot_data(), columns = ['Wind_GB'])
    PV_1 = pd.DataFrame(my_network.assets[4].get_plot_data(), columns = ['PV_MA'])
    Wind_1 = pd.DataFrame(my_network.assets[5].get_plot_data(), columns = ['Wind_MA'])
    PV_2 = pd.DataFrame(my_network.assets[8].get_plot_data(), columns = ['PV_ZA'])
    Wind_2 = pd.DataFrame(my_network.assets[9].get_plot_data(), columns = ['Wind_ZA'])
    
    HVDC0_out = pd.DataFrame(my_network.assets[12].flows.value[0:8760], columns = ['HVDC_GB-MA'])
    HVDC0_in = pd.DataFrame(my_network.assets[12].flows.value[8760:17520], columns = ['HVDC_MA-GB'])
    HVDC1_out = pd.DataFrame(my_network.assets[13].flows.value[0:8760], columns = ['HVDC_MA-ZA'])
    HVDC1_in = pd.DataFrame(my_network.assets[13].flows.value[8760:17520], columns = ['HVDC_ZA-MA'])
    
    flows = pd.concat ([flows, demand_0, demand_1, demand_2, BESS_ch_0, BESS_disch_0, BESS_ch_1, BESS_disch_1,
                        BESS_ch_2, BESS_disch_2, PV_0, Wind_0, PV_1, Wind_1, PV_2, Wind_2, HVDC0_out, HVDC0_in,
                        HVDC1_out, HVDC1_in], axis = 1)
    return(flows)

    
    
# def export_AUT_costs_sizes(my_network):

#     costs = pd.DataFrame()
#     sizes = pd.DataFrame()
    
#     ### Unmet demand asset
#     demand_s = pd.DataFrame(my_network.assets[3].asset_size(), columns = ["EL_Demand_UM_GWp"])
    
#     ### BESS ###
#     BESS_s = pd.DataFrame(my_network.assets[2].asset_size(), columns = ["BESS_GWh"])
#     BESS_c = pd.DataFrame(my_network.assets[2].cost.value, columns = ["BESS_G$"])

#     ### RE ###
#     PV = pd.DataFrame(my_network.assets[0].asset_size(), columns = ['PV'])
#     Wind = pd.DataFrame(my_network.assets[1].asset_size(), columns = ['Wind'])
    
#     ### Export to .csv in case study folder
#     size = pd.concat([size, demand_s, BESS_s, BESS_c, PV, Wind], axis=1)
#     return(costs, sizes)
    
        
    
    
    
    
    
    
    