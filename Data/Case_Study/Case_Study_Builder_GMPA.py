# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 15:01:31 2023

@author: aniq_
"""

import os
import pandas as pd
import numpy as np





base_case_study = "VN-TH-LA-KH"
base_scenario_name = "BAU"




base_folder = os.path.dirname(__file__)
case_study_folder_1 = os.path.join(base_folder, base_case_study + r"_Autarky")
case_study_folder_2 = os.path.join(base_folder, base_case_study + r"_Collab")
base_filename_1 = os.path.join(case_study_folder_1, base_scenario_name, "Asset_Parameters.csv")
base_filename_2 = os.path.join(case_study_folder_2, base_scenario_name, "Asset_Parameters.csv")




#### Update asset parameters in autarky case study ######

def update_scenarios(base_case_study):
    base_df = pd.read_csv(base_filename_1)

    for counter1 in range(10):
        scenario_name = str((np.arange(10)*10)[-counter1-1])
        new_filename = os.path.join(case_study_folder_1, scenario_name, "Asset_Parameters.csv")
        new_df = base_df.copy()
        asset_type_list = list(new_df["Asset_Type"])
        asset_type_list[0] = new_df["Asset_Type"][0] + counter1 + 1
        new_df["Asset_Type"] = asset_type_list
        new_df.to_csv(new_filename, index=False)

    base_df = pd.read_csv(base_filename_2)

    for counter1 in range(10):
        scenario_name = str((np.arange(10)*10)[-counter1-1])
        new_filename = os.path.join(case_study_folder_2, scenario_name, "Asset_Parameters.csv")
        new_df = base_df.copy()
        asset_type_list = list(new_df["Asset_Type"])
        asset_type_list[0] = new_df["Asset_Type"][0] + counter1 + 1
        new_df["Asset_Type"] = asset_type_list
        new_df.to_csv(new_filename, index=False)
    return


update_scenarios(base_case_study)
