#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 14:00:27 2023

@author: msgsty
"""

import pandas as pd
import matplotlib.pyplot as plt
import os



###### Autarky Case Studies #########
# case_study_name = "Autarky_SG"
# case_study_name = "Autarky_ID"
# case_study_name = "Autarky_MY"
# case_study_name = "Autarky_VN"
# case_study_name = "Autarky_PH"
# case_study_name = "Autarky_TH"
# case_study_name = "Autarky_KH"
# case_study_name = "Autarky_LA"
# case_study_name = "Autarky_MA"
# case_study_name = "Autarky_KE"
# case_study_name = "Autarky_ZA"
# case_study_name = "Autarky_KR"
# case_study_name = "Autarky_EG"
# case_study_name = "Autarky_NG"
# case_study_name = "Autarky_BR"
# case_study_name = "Autarky_CO"
# case_study_name = "Autarky_PE"
# case_study_name = "Autarky_CL"


###### Two Country Case Studies #########
# case_study_name = "SG-ID_Autarky"
# case_study_name = "SG-ID_Collab"

# case_study_name = "SG-MY_Autarky"
# case_study_name = "SG-MY_Collab"

# case_study_name = "SG-PH_Autarky"
# case_study_name = "SG-PH_Collab"

# case_study_name = "ID-MY_Autarky"
# case_study_name = "ID-MY_Collab"

# case_study_name = "MY-PH_Autarky"
# case_study_name = "MY-PH_Collab"

# case_study_name = "ID-PH_Autarky"
# case_study_name = "ID-PH_Collab"

# case_study_name = "VN-TH_Autarky"
# case_study_name = "VN-TH_Collab"

# case_study_name = "VN-LA_Autarky"
# case_study_name = "VN-LA_Collab"

# case_study_name = "VN-KH_Autarky"
# case_study_name = "VN-KH_Collab"

# case_study_name = "TH-LA_Autarky"
# case_study_name = "TH-LA_Collab"

# case_study_name = "TH-KH_Autarky"
# case_study_name = "TH-KH_Collab"

# case_study_name = "BR-CL_Autarky"
# case_study_name = "BR-CL_Collab"

# case_study_name = "LA-KH_Autarky"
# case_study_name = "LA-KH_Collab"

# case_study_name = "BR-CO_Autarky"
# case_study_name = "BR-CO_Collab"

# case_study_name = "BR-PE_Autarky"
# case_study_name = "BR-PE_Collab"

# case_study_name = "CO-CL_Autarky"
# case_study_name = "CO-CL_Collab"

# case_study_name = "CO-PE_Autarky"
# case_study_name = "CO-PE_Collab"

# case_study_name = "KR-LA_Autarky"
# case_study_name = "KR-LA_Collab"

# case_study_name = "KR-PE_Autarky"
# case_study_name = "KR-PE_Collab"

# case_study_name = "KR-TH_Autarky"
# case_study_name = "KR-TH_Collab"

###### Three Country Case Studies #########
# case_study_name = "SG-ID-MY_Autarky"
# case_study_name = "SG-ID-MY_Collab"

# case_study_name = "SG-ID-PH_Autarky"
# case_study_name = "SG-ID-PH_Collab"

# case_study_name = "SG-MY-PH_Autarky"
# case_study_name = "SG-MY-PH_Collab"

# case_study_name = "ID-MY-PH_Autarky"
# case_study_name = "ID-MY-PH_Collab"

# case_study_name = "VN-TH-LA_Autarky"
# case_study_name = "VN-TH-LA_Collab"

# case_study_name = "VN-TH-KH_Autarky"
# case_study_name = "VN-TH-KH_Collab"

# case_study_name = "TH-LA-KH_Autarky"
# case_study_name = "TH-LA-KH_Collab"

# case_study_name = "VN-LA-KH_Autarky"
# case_study_name = "VN-LA-KH_Collab"

# case_study_name = "BR-CO-CL_Autarky"
# case_study_name = "BR-CO-CL_Collab"

# case_study_name = "BR-CO-PE_Autarky"
# case_study_name = "BR-CO-PE_Collab"

# case_study_name = "BR-PE-CL_Autarky"
# case_study_name = "BR-PE-CL_Collab"

# case_study_name = "CO-PE-CL_Autarky"
# case_study_name = "CO-PE-CL_Collab"

# case_study_name = "KR-TH-LA_Autarky"
# case_study_name = "KR-TH-LA_Collab"

# case_study_name = "KR-TH-VN_Autarky"
# case_study_name = "KR-TH-VN_Collab"

###### Four Country Case Studies #########
# case_study_name = "SG-ID-MY-PH_Autarky"
# case_study_name = "SG-ID-MY-PH_Collab"

# case_study_name = "VN-TH-LA-KH_Autarky"
# case_study_name = "VN-TH-LA-KH_Collab"

# case_study_name = "BR-CO-PE-CL_Autarky"
# case_study_name = "BR-CO-PE-CL_Collab"

# case_study_name = "KR-TH-VN-LA_Autarky"
case_study_name = "KR-TH-VN-LA_Collab"


base_folder = os.path.dirname(__file__)
data_folder = os.path.join(base_folder, "Data")
case_study_folders_list = [x[0] for x in os.walk(data_folder)][1:]
case_study_folder = os.path.join(data_folder, "Case_Study", case_study_name)
total_data_filename = os.path.join(case_study_folder, "total_data_unrounded.csv")

plot_data_filename = os.path.join(case_study_folder, "mitigation_curve_data.csv")
plot_filename = os.path.join(case_study_folder, "mitigation_curve.png")

total_data = pd.read_csv(total_data_filename)
total_data = total_data.sort_values(by=['technology_name'])

df = pd.DataFrame()
row = pd.DataFrame()

while not total_data.empty:
    counter = 0
    checker = total_data["technology_name"].iloc[0]
    name = total_data["technology_name"].iloc[counter]
    rows = pd.DataFrame()
    num_rows = len(total_data)
    while name == checker:
        row = total_data.iloc[counter:counter+1]
        rows = pd.concat([rows, row], ignore_index=True)
        
        counter += 1
        if counter != num_rows:
            name = total_data["technology_name"].iloc[counter]
        else:
            name = ""

 
    rows = rows.sort_values(by=["collaboration_emissions"])
    rows = rows.set_index("collaboration_emissions")
    col_name = rows["technology_name"].iloc[0]
    # df.index = rows.index
    df[col_name] = rows["technology_cost"]
    df.index = rows.index
    

    total_data.drop(index=total_data.index[:counter], axis=0, inplace=True)
    

# df.to_csv({case_study}_collab_plot_data.csv")


##### Save figure in case study folder
fig, ax = plt.subplots()
df.plot.area(ax=ax)
ax.set_title(f"{case_study_name}")
ax.set_xlabel("Collaboration Emissions (MtCO2e)")
ax.set_ylabel("Costs (Billion USD)")
ax.set_xlim(left=0)
ax.legend(bbox_to_anchor=(0.5, -1.35), loc='lower center', borderaxespad=0, ncol=4)
fig.savefig(plot_filename, dpi=300, bbox_inches="tight")


    
    

