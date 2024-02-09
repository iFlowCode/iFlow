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
import PyQt5.QtWidgets as PQW
# # import PyQt5.QtGui as PQG
# # import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
# # import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from mpl_toolkits.mplot3d import Axes3D  
import glob
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import pickle
import datetime
# import time
import numpy as np
# from matplotlib import cm
# Import custom library
from Variables import VAR
from Options import OPT
from ScrollLabel import ScrollLabel
import TabSignProc as TSP
# # import STabFFTAnal as STFA
# # import STabLPMAnal as STLA

import WizardSP as WSP
import WizardPC as WPC
import WizardEC as WEC
#------------------------------------------------------------------------------#
'''
TabSignAnal Class
'''
class TabSignProc(PQW.QWidget):
    def __init__(self):
        super().__init__()
        print('TabSignProc - Start Class')
# Set Matplotlib fonts size
        TabSignProc.MPL_AxisTitle = int(VAR.GetMPLAxisTitleFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabSignProc.MPL_AxisTick = int(VAR.GetMPLAxisTickFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabSignProc.MPL_Legend = int(VAR.GetMPLLegendFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
# Store class object
        VAR.SetTabSignProc(VAR, self)
# Create grid layot for the window
        Layout_Tab_SignProc = PQW.QGridLayout()
# Button Calculate
        TabSignProc.Button_SP = PQW.QPushButton('Signal Processing')
        # TabSignProc.Button_SP.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Button_SP.setToolTip('Launch Signal Processing Wizard') # Tooltip message
        TabSignProc.Button_SP.clicked.connect(self.on_Button_SP_clicked) # Button event Click on
# #%%
# Groupbox Filter
        self.GroupBox_Filter = PQW.QGroupBox('Filter:')
# Create the Layout for the Groupbox Filter
        self.VBoxFilter = PQW.QVBoxLayout()
# Label
        Label_Method = PQW.QLabel('Method:')
# Element ComboBox Method
        TabSignProc.Combobox_Method = PQW.QComboBox()
        # TabSignProc.Combobox_Method.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_Method.setToolTip('Filter results by method') # Tooltip message
        #
        for item in VAR.GetProcessingMethod(VAR):
            TabSignProc.Combobox_Method.addItem(item)
#         #
        TabSignProc.Combobox_Method.currentIndexChanged.connect(self.on_Combobox_Method_change) # ComboBox event change item
# Label
        Label_Detrending = PQW.QLabel('Detrending:')
# Element ComboBox Detrending
        TabSignProc.Combobox_Detrending = PQW.QComboBox()
        # TabSignProc.Combobox_Detrending.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_Detrending.setToolTip('Filter results by detrending') # Tooltip message
        #
        for item in VAR.GetDetrending(VAR):
            TabSignProc.Combobox_Detrending.addItem(item)
        #
        TabSignProc.Combobox_Detrending.currentIndexChanged.connect(self.on_Combobox_Detrending_change) # ComboBox event change item
# Label
        Label_FFTwin = PQW.QLabel('FFT Window:')
# Element ComboBox FFT window
        TabSignProc.Combobox_FFTwin = PQW.QComboBox()
        # TabSignProc.Combobox_FFTwin.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_FFTwin.setToolTip('Filter results by FFT window') # Tooltip message
        #
        for item in VAR.GetFFTWindowfunction(VAR):
            TabSignProc.Combobox_FFTwin.addItem(item)
        #
        TabSignProc.Combobox_FFTwin.currentIndexChanged.connect(self.on_Combobox_FFTwin_change) # ComboBox event change item
# Add elements to the Layout
        self.VBoxFilter.addWidget(Label_Method)
        self.VBoxFilter.addWidget(TabSignProc.Combobox_Method)
        self.VBoxFilter.addWidget(Label_Detrending)
        self.VBoxFilter.addWidget(TabSignProc.Combobox_Detrending)
        self.VBoxFilter.addWidget(Label_FFTwin)
        self.VBoxFilter.addWidget(TabSignProc.Combobox_FFTwin)
# Add the Layout to the Groupbox Filter
        self.GroupBox_Filter.setLayout(self.VBoxFilter)
# #%%
# Groupbox Chart
        self.GroupBox_Chart = PQW.QGroupBox('Chart:')
# Create the lyout for the Groupbox Chart
        self.VBoxChart = PQW.QVBoxLayout()
# Label
        Label_Analysis = PQW.QLabel('Analysis:')
# Element ComboBox Analysis
        TabSignProc.Combobox_Analysis = PQW.QComboBox()
        # TabSignProc.Combobox_Analysis.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_Analysis.setToolTip('Choose analysis to show') # Tooltip message
        TabSignProc.Combobox_Analysis.currentIndexChanged.connect(self.on_Combobox_Analysis_change) # ComboBox event change item
# Label
        Label_ChartType = PQW.QLabel('Chart type:')
# Element Combobox ChartType
        TabSignProc.Combobox_ChartType = PQW.QComboBox()
        # TabSignProc.Combobox_ChartType.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_ChartType.setToolTip('Choose the data to display') # Tooltip message
        #
        for item in VAR.GetChartTypeSignalProcessin(VAR):
            TabSignProc.Combobox_ChartType.addItem(item)
        #
        TabSignProc.Combobox_ChartType.currentIndexChanged.connect(self.on_Combobox_ChartType_change) # ComboBox event change item
# Element Combobox ChartType
        TabSignProc.Combobox_ChartTimeFreq = PQW.QComboBox()
        # TabSignProc.Combobox_ChartTimeFreq.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
# #         TabSignProc.Combobox_ChartTimeFreq.setToolTip('Choose the data to display') # Tooltip message
        TabSignProc.Combobox_ChartTimeFreq.currentIndexChanged.connect(self.on_Combobox_ChartTimeFreq_change) # ComboBox event change item
# Add elements to the Layout
        self.VBoxChart.addWidget(Label_Analysis)
        self.VBoxChart.addWidget(TabSignProc.Combobox_Analysis)
        self.VBoxChart.addWidget(Label_ChartType)
        self.VBoxChart.addWidget(TabSignProc.Combobox_ChartType)
        self.VBoxChart.addWidget(TabSignProc.Combobox_ChartTimeFreq)
# Add the Layout to the Groupbox Chart
        self.GroupBox_Chart.setLayout(self.VBoxChart)
# #%%
# Groupbox Report
        self.GroupBox_Report = PQW.QGroupBox('Report:')
# Create Layout for the Groupbox Report
        self.VBoxReport = PQW.QVBoxLayout()
# Element EditLine
        TabSignProc.Label_Report = ScrollLabel(self)
        TabSignProc.Label_Report.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ')
# Add elements to the Layout
        self.VBoxReport.addWidget(TabSignProc.Label_Report)
# Add the Layout to the Groupbox Report
        self.GroupBox_Report.setLayout(self.VBoxReport)
# #%%
# Groupbox Sensors
        self.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
# Create Layout for the Groupbox Sensor
        TabSignProc.VBoxSensor = PQW.QGridLayout()
# #         TabSignProc.VBoxSensor = PQW.QVBoxLayout()
        self.GroupBox_Sensors.setLayout(TabSignProc.VBoxSensor)
# #%%
# FFTChart
        TabSignProc.Chart_Fig = plt.figure()
        TabSignProc.Canvas = FigureCanvas(TabSignProc.Chart_Fig)
        self.Toolbar = NavigationToolbar(TabSignProc.Canvas, self)
        TabSignProc.Canvas.draw()
# Insert element in the grid
        Layout_Tab_SignProc.addWidget(TabSignProc.Button_SP,0,0,1,2)
        Layout_Tab_SignProc.addWidget(self.GroupBox_Filter,2,0,1,2)
        Layout_Tab_SignProc.addWidget(self.GroupBox_Chart,3,0,2,2)
        Layout_Tab_SignProc.addWidget(self.GroupBox_Report,5,0,2,2)
        Layout_Tab_SignProc.addWidget(self.GroupBox_Sensors,7,0,4,2)
        Layout_Tab_SignProc.addWidget(self.Toolbar,0,2,1,8)
        Layout_Tab_SignProc.addWidget(TabSignProc.Canvas,1,2,10,8)
# Set layout of tab
        self.setLayout(Layout_Tab_SignProc)
#%%
    def Update(self,Case):
        print('TabSignProc Update - Case',Case)
        '''
        Case 0: Event generated by the starting of the GUI
        # Case 1: Event generated by on change project
        # Case 2: Event generated by button new project
        # Case 3: Event generated by button delete project
        # Case 4: Event generated by wizard AddProbe
        # Case 5: Event generated by Button Remove Probe
        # Case 6: Event generated by on active probe change
        Case 7: Event generated by wizard Signal Processing
        Case 8: on change method AND on change detrending AND on change FFTwin
        # Case 9: on change Analysis
        # Case 10:
        Case 11: SensorActiveChange
        Case 12: on_Combobox_ChartType_change
        # Case 13:
        Case 14: on_Combobox_ChartTimeFreq_change
        '''
        #
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        # Disconect all the internal events
        TabSignProc.Combobox_Method.currentIndexChanged.disconnect()
        TabSignProc.Combobox_Detrending.currentIndexChanged.disconnect()
        TabSignProc.Combobox_FFTwin.currentIndexChanged.disconnect()
        TabSignProc.Combobox_Analysis.currentIndexChanged.disconnect()
        TabSignProc.Combobox_ChartType.currentIndexChanged.disconnect()
        TabSignProc.Combobox_ChartTimeFreq.currentIndexChanged.disconnect()
        if(VAR.GetActiveProject(VAR) == None):
            TabSignProc.Button_SP.setEnabled(False)
            # Filter GroupBox
            TabSignProc.Combobox_Method.setCurrentIndex(0)
            TabSignProc.Combobox_Detrending.setCurrentIndex(0)
            TabSignProc.Combobox_FFTwin.setCurrentIndex(0)
            # Chart GroupBox
            TabSignProc.Combobox_ChartType.setCurrentIndex(0)
            TabSignProc.Combobox_ChartType.setEnabled(False)
            TabSignProc.Combobox_Analysis.clear()
            TabSignProc.Combobox_ChartTimeFreq.clear()
            # Report GroupBox
            TabSignProc.Label_Report.setText('There isn\'t any Project\nCreate one.')
            # Sensors GroupBox
            if TabSignProc.VBoxSensor is not None:
                while TabSignProc.VBoxSensor.count():
                    item = TabSignProc.VBoxSensor.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clearLayout(item.layout())
            # Chart
            TabSignProc.Chart_Fig.clear()
            TabSignProc.ax = TabSignProc.Chart_Fig.add_subplot(111)
            # TabFreqAnal.ax.legend()
            TabSignProc.ax.grid(True, which='both', axis='both', linestyle='--')
            TabSignProc.ax.set_ylabel('z (m)',fontsize=TabSignProc.MPL_AxisTitle)
            #
            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
            if OPT.GetTFAxAxisUnit(OPT) == 'Day':
                TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
            if OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
            TabSignProc.Canvas.draw()
            # Menu
            VAR.GetiFlowSelf(VAR).Menu_RunSP.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_SP_Export.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_SP_PhaseCorr.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_SP_BREcalc.setEnabled(False)
        else:
            if(VAR.GetActiveProbe(VAR) == None):
                TabSignProc.Button_SP.setEnabled(False)
                # Filter GroupBox
                TabSignProc.Combobox_Method.setCurrentIndex(0)
                TabSignProc.Combobox_Detrending.setCurrentIndex(0)
                TabSignProc.Combobox_FFTwin.setCurrentIndex(0)
                # Chart GroupBox
                TabSignProc.Combobox_ChartType.setCurrentIndex(0)
                TabSignProc.Combobox_ChartType.setEnabled(False)
                TabSignProc.Combobox_Analysis.clear()
                TabSignProc.Combobox_ChartTimeFreq.clear()
                # Report GroupBox
                TabSignProc.Label_Report.setText('There isn\'t any Probe\nImport one.')
                # Sensors GroupBox
                if TabSignProc.VBoxSensor is not None:
                    while TabSignProc.VBoxSensor.count():
                        item = TabSignProc.VBoxSensor.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            self.clearLayout(item.layout())
                # Chart
                TabSignProc.Chart_Fig.clear()
                TabSignProc.ax = TabSignProc.Chart_Fig.add_subplot(111)
                # TabFreqAnal.ax.legend()
                TabSignProc.ax.grid(True, which='both', axis='both', linestyle='--')
                TabSignProc.ax.set_ylabel('z (m)',fontsize=TabSignProc.MPL_AxisTitle)
                #
                if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                    TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
                if OPT.GetTFAxAxisUnit(OPT) == 'Day':
                    TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                if OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                    TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                TabSignProc.Canvas.draw()
                # Menu
                VAR.GetiFlowSelf(VAR).Menu_RunSP.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_SP_Export.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_SP_PhaseCorr.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_SP_BREcalc.setEnabled(False)
            else:
                Runs = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/*.run')
                #
                RunOK = []
                for Run in Runs:
                    Handle = open(Run,'r')
                    SimType = Handle.readline().split(';')[0]
                    if SimType == 'FFT':
                        Handle.readline().split(';')
                        Handle.readline().split(';')
                        SimFFTwim = Handle.readline().split(';')[0]
                        SimDetren = Handle.readline().split(';')[0]
                    else:
                        SimFFTwim = 'Ciccio'
                        SimDetren = 'Ciccio'
                    Handle.close()
                    #
                    if TabSignProc.Combobox_Method.currentText() == '' or SimType == TabSignProc.Combobox_Method.currentText():
                        if TabSignProc.Combobox_FFTwin.currentText() == '' or SimFFTwim == TabSignProc.Combobox_FFTwin.currentText():
                            if TabSignProc.Combobox_Detrending.currentText() == '' or SimDetren == TabSignProc.Combobox_Detrending.currentText():
                                RunOK.append('Run: '+(Run.replace('\\','/').split('/')[-1]).replace('.run',''))
                #
                TabSignProc.Button_SP.setEnabled(True)
                if len(RunOK) == 0:
                    # Filter GroupBox
                    TabSignProc.Combobox_Method.setCurrentIndex(0)
                    TabSignProc.Combobox_Detrending.setCurrentIndex(0)
                    TabSignProc.Combobox_FFTwin.setCurrentIndex(0)
                    # Chart GroupBox
                    TabSignProc.Combobox_ChartType.setCurrentIndex(0)
                    TabSignProc.Combobox_ChartType.setEnabled(False)
                    TabSignProc.Combobox_Analysis.clear()
                    TabSignProc.Combobox_ChartTimeFreq.clear()
                    # Report GroupBox
                    TabSignProc.Label_Report.setText('There isn\'t any Signal Processing\nRun one.')
                    # Sensors GroupBox
                    if TabSignProc.VBoxSensor is not None:
                        while TabSignProc.VBoxSensor.count():
                            item = TabSignProc.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    # Chart
                    TabSignProc.Chart_Fig.clear()
                    TabSignProc.ax = TabSignProc.Chart_Fig.add_subplot(111)
                    # TabFreqAnal.ax.legend()
                    TabSignProc.ax.grid(True, which='both', axis='both', linestyle='--')
                    TabSignProc.ax.set_ylabel('z (m)',fontsize=TabSignProc.MPL_AxisTitle)
                    #
                    if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                        TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
                    if OPT.GetTFAxAxisUnit(OPT) == 'Day':
                        TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                    if OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                        TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                    TabSignProc.Canvas.draw()
                    # Menu
                    VAR.GetiFlowSelf(VAR).Menu_SP_Export.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_SP_PhaseCorr.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_SP_BREcalc.setEnabled(False)
                else:
                    TabSignProc.Combobox_ChartType.setEnabled(True)
                    # Chart GroupBox
                    if (Case != 9) and (Case != 12) and (Case != 11) and (Case != 14): #!###############################
                        TabSignProc.Combobox_Analysis.clear()
                        ContRun = 0
                        for Run in RunOK:
                            TabSignProc.Combobox_Analysis.addItem(Run)
                            ContRun += 1
                        TabSignProc.Combobox_Analysis.setCurrentIndex(ContRun-1)
                    # Load Active RUN file
                    VAR.GetiFlowSelf(VAR).progress.setValue(10)
                    if (Case != -1): #!###############################
                        Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                        AnalysisType = Handle.readline().split(';')[0]
                        if AnalysisType == 'FFT':
                            MobileWin = Handle.readline().split(';')[0]
                            MobileWinLenght = Handle.readline().split(';')[0]
                            FFTwin = Handle.readline().split(';')[0]
                            Detrending = Handle.readline().split(';')[0]
                            dt = Handle.readline().split(';')[0]
                            PeriodsExt = Handle.readline().split(';')[0]
                            # Start = Handle.readline().split(';')[0]
                            # End = Handle.readline().split(';')[0]
                            Sensors = Handle.readline().split(';')[0]
                        elif AnalysisType == 'LPM':
                            MobileWin = Handle.readline().split(';')[0]
                            MobileWinLenght = Handle.readline().split(';')[0]
                            RefSens = Handle.readline().split(';')[0]
                            # UPSens = Handle.readline().split(';')[0]
                            # DOWNSens = Handle.readline().split(';')[0]
                            dt = Handle.readline().split(';')[0]
                            dof = Handle.readline().split(';')[0]
                            order = Handle.readline().split(';')[0]
                            Sensors = Handle.readline().split(';')[0]
                        Handle.close()
                    # Chart type
                    if (Case != 12) and (Case != 11) and (Case != 14): #!###############################
                        TabSignProc.Combobox_ChartType.clear()
                        for ChartType in VAR.GetChartTypeSignalProcessin(VAR):
                            if AnalysisType == 'FFT' and (ChartType =='SNR heatmap' or ChartType == 'SNR vs Time'):
                                pass
                            else:
                                TabSignProc.Combobox_ChartType.addItem(ChartType)
                    # Load Data
                    VAR.GetiFlowSelf(VAR).progress.setValue(20)
                    if (Case != 11) and (Case != 14):
                    # if (Case != 12) and (Case != 11) and (Case != 14): #!###############################
                        # startTime = time.time()
                        self.df_Time = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'_MobWinTime.pkz',compression='zip')
                        if AnalysisType == 'LPM':
                            with open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'_SRN.PdList','rb') as fSRN:
                                self.dfxSRN = pickle.load(fSRN)
                            fSRN.close()
                        VAR.GetiFlowSelf(VAR).progress.setValue(30)
                        # Amplitude
                        VAR.GetiFlowSelf(VAR).progress.setValue(40)
                        self.dfxAmplitude = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'_Amplitude.pkz',compression='zip')
                        # Phase
                        self.dfxPhase = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
                        VAR.GetiFlowSelf(VAR).progress.setValue(50)
                        # endTime = time.time()
                        # print('Load data: ',endTime-startTime)
                    # Chart type sub
                    if (Case != 11) and (Case != 14): #!###############################
                        if TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
                            # print(self.df_Time['Time'].tolist())
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            for item in self.df_Time['Time'].tolist():
                                # print(item)
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            self.Columns = (self.dfxAmplitude).columns.tolist()[2:]
                        elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            Freq = self.dfxAmplitude['Freq'].drop_duplicates()
                            Periods = (1.0/Freq/3600.0).tolist()
                            for item in Periods:
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            Periods = (np.array(Periods) - OPT.GetBasicPeriod(OPT))**2
                            pos = np.argmin(Periods)
                            TabSignProc.Combobox_ChartTimeFreq.setCurrentIndex(pos)
                            self.Columns = (self.dfxAmplitude).columns.tolist()[2:]
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            Freq = self.dfxAmplitude['Freq'].drop_duplicates()
                            Periods = (1.0/Freq/3600.0).tolist()
                            for item in Periods:
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            Periods = (np.array(Periods) - OPT.GetBasicPeriod(OPT))**2
                            pos = np.argmin(Periods)
                            TabSignProc.Combobox_ChartTimeFreq.setCurrentIndex(pos)
                            self.Columns = (self.dfxPhase).columns.tolist()[2:]
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            Freq = self.dfxAmplitude['Freq'].drop_duplicates()
                            Periods = (1.0/Freq/3600.0).tolist()
                            for item in Periods:
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            Periods = (np.array(Periods) - OPT.GetBasicPeriod(OPT))**2
                            pos = np.argmin(Periods)
                            TabSignProc.Combobox_ChartTimeFreq.setCurrentIndex(pos)
                            self.Columns = (self.dfxAmplitude).columns.tolist()[2:]
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            for item in self.df_Time['Time'].tolist():
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            self.Columns = self.dfxAmplitude.columns.tolist()[2:]
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
                            TabSignProc.Combobox_ChartTimeFreq.clear()
                            for item in self.df_Time['Time'].tolist():
                                TabSignProc.Combobox_ChartTimeFreq.addItem(str(item))
                            self.Columns = (self.dfxPhase).columns.tolist()[2:]
                    # Report GroupBox
                    if Case != 12 and (Case != 14): #!###############################
                        if AnalysisType == 'FFT':
                            Text = 'Method: FFT\n'
                            Text = Text+'Mobile window: '+MobileWin+'\n'
                            if MobileWin:
                                Text = Text+'Mobile window lenght: '+MobileWinLenght+' hr\n'
                            Text = Text+'FFT window: '+FFTwin+'\n'
                            Text = Text+'Detrending: '+Detrending+'\n'
                            Text = Text+'Period Extracted:\n'
                            for PeriodExt in PeriodsExt.split(','):
                                Text = Text+'\t'+PeriodExt+' hr\n'
                            Text = Text+'Processed sensors:\n'
                            for item in Sensors.split(','):
                                Text = Text+'\t'+item+'\n'
                        else:
                            Text = 'Method: LPM\n'
                            Text = Text+'Mobile window: '+MobileWin+'\n'
                            if MobileWin:
                                Text = Text+'Mobile window lenght: '+MobileWinLenght+' hr\n'
                            Text = Text+'Ref Sens: '+RefSens+'\n'
                            Text = Text+'Degree of freedom: '+dof+'\n'
                            Text = Text+'Order: '+order+'\n'
                            Text = Text+'Processed sensors:\n'
                            for item in Sensors.split(','):
                                Text = Text+'\t'+item+'\n'

                        #
                        TabSignProc.Label_Report.setText(Text)
                    # Sensors GroupBox
                    VAR.GetiFlowSelf(VAR).progress.setValue(60)
                    if (Case != 12) and (Case != 11) and (Case != 14): #!###############################
                        if TabSignProc.VBoxSensor is not None:
                            while TabSignProc.VBoxSensor.count():
                                item = TabSignProc.VBoxSensor.takeAt(0)
                                widget = item.widget()
                                if widget is not None:
                                    widget.deleteLater()
                                else:
                                    self.clearLayout(item.layout())
                        #
                        contPos = 0
                        for Sensor in self.Columns:
                            CheckBox = PQW.QCheckBox(Sensor)
                            CheckBox.setChecked(True)
                            CheckBox.toggled.connect(TabSignProc.SensorActiveChange)
                            if contPos % 2 == 0:
                                TabSignProc.VBoxSensor.addWidget(CheckBox,int(contPos/2),0,1,1)
                            else:
                                TabSignProc.VBoxSensor.addWidget(CheckBox,int(contPos/2),1,1,1)
                            contPos = contPos + 1
                    # Chart
                    if Case != -1:
                        #
                        if Case == 11:
                            if TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
                                pass
                            elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
                                Ylim = TabSignProc.ax.get_ylim()
                                Xlim = TabSignProc.ax.get_xlim()
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
                                Ylim = TabSignProc.ax.get_ylim()
                                Xlim = TabSignProc.ax.get_xlim()
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
                                Ylim = TabSignProc.ax.get_ylim()
                                Xlim = TabSignProc.ax.get_xlim()
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
                                Ylim = TabSignProc.ax.get_ylim()
                                Xlim = TabSignProc.ax.get_xlim()
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
                                Ylim = TabSignProc.ax.get_ylim()
                                Xlim = TabSignProc.ax.get_xlim()
                        #
                        TabSignProc.Chart_Fig.clear()
                        TabSignProc.ax = TabSignProc.Chart_Fig.add_subplot(111)
                        #
                        Colors = []
                        if(VAR.GetChartColors(VAR) is None):
                            Colors = []
                        else:
                            Colors = VAR.GetChartColors(VAR)
                            if len(Colors) < len(self.Columns):
                                Colors = []
                                VAR.SetChartColors(VAR,None)
                        #
                        VAR.GetiFlowSelf(VAR).progress.setValue(70)
                        #
                        if TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
                            TabSignProc.df_chart_data = self.dfxSRN[TabSignProc.Combobox_ChartTimeFreq.currentIndex()]
                            # TabSignProc.df_chart_data = 20*np.log10(TabSignProc.df_chart_data)
                            #
                            Ytemp = []
                            Heights = VAR.GetActiveParameters(VAR,7).split(',')
                            Flag = 0
                            # print(Sensors.split(','))
                            for i,Sensor in enumerate(VAR.GetActiveParameters(VAR,6).split(',')):
                                if Sensor in Sensors.split(','):
                                # if Sensor == UPSens:
                                #     Flag = 1
                                # if Flag == 1:
                                    Ytemp.append(float(Heights[i]))
                                # if Sensor == DOWNSens:
                                #     Flag = 0
                            #
                            TabSignProc.yChart = Ytemp
                            Y = []
                            for i in range(0,len(Ytemp)-1):
                                if i == 0:
                                    Y.append(Ytemp[i]-(Ytemp[i+1]-Ytemp[i])/2)
                                Y.append(Ytemp[i]+(Ytemp[i+1]-Ytemp[i])/2)
                            Y.append(Ytemp[len(Ytemp)-1]+(Ytemp[len(Ytemp)-1]-Ytemp[len(Ytemp)-2])/2)
                            #
                            TabSignProc.y = np.array(Y)
                            #
                            X = np.array(self.dfxAmplitude['Freq'].drop_duplicates().tolist())
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                pass
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                X = X * 86400.0
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                X = X * 3600.0
                            X = X.tolist()
                            X.append(X[-1]+(X[-1]-X[-2])/2)
                            TabSignProc.x = np.array(X)
                            #
                            plot = TabSignProc.ax.pcolormesh(TabSignProc.x, TabSignProc.y, TabSignProc.df_chart_data.T, cmap='RdBu')
                            cbar = TabSignProc.Chart_Fig.colorbar(plot, ax=TabSignProc.ax)
                            cbar.ax.set_ylabel('SNR', rotation=90,fontsize=TabSignProc.MPL_AxisTitle)
                        elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
                            # startTime = time.time()
                            ColName = ['Time']
                            for item in self.Columns:
                                ColName.append(item)
                            df_temp = pd.DataFrame(columns = ColName)
                            #
                            for i,item in enumerate(self.dfxSRN):
                                List_Temp = self.df_Time.iloc[i].tolist()
                                for item2 in (item[TabSignProc.Combobox_ChartTimeFreq.currentIndex()]).tolist():
                                    # List_Temp.append(10*np.log10(item2))
                                    List_Temp.append(item2)
                                df_temp.loc[i] = List_Temp
                            TabSignProc.df_chart_data = df_temp
                            # endTime = time.time()
                            # print('Chart data: ',endTime-startTime)
                            #
                            for i in range(0,len((VAR.GetActiveParameters(VAR,6).split(',')))):
                                try:
                                    if TabSignProc.VBoxSensor.itemAt(i).widget().text() in self.Columns:
                                        TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(True)
                                        if TabSignProc.VBoxSensor.itemAt(i).widget().isChecked():
                                            if(VAR.GetChartColors(VAR) == None):
                                                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                    if TabSignProc.df_chart_data.shape[0] == 1:
                                                        plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s'), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                    else:
                                                        plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s'), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                    if TabSignProc.df_chart_data.shape[0] == 1:
                                                        plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                    else:
                                                        plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                Colors.append(plot[0].get_color())
                                            else:
                                                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                    if TabSignProc.df_chart_data.shape[0] == 1:
                                                        plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s'), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                    else:
                                                        plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s'), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                    if TabSignProc.df_chart_data.shape[0] == 1:
                                                        plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                    else:
                                                        plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                    else:
                                        TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(False)
                                except:
                                    pass
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
                            # pass
                            # startTime = time.time()
                            #
                            TabSignProc.df_chart_data = self.dfxPhase[self.dfxPhase['Freq'] == 1.0/(float(TabSignProc.Combobox_ChartTimeFreq.currentText())*3600.0)]
                            del TabSignProc.df_chart_data['Freq']
                            # endTime = time.time()
                            # print('Chart data: ',endTime-startTime)
                            #
                            for i in range(0,len(self.Columns)):
                                if TabSignProc.VBoxSensor.itemAt(i).widget().text() in self.Columns:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(True)
                                    if TabSignProc.VBoxSensor.itemAt(i).widget().isChecked():
                                        if(VAR.GetChartColors(VAR) == None):
                                            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                else:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                else:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            Colors.append(plot[0].get_color())
                                        else:
                                            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                else:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                else:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                else:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(False)
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
                            # startTime = time.time()
                            #
                            TabSignProc.df_chart_data = self.dfxAmplitude[self.dfxAmplitude['Freq'] == 1.0/(float(TabSignProc.Combobox_ChartTimeFreq.currentText())*3600.0)]
                            del TabSignProc.df_chart_data['Freq']
                            # endTime = time.time()
                            # print('Chart data: ',endTime-startTime)
                            #
                            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                            First = Handle.readline().split(';')[0]
                            if First == 'FFT':
                                Handle.readline()
                                Handle.readline()
                                Wintype = Handle.readline().split(';')[0]
                                if Wintype == 'Rectangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,0)
                                elif Wintype == 'Triangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,1)
                                elif Wintype == 'Bartlett':
                                    Corr = OPT.GetFFTcorAMP(OPT,2)
                                elif Wintype == 'Hanning':
                                    Corr = OPT.GetFFTcorAMP(OPT,3)
                                elif Wintype == 'Hamming':
                                    Corr = OPT.GetFFTcorAMP(OPT,4)
                                elif Wintype == 'FlatTop':
                                    Corr = OPT.GetFFTcorAMP(OPT,5)
                                #
                                for Col in (TabSignProc.df_chart_data.columns.tolist())[1:]:
                                    TabSignProc.df_chart_data[Col] = TabSignProc.df_chart_data[Col] * Corr
                            Handle.close()
                            #
                            for i in range(0,len(self.Columns)):
                                if TabSignProc.VBoxSensor.itemAt(i).widget().text() in self.Columns:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(True)
                                    if TabSignProc.VBoxSensor.itemAt(i).widget().isChecked():
                                        if(VAR.GetChartColors(VAR) == None):
                                            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                else:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                                else:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            Colors.append(plot[0].get_color())
                                        else:
                                            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                else:
                                                    plot = TabSignProc.ax.plot(pd.to_datetime(TabSignProc.df_chart_data['Time'],unit='s').to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                                if TabSignProc.df_chart_data.shape[0] == 1:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                                else:
                                                    plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Time'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                else:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(False)
                            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                            First = Handle.readline().split(';')[0]
                            if First == 'FFT':
                                Handle.readline()
                                Handle.readline()
                                Wintype = Handle.readline().split(';')[0]
                                if Wintype == 'Rectangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,0)
                                elif Wintype == 'Triangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,1)
                                elif Wintype == 'Bartlett':
                                    Corr = OPT.GetFFTcorAMP(OPT,2)
                                elif Wintype == 'Hanning':
                                    Corr = OPT.GetFFTcorAMP(OPT,3)
                                elif Wintype == 'Hamming':
                                    Corr = OPT.GetFFTcorAMP(OPT,4)
                                elif Wintype == 'Flat Top':
                                    Corr = OPT.GetFFTcorAMP(OPT,5)
                                #
                                for Col in (TabSignProc.df_chart_data.columns.tolist())[1:]:
                                    TabSignProc.df_chart_data[Col] = TabSignProc.df_chart_data[Col] / Corr
                            Handle.close()
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
                            TabSignProc.df_chart_data = self.dfxAmplitude[self.dfxAmplitude['Time'] == float(TabSignProc.Combobox_ChartTimeFreq.currentText())]
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                pass
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x * 86400.0)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x * 3600.0)
                            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                            First = Handle.readline().split(';')[0]
                            if First == 'FFT':
                                Handle.readline()
                                Handle.readline()
                                Wintype = Handle.readline().split(';')[0]
                                if Wintype == 'Rectangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,0)
                                elif Wintype == 'Triangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,1)
                                elif Wintype == 'Bartlett':
                                    Corr = OPT.GetFFTcorAMP(OPT,2)
                                elif Wintype == 'Hanning':
                                    Corr = OPT.GetFFTcorAMP(OPT,3)
                                elif Wintype == 'Hamming':
                                    Corr = OPT.GetFFTcorAMP(OPT,4)
                                elif Wintype == 'Flat Top':
                                    Corr = OPT.GetFFTcorAMP(OPT,5)
                                #
                                for Col in (TabSignProc.df_chart_data.columns.tolist())[1:]:
                                    TabSignProc.df_chart_data[Col] = TabSignProc.df_chart_data[Col].apply(lambda x: x * Corr)
                            Handle.close()
                            #
                            for i in range(0,len(self.Columns)):
                                if TabSignProc.VBoxSensor.itemAt(i).widget().text() in self.Columns:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(True)
                                    if TabSignProc.VBoxSensor.itemAt(i).widget().isChecked():
                                        if(VAR.GetChartColors(VAR) == None):
                                            if TabSignProc.df_chart_data.shape[0] == 1:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            else:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            Colors.append(plot[0].get_color())
                                        else:
                                            if TabSignProc.df_chart_data.shape[0] == 1:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            else:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                else:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(False)
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                pass
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x / 86400.0)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x / 3600.0)
                            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+TabSignProc.Combobox_Analysis.currentText().replace('Run: ','')+'.run','r')
                            First = Handle.readline().split(';')[0]
                            if First == 'FFT':
                                Handle.readline()
                                Handle.readline()
                                Wintype = Handle.readline().split(';')[0]
                                if Wintype == 'Rectangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,0)
                                elif Wintype == 'Triangular':
                                    Corr = OPT.GetFFTcorAMP(OPT,1)
                                elif Wintype == 'Bartlett':
                                    Corr = OPT.GetFFTcorAMP(OPT,2)
                                elif Wintype == 'Hanning':
                                    Corr = OPT.GetFFTcorAMP(OPT,3)
                                elif Wintype == 'Hamming':
                                    Corr = OPT.GetFFTcorAMP(OPT,4)
                                elif Wintype == 'Flat Top':
                                    Corr = OPT.GetFFTcorAMP(OPT,5)
                                #
                                for Col in (TabSignProc.df_chart_data.columns.tolist())[1:]:
                                    TabSignProc.df_chart_data[Col] = TabSignProc.df_chart_data[Col] / Corr
                            Handle.close()
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
                            TabSignProc.df_chart_data = self.dfxPhase[self.dfxPhase['Time'] == float(TabSignProc.Combobox_ChartTimeFreq.currentText())]
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                pass
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x * 86400.0)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x * 3600.0)
                            #
                            for i in range(0,len(self.Columns)):
                                if TabSignProc.VBoxSensor.itemAt(i).widget().text() in self.Columns:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(True)
                                    if TabSignProc.VBoxSensor.itemAt(i).widget().isChecked():
                                        if(VAR.GetChartColors(VAR) == None):
                                            if TabSignProc.df_chart_data.shape[0] == 1:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            else:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text())
                                            Colors.append(plot[0].get_color())
                                        else:
                                            if TabSignProc.df_chart_data.shape[0] == 1:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            else:
                                                plot = TabSignProc.ax.plot(TabSignProc.df_chart_data['Freq'].to_numpy(), (TabSignProc.df_chart_data[TabSignProc.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabSignProc.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                else:
                                    TabSignProc.VBoxSensor.itemAt(i).widget().setEnabled(False)
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                pass
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x / 86400.0)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.df_chart_data['Freq'] = TabSignProc.df_chart_data['Freq'].apply(lambda x: x / 3600.0)
                        #
                        if TabSignProc.Combobox_ChartType.currentText() != 'SNR heatmap':
                            if len(self.Columns) > 5:
                                TabSignProc.ax.legend(ncol=int(len(self.Columns)/5+1),fontsize=TabSignProc.MPL_Legend)
                            else:
                                TabSignProc.ax.legend(ncol=len(self.Columns),fontsize=TabSignProc.MPL_Legend)
                        #
                        TabSignProc.ax.grid(True, which='both', axis='both', linestyle='--')
                        #
                        if TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
                            TabSignProc.ax.set_ylabel('Amplitude',fontsize=TabSignProc.MPL_AxisTitle)
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
                            TabSignProc.ax.set_ylabel('Phase',fontsize=TabSignProc.MPL_AxisTitle)
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
                            TabSignProc.ax.set_ylabel('Amplitude',fontsize=TabSignProc.MPL_AxisTitle)
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabSignProc.ax.set_xlabel('Time (s)',fontsize=TabSignProc.MPL_AxisTitle)
                            else:
                                pass
                        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
                            TabSignProc.ax.set_ylabel('Phase',fontsize=TabSignProc.MPL_AxisTitle)
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabSignProc.ax.set_xlabel('Time (s)',fontsize=TabSignProc.MPL_AxisTitle)
                            else:
                                pass
                        elif TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
                            TabSignProc.ax.set_ylabel('z (m)',fontsize=TabSignProc.MPL_AxisTitle)
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                TabSignProc.ax.set_xlabel('Frequency (Hz)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabSignProc.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabSignProc.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabSignProc.MPL_AxisTitle)
                        elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
                            TabSignProc.ax.set_ylabel('SNR (dB)',fontsize=TabSignProc.MPL_AxisTitle)
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                TabSignProc.ax.set_xlabel('Time (s)')
                            else:
                                pass
                        #
                        VAR.GetiFlowSelf(VAR).progress.setValue(90)
                        if Case == 11:
                            if TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
                                pass
                            elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
                                TabSignProc.ax.set_ylim(Ylim)
                                TabSignProc.ax.set_xlim(Xlim)
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
                                TabSignProc.ax.set_ylim(Ylim)
                                TabSignProc.ax.set_xlim(Xlim)
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
                                TabSignProc.ax.set_ylim(Ylim)
                                TabSignProc.ax.set_xlim(Xlim)
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
                                TabSignProc.ax.set_ylim(Ylim)
                                TabSignProc.ax.set_xlim(Xlim)
                            elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
                                TabSignProc.ax.set_ylim(Ylim)
                                TabSignProc.ax.set_xlim(Xlim)
                        else:
                            pass
                        #
                        TabSignProc.ax.tick_params(axis='both', labelsize=TabSignProc.MPL_AxisTick)
                        #
                        TabSignProc.Canvas.draw()
                        #
                        if(VAR.GetChartColors(VAR) is None):
                            VAR.SetChartColors(VAR, Colors)
                    # Menu
                    VAR.GetiFlowSelf(VAR).Menu_SP_Export.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_SP_PhaseCorr.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_SP_BREcalc.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_RunSP.setEnabled(True)
        # Connect all internal event
        TabSignProc.Combobox_Method.currentIndexChanged.connect(TabSignProc.on_Combobox_Method_change) # ComboBox event change item
        TabSignProc.Combobox_Detrending.currentIndexChanged.connect(TabSignProc.on_Combobox_Detrending_change) # ComboBox event change item
        TabSignProc.Combobox_FFTwin.currentIndexChanged.connect(TabSignProc.on_Combobox_FFTwin_change) # ComboBox event change item
        TabSignProc.Combobox_Analysis.currentIndexChanged.connect(TabSignProc.on_Combobox_Analysis_change) # ComboBox event change item
        TabSignProc.Combobox_ChartType.currentIndexChanged.connect(TabSignProc.on_Combobox_ChartType_change) # ComboBox event change item
        TabSignProc.Combobox_ChartTimeFreq.currentIndexChanged.connect(TabSignProc.on_Combobox_ChartTimeFreq_change) # ComboBox event change item
        #
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        #
        return

    def on_Button_SP_clicked(self):
        print('TabSignProc - on_Button_SP_clicked')
        # Lunch the wizard for importing a new probe
        WizardAddProbe = WSP.SignalProcessing()
        WizardAddProbe.exec_()
        return
#%%
    def on_Combobox_Method_change(self):
        print('TabSignProc - on_Combobox_Method_change')
        if TabSignProc.Combobox_Method.currentText() == 'LPM':
            TabSignProc.Combobox_Detrending.setEnabled(False)
            TabSignProc.Combobox_FFTwin.setEnabled(False)
        else:
            TabSignProc.Combobox_Detrending.setEnabled(True)
            TabSignProc.Combobox_FFTwin.setEnabled(True)
        TSP.TabSignProc.Update(TSP,8) #!
        return
#%%
    def on_Combobox_Detrending_change(self):
        print('TabSignProc - on_Combobox_Detrending_change')
        TSP.TabSignProc.Update(TSP,8) #!
        return
#%%
    def on_Combobox_FFTwin_change(self):
        print('TabSignProc - on_Combobox_FFTwin_change')
        TSP.TabSignProc.Update(TSP,8) #!
        return
# #%%
    def on_Combobox_Analysis_change(self):
        print('TabSignProc - on_Combobox_Analysis_change')
        TSP.TabSignProc.Update(TSP,9)
        return
#%%
    def on_Combobox_ChartType_change(self):
        print('TabSignProc - on_Combobox_ChartType_change')
        TSP.TabSignProc.Update(TSP,12)
        return
#%%
    def on_Combobox_ChartTimeFreq_change(self):
        print('TabSignProc - on_Combobox_ChartTimeFreq_change')
        TSP.TabSignProc.Update(TSP,14)
        return
#%%
    def SensorActiveChange(self):
        print('TabSignProc - SensorActiveChange')
        TSP.TabSignProc.Update(TSP,11)
        return
#%%
    def on_Button_SPExport_clicked(self):
        print('TabSignProc - on_Button_SPExport_clicked')
        dfcopy = TabSignProc.df_chart_data.copy()
        if TabSignProc.Combobox_ChartType.currentText() != 'SNR heatmap':
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                dfcopy['Time'] = pd.to_datetime(dfcopy['Time'],unit='s')
        if TabSignProc.Combobox_ChartType.currentText() == 'SNR heatmap':
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export SNR heatmap to File', '../exports/SRNheatmap_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                    Handle.write('Time: '+datetime.datetime.utcfromtimestamp(int(float(TabSignProc.Combobox_ChartTimeFreq.currentText()))).strftime('%Y-%m-%d %H:%M:%S')+'\n')
                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                    Handle.write('Time: '+str(TabSignProc.Combobox_ChartTimeFreq.currentText())+'\n\n')
                #
                string = ''
                for i in range(0,TabSignProc.x.shape[0]-1):
                    string = string +','+ str(TabSignProc.x[i])
                Handle.write(string+'\n')
                #
                
                for i in range(0,len(TabSignProc.yChart)):
                    string = str(TabSignProc.yChart[i])
                    for j in range(0,dfcopy.shape[0]):
                        string = string + ',' + str(dfcopy[j,i])
                    Handle.write(string+'\n')
                Handle.close()
        elif TabSignProc.Combobox_ChartType.currentText() == 'SNR vs Time':
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export SRN vs Time to File', '../exports/SNRvsTime_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                Handle.write('Frequency: '+TabSignProc.Combobox_ChartTimeFreq.currentText()+' hr-1\n\n')
                Handle.write(','.join(dfcopy.columns.tolist())+'\n')
                for i in range(0,dfcopy.shape[0]):
                    Handle.write(','.join([str(item) for item in dfcopy.iloc[i].tolist()])+'\n')
                Handle.close()
        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Time':
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Phase vs Time to File', '../exports/PhasevsTime_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                Handle.write('Frequency: '+TabSignProc.Combobox_ChartTimeFreq.currentText()+' hr-1\n\n')
                Handle.write(','.join(dfcopy.columns.tolist())+'\n')
                for i in range(0,dfcopy.shape[0]):
                    Handle.write(','.join([str(item) for item in dfcopy.iloc[i].tolist()])+'\n')
                Handle.close()
        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Time':
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Amplitude vs Time to File', '../exports/AmplitudevsTime_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                Handle.write('Frequency: '+TabSignProc.Combobox_ChartTimeFreq.currentText()+' hr-1\n\n')
                Handle.write(','.join(dfcopy.columns.tolist())+'\n')
                for i in range(0,dfcopy.shape[0]):
                    Handle.write(','.join([str(item) for item in dfcopy.iloc[i].tolist()])+'\n')
                Handle.close()
        elif TabSignProc.Combobox_ChartType.currentText() == 'Amplitude vs Frequency':
            dfcopy = dfcopy.drop(['Time'],axis=1)
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Amplitude vs Frequency to File', '../exports/AmplitudevsFrequency_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                    Handle.write('Time: '+datetime.datetime.utcfromtimestamp(int(float(TabSignProc.Combobox_ChartTimeFreq.currentText()))).strftime('%Y-%m-%d %H:%M:%S')+'\n')
                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                    Handle.write('Time: '+str(TabSignProc.Combobox_ChartTimeFreq.currentText())+'\n\n')
                #
                Handle.write(','.join(dfcopy.columns.tolist())+'\n')
                for i in range(0,dfcopy.shape[0]):
                    Handle.write(','.join([str(item) for item in dfcopy.iloc[i].tolist()])+'\n')
                Handle.close()
        elif TabSignProc.Combobox_ChartType.currentText() == 'Phase vs Frequency':
            dfcopy = dfcopy.drop(['Time'],axis=1)
            file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Phase vs Frequency to File', '../exports/PhasevsFrequency_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
            if file_export[0]:
                Handle = open(file_export[0],'w')
                Handle.write(TabSignProc.Combobox_Analysis.currentText()+'\n')
                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                    Handle.write('Time: '+datetime.datetime.utcfromtimestamp(int(float(TabSignProc.Combobox_ChartTimeFreq.currentText()))).strftime('%Y-%m-%d %H:%M:%S')+'\n')
                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                    Handle.write('Time: '+str(TabSignProc.Combobox_ChartTimeFreq.currentText())+'\n\n')
                #
                Handle.write(','.join(dfcopy.columns.tolist())+'\n')
                for i in range(0,dfcopy.shape[0]):
                    Handle.write(','.join([str(item) for item in dfcopy.iloc[i].tolist()])+'\n')
                Handle.close()
        #
        return

    def on_Button_SP_PhaseCorr_clicked(self):
        print('TabSignProc - on_Button_SP_PhaseCorr_clicked')
        # Lunch the wizard for importing a new probe
        WizardPhase = WPC.Phase()
        WizardPhase.exec_()
        TSP.TabSignProc.Update(TSP,9)
        return

    def on_Button_SP_BREcalc_clicked(self):
        print('TabSignProc - on_Button_SP_BREcalc_clicked')
        # Lunch the wizard for importing a new probe
        WizardElCalc = WEC.BREcalc()
        WizardElCalc.exec_()
        TSP.TabSignProc.Update(TSP,9)
        return
