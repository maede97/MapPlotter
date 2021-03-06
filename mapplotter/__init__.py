#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2019 Matthias Busenhart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module contains a simple plotter, which can receive data from map.geo.admin.ch, and plot the heights."""

__author__ = 'Matthias Busenhart'
__copyright__ = 'Copyright 2019, Matthias Busenhart'
__credits__ = "Matthias Busenhart"
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Matthias Busenhart'
__email__ = 'busenham@student.ethz.ch'
__status__ = 'Development'

import time
import pyperclip
import webbrowser
import PIL
import pyautogui as pya
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec, cm


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

class DataPoint:
    """simple Storage object for Datapoints"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Plotter:
    """
    Create 3D views from switzerland!
    Starts map.geo.admin.ch with given coordinates,
    then moves your mouse to points defined before, gets height of each point.
    Plots the crawled data in a plot.
    """
    def __init__(self, failsafe=True, wait_time = 0.2, browser_wait = 4, screen_boundary = (710, 535, 3610, 2050)):

        pya.FAILSAFE = failsafe # move to top left corner with mouse to stop crawling

        self.wait_time = wait_time
        self.browser_wait = browser_wait

        self.datapoints = []
        self.points = []

        self.menu_close = (500, 1380)

        self.click_offset = 50

        # Left top right bottom
        self.screen_boundary = screen_boundary

        self.image = None # background image

    def setCoords(self, long, lat):
        """Set coordinates from two numbers (CH1903 / LV03)"""
        self.long = long
        self.lat = lat

    def openBrowser(self):
        """starts browser tab with correct page"""
        url = "https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe&E=%s&N=%s&zoom=%s"
        url2 = url % (self.long, self.lat, self.level)
        webbrowser.open(url2)

    def copy(self):
        """returns current clipboard"""
        pya.hotkey('ctrl', 'c')
        time.sleep(self.wait_time)
        return pyperclip.paste()

    def setZoomLevel(self, level):
        """set zoom level of map"""
        self.level = level

    def getData(self, x, y):
        """let computer think that you clicked some stuff. gets data for you"""
        pya.rightClick(x,y) # perform right click to show Position overlay
        time.sleep(self.wait_time) # wait some time until page is ready
        pya.click(x,y+self.click_offset)
        pya.hotkey('ctrl','a') # select all text
        data = self.copy()
        data = data.split("Position")[1]
        data = data.split("Link mit Fadenkreuz")[0]
        data = data.split("\n")
        coord = data[2]
        height = data[-2]
        height = height.replace("Höhe\t","")
        coord = coord.replace("CH1903 / LV03\t","")
        height = height[:-2]
        height = float(height)
        coord = coord.replace("'","")
        coord = coord.replace(",","")
        coord = coord.split(" ")
        x = float(coord[0])
        y = float(coord[1])
        self.datapoints.append(DataPoint(x,y,height))

    def getAllPoints(self):
        """iterate over all points on screen and save their height
        failsafe: move mouse to top left corner"""
        self.openBrowser()
        time.sleep(self.browser_wait) # wait until browser is loaded
        pya.click(x=self.menu_close[0], y = self.menu_close[1])
        pya.moveTo(350, 1800)
        time.sleep(0.5)
        fullscreen = pya.screenshot()
        self.image = fullscreen.crop(self.screen_boundary)
        for p in self.points:
            x,y = p[0],p[1]
            try:
                self.getData(x,y)
            except pya.FailSafeException:
                print("FailSafe triggered")
                return
        pya.hotkey('ctrl', 'w') # close tab

    def setCoordsFromString(self, s):
        """pass a string to extract the starting coords,
        see setCoords(long, lat) for other method"""
        s = s.replace("'",'')
        s = s.replace(',','')
        s = s.split(" ")
        self.long = int(float(s[0]))
        self.lat = int(float(s[1]))

    def getX(self):
        """returns all x points as an array"""
        data = []
        for DP in self.datapoints:
            data.append(DP.x)
        return data
    def getY(self):
        """returns all y points as an array"""
        data = []
        for DP in self.datapoints:
            data.append(DP.y)
        return data
    def getZ(self):
        """returns all z points as an array"""
        data = []
        for DP in self.datapoints:
            data.append(DP.z)
        return data
    def saveDataToFile(self, filename="data"):
        """save point data to disk, using the filename given"""
        x = self.getX()
        y = self.getY()
        z = self.getZ()
        with open(filename+".xyz","w") as wr:
            wr.write("%s %s\n" % (self.x_am, self.y_am))
            for DP in self.datapoints:
                wr.write("%s %s %s\n" % (DP.x, DP.y, DP.z))
        self.image.save(filename+".png")
    def setPoints(self, x_am, y_am):
        """set amount of points, good where: 20, 8"""
        #Top left:
        x_start = self.screen_boundary[0]
        y_start = self.screen_boundary[1]

        x_total = self.screen_boundary[2] - x_start
        y_total = self.screen_boundary[3] - y_start

        x_offset = int(x_total / (x_am-1))
        y_offset = int(y_total / (y_am-1))

        self.x_am = x_am
        self.y_am = y_am

        for i in range(x_am):
            for j in range(y_am-1, -1, -1):
                self.points.append([x_start + i * x_offset, y_start + j * y_offset])
    def loadFromFile(self, filename):
        """load data from file. Needs filename.xyz and filename.png to exist
        where filename.xyz contains amount of points on first line:
        xAmount yAmount"""

        lines = [line.rstrip('\n') for line in open(filename+".xyz")]
        # first lines contains x_am, y_am
        x_am, y_am = lines[0].split(" ")
        self.x_am = int(x_am)
        self.y_am = int(y_am)
        lines = lines[1:]
        for line in lines:
            x,y,z = line.split(" ")
            x = float(x)
            y = float(y)
            z = float(z)
            self.datapoints.append(DataPoint(x,y,z))
        self.image = PIL.Image.open(filename+".png")

    def handlePlotClick(self, event):
        if(event.button != 1): # only left click
            return
        if(isinstance(event.inaxes,Axes3D)): # only on bottom two plots
            return
        # we need to add a dot here
        # can't add dot in 3D, because of wrong layering at 3d rendering
        self.ax2.scatter(event.xdata, event.ydata, s=50,c="red")
        self.ax3.scatter(event.xdata, event.ydata, s=50,c="red")

        plt.draw() # redraw plot

    def plot(self, overlay=False):
        """show a simple plot: 3D on top, contourf bottom left and image bottom right"""
        X = self.getX()
        Y = self.getY()
        Z = self.getZ()

        fig = plt.figure()

        fig.suptitle("MapPlotter")

        gs = gridspec.GridSpec(2,20)

        self.ax1 = fig.add_subplot(gs[0,:], projection='3d')
        triang = mtri.Triangulation(X, Y)
        self.ax1.plot_trisurf(triang, Z)

        self.ax1.set_xlabel("Ost-West")
        self.ax1.set_ylabel("Nord-Süd")
        self.ax1.set_zlabel("Höhe ü. M.")

        self.ax2 = fig.add_subplot(gs[1,2:11])
        Z_ = np.array(Z)
        Z_ = Z_.reshape(-1, self.y_am) # my points start at bottom
        Z_ = np.transpose(Z_)

        self.ax2.set_aspect("equal")
        
        p = self.ax2.contourf(Z_, cmap = cm.coolwarm, extent=[min(X), max(X), min(Y), max(Y)])

        self.ax3 = fig.add_subplot(gs[1,11:])
        self.ax3.yaxis.tick_right()
        self.ax3.yaxis.set_label_position("right")
        self.ax3.imshow(self.image,extent=[min(X), max(X), min(Y), max(Y)])
        if(overlay):
            self.ax3.contourf(Z_,cmap=cm.coolwarm,extent=[min(X), max(X), min(Y), max(Y)],alpha=0.5)
        ax4 = fig.add_subplot(gs[1,0])
        ax4.yaxis.tick_left()
        ax4.yaxis.set_label_position("left")
        plt.colorbar(p, cax=ax4, shrink=0.1)

        fig.canvas.mpl_connect('button_press_event',self.handlePlotClick)
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()