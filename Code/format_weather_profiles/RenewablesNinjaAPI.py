#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:27:23 2021

To do:
    Remove hard coded API token
    Docstrings
    save data
    if data saved, import rather than call

@author: Scot Wheeler

Last updated: 25/09/2024 by Mónica Sagastuy-Breña
For application in GMPA
"""


__version__ = "0.5.1"

import pandas as pd
import requests
import json
import datetime
import time
from tqdm import tqdm
import os
import numpy as np


class Renewables_Ninja():
    """
    API tools for renewables.ninja.

    Input
    -----
    user_tokem : str
        obtained from renewables.ninja website
    latitude : float

    longitude : float
    """

    def __init__(self, location="", user_token="",
                 latitude=51.586, longitude=-1.250):

        self.location = location
        if user_token == "":
            try:
                with open('creds.json') as json_file:
                    user_token = json.load(json_file)["api_token"]
            except:
                raise Exception("""
You need to provide an API user token either as an argument or using a
credential json file with the "api_token" parameter.\

API tokens can be obtained from your renewables.ninja profile
                                    """)
        self.rn_token = user_token
        
        self.api_base = 'https://www.renewables.ninja/api/'
        self.latitude = latitude
        self.longitude = longitude
        self.calls = pd.DataFrame({"call_time": []})

    def _limits(self):
        s = requests.session()
        # Send token header with each request
        s.headers = {'Authorization': 'Token ' + self.rn_token}

        url = self.api_base + 'limits'

        r = s.get(url)
        print(r.text)

    def _check_api_limit(self):
        # reached api limit (50 per hour)
        hour_lim = (datetime.datetime.today()
                    - datetime.timedelta(minutes=59))
        min_lim = (datetime.datetime.today()
                   - datetime.timedelta(seconds=59))
        if self.calls[self.calls["call_time"] > hour_lim].size > 49:
            print("Waiting for API hour limit")
            time.sleep((60*60+10))
        # reached api limit (6 per min)
        if self.calls[self.calls["call_time"] > min_lim].size > 5:
            print("Waiting for API minute limit")
            time.sleep(61)    

    def _check_api_limit_pbar(self, pbar):
        # reached api limit (50 per hour)
        hour_lim = (datetime.datetime.today()
                    - datetime.timedelta(minutes=59))
        min_lim = (datetime.datetime.today()
                   - datetime.timedelta(seconds=59))
        if self.calls[self.calls["call_time"] > hour_lim].size > 49:
            pbar.display("Waiting for API hour limit")
            time.sleep((60*60+10))
        # reached api limit (6 per min)
        if self.calls[self.calls["call_time"] > min_lim].size > 5:
            pbar.display("Waiting for API minute limit")
            time.sleep(61)

    def get_renewables_ninja_PV(self, capacity=1, tilt=35, azim=180.0,
                                year=2018, drop_leap_year=False, **kwargs):
        """
        Get PV data from renewables.ninja api.

        Parameters
        ----------
        capacity : TYPE, optional
            DESCRIPTION. The default is 1.
        tilt : TYPE, optional
            DESCRIPTION. The default is 35.
        azim : TYPE, optional
            DESCRIPTION. The default is 180.0.
        year : TYPE, optional
            DESCRIPTION. The default is 2018.
        drop_leap_year : TYPE, optional
            DESCRIPTION. The default is True.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.
        metadata : TYPE
            DESCRIPTION.

        """
        
        # self.calls = self.calls.append(
        #     {"call_time": datetime.datetime.today()}, ignore_index=True)
        self.calls = pd.concat([self.calls,
            pd.DataFrame({"call_time": datetime.datetime.today()},
                         index=[0])],
                               ignore_index=True)
        
        if "system_loss" in kwargs.keys():
            system_loss = float(kwargs["system_loss"])
        else:
            system_loss = 0.10  # in 10%
        if "tracking" in kwargs.keys():
            tracking = kwargs["tracking"]
        else:
            tracking = 0

        if "dataset" in kwargs.keys():
            dataset = kwargs["dataset"]
        else:
            dataset = "merra2"

        date_from = str(year)+"-01-01"
        date_to = str(year)+"-12-31"

        s = requests.session()
        # Send token header with each request
        s.headers = {'Authorization': 'Token ' + self.rn_token}

        url = self.api_base + 'data/pv'

        args = {
            'lat': self.latitude,
            'lon': self.longitude,
            'date_from': date_from,
            'date_to': date_to,
            'dataset': dataset,
            'capacity': float(capacity),
            'system_loss': float(system_loss),
            'tracking': tracking,
            'tilt': float(tilt),
            'azim': float(azim),
            'raw': True,
            'format': 'json',
            'local_time': True,
            }

        r = s.get(url, params=args)
        parsed_response = json.loads(r.text)

        # Parse JSON to get a pandas.DataFrame
        df = pd.read_json(json.dumps(parsed_response['data']),
                          orient='index')
        metadata = parsed_response['metadata']

        if drop_leap_year:
            if year % 4 == 0:
                df.drop(df.index[1416:1440], inplace=True)

        return df, metadata

    def get_renewables_ninja_wind(self, capacity=1,
                                  height=80, year=2014,
                                  drop_leap_year=False, **kwargs):
        """
        Get wind output from renewables.ninja api.

        Parameters
        ----------
        capacity : TYPE, optional
            DESCRIPTION. The default is 1.
        height : TYPE, optional
            DESCRIPTION. The default is 80.
        year : TYPE, optional
            DESCRIPTION. The default is 2014.
        drop_leap_year : TYPE, optional
            DESCRIPTION. The default is True.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.
        metadata : TYPE
            DESCRIPTION.

        """
        
        # self.calls = self.calls.append(
        #     {"call_time": datetime.datetime.today()}, ignore_index=True)
        self.calls = pd.concat([self.calls,
            pd.DataFrame({"call_time": datetime.datetime.today()},
                         index=[0])],
                               ignore_index=True)
        
        
        if "turbine" in kwargs.keys():
            turbine = str(kwargs["turbine"])
        else:
            turbine = 'Vestas V80 2000'

        date_from = str(year) + "-01-01"
        date_to = str(year) + "-12-31"

        s = requests.session()
        # Send token header with each request
        s.headers = {'Authorization': 'Token ' + self.rn_token}
        url = self.api_base + 'data/wind'

        args = {
            'lat': self.latitude,
            'lon': self.longitude,
            'date_from': date_from,
            'date_to': date_to,
            'capacity': float(capacity),
            'height': float(height),
            'turbine': turbine,
            'raw': True,
            'format': 'json',
            'local_time': True,
            }

        r = s.get(url, params=args)
        parsed_response = json.loads(r.text)

        # Parse JSON to get a pandas.DataFrame
        df = pd.read_json(json.dumps(parsed_response['data']),
                          orient='index')
        metadata = parsed_response['metadata']

        if drop_leap_year:
            if year % 4 == 0:
                df.drop(df.index[1416:1440], inplace=True)

        return df, metadata

    def get_renewables_ninja_weather(self, years=[2018],
                                     drop_leap_year=False, **kwargs):
        """
        Get weather data from renewables.ninja api.

        Parameters
        ----------
        years : TYPE, optional
            DESCRIPTION. The default is [2018].
        drop_leap_year : TYPE, optional
            DESCRIPTION. The default is True.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        data = pd.DataFrame()
        with tqdm(total=len(years)) as pbar:
            for year in years:
                self._check_api_limit_pbar(pbar)
                # self.calls = self.calls.append(
                #     {"call_time": datetime.datetime.today()}, ignore_index=True)
                self.calls = pd.concat([self.calls,
                    pd.DataFrame({"call_time": datetime.datetime.today()},
                                 index=[0])],
                                       ignore_index=True)

                date_from = str(year) + "-01-01"
                date_to = str(year) + "-12-31"
    
                s = requests.session()
                # Send token header with each request
                s.headers = {'Authorization': 'Token ' + self.rn_token}
                url = self.api_base + 'data/weather'
    
                args = {
                    'lat': self.latitude,
                    'lon': self.longitude,
                    'date_from': date_from,
                    'date_to': date_to,
                    'format': 'json',
                    'local_time': True,
                    'var_t2m': True,
                    'var_prectotland': True,
                    'var_precsnoland': True,
                    'var_rhoa': True,
                    'var_swgdn': True,
                    'var_swtdn': True,
                    'var_cldtot': True
                    }

                r = s.get(url, params=args)

                parsed_response = json.loads(r.text)
    
                # Parse JSON to get a pandas.DataFrame
                df = pd.read_json(json.dumps(parsed_response['data']),
                                  orient='index')
                metadata = parsed_response['metadata']
    
                if drop_leap_year:
                    if year % 4 == 0:
                        df.drop(df.index[1416:1440], inplace=True)
    
                data = pd.concat([data, df])
                pbar.update(1)
            pbar.close()

        return data
    
    def multi_get_renewables_ninja_PV(self, capacities=[1], tilts=[35],
                                      azims=[180.0], years=[2018], **kwargs):
        """
        Do multiple calls for PV data from renewables.ninja api

        Parameters
        ----------
        capacities : TYPE, optional
            DESCRIPTION. The default is [1].
        tilts : TYPE, optional
            DESCRIPTION. The default is [35].
        azims : TYPE, optional
            DESCRIPTION. The default is [180.0].
        years : TYPE, optional
            DESCRIPTION. The default is [2018].
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        
        total_calls = (len(capacities)
                       * len(tilts)
                       * len(azims)
                       * len(years))
        calls = 0
        data = pd.DataFrame({})
        
        with tqdm(total = total_calls) as pbar:
            for capacity in capacities:
                for tilt in tilts:
                    for azim in azims:
                        for year in years:
                            self._check_api_limit_pbar(pbar)
                            df, metadf = self.get_renewables_ninja_PV(
                                capacity=capacity,
                                tilt=tilt,
                                azim=azim,
                                year=year,
                                **kwargs)
                            df["capacity"] = capacity
                            df["tilt"] = tilt
                            df["azim"] = azim
                            df["year"] = year
                            data = pd.concat([data, df])
                            calls += 1
                            pbar.update(1)
                            
            pbar.close()
                        
        return data
    
    def multi_get_renewables_ninja_wind(self, capacities=[1], heights=[80],
                                        years=[2018], **kwargs):
        """
        Do multiple calls for wind data from renewables.ninja api

        Parameters
        ----------
        capacities : TYPE, optional
            DESCRIPTION. The default is [1].
        heights : TYPE, optional
            DESCRIPTION. The default is [80].
        years : TYPE, optional
            DESCRIPTION. The default is [2018].
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        """
        
        total_calls = (len(capacities)
                       * len(heights)
                       * len(years))
        data = pd.DataFrame({})
        calls = 0
        
        with tqdm(total = total_calls) as pbar:
            for capacity in capacities:
                for height in heights:
                    for year in years:
                        self._check_api_limit_pbar(pbar)
                        df, metadf = self.get_renewables_ninja_wind(
                            capacity=capacity,
                            height=height,
                            year=year,
                            **kwargs)
                        df["capacity"] = capacity
                        df["height"] = height
                        df["year"] = year
                        data = pd.concat([data, df])
                        calls += 1
                        pbar.update(1)
            pbar.close()
                        
        return data
                        


if __name__ == "__main__":

  
#%%  GMPA runs for temporary resource profiles Phase 2
# Save this script into GMPA folder, rather than STEVFNs folder

    root_dir = os.path.dirname(__file__)
    save_rn_data_folder = os.path.join(root_dir, "RenewablesNinjaData")
    if not os.path.exists(save_rn_data_folder):
        os.makedirs(save_rn_data_folder)
    
    countries = ['MAR', 'KEN', 'ZAF', 'KOR', 'EGY', 'NGA', 'BRA', 'COL', 'PER', 'CHL']
    lat_lon_df = pd.read_csv(os.path.join(root_dir, "lat–lon-data.csv"))
    lat_lon_df = lat_lon_df.set_index('Unnamed: 0')
    lat_lon_df = lat_lon_df.T
    
    for country in countries:
    
        lat = lat_lon_df.loc['lat', f'{country}']
        lat = np.int64(np.round((lat) / 0.5)) * 0.5
        lat = min(lat,90.0)
        lat = max(lat,-90.0)
        
        lon = lat_lon_df.loc['lon', f'{country}']
        lon = np.int64(np.round((lon) / 0.625)) * 0.625
        lon = min(lon, 179.375)
        lon = max(lon, -180.0)
    
       
        data = Renewables_Ninja(location=f'{lat}-{lon}',
                                latitude= lat,
                                longitude= lon,
                                user_token="ab8d801114b7545e85c09883f263cc9b339b7b54")   
        
        
        data_pv, data_pv_meta = data.get_renewables_ninja_PV(year=2019)
        data_pv.to_csv(os.path.join(save_rn_data_folder, f"{country}_PV_lat{lat}.csv"))
        
        data_wind, data_wind_meta = data.get_renewables_ninja_wind(year=2019)
        data_wind.to_csv(os.path.join(save_rn_data_folder, f"{country}_WINDONSHORE_lat{lat}.csv"))
    
    
    '''
    For Offshore wind, select coordinates in the sea closeby to country
    '''
    
    for country in countries:
    
        lat_off = lat_lon_df.loc['lat_offshore', f'{country}']
        lat_off = np.int64(np.round((lat_off) / 0.5)) * 0.5
        lat_off = min(lat_off,90.0)
        lat_off = max(lat_off,-90.0)
        
        lon_off = lat_lon_df.loc['lon_offshore', f'{country}']
        lon_off = np.int64(np.round((lon_off) / 0.625)) * 0.625
        lon_off = min(lon_off, 179.375)
        lon_off = max(lon_off, -180.0)
    
        data_offshore = Renewables_Ninja(location=f'{lat_off}-{lon_off}',
                                    latitude= lat_off,
                                    longitude= lon_off,
                                    user_token="ab8d801114b7545e85c09883f263cc9b339b7b54") 
        
        data_offshore, data_offshore_meta = data.get_renewables_ninja_wind(year=2019)
        data_offshore.to_csv(os.path.join(save_rn_data_folder, f"{country}_WINDOFFSHORE_lat{lat}.csv"))
        
    

    
    
    
