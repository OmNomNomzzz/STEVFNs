#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:37:30 2024

@author: Mónica Sagastuy-Breña

This script is specific to GMPA Pilot and 2nd phases and with the workflow for
Climate Analytics processed renewables data, hardcoded for this specitic format.

It reads the RES analysis files for capacity factor profiles for PV and Wind obtained
by Climate Analytics, prepares and saves them as STEVFNs inputs directly into their asset folders.


PLEASE NOTE: The function for wind is hardcoded to average out 10 binned profiles into one
If a wind file has a different format, or does not exist, this function will not work
and the profile will have to be handled manually.
Please contact Mónica if this arises.

Methodology:
    1. In Box, go to Modelling > res_analysis and download the folders named for the countries
    that need STEVFNs-formatted renewable energy profiles
    2. Save those folders (named by three-letter ISO abbreviation per country) into the
    raw_from_Box folder in STEVFNs repo
    3. Edit the list defined after the functions in this script to include those countries
    4. Run both of the functions
    
    5. Check that the Asset Folders for:
        RE_PV_Openfield_Lim
        RE_PV_Openfield_BAU
        RE_PV_Rooftop_Lim
        
        RE_WIND_Onshore_Lim
        RE_WIND_Onshore_BAU
        RE_WIND_Offshore_Lim
     Have created new folders with the renewable data processed as required.

"""

import pandas as pd
import numpy as np
import os


CODE_DIR = os.path.split(os.getcwd())[0]
stevfns_inputs = os.path.join(CODE_DIR, "Assets")

root_dir = os.path.dirname(__file__)
location_parameters_filename = os.path.join(root_dir, 'lat–lon-data.csv')
raw_data_folder = os.path.join(root_dir, "raw_from_Box")


onshore_wind_folder = os.path.join(stevfns_inputs, "RE_WIND_Onshore_Lim", "profiles", "WINDOUT")
offshore_wind_folder = os.path.join(stevfns_inputs, "RE_WIND_Offshore_Lim", "profiles", "WINDOUT")
rooftop_pv_folder = os.path.join(stevfns_inputs, "RE_PV_Rooftop_Lim", "profiles", "PVOUT")
openfield_pv_folder = os.path.join(stevfns_inputs, "RE_PV_Openfield_Lim", "profiles", "PVOUT")

# BAU folders to save profiles there as well
onshore_windbau_folder = os.path.join(stevfns_inputs, "RE_WIND_Onshore_BAU", "profiles", "WINDOUT")
openfield_pvbau_folder = os.path.join(stevfns_inputs, "RE_PV_Openfield_BAU", "profiles", "PVOUT")


lat_lon_df = pd.read_csv(location_parameters_filename)
lat_lon_df = lat_lon_df.set_index('Unnamed: 0')
lat_lon_df = lat_lon_df.T

def get_pv_inputs(countries):
    '''
    
    Parameters
    ----------
    countries : LIST
        DESCRIPTION: List of countries to get PV data from. Each country is a string of
        two-letter ISO abbreviation, all caps. e.g. to get PV data for Great Britain,
        Kenya and South Africa in one go countries = ['GBR', 'KEN', 'ZAF']

    Returns
    -------
    None.

    '''
    
    for country in countries:
    
        lat = lat_lon_df.loc['lat', f'{country}']
        lat = np.int64(np.round((lat) / 0.5)) * 0.5
        lat = min(lat,90.0)
        lat = max(lat,-90.0)
        
        lon = lat_lon_df.loc['lon', f'{country}']
        lon = np.int64(np.round((lon) / 0.625)) * 0.625
        lon = min(lon, 179.375)
        lon = max(lon, -180.0)

        '''
        OPENFIELD PV
        '''
        
        # Extract CF profile for openfield PV, Climate Analytics format
        PVopen_CF_df = pd.read_csv(os.path.join(raw_data_folder, 'res_analysis',
                                                f'{country}', 'pvopenfield', 'capacity_factor_binned.csv'))
        PVopen_CF_df = PVopen_CF_df.T
        PVopen_CF_df = PVopen_CF_df.drop([0, 1], axis=1)
        PVopen_CF_df = PVopen_CF_df.drop('Unnamed: 0', axis=0)
        
        # Find/create directory for openfield PV profiles
        pv_of_dir = os.path.join(openfield_pv_folder, f'lat{lat}')
        if not os.path.exists(pv_of_dir):
            os.makedirs(pv_of_dir) 
        pv_of_filename = os.path.join(pv_of_dir, f'PVOUT_lat{lat}_lon{lon}.csv')
        
        # save formatted files into PV Openfield Lim and PV Openfield BAU asset folders
        PVopen_CF_df.to_csv(pv_of_filename, index=False, header=False)
        
        pv_ofbau_dir = os.path.join(openfield_pvbau_folder, f'lat{lat}')
        if not os.path.exists(pv_ofbau_dir):
            os.makedirs(pv_ofbau_dir)
        PVopen_CF_df.to_csv(os.path.join(pv_ofbau_dir, f'PVOUT_lat{lat}_lon{lon}.csv'),
                            index=False, header=False)
        
        '''
        ROOFTOP PV
        '''
        
        # Extract CF profile for rooftop PV, Climate Analytics format
        PVroof_CF_df = pd.read_csv(os.path.join(raw_data_folder, 'res_analysis',
                                                f'{country}', 'pvrooftop', 'capacity_factor_binned.csv'))
        PVroof_CF_df = PVroof_CF_df.T
        PVroof_CF_df = PVroof_CF_df.drop([0, 1], axis=1)
        PVroof_CF_df = PVroof_CF_df.drop('Unnamed: 0', axis=0)
        
        # Find/create directory for openfield PV profiles
        pv_rt_dir = os.path.join(rooftop_pv_folder, f'lat{lat}')
        if not os.path.exists(pv_rt_dir):
            os.makedirs(pv_rt_dir) 
        pv_rt_filename = os.path.join(pv_rt_dir, f'PVOUT_lat{lat}_lon{lon}.csv')
        
        # Save csv with correct format
        PVroof_CF_df.to_csv(pv_rt_filename, index=False, header=False)
    
    return


def get_wind_inputs(countries):
    '''
    
    Parameters
    ----------
    countries : LIST
        DESCRIPTION: List of countries to get WIND data from. Each country is a string of
        two-letter ISO abbreviation, all caps. e.g. to get WIND data for Great Britain,
        Kenya and South Africa in one go countries = ['GB', 'KE', 'ZA']

    Returns
    -------
    None.

    '''
    
    for country in countries:
    
        lat = lat_lon_df.loc['lat', f'{country}']
        lat = np.int64(np.round((lat) / 0.5)) * 0.5
        lat = min(lat,90.0)
        lat = max(lat,-90.0)
        
        lon = lat_lon_df.loc['lon', f'{country}']
        lon = np.int64(np.round((lon) / 0.625)) * 0.625
        lon = min(lon, 179.375)
        lon = max(lon, -180.0)

        '''
        ONSHORE WIND
        '''
        # Extract CF profile for Onshore wind
        WindOnshore_CF_df = pd.read_csv(os.path.join(raw_data_folder, 'res_analysis',
                                                f'{country}', 'windonshore', 'capacity_factor_binned.csv'), header=None)
        WindOnshore_CF_df = WindOnshore_CF_df.drop([0,1], axis=1)
        WindOnshore_CF_df = WindOnshore_CF_df.drop([0,1,2], axis=0)
        WindOnshore_CF_df = WindOnshore_CF_df.T
        WindOnshore_CF_df = WindOnshore_CF_df.astype(float)
        
        WindOnshore_CF_df['A'] = (WindOnshore_CF_df[3] + WindOnshore_CF_df[4])/2
        WindOnshore_CF_df['B'] = (WindOnshore_CF_df[5] + WindOnshore_CF_df[6])/2
        WindOnshore_CF_df['C'] = (WindOnshore_CF_df[7] + WindOnshore_CF_df[8])/2
        WindOnshore_CF_df['D'] = (WindOnshore_CF_df[9] + WindOnshore_CF_df[10])/2
        WindOnshore_CF_df['E'] = (WindOnshore_CF_df[11] + WindOnshore_CF_df[12])/2
        WindOnshore_CF_df['F'] = (WindOnshore_CF_df['A'] + WindOnshore_CF_df['B'])/2
        WindOnshore_CF_df['G'] = (WindOnshore_CF_df['C'] + WindOnshore_CF_df['D']+ WindOnshore_CF_df['E'])/3
        WindOnshore_CF_df['MeanProfile'] =(WindOnshore_CF_df['F'] + WindOnshore_CF_df['G'])/2
        
        avg_wind_on_CF_df = pd.DataFrame(data=WindOnshore_CF_df['MeanProfile'])
        
        # Find/create directory for onshore wind profiles in STEVFNs
        wind_on_dir = os.path.join(onshore_wind_folder, 'WINDOUT', f'lat{lat}')
        if not os.path.exists(wind_on_dir):
            os.makedirs(wind_on_dir)
        wind_on_filename = os.path.join(wind_on_dir, f'WINDOUT_lat{lat}_lon{lon}.csv')
        
        # save formatted files into PV Openfield Lim and PV Openfield BAU asset folders
        avg_wind_on_CF_df.to_csv(wind_on_filename, index=False, header=False)
        
        wind_onbau_dir = os.path.join(onshore_windbau_folder, f'lat{lat}')
        if not os.path.exists(wind_onbau_dir):
            os.makedirs(wind_onbau_dir)
        avg_wind_on_CF_df.to_csv(os.path.join(wind_onbau_dir, f'WINDOUT_lat{lat}_lon{lon}.csv'),
                                 index=False, header=False)
        
        '''
        OFFSHORE WIND
        '''
        
        # Extract CF profile for Offshore wind
        WindOffshore_CF_df = pd.read_csv(os.path.join(raw_data_folder, 'res_analysis',
                                                f'{country}', 'windoffshore', 'capacity_factor_binned.csv'), header=None)
        WindOffshore_CF_df = WindOffshore_CF_df.drop([0,1], axis=1)
        WindOffshore_CF_df = WindOffshore_CF_df.drop([0,1,2], axis=0)
        WindOffshore_CF_df = WindOffshore_CF_df.T
        WindOffshore_CF_df = WindOffshore_CF_df.astype(float)
        
        WindOffshore_CF_df['A'] = (WindOffshore_CF_df[3] + WindOffshore_CF_df[4])/2
        WindOffshore_CF_df['B'] = (WindOffshore_CF_df[5] + WindOffshore_CF_df[6])/2
        WindOffshore_CF_df['C'] = (WindOffshore_CF_df[7] + WindOffshore_CF_df[8])/2
        WindOffshore_CF_df['D'] = (WindOffshore_CF_df[9] + WindOffshore_CF_df[10])/2
        WindOffshore_CF_df['E'] = (WindOffshore_CF_df[11] + WindOffshore_CF_df[12])/2
        WindOffshore_CF_df['F'] = (WindOffshore_CF_df['A'] + WindOffshore_CF_df['B'])/2
        WindOffshore_CF_df['G'] = (WindOffshore_CF_df['C'] + WindOffshore_CF_df['D']+ WindOffshore_CF_df['E'])/3
        WindOffshore_CF_df['MeanProfile'] =(WindOffshore_CF_df['F'] + WindOffshore_CF_df['G'])/2
        
        avg_wind_off_CF_df = pd.DataFrame(data=WindOffshore_CF_df['MeanProfile'])
        
        # Find/create directory for onshore wind profiles in STEVFNs
        wind_off_dir = os.path.join(offshore_wind_folder, 'WINDOUT', f'lat{lat}')
        if not os.path.exists(wind_on_dir):
            os.makedirs(wind_on_dir)
        wind_off_filename = os.path.join(wind_off_dir, f'WINDOUT_lat{lat}_lon{lon}.csv')
        
        avg_wind_off_CF_df.to_csv(wind_off_filename, index=False, header=False)
        
    return


#%%
countries = ['XXX']

get_pv_inputs(countries)
get_wind_inputs(countries)



