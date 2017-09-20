# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:31:22 2017

@author: Khalil Al Hooti
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar 
 
class Mapp:
    
    def __init__(self, well = None, vibs = None, vib_numb = None, well_name = None, vib_name=None):
        self.well     = well
        self.vibs     = vibs
        self.vib_numb = vib_numb
        self.well_name = None
        self.vib_name = None
        
        
    @property    
    def azimuth(self):
        self.azim =     pd.read_excel('v1contract.xlsx', names = ['Azimuth'],
                                      sheetname=self.well, parse_cols=[self.vibs],
                                     dtype={'Azimuth':np.float})
        return self.azim
    
    @property
    def well_loc(self):
        well_location =    pd.read_excel('locations.xlsx', names =['well', 'x', 'y'],header=None,
                                         sheetname=self.well, parse_cols=[0,1,2],
                                        dtype={'x':np.float, 'y':np.float})
        self.well_location = well_location.iloc[8]
        return self.well_location
    
    @property
    def vib_loc(self):
        vib_location =    pd.read_excel('locations.xlsx', names =['vib', 'x', 'y'],header=None,
                                        sheetname=self.well, parse_cols=[0,1,2],
                                       dtype={'x':np.float, 'y':np.float})
        self.vib_location = vib_location.iloc[self.vib_numb]
        return self.vib_location
    
    @property
    def plotting(self):
        well_x = self.well_loc.x
        well_y = self.well_loc.y

        vib_x = self.vib_loc.x
        vib_y = self.vib_loc.y

        legendEntries=[]
        legendText = ['Geop 1', 'Geop 2', 'Geop 3', 'Geop 4', 'Geop 5', 'Geop 6', 'Geop 7', 'Geop 8']
        
        wieght =np.sqrt((well_x-vib_x)**2 - (well_y-vib_y)**2)

        fig, ax = plt.subplots(figsize= (8,8))
        counter = 0
        
        for m in self.azimuth.Azimuth:
            g_x = well_x + np.sin(np.deg2rad(m)) * 160*wieght
            g_y = well_y + np.cos(np.deg2rad(m)) * 160*wieght
        
            x = [well_x,g_x]
            y = [well_y, g_y]
           
           
            legendEntries.append(ax.plot(x,y, label= legendText[counter]))
            
            if m >=0 and m < 180: 
                ax.arrow(g_x, g_y, 0.1, 0.1*np.tan(np.deg2rad(90-m)), shape = 'full', lw = 0,
                 length_includes_head = False, width =2)
            elif m>=180 and m <360:
                ax.arrow(g_x, g_y, -0.1, -0.1*np.tan(np.deg2rad(90-m)), shape = 'full', lw = 0,
                 length_includes_head = False, width =2)
            counter+=1
        
            
        ax.scatter(well_x, well_y, s = 300, marker = '*', c = 'k', label = 'MS well {}'.format(self.well_name))
        ax.scatter(vib_x, vib_y, s =  100, marker = 'D', c = 'r', label = 'Vib shot {}'.format(self.vib_name))
        ax.ticklabel_format(useOffset=False)
        
        # box = ax.get_position()
        # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        plt.legend(labelspacing= 1, fontsize = 11, loc = 'best',  shadow=False, ncol=2)
        ax.axis('equal')
        ax.set_xlabel('Easting')
        ax.set_ylabel('Northing')
        scalebar = ScaleBar(1.0, location = 'lower right', height_fraction = 0.005, pad = 1)
        plt.gca().add_artist(scalebar)
        ax.grid(linestyle='-', linewidth=0.2)
    
