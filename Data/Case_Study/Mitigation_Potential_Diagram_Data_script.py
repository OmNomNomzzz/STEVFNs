# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:42:23 2023

@author: aniqa
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os



base_folder = os.path.dirname(__file__)

total_no_action_filename = os.path.join(base_folder, "BAU_No_Action", "total_data_unrounded.csv")
total_autarky_filename = os.path.join(base_folder, "total_data_unrounded_autarky.csv")
total_collaboration_filename = os.path.join(base_folder, "total_data_unrounded_collaboration.csv")
combined_autarky_filename = os.path.join(base_folder, "combined_data_autarky.csv")
combined_collaboration_filename = os.path.join(base_folder, "combined_data_collaboration.csv")
heatmap_autarky_filename = os.path.join(base_folder, "heatmap_autarky.csv")
heatmap_collaboration_filename = os.path.join(base_folder, "heatmap_collaboration.csv")


website_folder = os.path.join(base_folder, "Results_for_Website")
if not(os.path.isdir(website_folder)):
    os.mkdir(website_folder)
total_autarky_website_filename = os.path.join(website_folder, "total_data_autarky.csv")
total_collaboration_website_filename = os.path.join(website_folder, "total_data_collaboration.csv")
combined_autarky_website_filename = os.path.join(website_folder, "combined_data_autarky.csv")
combined_collaboration_website_filename = os.path.join(website_folder, "combined_data_collaboration.csv")
heatmap_autarky_website_filename = os.path.join(website_folder, "heatmap_autarky.csv")
heatmap_collaboration_website_filename = os.path.join(website_folder, "heatmap_collaboration.csv")



def generate_combined_df(total_autarky_df, total_collaboration_df, total_no_action_df):
    combined_columns = ["country_1", 
                  "country_2",
                  "country_3",
                  "country_4",
                  "emissions",
                  "cost",
                  "marginal_abatement_cost",
                  "average_abatement_cost",
                  ]
    combined_autarky_df = pd.DataFrame(columns = combined_columns)
    combined_collaboration_df = pd.DataFrame(columns = combined_columns)
    BAU_cost_list = np.zeros(4)
    BAU_emissions_list = np.zeros(4)
    for country_1 in np.unique(total_autarky_df["country_1"]):
        con_1 = total_autarky_df["country_1"] == country_1
        t_df_1 = total_autarky_df[con_1]
        
        con_1a = total_collaboration_df["country_1"] == country_1
        t_df_1a = total_collaboration_df[con_1a]
        
        con_1b = total_no_action_df["country_1"] == country_1
        t_df_1b = total_no_action_df[con_1b]
        BAU_emissions_list[0] = t_df_1b["collaboration_emissions"].iloc[0]
        BAU_cost_list[0] = np.array(t_df_1b["technology_cost"]).sum()
        
        for country_2 in np.unique(t_df_1["country_2"]):
            con_2 = t_df_1["country_2"] == country_2
            t_df_2 = t_df_1[con_2]
            
            con_2a = t_df_1a["country_2"] == country_2
            t_df_2a = t_df_1a[con_2a]
            
            if country_2 != "":
                con_2b = total_no_action_df["country_1"] == country_2
                t_df_2b = total_no_action_df[con_2b]
                BAU_emissions_list[1] = t_df_2b["collaboration_emissions"].iloc[0]
                BAU_cost_list[1] = np.array(t_df_2b["technology_cost"]).sum()
            else:
                BAU_emissions_list[1] = 0
                BAU_cost_list[1] = 0
            
            for country_3 in np.unique(t_df_2["country_3"]):
                con_3 = t_df_2["country_3"] == country_3
                t_df_3 = t_df_2[con_3]
                
                con_3a = t_df_2a["country_3"] == country_3
                t_df_3a = t_df_2a[con_3a]
                
                if country_3 != "":
                    con_3b = total_no_action_df["country_1"] == country_3
                    t_df_3b = total_no_action_df[con_3b]
                    BAU_emissions_list[2] = t_df_3b["collaboration_emissions"].iloc[0]
                    BAU_cost_list[2] = np.array(t_df_3b["technology_cost"]).sum()
                else:
                    BAU_emissions_list[2] = 0
                    BAU_cost_list[2] = 0
                
                for country_4 in np.unique(t_df_3["country_4"]):
                    con_4 = t_df_3["country_4"] == country_4
                    t_df_4 = t_df_3[con_4]
                    
                    con_4a = t_df_3a["country_4"] == country_4
                    t_df_4a = t_df_3a[con_4a]
                    
                    if country_4 != "":
                        con_4b = total_no_action_df["country_1"] == country_4
                        t_df_4b = total_no_action_df[con_4b]
                        BAU_emissions_list[3] = t_df_4b["collaboration_emissions"].iloc[0]
                        BAU_cost_list[3] = np.array(t_df_4b["technology_cost"]).sum()
                    else:
                        BAU_emissions_list[3] = 0
                        BAU_cost_list[3] = 0
                    
                    autarky_emissions_list = np.flip(np.sort(np.unique(t_df_4["collaboration_emissions"])))
                    previous_autarky_cost = 0
                    previous_autarky_emissions = 0
                    BAU_cost = BAU_cost_list.sum()
                    BAU_emissions = BAU_emissions_list.sum()
                    # BAU_cost = 0
                    # BAU_emissions = 0
                    for counter1 in range(len(autarky_emissions_list)):
                        autarky_emissions = autarky_emissions_list[counter1]
                        con_5 = t_df_4["collaboration_emissions"] == autarky_emissions
                        t_df_5 = t_df_4[con_5]
                        if list(t_df_5["technology_cost"])[0] != list(t_df_5["technology_cost"])[0]:
                            continue
                        autarky_cost = np.sum(t_df_5["technology_cost"])
                        if counter1 == 0:
                            marginal_abatement_cost = ((autarky_cost - BAU_cost) / 
                                                       (BAU_emissions - autarky_emissions))
                            marginal_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                            average_abatement_cost = ((autarky_cost - BAU_cost) / 
                                                       (BAU_emissions - autarky_emissions))
                            average_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                        else:
                            marginal_abatement_cost = ((autarky_cost - previous_autarky_cost) / 
                                                       (previous_autarky_emissions - autarky_emissions))
                            marginal_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                            average_abatement_cost = ((autarky_cost - BAU_cost) / 
                                                       (BAU_emissions - autarky_emissions))
                            average_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                        t_df_6 = pd.DataFrame({"country_1": [country_1], 
                                      "country_2": [country_2],
                                      "country_3": [country_3],
                                      "country_4": [country_4],
                                      "emissions": [autarky_emissions],
                                      "cost": [autarky_cost],
                                      "marginal_abatement_cost": [marginal_abatement_cost],
                                      "average_abatement_cost": [average_abatement_cost],
                                      })
                        combined_autarky_df = pd.concat([combined_autarky_df, t_df_6], ignore_index=True)
                        previous_autarky_cost = autarky_cost
                        previous_autarky_emissions = autarky_emissions
                    
                    collaboration_emissions_list = np.flip(np.sort(np.unique(t_df_4a["collaboration_emissions"])))
                    previous_collaboration_cost = 0
                    previous_collaboration_emissions = 0
                    for counter1 in range(len(collaboration_emissions_list)):
                        collaboration_emissions = collaboration_emissions_list[counter1]
                        con_5a = t_df_4a["collaboration_emissions"] == collaboration_emissions
                        t_df_5a = t_df_4a[con_5a]
                        if list(t_df_5a["technology_cost"])[0] != list(t_df_5a["technology_cost"])[0]:
                            continue
                        collaboration_cost = np.sum(t_df_5a["technology_cost"])
                        if counter1 == 0:
                            if country_2 == "":
                                marginal_abatement_cost = ((collaboration_cost - BAU_cost) / 
                                                           (BAU_emissions - collaboration_emissions))
                                marginal_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                                average_abatement_cost = ((collaboration_cost - BAU_cost) / 
                                                           (BAU_emissions - collaboration_emissions))
                                average_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                            else:
                                marginal_abatement_cost = ((collaboration_cost - BAU_cost) / 
                                                       (BAU_emissions - collaboration_emissions))
                                marginal_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                                average_abatement_cost = ((collaboration_cost - BAU_cost) / 
                                                       (BAU_emissions - collaboration_emissions))
                                average_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                        else:
                            marginal_abatement_cost = ((collaboration_cost - previous_collaboration_cost) / 
                                                       (previous_collaboration_emissions - collaboration_emissions))
                            marginal_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                            average_abatement_cost = ((collaboration_cost - BAU_cost) / 
                                                       (BAU_emissions - collaboration_emissions))
                            average_abatement_cost *= 1e3 # Change units from [k$/tCO2e] to [$/tCO2e]
                        if BAU_emissions == collaboration_emissions:
                            marginal_abatement_cost = 0
                            average_abatement_cost = 0
                        t_df_6a = pd.DataFrame({"country_1": [country_1], 
                                      "country_2": [country_2],
                                      "country_3": [country_3],
                                      "country_4": [country_4],
                                      "emissions": [collaboration_emissions],
                                      "cost": [collaboration_cost],
                                      "marginal_abatement_cost": [marginal_abatement_cost],
                                      "average_abatement_cost": [average_abatement_cost],
                                      })
                        combined_collaboration_df = pd.concat([combined_collaboration_df, t_df_6a], ignore_index=True)
                        previous_collaboration_cost = collaboration_cost
                        previous_collaboration_emissions = collaboration_emissions
    return (combined_autarky_df, combined_collaboration_df)



def generate_heatmap_df(combined_autarky_df, combined_collaboration_df, total_no_action_df, marginal_cutoffs = [50,100,200], average_cutoffs = [50,100,200]):
    heatmap_columns = ["country_1", 
                  "country_2",
                  "country_3",
                  "country_4",
                  "Mitigation_Potential(MtCO2e)",
                  "Mitigation_Cost($/tCO2e)",
                  ]
    marginal_columns = []
    for counter1 in range(len(marginal_cutoffs)):
        marginal_columns += ["Mitigation_Potential_at_" + str(marginal_cutoffs[counter1]) + "($/tCO2e)",]
    heatmap_columns += marginal_columns
    average_columns = []
    for counter1 in range(len(average_cutoffs)):
        average_columns += ["Mitigation_Potential_at_Average_" + str(average_cutoffs[counter1]) + "($/tCO2e)",]
    heatmap_columns += average_columns
    heatmap_autarky_df = pd.DataFrame(columns = heatmap_columns)
    heatmap_collaboration_df = pd.DataFrame(columns = heatmap_columns)
    BAU_cost_list = np.zeros(4)
    BAU_emissions_list = np.zeros(4)
    
    for country_1 in np.unique(combined_autarky_df["country_1"]):
        con_1 = combined_autarky_df["country_1"] == country_1
        t_df_1 = combined_autarky_df[con_1]
        
        con_1a = combined_collaboration_df["country_1"] == country_1
        t_df_1a = combined_collaboration_df[con_1a]
        
        con_1b = total_no_action_df["country_1"] == country_1
        t_df_1b = total_no_action_df[con_1b]
        BAU_emissions_list[0] = t_df_1b["collaboration_emissions"].iloc[0]
        BAU_cost_list[0] = np.array(t_df_1b["technology_cost"]).sum()
        
        for country_2 in np.unique(t_df_1["country_2"]):
            con_2 = t_df_1["country_2"] == country_2
            t_df_2 = t_df_1[con_2]
            
            con_2a = t_df_1a["country_2"] == country_2
            t_df_2a = t_df_1a[con_2a]
            
            if country_2 != "":
                con_2b = total_no_action_df["country_1"] == country_2
                t_df_2b = total_no_action_df[con_2b]
                BAU_emissions_list[1] = t_df_2b["collaboration_emissions"].iloc[0]
                BAU_cost_list[1] = np.array(t_df_2b["technology_cost"]).sum()
            else:
                BAU_emissions_list[1] = 0
                BAU_cost_list[1] = 0
            
            for country_3 in np.unique(t_df_2["country_3"]):
                con_3 = t_df_2["country_3"] == country_3
                t_df_3 = t_df_2[con_3]
                
                con_3a = t_df_2a["country_3"] == country_3
                t_df_3a = t_df_2a[con_3a]
                
                if country_3 != "":
                    con_3b = total_no_action_df["country_1"] == country_3
                    t_df_3b = total_no_action_df[con_3b]
                    BAU_emissions_list[2] = t_df_3b["collaboration_emissions"].iloc[0]
                    BAU_cost_list[2] = np.array(t_df_3b["technology_cost"]).sum()
                else:
                    BAU_emissions_list[2] = 0
                    BAU_cost_list[2] = 0
                
                for country_4 in np.unique(t_df_3["country_4"]):
                    con_4 = t_df_3["country_4"] == country_4
                    t_df_4 = t_df_3[con_4]
                    
                    con_4a = t_df_3a["country_4"] == country_4
                    t_df_4a = t_df_3a[con_4a]
                    
                    if country_4 != "":
                        con_4b = total_no_action_df["country_1"] == country_4
                        t_df_4b = total_no_action_df[con_4b]
                        BAU_emissions_list[3] = t_df_4b["collaboration_emissions"].iloc[0]
                        BAU_cost_list[3] = np.array(t_df_4b["technology_cost"]).sum()
                    else:
                        BAU_emissions_list[3] = 0
                        BAU_cost_list[3] = 0
                    
                    BAU_cost = BAU_cost_list.sum()
                    BAU_emissions = BAU_emissions_list.sum()
                    
                    # con_4_1 = t_df_4["emissions"] == t_df_4["emissions"].max()
                    # t_df_4_1 = t_df_4[con_4_1]
                    # BAU_emissions = float(t_df_4_1["emissions"])
                    # BAU_cost = float(t_df_4_1["cost"])
                    con_4_2 = t_df_4["emissions"] == t_df_4["emissions"].min()
                    t_df_4_2 = t_df_4[con_4_2]
                    maximum_potential_emissions = float(t_df_4_2["emissions"])
                    # maximum_potential_cost = float(t_df_4_2["cost"])
                    mitigation_potential = BAU_emissions - maximum_potential_emissions
                    if float(t_df_4_2["emissions"])==0:
                        mitigation_cost = float(t_df_4_2["average_abatement_cost"])
                    else:
                        mitigation_cost = ""
                    mitigation_potential_list = []
                    for marginal_cutoff in marginal_cutoffs:
                        con_5 = t_df_4["marginal_abatement_cost"] <= marginal_cutoff
                        t_df_5 = t_df_4[con_5]
                        con_6 = t_df_5["emissions"] == t_df_5["emissions"].min()
                        t_df_6 = t_df_5[con_6]
                        if len(t_df_6)>0:
                            mitigation_potential_list += [BAU_emissions - float(t_df_6["emissions"]),]
                        else:
                            mitigation_potential_list += [0,]
                    mitigation_potential_average_list = []
                    for average_cutoff in average_cutoffs:
                        con_5 = t_df_4["average_abatement_cost"] <= average_cutoff
                        t_df_5 = t_df_4[con_5]
                        con_6 = t_df_5["emissions"] == t_df_5["emissions"].min()
                        t_df_6 = t_df_5[con_6]
                        if len(t_df_6)>0:
                            mitigation_potential_average_list += [BAU_emissions - float(t_df_6["emissions"]),]
                        else:
                            mitigation_potential_average_list += [0,]
                    t_dict = {"country_1": [country_1], 
                                      "country_2": [country_2],
                                      "country_3": [country_3],
                                      "country_4": [country_4],
                                      "Mitigation_Potential(MtCO2e)": [mitigation_potential],
                                      "Mitigation_Cost($/tCO2e)": [mitigation_cost],
                                      "BAU_Emissions(MtCO2e)": [BAU_emissions],
                                      }
                    for counter1 in range(len(marginal_cutoffs)):
                        t_dict[marginal_columns[counter1]] = mitigation_potential_list[counter1]
                    for counter1 in range(len(average_cutoffs)):
                        t_dict[average_columns[counter1]] = mitigation_potential_average_list[counter1]
                    t_df_8 = pd.DataFrame(t_dict)
                    heatmap_autarky_df = pd.concat([heatmap_autarky_df, t_df_8], ignore_index=True)
                    
                    con_4_2a = t_df_4a["emissions"] == t_df_4a["emissions"].min()
                    t_df_4_2a = t_df_4a[con_4_2a]
                    maximum_potential_emissions = float(t_df_4_2a["emissions"])
                    # maximum_potential_cost = float(t_df_4_2["cost"])
                    mitigation_potential = BAU_emissions - maximum_potential_emissions
                    if float(t_df_4_2a["emissions"])==0:
                        mitigation_cost = float(t_df_4_2a["average_abatement_cost"])
                    else:
                        mitigation_cost = ""
                    mitigation_potential_list = []
                    for marginal_cutoff in marginal_cutoffs:
                        con_5a = t_df_4a["marginal_abatement_cost"] <= marginal_cutoff
                        t_df_5a = t_df_4a[con_5a]
                        con_6a = t_df_5a["emissions"] == t_df_5a["emissions"].min()
                        t_df_6a = t_df_5a[con_6a]
                        if len(t_df_6a)>0:
                            mitigation_potential_list += [BAU_emissions - float(t_df_6a["emissions"]),]
                        else:
                            mitigation_potential_list += [0,]
                    mitigation_potential_average_list = []
                    for average_cutoff in average_cutoffs:
                        con_5a = t_df_4a["average_abatement_cost"] <= average_cutoff
                        t_df_5a = t_df_4a[con_5a]
                        con_6a = t_df_5a["emissions"] == t_df_5a["emissions"].min()
                        t_df_6a = t_df_5a[con_6a]
                        if len(t_df_6a)>0:
                            mitigation_potential_average_list += [BAU_emissions - float(t_df_6a["emissions"]),]
                        else:
                            mitigation_potential_average_list += [0,]
                    t_dict = {"country_1": [country_1], 
                                      "country_2": [country_2],
                                      "country_3": [country_3],
                                      "country_4": [country_4],
                                      "Mitigation_Potential(MtCO2e)": [mitigation_potential],
                                      "Mitigation_Cost($/tCO2e)": [mitigation_cost],
                                      "BAU_Emissions(MtCO2e)": [BAU_emissions],
                                      }
                    for counter1 in range(len(marginal_cutoffs)):
                        t_dict[marginal_columns[counter1]] = mitigation_potential_list[counter1]
                    for counter1 in range(len(average_cutoffs)):
                        t_dict[average_columns[counter1]] = mitigation_potential_average_list[counter1]
                    t_df_8a = pd.DataFrame(t_dict)
                    heatmap_collaboration_df = pd.concat([heatmap_collaboration_df, t_df_8a], ignore_index=True)
    return (heatmap_autarky_df, heatmap_collaboration_df)


def data_for_website(data_df, final_columns, columns_to_round):
    website_data_df = pd.DataFrame(columns = final_columns)
    for column_name in final_columns:
        website_data_df[column_name] = data_df[column_name]
    # for column_name in columns_to_round:
    #     website_data_df[column_name] = round(website_data_df[column_name],1)
    return website_data_df

def generate_data_for_website(total_autarky_df, 
                              total_collaboration_df,
                              combined_autarky_df,
                              combined_collaboration_df,
                              heatmap_autarky_df,
                              heatmap_collaboration_df,
                              average_cutoffs = [50,100,200],):
    final_columns_total_data = ["country_1", 
                  "country_2",
                  "country_3",
                  "country_4",
                  "collaboration_emissions",
                  "technology_name",
                  "technology_cost",
                  ]
    columns_to_round_total_data = ["collaboration_emissions",
                        "technology_cost",]
    
    total_autarky_website_df = data_for_website(total_autarky_df, 
                                                  final_columns_total_data,
                                                  columns_to_round_total_data)
    
    total_collaboration_website_df = data_for_website(total_collaboration_df, 
                                                  final_columns_total_data,
                                                  columns_to_round_total_data)
    
    final_columns_combined_data = ["country_1", 
                  "country_2",
                  "country_3",
                  "country_4",
                  "emissions",
                  "cost",
                  ]
    columns_to_round_combined_data = ["emissions",
                        "cost",]
    
    combined_autarky_website_df = data_for_website(combined_autarky_df, 
                                                  final_columns_combined_data,
                                                  columns_to_round_combined_data)
    
    combined_collaboration_website_df = data_for_website(combined_collaboration_df, 
                                                  final_columns_combined_data,
                                                  columns_to_round_combined_data)
    
    average_columns = []
    for counter1 in range(len(average_cutoffs)):
        average_columns += ["Mitigation_Potential_at_Average_" + str(average_cutoffs[counter1]) + "($/tCO2e)",]
    
    final_columns_heatmap = ["country_1", 
                  "country_2",
                  "country_3",
                  "country_4",
                  "Mitigation_Cost($/tCO2e)",
                  "BAU_Emissions(MtCO2e)",
                  "Mitigation_Potential(MtCO2e)",
                  ]
    columns_to_round_heatmap = ["Mitigation_Cost($/tCO2e)",
    "BAU_Emissions(MtCO2e)",
    "Mitigation_Potential(MtCO2e)",
    ]
    
    final_columns_heatmap += average_columns
    columns_to_round_heatmap += average_columns
    
    heatmap_autarky_website_df = data_for_website(heatmap_autarky_df, 
                                                  final_columns_heatmap,
                                                  columns_to_round_heatmap)
    
    heatmap_collaboration_website_df = data_for_website(heatmap_collaboration_df, 
                                                  final_columns_heatmap,
                                                  columns_to_round_heatmap)
    
    return (total_autarky_website_df, 
            total_collaboration_website_df,
            combined_autarky_website_df,
            combined_collaboration_website_df,
            heatmap_autarky_website_df,
            heatmap_collaboration_website_df)


##### Load Data #########

total_no_action_df = pd.read_csv(total_no_action_filename, keep_default_na=False)
total_autarky_df = pd.read_csv(total_autarky_filename, keep_default_na=False)
total_collaboration_df = pd.read_csv(total_collaboration_filename, keep_default_na=False)


##### Process Data #####


(combined_autarky_df, combined_collaboration_df) = generate_combined_df(total_autarky_df, total_collaboration_df, total_no_action_df)


marginal_cutoffs = [0, 50, 100, 200] #[0.01, 0.025, 0.05, 0.1] value in [$/tCO2e]
average_cutoffs = [0, 10, 20, 50] #[0.01, 0.025, 0.05, 0.1] value in [$/tCO2e]

(heatmap_autarky_df, heatmap_collaboration_df) = generate_heatmap_df(combined_autarky_df, combined_collaboration_df, 
                                                                      total_no_action_df,
                                                                      marginal_cutoffs, average_cutoffs)

(total_autarky_website_df, 
 total_collaboration_website_df,
 combined_autarky_website_df,
 combined_collaboration_website_df,
 heatmap_autarky_website_df,
 heatmap_collaboration_website_df) = generate_data_for_website(total_autarky_df, 
                                                               total_collaboration_df,
                                                               combined_autarky_df,
                                                               combined_collaboration_df,
                                                               heatmap_autarky_df,
                                                               heatmap_collaboration_df,
                                                               average_cutoffs)
                                                              


###### Save Data #############
# combined_autarky_df.to_csv(combined_autarky_filename, index =False)
# combined_collaboration_df.to_csv(combined_collaboration_filename, index =False)

# heatmap_autarky_df.to_csv(heatmap_autarky_filename, index=False)
# heatmap_collaboration_df.to_csv(heatmap_collaboration_filename, index=False)


## Save data for website ###

total_autarky_website_df.to_csv(total_autarky_website_filename, index=False)
total_collaboration_website_df.to_csv(total_collaboration_website_filename, index=False)
combined_autarky_website_df.to_csv(combined_autarky_website_filename, index=False)
combined_collaboration_website_df.to_csv(combined_collaboration_website_filename, index=False)
heatmap_autarky_website_df.to_csv(heatmap_autarky_website_filename, index=False)
heatmap_collaboration_website_df.to_csv(heatmap_collaboration_website_filename, index=False)


