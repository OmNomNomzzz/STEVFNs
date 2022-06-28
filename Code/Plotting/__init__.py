#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 11:17:12 2021

@author: aniqahsan
"""
import numpy as np
import matplotlib.pyplot as plt

####### Define Classes #######


class stackplot_artist:
    """Class that takes assets and draws a stackplot """
    def __init__(self):
        self.flows_dictionary = dict()
        return
    
    def add_asset(self, asset_name, asset):
        self.flows_dictionary[asset_name] = asset.get_plot_data()
        return
    
    def set_times(self, times):
        self.times = times
        return
    
    def plot(self, show = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        if not(hasattr(self, "times")):
            self.times = np.arange(self.flows_dictionary[list(self.flows_dictionary)[0]].size)
        self.ax.stackplot(self.times, self.flows_dictionary.values(), labels = self.flows_dictionary.keys())
        self.ax.legend()
        if show == 1:
            plt.show()
        return


class bar_chart_artist2:
    """Class that takes assets and draws a bar graph"""
    def __init__(self, title = None):
        self.bars_dictionary = dict()
        self.group_names_list = []
        if title != None:
            self.title = title
        return
    
    def add_asset(self, asset_name, asset):
        if asset_name in self.bars_dictionary:
            self.bars_dictionary[asset_name] += [asset.size()]
        else:
            self.bars_dictionary[asset_name] = [asset.size()]
        return
    
    def add_group(self, group_name):
        self.group_names_list += [group_name] # list of group names
        return
    
    def plot(self, show =1, show_legend = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        width = 0.35
        asset_names_list = list(self.bars_dictionary.keys())
        N_assets = len(asset_names_list)
        N_groups = len(self.group_names_list)
        x = np.arange(N_groups)
        width = 1.0/(N_assets + 1)
        bars_list = []
        for counter1 in range(N_assets):
            asset_name = asset_names_list[counter1]
            bars_list += [self.ax.bar(x + width * (counter1-(N_assets-1)*0.5), 
                                      self.bars_dictionary[asset_name][:N_groups],
                                      width,
                                      label = asset_name)]
            # self.ax.bar_label(bars_list[counter1], padding=3)
            
        ### add some labels ###
        if hasattr(self, "title"):
            self.ax.set_title(self.title)
        self.ax.set_ylabel("Asset Size")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(self.group_names_list)
        self.ax.legend()
        
        self.fig.tight_layout()
        plt.show()
        return
        

class line_graph_artist:
    """Class that takes assets and draws a line graph"""
    def __init__(self):
        self.flows_dictionary = dict()
        return
    
    def add_asset(self, asset_name, asset):
        self.flows_dictionary[asset_name] = asset.get_plot_data()
        return
    
    def set_times(self, times):
        self.times = times
        return
    
    def plot(self, show = 1, show_legend = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        if not(hasattr(self, "times")):
            self.times = np.arange(self.flows_dictionary[list(self.flows_dictionary)[0]].size)
        for flow_name, flow in self.flows_dictionary.items():
            self.ax.plot(self.times, flow, label = flow_name)
        if show_legend == 1:
            self.ax.legend()
        if show == 1:
            plt.show()
        return


class multiple_artists:
    """Class that takes assets and draws multiple graphs"""
    def __init__(self):
        self.artist_dictionary = dict()
        return
    
    def add_artist(self, artist_name, artist):
        self.artist_dictionary[artist_name] = artist
        return
    
    def plot(self, figure_title = None, show_legend = 1):
        N_artists = len(self.artist_dictionary)
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots(len(self.artist_dictionary), 1, figsize=(6.4, 4.8))
        artist_names = list(self.artist_dictionary.keys())
        for counter1 in range(N_artists):
            artist_name = artist_names[counter1]
            artist = self.artist_dictionary[artist_name]
            artist.fig = self.fig
            artist.ax = self.ax[counter1]
            artist.plot(show = 0, show_legend = 1)
            artist.ax.set_title(artist_name)
        if figure_title != None:
            self.fig.suptitle(figure_title, y=1.03)
        self.fig.tight_layout()
        plt.show()
        return


class bar_chart_artist:
    """Class that takes assets and draws a bar graph"""
    def __init__(self, title = None):
        self.bar_data_dict = dict()
        self.x_ticks_data_dict = dict({
                                "ticks" : [],
                                "labels" : []
                                })
        if title != None:
            self.title = title
        return
    
    def plot(self, bar_width = 1.0, bar_spacing = 3.0, show =1, show_legend = 1):
        if not(hasattr(self, "fig")) or not(hasattr(self, "ax")):
            self.fig, self.ax = plt.subplots()
        #add bar charts
        bar_charts_list = []
        bar_names = list(self.bar_data_dict.keys())
        for counter1 in range(len(bar_names)):
            bar_name = bar_names[counter1]
            bar_data = self.bar_data_dict[bar_name]
            bar_charts_list += [self.ax.bar(
                            x = bar_data["x"],
                            height = bar_data["height"],
                            width = bar_width,
                            label = bar_name
                            )]
        ### add some labels ###
        if hasattr(self, "title"):
            self.ax.set_title(self.title)
        self.ax.set_xticks(self.x_ticks_data_dict["ticks"])
        self.ax.set_xticklabels(self.x_ticks_data_dict["labels"])
        self.ax.set_ylabel("Size of Assets")
        self.ax.legend(ncol = 2)
        self.fig.tight_layout()
        plt.show()
        return