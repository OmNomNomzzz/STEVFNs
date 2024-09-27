#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:08:02 2024

@author: Mónica Sagastuy-Breña

This script creates a csv with location names (ISO 2-letter country abbreviation)
their full coordinates from Location_Parameters.csv and their rounded coordinates
for naming files for renewable potential.

It then creates the folders and csv files associated with this data ready for input
into each profiles folder for the asset folders:
    RE_PV_Openfield_Lim
    RE_PV_Rooftop_Lim
    RE_WIND_Onshore_Lim
    RE_WIND_Offshore_Lim
    
In the main STEVFNs directory, it also creates a csv file with the country abbreviations
and the rounded lat and lon values, for later manual input of the profiles from Climate Analytics
"""

import pandas as pd
import numpy as np
import csv
import os

root_dir = os.path.dirname(__file__)
loc_params_file = os.path.join(root_dir, "Data", "Case_Study", "Phase_2_Case_Study", "BAU", "Location_Parameters.csv")
onshore_wind_dir = os.path.join(root_dir, "Code", "Assets", "RE_WIND_Onshore_Lim", "profiles")
offshore_wind_dir = os.path.join(root_dir, "Code", "Assets", "RE_WIND_Offshore_Lim", "profiles")
rooftop_pv_dir = os.path.join(root_dir, "Code", "Assets", "RE_PV_Rooftop_Lim", "profiles")
openfield_pv_dir = os.path.join(root_dir, "Code", "Assets", "RE_PV_Openfield_Lim", "profiles")
openfield_pvbau_dir = os.path.join(root_dir, "Code", "Assets", "RE_PV_Openfield_BAU", "profiles")
onshore_windbau_dir = os.path.join(root_dir, "Code", "Assets", "RE_WIND_Onshore_BAU", "profiles")

loc_params_df = pd.read_csv(loc_params_file)
loc_params_df.set_index(loc_params_df['location_name'], inplace=True)

countries = ['MA', 'KE', 'ZA', 'KR', 'EG', 'NG', 'BR', 'CO', 'PE', 'CL']

final_lat_lon_df = pd.DataFrame()

for country in countries:
    lat = loc_params_df.loc[f'{country}', 'lat']
    lon = loc_params_df.loc[f'{country}', 'lon']
    
    lat = np.int64(np.round((lat) / 0.5)) * 0.5
    lat = min(lat,90.0)
    lat = max(lat,-90.0)
    lon = np.int64(np.round((lon) / 0.625)) * 0.625
    lon = min(lon, 179.375)
    lon = max(lon, -180.0)
    
    # Create empty RE file for onshore wind 
    wind_on_directory = os.path.join(onshore_wind_dir, 'WINDOUT', f'lat{lat}')
    if not os.path.exists(wind_on_directory):
        os.makedirs(wind_on_directory)
    wind_on_filename = os.path.join(wind_on_directory, f'WINDOUT_lat{lat}_lon{lon}.csv')
    with open(wind_on_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
    # Create empty RE file for onshore wind  in BAU asset
    wind_onbau_directory = os.path.join(onshore_windbau_dir, 'WINDOUT', f'lat{lat}')
    if not os.path.exists(wind_onbau_directory):
        os.makedirs(wind_onbau_directory)
    wind_onbau_filename = os.path.join(wind_onbau_directory, f'WINDOUT_lat{lat}_lon{lon}.csv')
    with open(wind_onbau_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
       
    # Create empty RE file for offshore wind
    wind_off_directory = os.path.join(offshore_wind_dir, 'WINDOUT', f'lat{lat}')
    if not os.path.exists(wind_off_directory):
        os.makedirs(wind_off_directory)
    wind_off_filename = os.path.join(wind_off_directory, f'WINDOUT_lat{lat}_lon{lon}.csv')
    with open(wind_off_filename, mode='w', newline='') as file:
        writer = csv.writer(file)   
    
    # Create empty RE file for rooftop pv
    pv_rt_directory = os.path.join(rooftop_pv_dir, 'PVOUT', f'lat{lat}')
    if not os.path.exists(pv_rt_directory):
        os.makedirs(pv_rt_directory) 
    pv_rt_filename = os.path.join(pv_rt_directory, f'PVOUT_lat{lat}_lon{lon}.csv')
    with open(pv_rt_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
    # Create empty RE file for openfield pv
    pv_of_directory = os.path.join(openfield_pv_dir, 'PVOUT', f'lat{lat}')
    if not os.path.exists(pv_of_directory):
        os.makedirs(pv_of_directory) 
    pv_of_filename = os.path.join(pv_of_directory, f'PVOUT_lat{lat}_lon{lon}.csv')
    with open(pv_of_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
    
    # Create empty RE file for openfield pv in BAU asset
    pv_ofbau_directory = os.path.join(openfield_pvbau_dir, 'PVOUT', f'lat{lat}')
    if not os.path.exists(pv_ofbau_directory):
        os.makedirs(pv_ofbau_directory) 
    pv_ofbau_filename = os.path.join(pv_ofbau_directory, f'PVOUT_lat{lat}_lon{lon}.csv')
    with open(pv_ofbau_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        
    
    
    # Create a csv file to view each country's name and rounded lat lon values, if useful
    
    
    # final_lat_lon_df = pd.concat([final_lat_lon_df,
    #                               pd.DataFrame({'location_name': [country], 'lat': [lat],
    #                                             'lon': [lon]})], ignore_index=True)
    # final_lat_lon_df.to_csv(os.path.join(root_dir, "Location_Parameters_for_RE_Profiles.csv"), index=False)
    

    


    
    
    