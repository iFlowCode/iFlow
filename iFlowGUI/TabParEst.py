#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      user
#
# Created:     02/18/2021
# Copyright:   (c) user 2021
#              Center for Ecohydraulics
#              University of Idaho
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import standard library
# # import os,sys
# from typing import Text
from asyncio.selector_events import BaseSelectorEventLoop
from signal import Signals
import PyQt5.QtWidgets as PQW
# # import PyQt5.QtGui as PQG
# # import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import glob
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
import pandas as pd
# # # import pickle
# # import datetime
# # import time
# # import numpy as np
from matplotlib.ticker import FormatStrFormatter
# from pandas.core.indexes.base import Index
# # Import custom library
from Variables import VAR
from ScrollLabel import ScrollLabel
import TabParEst as TPE
# # import STabFFTAnal as STFA
# # import STabLPMAnal as STLA

import WizardPE as WPE
#------------------------------------------------------------------------------#
'''
TabParEst Class
'''
class TabParEst(PQW.QWidget):
    def __init__(self):
        super().__init__()
        print('TabParEst - Start Class')
# Set Matplotlib fonts size
        TabParEst.MPL_AxisTitle = int(VAR.GetMPLAxisTitleFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabParEst.MPL_AxisTick = int(VAR.GetMPLAxisTickFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabParEst.MPL_Legend = int(VAR.GetMPLLegendFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
# Store class object
        VAR.SetTabParEst(VAR, self)
# Create grid layot for the window
        Layout_Tab_ParEst = PQW.QGridLayout()
# Button Calculate
        TabParEst.Button_PE = PQW.QPushButton('Parameter Estimation')
#!         TabParEst.Button_PE.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
#!         TabParEst.Button_PE.setToolTip('Launch Parameter Estimation Wizard') # Tooltip message
        TabParEst.Button_PE.clicked.connect(self.on_Button_PE_clicked) # Button event Click on
# Groupbox Filter
        self.GroupBox_Filter = PQW.QGroupBox('Filter:')
# Create the Layout for the Groupbox Filter
        self.VBoxFilter = PQW.QVBoxLayout()
# Label
        Label_Method = PQW.QLabel('Method:')
# Element ComboBox Method
        TabParEst.Combobox_Method = PQW.QComboBox()
#!         TabParEst.Combobox_Method.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
#!         TabParEst.Combobox_Method.setToolTip('Filter results by method') # Tooltip message
        #
        for item in VAR.GetEstimationMethod(VAR):
            TabParEst.Combobox_Method.addItem(item)
        #
        TabParEst.Combobox_Method.currentIndexChanged.connect(self.on_Combobox_Method_change) # ComboBox event change item
# Add elements to the Layout
        self.VBoxFilter.addWidget(Label_Method)
        self.VBoxFilter.addWidget(TabParEst.Combobox_Method)
# Add the Layout to the Groupbox Filter
        self.GroupBox_Filter.setLayout(self.VBoxFilter)
# Groupbox Chart
        self.GroupBox_Chart = PQW.QGroupBox('Chart:')
# Create the lyout for the Groupbox Chart
        self.VBoxChart = PQW.QVBoxLayout()
# Label
        Label_Analysis = PQW.QLabel('Analysis:')
# Element ComboBox Analysis
        TabParEst.Combobox_Analysis = PQW.QComboBox()
#!         TabParEst.Combobox_Analysis.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
#!         TabParEst.Combobox_Analysis.setToolTip('Choose analysis to show') # Tooltip message
        TabParEst.Combobox_Analysis.currentIndexChanged.connect(self.on_Combobox_Analysis_change) # ComboBox event change item
# Label
        Label_ChartType = PQW.QLabel('Chart type:')
# Element Combobox ChartType
        TabParEst.Combobox_ChartType = PQW.QComboBox()
#!         TabParEst.Combobox_ChartType.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
#!         TabParEst.Combobox_ChartType.setToolTip('Choose the data to display') # Tooltip message
        #
        for item in VAR.GetChartTypeParameterEstimation(VAR):
            TabParEst.Combobox_ChartType.addItem(item)
        #
        TabParEst.Combobox_ChartType.currentIndexChanged.connect(self.on_Combobox_ChartType_change) # ComboBox event change item
# Add elements to the Layout
        self.VBoxChart.addWidget(Label_Analysis)
        self.VBoxChart.addWidget(TabParEst.Combobox_Analysis)
        self.VBoxChart.addWidget(Label_ChartType)
        self.VBoxChart.addWidget(TabParEst.Combobox_ChartType)
# Add the Layout to the Groupbox Chart
        self.GroupBox_Chart.setLayout(self.VBoxChart)
# Groupbox Report
        self.GroupBox_Report = PQW.QGroupBox('Report:')
# Create Layout for the Groupbox Report
        self.VBoxReport = PQW.QVBoxLayout()
# Element EditLine
        TabParEst.Label_Report = ScrollLabel(self)
        TabParEst.Label_Report.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ')
# Add elements to the Layout
        self.VBoxReport.addWidget(TabParEst.Label_Report)
# Add the Layout to the Groupbox Report
        self.GroupBox_Report.setLayout(self.VBoxReport)
# Groupbox Sensors
        self.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
# Create Layout for the Groupbox Sensor
        TabParEst.VBoxSensor = PQW.QGridLayout()
#!         TabParEst.VBoxSensor = PQW.QVBoxLayout()
        self.GroupBox_Sensors.setLayout(TabParEst.VBoxSensor)
# FFTChart
        TabParEst.Chart_Fig = plt.figure()
        TabParEst.Canvas = FigureCanvas(TabParEst.Chart_Fig)
        self.Toolbar = NavigationToolbar(TabParEst.Canvas, self)
        TabParEst.Canvas.draw()
# Insert element in the grid
        Layout_Tab_ParEst.addWidget(TabParEst.Button_PE,0,0,1,2)
        Layout_Tab_ParEst.addWidget(self.GroupBox_Filter,2,0,1,2)
        Layout_Tab_ParEst.addWidget(self.GroupBox_Chart,3,0,1,2)
        Layout_Tab_ParEst.addWidget(self.GroupBox_Report,5,0,2,2)
        Layout_Tab_ParEst.addWidget(self.GroupBox_Sensors,7,0,4,2)
        Layout_Tab_ParEst.addWidget(self.Toolbar,0,2,1,8)
        Layout_Tab_ParEst.addWidget(TabParEst.Canvas,1,2,10,8)
# Set layout of tab
        self.setLayout(Layout_Tab_ParEst)
#
    def Update(self,Case):
        print('TabParEst Update - Case',Case)
        '''
        Case 0: Event generated by the starting of the GUI
        # Case 1: Event generated by on change project
        # Case 2: Event generated by button new project
        # Case 3: Event generated by button delete project
        # Case 4: Event generated by wizard AddProbe
        # Case 5: Event generated by Button Remove Probe
        # Case 6: Event generated by on active probe change
        # Case 7: Event generated by wizard Signal Processing
        # Case 8:x
        # Case 9:x
        # Case 10:
        # Case 11:
        # Case 12:
        # Case 13:
        '''
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        # Disconect all the internal events
        TabParEst.Combobox_Method.currentIndexChanged.disconnect()
        TabParEst.Combobox_Analysis.currentIndexChanged.disconnect()
        TabParEst.Combobox_ChartType.currentIndexChanged.disconnect()
        if(VAR.GetActiveProject(VAR) == None):
            TabParEst.Button_PE.setEnabled(False)
            # Filter GroupBox
            TabParEst.Combobox_Method.setCurrentIndex(0)
            # Chart GroupBox
            TabParEst.Combobox_ChartType.setCurrentIndex(3)
            TabParEst.Combobox_ChartType.setEnabled(False)
            TabParEst.Combobox_Analysis.clear()
            # Report GroupBox
            TabParEst.Label_Report.setText('There isn\'t any Project\nCreate one.')
            # Sensors GroupBox
            if TabParEst.VBoxSensor is not None:
                while TabParEst.VBoxSensor.count():
                    item = TabParEst.VBoxSensor.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clearLayout(item.layout())
            # Chart
            TabParEst.Chart_Fig.clear()
            TabParEst.ax = TabParEst.Chart_Fig.add_subplot(111)
#!             TabFreqAnal.ax.legend()
            TabParEst.ax.grid(True, which='both', axis='both', linestyle='--')
            TabParEst.ax.set_ylabel('Flux (m s$^{-1}$)',fontsize=TabParEst.MPL_AxisTitle)
            #
            TabParEst.ax.set_xlabel('Time (s)',fontsize=TabParEst.MPL_AxisTitle)
            TabParEst.Canvas.draw()
            # Menu
            VAR.GetiFlowSelf(VAR).Menu_RunPE.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_PE_Export_Eta.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_PE_Export_Ke.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_PE_Export_Flow.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_PE_Export_Height.setEnabled(False)
#!             VAR.GetiFlowSelf(VAR).Menu_RunPE_Compare.setEnabled(False)
        else:
            if(VAR.GetActiveProbe(VAR) == None):
                TabParEst.Button_PE.setEnabled(False)
                # Filter GroupBox
                TabParEst.Combobox_Method.setCurrentIndex(0)
                # Chart GroupBox
                TabParEst.Combobox_ChartType.setCurrentIndex(3)
                TabParEst.Combobox_ChartType.setEnabled(False)
                TabParEst.Combobox_Analysis.clear()
                # Report GroupBox
                TabParEst.Label_Report.setText('There isn\'t any Probe\nImport one.')
                # Sensors GroupBox
                if TabParEst.VBoxSensor is not None:
                    while TabParEst.VBoxSensor.count():
                        item = TabParEst.VBoxSensor.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            self.clearLayout(item.layout())
                # Chart
                TabParEst.Chart_Fig.clear()
                TabParEst.ax = TabParEst.Chart_Fig.add_subplot(111)
#!                 TabFreqAnal.ax.legend()
                TabParEst.ax.grid(True, which='both', axis='both', linestyle='--')
                TabParEst.ax.set_ylabel('Flux (m s$^{-1}$)',fontsize=TabParEst.MPL_AxisTitle)
                #
                TabParEst.ax.set_xlabel('Time (s)',fontsize=TabParEst.MPL_AxisTitle)
                TabParEst.Canvas.draw()
                # Menu
                VAR.GetiFlowSelf(VAR).Menu_RunPE.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_PE_Export_Eta.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_PE_Export_Ke.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_PE_Export_Flow.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_PE_Export_Height.setEnabled(False)
#!                 VAR.GetiFlowSelf(VAR).Menu_RunPE_Compare.setEnabled(False)
            else:
                RunsPrev = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/*.run')
                if len(RunsPrev) == 0:
                    VAR.GetiFlowSelf(VAR).Menu_RunPE.setEnabled(False) #!
                    TabParEst.Button_PE.setEnabled(False)
                else:
                    VAR.GetiFlowSelf(VAR).Menu_RunPE.setEnabled(True)
                    TabParEst.Button_PE.setEnabled(True)
                #
                Runs = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/*.run')
                #
                RunOK = []
                for Run in Runs:
                    Handle = open(Run,'r')
                    SimType = Handle.readline().split(';')[0]
                    Handle.close()
                    #
                    if TabParEst.Combobox_Method.currentText() == '' or SimType == TabParEst.Combobox_Method.currentText():
                        RunOK.append('Run: '+(Run.replace('\\','/').split('/')[-1]).replace('.run',''))
                #
                if len(RunOK) == 0:
                    # Filter GroupBox
                    TabParEst.Combobox_Method.setCurrentIndex(0)
                    # Chart GroupBox
                    TabParEst.Combobox_ChartType.setCurrentIndex(3)
                    TabParEst.Combobox_ChartType.setEnabled(False)
                    TabParEst.Combobox_Analysis.clear()
                    # Report GroupBox
                    TabParEst.Label_Report.setText('There isn\'t any estimation\nPerform one.')
                    # Sensors GroupBox
                    if TabParEst.VBoxSensor is not None:
                        while TabParEst.VBoxSensor.count():
                            item = TabParEst.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    # Chart
                    TabParEst.Chart_Fig.clear()
                    TabParEst.ax = TabParEst.Chart_Fig.add_subplot(111)
#!                     TabFreqAnal.ax.legend()
                    TabParEst.ax.grid(True, which='both', axis='both', linestyle='--')
                    TabParEst.ax.set_ylabel('Eta',fontsize=TabParEst.MPL_AxisTitle)
                    #
                    TabParEst.ax.set_xlabel('Time (s)',fontsize=TabParEst.MPL_AxisTitle)
                    TabParEst.Canvas.draw()
                    # Menu
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Eta.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Ke.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Flow.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Height.setEnabled(False)
#!                     VAR.GetiFlowSelf(VAR).Menu_RunPE_Compare.setEnabled(False)
                else:
                    TabParEst.Combobox_ChartType.setEnabled(True)
                    # Chart GroupBox
                    if (Case != 8) and (Case != 10) and (Case != 11):
                        TabParEst.Combobox_Analysis.clear()
                        for Run in RunOK:
                            TabParEst.Combobox_Analysis.addItem(Run)
                    # Load Active RUN file
                    if (Case != -1):
                        Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                        TabParEst.AnalysisType = Handle.readline().split(';')[0]
                        #
                        if TabParEst.AnalysisType == 'Analytical':
                            RunSP = Handle.readline().split(';')[0]
                            Handle.readline().split(';')[0]
                            PeriodValue = Handle.readline().split(';')[0]
                            KeElev = Handle.readline().split(';')[0]
                            KeTopSensor = Handle.readline().split(';')[0]
                            SensorsUsed = Handle.readline().split(';')[0].split(',')
                            Handle.readline().split(';')[0]
                            Handle.readline().split(';')[0]
                            BedRiver = Handle.readline().split(';')[0]
                            Gamma = Handle.readline().split(';')[0]
                            From = Handle.readline().split(';')[0]
                            To = Handle.readline().split(';')[0]
                            KeList = Handle.readline().split(';')[0].split(',')
                        elif TabParEst.AnalysisType == 'MLEn' or TabParEst.AnalysisType == 'MLEnZ':
                            LPMRun = Handle.readline().split(';')[0]
                            SensorsUsed = Handle.readline().split(';')[0]
                            Handle.readline().split(';')[0]
                            FreqOK = Handle.readline().split(';')[0]
                            MethodDV = Handle.readline().split(';')[0]
                            Diffu = Handle.readline().split(';')[0]
                            Veloc = Handle.readline().split(';')[0]
                            Method = Handle.readline().split(';')[0]
                            SRNLimit = Handle.readline().split(';')[0]
                            FreqLimit = Handle.readline().split(';')[0]
                            MinMaxSRN = Handle.readline().split(';')[0]
                            cw_x_rhow = Handle.readline().split(';')[0]
                            c_x_rho = Handle.readline().split(';')[0]
                            IniFlag = Handle.readline().split(';')[0]
                            if TabParEst.AnalysisType == 'MLEnZ':
                                d50 = Handle.readline().split(';')[0]
                                Zuser = Handle.readline().split(';')[0]
                        Handle.close()
                    # Chart type
                    VAR.GetiFlowSelf(VAR).progress.setValue(20)
                    if (Case != 11) and (Case != 8): #!###############################
                        TabParEst.Combobox_ChartType.clear()
                        for ChartType in VAR.GetChartTypeParameterEstimation(VAR):
                            if TabParEst.AnalysisType == 'MLEn' and (ChartType =='Eta' or ChartType =='Heights'):
                                pass
                            elif TabParEst.AnalysisType == 'MLEnZ' and (ChartType =='Eta'):
                                pass
                            elif TabParEst.AnalysisType == 'Analytical' and (ChartType =='Q' or ChartType =='K'):
                                pass
                            else:
                                TabParEst.Combobox_ChartType.addItem(ChartType)
                    # Report GroupBox
                    if (Case != -1): #!###############################
#!                         AnalysisType = Handle.readline().split(';')[0]
                        Text = 'Signal processing: '+TabParEst.AnalysisType+'\n'
                        if TabParEst.AnalysisType == 'Analytical':
                            Text = Text + 'Signal Processing Run'+RunSP+'\n'
                            Text = Text + 'Period used: '+PeriodValue+'\n'
                            Text = Text + 'Used for ke:\n'
                            Text = Text + 'Bed elev: '+KeElev+'\n'
                            Text = Text + 'Water sensor: '+KeTopSensor+'\n'
                            Text = Text + 'Used for estimation:\n'
                            Text = Text + 'Bed-river elevetion: '+BedRiver+'\n'
                            Text = Text + 'Gamma: '+str(Gamma)+'\n'
                            Text = Text + 'Ke:\n'
                            for i,item in enumerate(KeList):
                                Text = Text + '\t' + SensorsUsed[i] +': ' + item +'\n'
                        elif TabParEst.AnalysisType == 'MLEn' or TabParEst.AnalysisType == 'MLEnZ':
                            Text = Text +'LPM Run:'+LPMRun+'\n'
                            if FreqOK == '0':
                                Text = Text +'Frequency: Best Frequency\n'
                            elif FreqOK == '1':
                                Text = Text +'Frequency: Best 5 Frequencies\n'
                            elif FreqOK == '2':
                                Text = Text +'All Frequencies > '+SRNLimit+' db\n'
                            Text = Text +'FreqLimit: '+str(1.0/float(FreqLimit)/3600.0)+' days\n'
                            if MinMaxSRN == '0':
                                Text = Text +'MinMaxSRN: MAX\n'
                            elif MinMaxSRN == '1':
                                Text = Text +'MinMaxSRN: MIN\n'
                            Text = Text +'Method: '+Method+'\n'
                            Text = Text +'Estimate: '+MethodDV+'\n'
                            if MethodDV == 'V':
                                Text = Text +'Diffusivity: '+Diffu+'\n'
                            if MethodDV == 'D':
                                Text = Text +'Velocity: '+Veloc+'\n'
                            if IniFlag == '0':
                                Text = Text +'StartCondition: Everytime\n'
                            elif IniFlag == '1':
                                Text = Text +'StartCondition: First Time\n'
                            Text = Text +'cw_x_rhow: '+cw_x_rhow+'\n'
                            Text = Text +'c_x_rho: '+c_x_rho+'\n'
                            if TabParEst.AnalysisType == 'MLEnZ':
                                Text = Text +'d50: '+d50+' m\n'
                                Text = Text +'Starting z: '+Zuser+' m\n'
                            Text = Text +'Sensors:\n'
                            for Sensor in SensorsUsed.split(','):
                                Text = Text + '\t'+Sensor+'\n'
                        TabParEst.Label_Report.setText(Text)
                    # Load Data
                    VAR.GetiFlowSelf(VAR).progress.setValue(40)
                    if (Case != -1):
                        if TabParEst.AnalysisType == 'MLEn':
                            if TabParEst.Combobox_ChartType.currentText() == 'K':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_K.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Ke':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Diffusivity.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Flux':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Velocity.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Q':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Q.pkz', compression= 'zip')
                        elif TabParEst.AnalysisType == 'MLEnZ':
                            if TabParEst.Combobox_ChartType.currentText() == 'K':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_K.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Ke':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Diffusivity.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Flux':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Velocity.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Q':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Q.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Heights':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Heights.pkz', compression= 'zip')
                        else:
                            if TabParEst.Combobox_ChartType.currentText() == 'Heights':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_BEC.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Flux':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Q.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Eta':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_eta2.pkz', compression= 'zip')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Ke':
                                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Ke.pkz', compression= 'zip')
#!                             MobTimeWin = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+RunAct+'_MobWinTime.pkz',compression='zip')
                    # Sensors GroupBox
                    if (Case != 8):
                        # Delete all object in the group Sensors
                        if TabParEst.VBoxSensor is not None:
                            while TabParEst.VBoxSensor.count():
                                item = TabParEst.VBoxSensor.takeAt(0)
                                widget = item.widget()
                                if widget is not None:
                                    widget.deleteLater()
                                else:
                                    self.clearLayout(item.layout())
                            if TabParEst.AnalysisType == 'MLEn' or TabParEst.AnalysisType == 'MLEnZ':
                                CheckBox = PQW.QCheckBox('Uncertainty')
                                if TabParEst.Combobox_ChartType.currentText() == 'Heights':
                                    CheckBox.setEnabled(False)
                                    CheckBox.setChecked(False)
                                else:
                                    CheckBox.setEnabled(True)
                                CheckBox.setChecked(False)
                                CheckBox.toggled.connect(TabParEst.SensorActiveChange)
                                TabParEst.VBoxSensor.addWidget(CheckBox)
                            else:
                                for sensor in df_chart.columns.tolist()[1:]:
                                    CheckBox = PQW.QCheckBox(sensor)
                                    CheckBox.setChecked(True)
                                    CheckBox.toggled.connect(TabParEst.SensorActiveChange)
                                    TabParEst.VBoxSensor.addWidget(CheckBox)
                    # Chart
                    VAR.GetiFlowSelf(VAR).progress.setValue(60)
                    if (Case != -1):
                        if Case == 8:
                            Ylim = TabParEst.ax.get_ylim()
                            Xlim = TabParEst.ax.get_xlim()
                        #
                        TabParEst.Chart_Fig.clear()
                        TabParEst.ax = TabParEst.Chart_Fig.add_subplot(111)
                        if(VAR.GetChartColors(VAR) is None):
                            Colors = []
                        else:
                            Colors = VAR.GetChartColors(VAR)
                            if len(Colors) < len(df_chart.columns.tolist()):
                                Colors = []
                                VAR.SetChartColors(VAR,None)
                        #
                        if TabParEst.AnalysisType == 'MLEn' or TabParEst.AnalysisType == 'MLEnZ':
                            if TabParEst.Combobox_ChartType.currentText() == 'Ke':
                                if df_chart.shape[0] == 1:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Dif'].to_numpy(), 'o', label = 'Diffusivity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Dif']+df_chart['DifI']).to_numpy(), 'v', label = '+Diffusivity')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Dif']-df_chart['DifI']).to_numpy(), '^', label = '-Diffusivity')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Dif'].to_numpy(), 'o', label = 'Diffusivity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Dif']+df_chart['DifI']).to_numpy(), 'v', label = '+Diffusivity')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Dif']-df_chart['DifI']).to_numpy(), '^', label = '-Diffusivity')
                                else:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Dif'].to_numpy(), '-', label = 'Diffusivity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Dif']+df_chart['DifI']).to_numpy(), 'v', label = '+Diffusivity')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Dif']-df_chart['DifI']).to_numpy(), '^', label = '-Diffusivity')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Dif'].to_numpy(), '-', label = 'Diffusivity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Dif']+df_chart['DifI']).to_numpy(), '-', label = '+Diffusivity')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Dif']-df_chart['DifI']).to_numpy(), '-', label = '-Diffusivity')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Flux':
                                if df_chart.shape[0] == 1:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Vel'].to_numpy(), 'o', label = 'Velocity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), 'v', label = '+Velocity')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '^', label = '-Velocity')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Vel'].to_numpy(), 'o', label = 'Velocity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']+df_chart['VelI']), 'v', label = '+Velocity')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']-df_chart['VelI']), '^', label = '-Velocity')
                                else:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Vel'].to_numpy(), '-', label = 'Velocity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), '-', label = '+Velocity')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '-', label = '-Velocity')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Vel'].to_numpy(), '-', label = 'Velocity')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), '-', label = '+Velocity')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '-', label = '-Velocity')
                            elif TabParEst.Combobox_ChartType.currentText() == 'K':
                                if df_chart.shape[0] == 1:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['K'].to_numpy(), 'o', label = 'K')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['K']+df_chart['KI']).to_numpy(), 'v', label = '+K')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['K']-df_chart['KI']).to_numpy(), '^', label = '-K')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['K'].to_numpy(), 'o', label = 'K')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['K']+df_chart['KI']).to_numpy(), 'v', label = '+K')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['K']-df_chart['KI']).to_numpy(), '^', label = '-K')
                                else:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['K'].to_numpy(), '-', label = 'K')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['K']+df_chart['KI']).to_numpy(), 'v', label = '+K')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['K']-df_chart['KI']).to_numpy(), '^', label = '-K')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['K'].to_numpy(), '-', label = 'K')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['K']+df_chart['KI']).to_numpy(), '-', label = '+K')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['K']-df_chart['KI']).to_numpy(), '-', label = '-K')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Q':
                                if df_chart.shape[0] == 1:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s'), df_chart['Vel'].to_numpy(), 'o', label = 'Q')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), 'v', label = '+Q')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '^', label = '-Q')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Vel'].to_numpy(), 'o', label = 'Q')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']+df_chart['VelI']), 'v', label = '+Q')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']-df_chart['VelI']), '^', label = '-Q')
                                else:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Vel'].to_numpy(), '-', label = 'Q')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), '-', label = '+Q')
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '-', label = '-Q')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Vel'].to_numpy(), '-', label = 'Q')
                                        if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']+df_chart['VelI']).to_numpy(), '-', label = '+Q')
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart['Vel']-df_chart['VelI']).to_numpy(), '-', label = '-Q')
                            elif TabParEst.Combobox_ChartType.currentText() == 'Heights' and TabParEst.AnalysisType == 'MLEnZ':
                                if df_chart.shape[0] == 1:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Heights'].to_numpy(), 'o', label = 'Heights')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Heights'].to_numpy(), 'o', label = 'Heights')
                                else:
                                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                        plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), df_chart['Heights'].to_numpy(), '-', label = 'Heights')
                                    else:
                                        plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), df_chart['Heights'].to_numpy(), '-', label = 'Heights')
                        else:
                            for i in range(0,len(df_chart.columns.tolist()[1:])):
                                if TabParEst.VBoxSensor.itemAt(i).widget().isChecked():
                                    if(VAR.GetChartColors(VAR) == None):
                                        if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart[TabParEst.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabParEst.VBoxSensor.itemAt(i).widget().text())
                                        elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                            plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart[TabParEst.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabParEst.VBoxSensor.itemAt(i).widget().text())
                                        Colors.append(plot[0].get_color())
                                    else:
                                        if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                            plot = TabParEst.ax.plot(pd.to_datetime(df_chart['Time'],unit='s').to_numpy(), (df_chart[TabParEst.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabParEst.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                        elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                            try:
                                                plot = TabParEst.ax.plot(df_chart['Time'].to_numpy(), (df_chart[TabParEst.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabParEst.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            except:
                                                pass
                        #
                        if TabParEst.Combobox_ChartType.currentText() == 'Eta':
                            TabParEst.ax.set_ylabel('Eta')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        elif TabParEst.Combobox_ChartType.currentText() == 'Ke':
                            TabParEst.ax.set_ylabel('Ke ($m^2$ $s^{-1}$)')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        elif TabParEst.Combobox_ChartType.currentText() == 'Heights':
                            TabParEst.ax.set_ylabel('Heights (m)')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        elif TabParEst.Combobox_ChartType.currentText() == 'Flux':
                            TabParEst.ax.set_ylabel('Flux ($m$ $s^{-1}$)')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        elif TabParEst.Combobox_ChartType.currentText() == 'K':
                            TabParEst.ax.set_ylabel('K ($m^2$ $s^{-1}$)')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        elif TabParEst.Combobox_ChartType.currentText() == 'Q':
                            TabParEst.ax.set_ylabel('Q ($m$ $s^{-1}$)')
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabParEst.ax.set_xlabel('Time (s)')
                        #
                        TabParEst.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2e'))
                        #
                        if TabParEst.AnalysisType == 'MLEn':
                            if TabParEst.VBoxSensor.itemAt(0).widget().isChecked():
                                TabParEst.ax.legend(loc=9, ncol=3)
                            else:
                                TabParEst.ax.legend(loc=9, ncol=1)
                        else:
                            if len(df_chart.columns.tolist()[1:]) > 5:
                                TabParEst.ax.legend(ncol=int(len(df_chart.columns.tolist()[1:])/5+1),fontsize=TabParEst.MPL_Legend)
                            else:
                                TabParEst.ax.legend(ncol=len(df_chart.columns.tolist()[1:]),fontsize=TabParEst.MPL_Legend)
                        #
                        TabParEst.ax.grid(True, which='both', axis='both', linestyle='--')
                        #
#!                         if Case == 8:
#!                             TabParEst.ax.set_ylim(Ylim)
#!                             TabParEst.ax.set_xlim(Xlim)
                        #
                        TabParEst.ax.tick_params(axis='both', labelsize=TabParEst.MPL_AxisTick)
                        #
                        TabParEst.Canvas.draw()
                    # Menu
                    VAR.GetiFlowSelf(VAR).progress.setValue(80)
                    if TabParEst.AnalysisType == 'Analytical':
                        VAR.GetiFlowSelf(VAR).Menu_PE_Export_Eta.setEnabled(True)
                        VAR.GetiFlowSelf(VAR).Menu_PE_Export_Height.setEnabled(True)
                    elif TabParEst.AnalysisType == 'MLEn':
                        VAR.GetiFlowSelf(VAR).Menu_PE_Export_Eta.setEnabled(False)
                        VAR.GetiFlowSelf(VAR).Menu_PE_Export_Height.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Ke.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_PE_Export_Flow.setEnabled(True)
#!                     VAR.GetiFlowSelf(VAR).Menu_RunPE_Compare.setEnabled(False)
        # Connect all internal event
        TabParEst.Combobox_Method.currentIndexChanged.connect(TabParEst.on_Combobox_Method_change) # ComboBox event change item
        TabParEst.Combobox_ChartType.currentIndexChanged.connect(TabParEst.on_Combobox_ChartType_change) # ComboBox event change item
        TabParEst.Combobox_Analysis.currentIndexChanged.connect(TabParEst.on_Combobox_Analysis_change) # ComboBox event change item
        #
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        #
        return

    def on_Button_PE_clicked(self):
        print('TabParEst - on_Button_PE_clicked')
        # Lunch the wizard for parameter estimatio
        WizardParEst = WPE.ParameterEstimation()
        WizardParEst.exec_()
        TPE.TabParEst.Update(TPE,7)
        return

    def on_Combobox_Method_change(self):
        print('TabParEst - on_Combobox_Method_change')
        TPE.TabParEst.Update(TPE,9) #!
        return

    def on_Combobox_Analysis_change(self):
        print('TabParEst - on_Combobox_Analysis_change')
        TPE.TabParEst.Update(TPE,10)
        return

    def on_Combobox_ChartType_change(self):
        print('TabParEst - on_Combobox_ChartType_change')
        TPE.TabParEst.Update(TPE,11)
        return

    def SensorActiveChange(self):
        print('TabParEst - SensorActiveChange')
        TPE.TabParEst.Update(TPE,8)
        return

    def on_Button_PE_Export_Eta_clicked(self):
        print('TabParEst - on_Button_PE_Export_Eta_clicked')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Eta to File', '../exports/Eta_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            if TabParEst.AnalysisType == 'MLEn':
                pass
            else:
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Eta.pkz', compression= 'zip')
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                df_chart['Time'] = pd.to_datetime(df_chart['Time'],unit='s')
            df_chart.to_csv(file_export[0],index=False)
        return

    def on_Button_PE_Export_Ke_clicked(self):
        print('TabParEst - on_Combobox_ChartType_change')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Ke to File', '../exports/Ke_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            if TabParEst.AnalysisType == 'MLEn':
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Diffusivity.pkz', compression= 'zip')
            else:
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Ke.pkz', compression= 'zip')
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                df_chart['Time'] = pd.to_datetime(df_chart['Time'],unit='s')
            df_chart.to_csv(file_export[0],index=False)
        return

    def on_Button_PE_Export_Flow_clicked(self):
        print('TabParEst - on_Combobox_ChartType_change')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Flow to File', '../exports/Flow_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            if TabParEst.AnalysisType == 'MLEn':
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Velocity.pkz', compression= 'zip')
            else:
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_Q.pkz', compression= 'zip')
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                df_chart['Time'] = pd.to_datetime(df_chart['Time'],unit='s')
            df_chart.to_csv(file_export[0],index=False)
        return

    def on_Button_PE_Export_Height_clicked(self):
        print('TabParEst - on_Combobox_ChartType_change')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Height to File', '../exports/Height_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            if TabParEst.AnalysisType == 'MLEn':
                pass
            else:
                df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+TabParEst.Combobox_Analysis.currentText().replace('Run: ','')+'_BEC.pkz', compression= 'zip')
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                df_chart['Time'] = pd.to_datetime(df_chart['Time'],unit='s')
            df_chart.to_csv(file_export[0],index=False)
        return