#!/usr/bin/env python

import wx
import wx.grid
import numpy as np
import csv
import os
import sys
import glob
import subprocess
import datetime
import shutil
import time
import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.font_manager import FontProperties
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from pandas import *
from wx.lib import sheet
from threading import *

class splashScreen(wx.SplashScreen):
    def __init__(self, parent=None):
        tobitmap = wx.Image(name= "logo_splash_2.jpg").ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 4000
        wx.SplashScreen.__init__(self, tobitmap, splashStyle, splashDuration, parent)
        
    def OnExit(self, evt):
        self.Hide()
        MyFrame = App(None, -1, "-")
        app.SetTopWindow(MyFrame)
        MyFrame.Show(True)
        evt.Skip()

class newgraph(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, id)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def plot(self, selectionAll, selectionG, selectionX, selectionY):
        
#         count = 0
#         keep = True
#         progress = wx.ProgressDialog("Creating graphs...", "Plotting data with selected values")
#         while keep and count < 10:
#                 count = count + 1
#                 keep = progress.Update(count)
#         progress.Destroy()
        
        windspd = {}
        FV = {}
        plot = {}
        preffix = "vpp_output_"
        xaxis = selectionX
        yaxis = selectionY
        fontp = FontProperties()
        fontp.set_size('small')
        plot = {}
        angles = np.arange(0,360,15)
        markers = ["-", "--", "-.", ":", ".", "o", "^", "<", ">", "1", "2", "3", "4", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_", "-", "--", "-.", ":", ".", "o", "^", "<", ">", "1", "2", "3", "4", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
        if selectionG == "Rectangular":
            if selectionAll == "All":
                for i in range(len(ficheros)):
                    windspd[i] = dataf[i].TWS.unique()
                    if i == 0:
                        windsp = windspd[i]
                    else:
                        windsp = np.concatenate((windsp,windspd[i]), axis=0) 
                    windspdef = set(windsp)
                for speed in windspdef:
                    for i in range(len(ficheros)):
                        FV[speed] = dataf[i][dataf[i]['TWS']==speed]
                        labels = nname[i]+"_TWS_"+str(speed)
                        if FV[speed].empty:
                            continue
                        else:
                            plot[speed] = FV[speed][[xaxis, yaxis]]
                            xvalue = FV[speed][selectionX]
                            yvalue = FV[speed][selectionY]
                            ax = plt.subplot(111)
                            if len(plot[speed])==1:
                                marker = markers[int(speed)]
                                #plot[speed].plot(x=xaxis, y=yaxis, marker=marker, label=labels)
                                ax.plot(xvalue, yvalue, label=labels, marker=marker)
                                plt.ylabel(yaxis)
                                plt.xlabel(xaxis)
                                #limits = ax.axis()
#                                 ax.xaxis.set_major_locator(plt.MultipleLocator(10))
#                                 ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
#                                 ax.yaxis.set_major_locator(plt.MultipleLocator(10))
#                                 ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#                                 ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
#                                 ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
#                                 ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
#                                 ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
                                ax.grid(True)
                                #plt.title("Boat performance@TWS_"+str(speed))
                                plt.title("Boat performance")
                                if xaxis == "TWA":
                                    plt.axis([30, 180, 0, 30])
                                    plt.legend(loc='best', prop=fontp)
                                else:
                                    plt.legend(loc='best', prop=fontp)
                                    continue
                                
                            else:
                                marker = markers[int(speed)]
                                #plot[speed].plot(x=xaxis, y=yaxis, label=labels)
                                ax.plot(xvalue, yvalue, label=labels, marker=marker)
                                plt.ylabel(yaxis)
                                plt.xlabel(xaxis)
                                #limits = ax.axis()
#                                 ax.xaxis.set_major_locator(plt.MultipleLocator(10))
#                                 ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
#                                 ax.yaxis.set_major_locator(plt.MultipleLocator(10))
#                                 ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#                                 ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
#                                 ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
#                                 ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
#                                 ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
                                ax.grid(True)
                                plt.title("Boat performance")
                                if xaxis == "TWA":
                                    plt.axis([30, 180, 0, 30])
                                    plt.legend(loc='best', prop=fontp)
                                else:
                                    plt.legend(loc='best', prop=fontp)
                                    continue
                plt.show()        
            else:
                n = len(ficheros)+1
                lname[n] = os.path.splitext(selectionAll)[0]
                nname[n] = lname[n].replace(preffix, "")
                tempname = "_csv_processed.csv"
                tempfile[n] = os.path.join(lname[n] + tempname)
                dataf[n] = read_csv(tempfile[n]) 
                windspd[n] = dataf[n].TWS.unique()
                windsp = windspd[n]
                windspdef = set(windsp)
                for speed in windspdef:
                    FV[speed] = dataf[n][dataf[n]['TWS']==speed]
                    labels = nname[n]+"_TWS_"+str(speed)
                    if FV[speed].empty:
                        continue
                    else:
                        plot[speed] = FV[speed][[xaxis, yaxis]]
                        xvalue = FV[speed][selectionX]
                        yvalue = FV[speed][selectionY]
                        ax = plt.subplot(111)
                        if len(plot[speed])==1:
                            marker = markers[int(speed)]
                            #plot[speed].plot(x=xaxis, y=yaxis, marker=marker, label=labels)
                            ax.plot(xvalue, yvalue, label=labels, marker=marker)
                            plt.ylabel(yaxis)
                            plt.xlabel(xaxis)
#                             ax.xaxis.set_major_locator(plt.MultipleLocator(10))
#                             ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
#                             ax.yaxis.set_major_locator(plt.MultipleLocator(10))
#                             ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#                             ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
#                             ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
#                             ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
#                             ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
                            ax.grid(True)
                            plt.title("Boat performance")
                            if xaxis == "TWA":
                                plt.axis([30, 180, 0, 30])
                                plt.legend(loc='best', prop=fontp)
                            else:
                                plt.legend(loc='best', prop=fontp)
                                continue
                        else:
                            marker = markers[int(speed)]
                            #plot[speed].plot(x=xaxis, y=yaxis, label=labels)
                            ax.plot(xvalue, yvalue, label=labels, marker=marker)
                            plt.ylabel(yaxis)
                            plt.xlabel(xaxis)
#                             ax.xaxis.set_major_locator(plt.MultipleLocator(10))
#                             ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
#                             ax.yaxis.set_major_locator(plt.MultipleLocator(10))
#                             ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
#                             ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
#                             ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
#                             ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
#                             ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
                            ax.grid(True)
                            plt.title("Boat performance")
                            if xaxis == "TWA":
                                plt.axis([30, 180, 0, 30])
                                plt.legend(loc='best', prop=fontp)
                            else:
                                plt.legend(loc='best', prop=fontp)
                                continue
                plt.show()
        else:
            if selectionAll == "All":
                for i in range(len(ficheros)):
                    windspd[i] = dataf[i].TWS.unique()
                    if i == 0:
                        windsp = windspd[i]
                    else:
                        windsp = np.concatenate((windsp,windspd[i]), axis=0) 
                    windspdef = set(windsp)
                for speed in windspdef:
                    for i in range(len(ficheros)):
                            FV[speed] = dataf[i][dataf[i]['TWS']==speed]
                            if FV[speed].empty:
                                continue
                            else:
                                label = nname[i]
                                label_speed = nname[i]+"_TWS_"+str(speed)
                                ax = plt.subplot(111, polar=True)
                                ax.set_theta_zero_location("N")
                                ax.set_theta_direction(-1)
                                plot[speed] = FV[speed][['TWA', 'BoatSpeed']]
                                if len(plot[speed])==1:
                                    TWA = []
                                    TWA = FV[speed].TWA
                                    TWA_rad = []
                                    TWA_rad = TWA*np.pi/180
                                    BS = FV[speed].BoatSpeed
                                    marker = markers[int(speed)]
                                    ax.plot(TWA_rad, BS, label=label_speed, marker=marker)
                                    plt.ylabel('BoatSpeed')
                                    plt.xlabel('TWA')
                                    plt.title("Boat performance: polars diagram")
                                    plt.legend(loc='lower center', mode="expand", ncol=5, prop ={'size':8})
                                    plt.grid(True)
                                else:
                                    TWA = []
                                    TWA = FV[speed].TWA
                                    TWA_rad = []
                                    TWA_rad = TWA*np.pi/180
                                    BS = FV[speed].BoatSpeed
                                    marker = markers[int(speed)]
                                    ax.plot(TWA_rad, BS, label=label_speed, marker=marker)
                                    plt.ylabel('BoatSpeed')
                                    plt.xlabel('TWA')
                                    plt.title("Boat performance: polars diagram")
                                    plt.legend(loc='lower center', mode="expand", ncol=5, prop ={'size':8})
                                    plt.grid(True)
                plt.show()
            else:
                n = len(file)+1
                lname[n] = os.path.splitext(selectionAll)[0]
                nname[n] = lname[n].replace(preffix, "")
                tempname = "_csv_processed.csv"
                tempfile[n] = os.path.join(lname[n] + tempname)
                dataf[n] = read_csv(tempfile[n]) 
                windspd[n] = dataf[n].TWS.unique()
                windsp = windspd[n]
                windspdef = set(windsp)
                for speed in windspdef:
                        FV[speed] = dataf[n][dataf[n]['TWS']==speed]
                        if FV[speed].empty:
                            continue
                        else:
                            label = nname[n]
                            label_speed = nname[n]+"_TWS_"+str(speed)
                            ax = plt.subplot(111, polar=True)
                            ax.set_theta_zero_location("N")
                            ax.set_theta_direction(-1)
                            plot[speed] = FV[speed][['TWA', 'BoatSpeed']]
                            if len(plot[speed])==1:
                                TWA = []
                                TWA = FV[speed].TWA
                                TWA_rad = []
                                TWA_rad = TWA*np.pi/180
                                BS = FV[speed].BoatSpeed
                                marker = markers[int(speed)]
                                ax.plot(TWA_rad, BS, label=label_speed, marker=marker)
                                plt.ylabel('BoatSpeed')
                                plt.xlabel('TWA')
                                plt.title("Boat performance: polars diagram")
                                plt.legend(loc='lower center', mode="expand", ncol=5, prop ={'size':8})
                                plt.grid(True)
                            else:
                                TWA = []
                                TWA = FV[speed].TWA
                                TWA_rad = []
                                TWA_rad = TWA*np.pi/180
                                BS = FV[speed].BoatSpeed
                                marker = markers[int(speed)]
                                ax.plot(TWA_rad, BS, label=label_speed, marker=marker)
                                plt.ylabel('BoatSpeed')
                                plt.xlabel('TWA')
                                plt.title("Boat performance: polars diagram")
                                plt.legend(loc='lower center', mode="expand", ncol=5, prop ={'size':8})
                                plt.grid(True)
                plt.show()

class App(wx.Frame):
         
    def OnExit(self, event):
        global directory
        if directory:
            os.chdir(directory)
            shutil.rmtree(tempdir)
            self.Destroy()
        else:
            self.Destroy()
    
    def twiddle(self):
        x,y = self.GetSize()
        self.SetSize((x, y+1))
        self.SetSize((x,y))
        
    def OnFiles(self, event):
        global selectionAll
        selectionAll = self.choiceF.GetStringSelection()
        return selectionAll
    
    def OnGraphType(self, event):
        global selectionG
        selectionG = self.choiceT.GetStringSelection()
        if selectionG == "Polar":
            global selectionX 
            selectionX = ""
            global selectionY 
            selectionY = ""
            return selectionG, selectionX, selectionY
        else:
            return selectionG
        
    def OnFixed(self, event):
        global selectionFV 
        selectionFV = self.choiceV.GetStringSelection()
        return selectionFV
        
    def OnAxisX(self, event):
        global selectionX 
        selectionX = self.choiceX.GetStringSelection()
        return selectionX
        
    def OnAxisY(self, event):
        global selectionY 
        selectionY = self.choiceY.GetStringSelection()
        return selectionY
        
    def OnGraph(self, event):
        #try:
        ngraph = newgraph(parent=None, id=-1)
        ngraph.plot(selectionAll, selectionG, selectionX, selectionY)
        
    def onOpen(self, event):
        
        wildcard = '*.csv'
        dlg = wx.FileDialog(None, "Choose a csv file:", defaultFile="", wildcard=wildcard, style=wx.DD_CHANGE_DIR)
        
        if dlg.ShowModal() == wx.ID_OK:
            dir = dlg.GetPath()
            global directory
            directory = os.path.split(dir)[0]
            print(directory)
            os.chdir(directory)
            global file2read
            global dataf
            global nname 
            global lname
            global tempfile
            global ficheros
            global tempdir
            tempdir = os.path.join(directory + '\\temp')
            print(tempdir)
            file2read = os.path.split(dir)[1]
            lname = file2read
            preffix = "vpp_output_"
            fontp = FontProperties()
            fontp.set_size('small')
            csv_header = ["Hull", "Sailset", "Sail Trim", "Dagger", "Canting", "Trim Tab", "TWS", "TWA", "AWS_mh", "AWA_mh", "TWS_ce", "AWS_ce", "AWA_ce", "TWS_10m", "AWS_10m", "AWA_10m", "BoatSpeed", "VMG", "Heel", "Leeway", "Rudder", "WS", "Trim", "Sink", "Mass", "Xcg", "Ycg", "Zcg", "Flat", "Cl", "Cd", "Cup", "h", "Xce", "Yce", "Zce", "Heeling Force", "Righting Moment", "Sails Fx", "Sails Fy", "Sails Fz", "Sails Mx", "Sails My", "Sails Mz", "Hull Fx", "Hull Fy", "Hull Fz", "Hull Mx", "Hull My", "Hull Mz", "Delta_Mx", "Delta_Mx_deflection", "Keel Fx", "Keel Fy", "Keel Fz", "Keel Mx", "Keel My", "Keel Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "Bulb Fx", "Bulb Fy", "Bulb Fz", "Bulb Mx", "Bulb My", "Bulb Mz", "Cl", "Cd", "SCl", "SCd", "h", "Dagger Fx", "Dagger Fy", "Dagger Fz", "Dagger Mx", "Dagger My", "Dagger Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "Rudder Fx", "Rudder Fy", "Rudder Fz", "Rudder Mx", "Rudder My", "Rudder Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "R_Angle", "STRB_Rudder Fx", "STRB_Rudder Fy", "STRB_Rudder Fz", "STRB_Rudder Mx", "STRB_Rudder My", "STRB_Rudder Mz", "AoA", "Cl", "Cd", "h", "WS", "R_Angle", "Hull Area", "Hull Fx", "Hull Fy", "Hull Fz", "Hull Mx", "Hull My", "Hull Mz", "Cl", "Cd", "Cup", "h", "Xce", "Yce", "Zce", "Rudder Fx", "Rudder Fy", "Rudder Fz", "Rudder Mx", "Rudder My", "Rudder Mz", "Rig Area", "Rig Fx", "Rig Fy", "Rig Fz", "Rig Mx", "Rig My", "Rig Mz", "Rig Cl", "Rig Cd", "Cup", "h", "Xce", "Yce", "Zce", "Drag", "Side Force", "RFx", "RFy", "RFz", "RMx", "RMy", "RMz", "", ""]
            dataf = {}
            windspd = {}
            tempfile = {}
            #noftabs = len(files)
            dims = []
            datacols = []
            datarows = []
            ficheros = ""
            if os.path.isdir(tempdir):
                pass
            else:
                os.mkdir("temp")
            shutil.copy(file2read, "temp")
            os.chdir("temp")
            nname = file2read.replace(preffix, "")
            tempname = "_csv_processed.csv" 
            tempfile = os.path.join(file2read + tempname )
            ficheros = ficheros + tempfile
            csv_newfile = open(tempfile, "ab")
            csv_newwrite = csv.writer(csv_newfile)
            csv_newwrite.writerow(csv_header)
            csv_file = open(file2read, "rb")
            reader_file = csv.reader(csv_file, delimiter=',')
            for row in reader_file:
                if len(row)> 9:
                    csv_newwrite.writerow(row)
            csv_file.close()
            csv_newfile.close()
            dataf = read_csv(tempfile)
            dims = dataf.shape
            datarows = dims[0]
            datacols = dims[1]
            matriz = np.array(dataf)
            
            if getattr(self, 'grid', 0):
                self.grid.Destroy()
            self.grid = wx.grid.Grid(self.nbk, 0)
            self.grid.CreateGrid(datarows, datacols)
                 
            for p in range(len(csv_header)):
                self.grid.SetColLabelValue(p, csv_header[p])
                 
            for row in range(datarows):
                for col in range(datacols):
                    self.grid.SetCellValue(row,col,str(matriz[row][col]))
                             
            self.grid.AutoSizeColumns(True)
            self.nbk.AddPage(self.grid, nname, select=True)
            
            
            #grid_sizer = wx.BoxSizer(wx.VERTICAL)
            #grid_sizer.Add(self.nbk ,1 , wx.ALL|wx.EXPAND, 5)
            #self.panel = wx.Panel(self.nbk, -1)
            #self.panel.SetSizer(grid_sizer)
            #self.bottom_panel.SetSizer(grid_sizer)
            #self.panel.Layout()
            #self.bottom_panel.Layout()
            
        dlg.Destroy()
            
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'JYD VPP grapher')
        
        mySplash = splashScreen()
        mySplash.Show()
        wx.Sleep(2)
        
        self.nbk = wx.Notebook(self, id=wx.ID_ANY, style=wx.NB_TOP)
        
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
        file_menu = wx.Menu()
        
        menu_item = file_menu.Append(wx.ID_OPEN, '&Open...', 'Open and read a CSV file')
        self.Bind(wx.EVT_MENU, self.onOpen, menu_item)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, '&File')
        self.SetMenuBar(menu_bar)
        self.Show()
        self.Maximize()
#         self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.SetMinSize(wx.Size(900,600))
#         self.bottom_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         bottomSizer = wx.BoxSizer(wx.VERTICAL)
#         #self.bottom_panel.SetSizer( bottomSizer )
#         #self.bottom_panel.Layout()
#         bottomSizer.Fit( self.bottom_panel )
#         sizer.Add( self.bottom_panel, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        #self.grid_panel =  wx.Panel(self.nbk, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        #self.grid_panel.SetSizer( grid_sizer )
        #self.grid_panel.Layout()
        #grid_sizer.Fit( self.grid_panel )
        #sizer.Add( self.grid_panel, 1, wx.EXPAND |wx.ALL, 5 )
        #grid_sizer.Add(self.grid, 1, wx.EXPAND)
        
        #self.nbk.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.tabChanged)
        #self.nbk.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.tabChanging)
        
        
        
#         filelist = ["", "All"]
#         i = 0
#         while (i < len(files)):
#             filelist.append(files[i])
#             i += 1
#             
#         self.top_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
#         topSizer = wx.BoxSizer( wx.HORIZONTAL )
#         
#         self.stextF = wx.StaticText(self.top_panel, wx.ID_ANY, u"Select files to graph:", wx.DefaultPosition, wx.DefaultSize, 0)
#         topSizer.Add(self.stextF, 0, wx.ALL, 5)
#         self.choiceF = wx.Choice(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=filelist)
#         topSizer.Add(self.choiceF, 0, wx.ALL, 5)
#         self.Bind(wx.EVT_CHOICE, self.OnFiles, self.choiceF)
#         
#         samplelist_type = ["", "Rectangular", "Polar"]
#         self.stextT = wx.StaticText(self.top_panel, wx.ID_ANY, u"Select graph type:", wx.DefaultPosition, wx.DefaultSize, 0)
#         topSizer.Add(self.stextT, 0, wx.ALL, 5)
#         self.choiceT = wx.Choice(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=samplelist_type)
#         topSizer.Add(self.choiceT, 0, wx.ALL, 5)
#         self.Bind(wx.EVT_CHOICE, self.OnGraphType, self.choiceT)
#         
#         samplelist_fixed = ["", "TWS", "AWS"]
#         samplelist = ["", "Dagger", "Canting", "Trim Tab", "TWS", "TWA", "AWS_mh", "AWA_mh", "TWS_ce", "AWS_ce", "AWA_ce", "TWS_10m", "AWS_10m", "AWA_10m", "BoatSpeed", "VMG", "Heel", "Leeway", "Rudder", "WS", "Trim", "Sink", "Mass", "Xcg", "Ycg", "Zcg", "Flat", "Cl", "Cd", "Cup", "h", "Xce", "Yce", "Zce", "Heeling Force", "Righting Moment", "Sails Fx", "Sails Fy", "Sails Fz", "Sails Mx", "Sails My", "Sails Mz", "Hull Fx", "Hull Fy", "Hull Fz", "Hull Mx", "Hull My", "Hull Mz", "Delta_Mx", "Delta_Mx_deflection", "Keel Fx", "Keel Fy", "Keel Fz", "Keel Mx", "Keel My", "Keel Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "Bulb Fx", "Bulb Fy", "Bulb Fz", "Bulb Mx", "Bulb My", "Bulb Mz", "Cl", "Cd", "SCl", "SCd", "h", "Dagger Fx", "Dagger Fy", "Dagger Fz", "Dagger Mx", "Dagger My", "Dagger Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "Rudder Fx", "Rudder Fy", "Rudder Fz", "Rudder Mx", "Rudder My", "Rudder Mz", "AoA", "Cl", "Cd", "SCl", "SCd", "h", "R_Angle", "STRB_Rudder Fx", "STRB_Rudder Fy", "STRB_Rudder Fz", "STRB_Rudder Mx", "STRB_Rudder My", "STRB_Rudder Mz", "AoA", "Cl", "Cd", "h", "WS", "R_Angle", "Hull Area", "Hull Fx", "Hull Fy", "Hull Fz", "Hull Mx", "Hull My", "Hull Mz", "Cl", "Cd", "Cup", "h", "Xce", "Yce", "Zce", "Rudder Fx", "Rudder Fy", "Rudder Fz", "Rudder Mx", "Rudder My", "Rudder Mz", "Rig Area", "Rig Fx", "Rig Fy", "Rig Fz", "Rig Mx", "Rig My", "Rig Mz", "Rig Cl", "Rig Cd", "Cup", "h", "Xce", "Yce", "Zce", "Drag", "Side Force", "RFx", "RFy", "RFz", "RMx", "RMy", "RMz"]
#         
#         self.stextX = wx.StaticText(self.top_panel, wx.ID_ANY, u"Select value for X:", wx.DefaultPosition, wx.DefaultSize, 0)
#         topSizer.Add(self.stextX, 0, wx.ALL, 5)
#         self.choiceX = wx.Choice(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=samplelist)
#         topSizer.Add(self.choiceX, 0, wx.ALL, 5)
#         self.Bind(wx.EVT_CHOICE, self.OnAxisX, self.choiceX)
#         
#         self.stextY = wx.StaticText(self.top_panel, wx.ID_ANY, u"Select value for Y:", wx.DefaultPosition, wx.DefaultSize, 0)
#         topSizer.Add(self.stextY, 0, wx.ALL, 5)
#         self.choiceY = wx.Choice(self.top_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choices=samplelist)
#         topSizer.Add(self.choiceY, 0, wx.ALL, 5)
#         self.Bind(wx.EVT_CHOICE, self.OnAxisY, self.choiceY)
#         
#         self.GraphButton = wx.Button(self.top_panel, wx.ID_ANY, u"Graph Values", wx.DefaultPosition, wx.DefaultSize, 0)
#         topSizer.Add(self.GraphButton, 0, wx.ALL, 5)
#         self.Bind(wx.EVT_BUTTON, self.OnGraph, self.GraphButton)
#         
#         self.top_panel.SetSizer(topSizer)
#         self.top_panel.Layout()
#         topSizer.Fit( self.top_panel )
#         sizer.Add( self.top_panel, 0, wx.EXPAND|wx.ALL, 5 )
# 
#         self.SetSizer( sizer )
#         self.Layout()
#         self.Maximize()
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = App(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
        
