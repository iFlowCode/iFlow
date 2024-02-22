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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import glob
# # from datetime import datetime
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
import pandas as pd
# # import pickle
# # import datetime
# # import time
import numpy as np
# Import custom library
from Variables import VAR
from Options import OPT
from ScrollLabel import ScrollLabel
import TabFreqAnal as TFA
# # import STabFFTAnal as STFA
# # import STabLPMAnal as STLA
import WizManageHarmonics as WMH
from loguru import logger

import WizardFA as WFA
#------------------------------------------------------------------------------#
'''
TabFreqAnal Class
'''
class TabFreqAnal(PQW.QWidget):
    def __init__(self):
        super().__init__()
        logger.debug('TabFreqAnal - Start Class')
        # Set Matplotlib fonts size
        TabFreqAnal.MPL_AxisTitle = int(VAR.GetMPLAxisTitleFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabFreqAnal.MPL_AxisTick = int(VAR.GetMPLAxisTickFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabFreqAnal.MPL_Legend = int(VAR.GetMPLLegendFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # Store class object
        VAR.SetTabFreqAnal(VAR, self)
        # Create grid layot for the window
        Layout_Tab_FreqAnal = PQW.QHBoxLayout()
        # Layout_Tab_FreqAnal = PQW.QGridLayout()
        # Left collumn
        container_left = PQW.QFrame()
        Layout_Tab_FreqAnal_Left = PQW.QVBoxLayout()
        # Button Calculate
        TabFreqAnal.Button_FA = PQW.QPushButton('Frequency analysis')
        TabFreqAnal.Button_FA.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        # #         TabFreqAnal.Button_FA.setToolTip('Launch Frequency analysis Wizard') # Tooltip message
        TabFreqAnal.Button_FA.clicked.connect(self.on_Button_FA_clicked) # Button event Click on
        Layout_Tab_FreqAnal_Left.addWidget(TabFreqAnal.Button_FA)
        # Groupbox Filter
        self.GroupBox_Filter = PQW.QGroupBox('Filter:')
        # Create the Layout for the Groupbox Filter
        self.VBoxFilter = PQW.QVBoxLayout()
        # Label
        Label_FFTWin = PQW.QLabel('FFTWin:')
        # Element ComboBox FFTWin
        TabFreqAnal.Combobox_FFTWin = PQW.QComboBox()
        TabFreqAnal.Combobox_FFTWin.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        #         TabFreqAnal.Combobox_FFTWin.setToolTip('Filter results by FTTwin') # Tooltip message
        #
        for item in VAR.GetFFTWindowfunction(VAR):
            TabFreqAnal.Combobox_FFTWin.addItem(item)
        #
        TabFreqAnal.Combobox_FFTWin.currentIndexChanged.connect(self.on_Combobox_FFTWin_change) # ComboBox event change item
        # Add elements to the Layout
        self.VBoxFilter.addWidget(Label_FFTWin)
        self.VBoxFilter.addWidget(TabFreqAnal.Combobox_FFTWin)
        # Add the Layout to the Groupbox Filter
        self.GroupBox_Filter.setLayout(self.VBoxFilter)

        Layout_Tab_FreqAnal_Left.addWidget(self.GroupBox_Filter)
        #
        # Groupbox Chart
        self.GroupBox_Chart = PQW.QGroupBox('Chart:')
        # Create the lyout for the Groupbox Chart
        self.VBoxChart = PQW.QVBoxLayout()
        # Label
        Label_Analysis = PQW.QLabel('Analysis:')
        # Element ComboBox Analysis
        TabFreqAnal.Combobox_Analysis = PQW.QComboBox()
        # TabFreqAnal.Combobox_Analysis.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        # #         TabFreqAnal.Combobox_Analysis.setToolTip('Choose analysis to show') # Tooltip message
        TabFreqAnal.Combobox_Analysis.currentIndexChanged.connect(self.on_Combobox_Analysis_change) # ComboBox event change item
        # Label
        Label_ChartType = PQW.QLabel('Chart type:')
        # Element Combobox ChartType
        TabFreqAnal.Combobox_ChartType = PQW.QComboBox()
        # TabFreqAnal.Combobox_ChartType.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        # #         TabFreqAnal.Combobox_ChartType.setToolTip('Choose the data to display') # Tooltip message
        #
        for item in VAR.GetChartTypeFrequecyAnalysis(VAR):
            TabFreqAnal.Combobox_ChartType.addItem(item)
        #
        TabFreqAnal.Combobox_ChartType.currentIndexChanged.connect(self.on_Combobox_ChartType_change) # ComboBox event change item
        # Label
        Label_TopSensor = PQW.QLabel('TopSensor:')
        # Element Combobox TopSensor
        TabFreqAnal.Combobox_TopSensor = PQW.QComboBox()
        # TabFreqAnal.Combobox_TopSensor.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        # #         TabFreqAnal.Combobox_TopSensor.setToolTip('Choose the TopSensor') # Tooltip message
        #         #
        TabFreqAnal.Combobox_TopSensor.currentIndexChanged.connect(self.on_Combobox_TopSensor_change) # ComboBox event change item
        # Add elements to the Layout
        self.VBoxChart.addWidget(Label_Analysis)
        self.VBoxChart.addWidget(TabFreqAnal.Combobox_Analysis)
        self.VBoxChart.addWidget(Label_ChartType)
        self.VBoxChart.addWidget(TabFreqAnal.Combobox_ChartType)
        self.VBoxChart.addWidget(Label_TopSensor)
        self.VBoxChart.addWidget(TabFreqAnal.Combobox_TopSensor)
        # Add the Layout to the Groupbox Chart
        self.GroupBox_Chart.setLayout(self.VBoxChart)
        #
        Layout_Tab_FreqAnal_Left.addWidget(self.GroupBox_Chart)
        # Groupbox Report
        self.GroupBox_Report = PQW.QGroupBox('Report:')
        # Create Layout for the Groupbox Report
        self.VBoxReport = PQW.QVBoxLayout()
        # Element EditLine
        TabFreqAnal.Label_Report = ScrollLabel(self)
        TabFreqAnal.Label_Report.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ')
        # Add elements to the Layout
        self.VBoxReport.addWidget(TabFreqAnal.Label_Report)
        # Add the Layout to the Groupbox Report
        self.GroupBox_Report.setLayout(self.VBoxReport)
        #
        Layout_Tab_FreqAnal_Left.addWidget(self.GroupBox_Report)
        # Groupbox Sensors
        self.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
        # Create Layout for the Groupbox Sensor
        TabFreqAnal.VBoxSensor = PQW.QGridLayout()
        # #         TabFreqAnal.VBoxSensor = PQW.QVBoxLayout()
        self.GroupBox_Sensors.setLayout(TabFreqAnal.VBoxSensor)
        #
        Layout_Tab_FreqAnal_Left.addWidget(self.GroupBox_Sensors)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Tab_FreqAnal_Left)
        # Chart column
        container_right = PQW.QFrame()
        Layout_Tab_FreqAnal_Right = PQW.QVBoxLayout()
        TabFreqAnal.Chart_Fig = plt.figure()
        TabFreqAnal.Canvas = FigureCanvas(TabFreqAnal.Chart_Fig)
        self.Toolbar = NavigationToolbar(TabFreqAnal.Canvas, self)
        TabFreqAnal.Canvas.draw()
        #
        Layout_Tab_FreqAnal_Right.addWidget(self.Toolbar)
        Layout_Tab_FreqAnal_Right.addWidget(TabFreqAnal.Canvas)
        #
        container_right.setLayout(Layout_Tab_FreqAnal_Right)
        #
        Layout_Tab_FreqAnal.addWidget(container_left)
        Layout_Tab_FreqAnal.addWidget(container_right)
        # Set layout of tab
        self.setLayout(Layout_Tab_FreqAnal)

    # @logger.catch
    def Update(self,Case):
        logger.debug(f"TabFreqAnal Update - Case: {Case}")
        '''
        Case 0: Event generated by the starting of the GUI
        Case 1: Event generated by on change project #TODO
        Case 2: Event generated by button new project AND rename project #TODO
        Case 3: Event generated by button delete project #TODO
        Case 4: Event generated by rename probe AND import probe #TODO wizard AddProbe 
        Case 5: Event generated by Button Remove Probe #TODO
        Case 6: Event generated by on active probe change #TODO
        # Case 7: Event generated by wizard Signal Processing
        Case 8: on combobox analysis change
        Case 9: on chart type change
        Case 10: on TopSensor change AND SensorActiveChange
        Case 11: FFTwin filter Change
        # Case 12: #!
        # Case 13: #!
        '''
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        # Disconect all the internal events
        TabFreqAnal.Combobox_FFTWin.currentIndexChanged.disconnect()
        TabFreqAnal.Combobox_Analysis.currentIndexChanged.disconnect()
        TabFreqAnal.Combobox_TopSensor.currentIndexChanged.disconnect()
        TabFreqAnal.Combobox_ChartType.currentIndexChanged.disconnect()
        #
        if(VAR.GetActiveProject(VAR) == None):
            TabFreqAnal.Button_FA.setEnabled(False)
            # Filter GroupBox
            TabFreqAnal.Combobox_FFTWin.setCurrentIndex(0)
            # Chart GroupBox
            TabFreqAnal.Combobox_ChartType.setCurrentIndex(0)
            TabFreqAnal.Combobox_ChartType.setEnabled(False)
            TabFreqAnal.Combobox_Analysis.clear()
            TabFreqAnal.Combobox_TopSensor.clear()
            # Report GroupBox
            TabFreqAnal.Label_Report.setText('There isn\'t any Project\nCreate one.')
            # Sensors GroupBox
            if TabFreqAnal.VBoxSensor is not None:
                while TabFreqAnal.VBoxSensor.count():
                    item = TabFreqAnal.VBoxSensor.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clearLayout(item.layout())
            # Chart
            TabFreqAnal.Chart_Fig.clear()
            TabFreqAnal.ax = TabFreqAnal.Chart_Fig.add_subplot(111)
            # TabFreqAnal.ax.legend()
            TabFreqAnal.ax.grid(True, which='both', axis='both', linestyle='--')
            TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
            #
            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                TabFreqAnal.ax.set_xlabel('Frequency (Hz)',fontsize=TabFreqAnal.MPL_AxisTitle)
            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                TabFreqAnal.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                TabFreqAnal.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
            TabFreqAnal.ax.tick_params(axis='both', labelsize=TabFreqAnal.MPL_AxisTick)
            TabFreqAnal.Canvas.draw()
            # Menu Update
            VAR.GetiFlowSelf(VAR).Menu_RunFA.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_FA_Export_PDA.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_FA_Export_Amplitude.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_FA_Export_Phase.setEnabled(False)
        else:
            if(VAR.GetActiveProbe(VAR) == None):
                TabFreqAnal.Button_FA.setEnabled(False)
                # Filter GroupBox
                TabFreqAnal.Combobox_FFTWin.setCurrentIndex(0)
                # Chart GroupBox
                TabFreqAnal.Combobox_ChartType.setCurrentIndex(0)
                TabFreqAnal.Combobox_ChartType.setEnabled(False)
                TabFreqAnal.Combobox_Analysis.clear()
                TabFreqAnal.Combobox_TopSensor.clear()
                # Report GroupBox
                TabFreqAnal.Label_Report.setText('There isn\'t any Probe\nImport one.')
                # Sensors GroupBox
                if TabFreqAnal.VBoxSensor is not None:
                    while TabFreqAnal.VBoxSensor.count():
                        item = TabFreqAnal.VBoxSensor.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            self.clearLayout(item.layout())
                # Chart
                TabFreqAnal.Chart_Fig.clear()
                TabFreqAnal.ax = TabFreqAnal.Chart_Fig.add_subplot(111)
                # TabFreqAnal.ax.legend()
                TabFreqAnal.ax.grid(True, which='both', axis='both', linestyle='--')
                TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
                #
                if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                    TabFreqAnal.ax.set_xlabel('Frequency (Hz)',fontsize=TabFreqAnal.MPL_AxisTitle)
                elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                    TabFreqAnal.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                    TabFreqAnal.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                TabFreqAnal.Canvas.draw()
                # Menu Update
                VAR.GetiFlowSelf(VAR).Menu_RunFA.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_FA_Export_PDA.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_FA_Export_Amplitude.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_FA_Export_Phase.setEnabled(False)
                #
                if OPT.GetHarmonicFlag(OPT) == 'True':
                    VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Hide Harmonics')
                else:
                    VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Show Harmonics')
            else:
                Runs = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/*.run')
                if len(Runs) == 0:
                    TabFreqAnal.Button_FA.setEnabled(True)
                    # Filter GroupBox
                    TabFreqAnal.Combobox_FFTWin.setCurrentIndex(0)
                    # Chart GroupBox
                    TabFreqAnal.Combobox_ChartType.setCurrentIndex(0)
                    TabFreqAnal.Combobox_ChartType.setEnabled(False)
                    TabFreqAnal.Combobox_Analysis.clear()
                    TabFreqAnal.Combobox_TopSensor.clear()
                    # Report GroupBox
                    TabFreqAnal.Label_Report.setText('There isn\'t any Frequency analysis\nRun one.')
                    # Sensors GroupBox
                    if TabFreqAnal.VBoxSensor is not None:
                        while TabFreqAnal.VBoxSensor.count():
                            item = TabFreqAnal.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    # Chart
                    TabFreqAnal.Chart_Fig.clear()
                    TabFreqAnal.ax = TabFreqAnal.Chart_Fig.add_subplot(111)
                    # TabFreqAnal.ax.legend()
                    TabFreqAnal.ax.grid(True, which='both', axis='both', linestyle='--')
                    TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
                    #
                    if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                        TabFreqAnal.ax.set_xlabel('Frequency (Hz)',fontsize=TabFreqAnal.MPL_AxisTitle)
                    elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                        TabFreqAnal.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                    elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                        TabFreqAnal.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                    TabFreqAnal.Canvas.draw()
                    # Menu Update
                    VAR.GetiFlowSelf(VAR).Menu_RunFA.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_FA_Export_PDA.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_FA_Export_Amplitude.setEnabled(False)
                    VAR.GetiFlowSelf(VAR).Menu_FA_Export_Phase.setEnabled(False)
                    #
                    if OPT.GetHarmonicFlag(OPT) == 'True':
                        VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Hide Harmonics')
                    else:
                        VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Show Harmonics')
                else:
                    VAR.GetiFlowSelf(VAR).progress.setValue(20)
                    TabFreqAnal.Button_FA.setEnabled(True)
                    TabFreqAnal.Combobox_ChartType.setEnabled(True)
                    # Filter GroupBox
                    if (Case != 11) and (Case != 8) and (Case != 9):
                        TabFreqAnal.Combobox_FFTWin.setCurrentIndex(0)
                    # Chart GroupBox
                    if (Case != 8) and (Case != 9):
                        TabFreqAnal.Combobox_Analysis.clear()
                        ContRun = 0
                        for Run in Runs:
                            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+Run.replace('\\','/').split('/')[-1],'r')
                            CheckFilter = Handle.readline().split(';')[0]
                            Handle.close()
                            if TabFreqAnal.Combobox_FFTWin.currentText() == '' or CheckFilter == TabFreqAnal.Combobox_FFTWin.currentText():
                                TabFreqAnal.Combobox_Analysis.addItem('Run: '+Run.replace('\\','/').split('/')[-1].replace('.run',''))
                                ContRun += 1
                        TabFreqAnal.Combobox_Analysis.setCurrentIndex(ContRun-1)
                    #
                    if (Case != 8) and (Case != 10):
                        TabFreqAnal.Combobox_TopSensor.clear()
                        for item in VAR.GetActiveParameters(VAR,6).split(','):
                            TabFreqAnal.Combobox_TopSensor.addItem(item)
                        if TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs PSD':
                            TabFreqAnal.Combobox_TopSensor.setEnabled(False)
                        elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs Amplitude':
                            TabFreqAnal.Combobox_TopSensor.setEnabled(False)
                        elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs LogAmpRatio':
                            TabFreqAnal.Combobox_TopSensor.setEnabled(True)
                        elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs DiffPhase':
                            TabFreqAnal.Combobox_TopSensor.setEnabled(True)
                    # Report GroupBox
                    VAR.GetiFlowSelf(VAR).progress.setValue(40)
                    if Case != -1:
                        ActiveRun = TabFreqAnal.Combobox_Analysis.currentText()
                        if ActiveRun == '':
                            TabFreqAnal.Label_Report.setText('There isn\'t any Frequency analysis\nRun one.')
                            # Sensors GroupBox
                            if TabFreqAnal.VBoxSensor is not None:
                                while TabFreqAnal.VBoxSensor.count():
                                    item = TabFreqAnal.VBoxSensor.takeAt(0)
                                    widget = item.widget()
                                    if widget is not None:
                                        widget.deleteLater()
                                    else:
                                        self.clearLayout(item.layout())
                            # Chart
                            TabFreqAnal.Chart_Fig.clear()
                            TabFreqAnal.ax = TabFreqAnal.Chart_Fig.add_subplot(111)
                            # TabFreqAnal.ax.legend()
                            TabFreqAnal.ax.grid(True, which='both', axis='both', linestyle='--')
                            TabFreqAnal.ax.set_ylabel('PSD')
                            #
                            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                TabFreqAnal.ax.set_xlabel('Frequency (Hz)',fontsize=TabFreqAnal.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                TabFreqAnal.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                TabFreqAnal.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                            #
                            if TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs PSD':
                                TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
                            elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs Amplitude':
                                TabFreqAnal.ax.set_ylabel('Amplitude',fontsize=TabFreqAnal.MPL_AxisTitle)
                            elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs LogAmpRatio':
                                TabFreqAnal.ax.set_ylabel('LogAmpRatio',fontsize=TabFreqAnal.MPL_AxisTitle)
                            elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs DiffPhase':
                                TabFreqAnal.ax.set_ylabel('DiffPhase',fontsize=TabFreqAnal.MPL_AxisTitle)
                            #
                            TabFreqAnal.Canvas.draw()
                            # Menu Update
                            VAR.GetiFlowSelf(VAR).Menu_RunFA.setEnabled(True)
                            VAR.GetiFlowSelf(VAR).Menu_FA_Export_PDA.setEnabled(False)
                            VAR.GetiFlowSelf(VAR).Menu_FA_Export_Amplitude.setEnabled(False)
                            VAR.GetiFlowSelf(VAR).Menu_FA_Export_Phase.setEnabled(False)
                            #
                            if OPT.GetHarmonicFlag(OPT) == 'True':
                                VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Hide Harmonics')
                            else:
                                VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Show Harmonics')
                        else:
                            HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'.run','r')
                            Rows = HandleRun.readlines()
                            HandleRun.close()
                            FFTwinType = (Rows[0]).split(';')[0]
                            Text = 'FFT window: '+FFTwinType+'\n'
                            dfTemp = pd.DataFrame()
                            dfTemp['A'] = [float((Rows[1]).split(';')[0])]
                            dfTemp['B'] = [float((Rows[2]).split(';')[0])]
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                Text = Text + 'From: ' + str((Rows[1]).split(';')[0])+'\n'
                            else:
                                Text = Text + 'From: ' +pd.Timestamp(dfTemp['A'].iloc[0], unit='s').strftime('%Y-%m-%d %H:%M:%S')+'\n'
                            if VAR.GetActiveParameters(VAR,2) == 'Time':
                                Text = Text + 'To: ' + str((Rows[2]).split(';')[0])+'\n'
                            else:
                                Text = Text + 'To: ' + pd.Timestamp(dfTemp['B'].iloc[0], unit='s').strftime('%Y-%m-%d %H:%M:%S')+'\n'
                            TabFreqAnal.Label_Report.setText(Text)
                            # Load Data
                            VAR.GetiFlowSelf(VAR).progress.setValue(60)
                            if Case != -1:
                                if TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs PSD':
                                    self.df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'_PSD.pkz',compression='zip')
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs Amplitude':
                                    self.df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'_Amplitude.pkz',compression='zip')
                                    if FFTwinType == 'Rectangular':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,0)
                                    elif FFTwinType == 'Triangular':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,1)
                                    elif FFTwinType == 'Bartlett':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,2)
                                    elif FFTwinType == 'Hanning':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,3)
                                    elif FFTwinType == 'Hamming':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,4)
                                    elif FFTwinType == 'Flat Top':
                                        FFTwinCor = OPT.GetFFTcorAMP(OPT,5)
                                    for Sensor in (self.df_chart.columns.tolist())[1:]:
                                        self.df_chart[Sensor] = self.df_chart[Sensor] * FFTwinCor
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs LogAmpRatio':
                                    self.df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'_Amplitude.pkz',compression='zip')
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs DiffPhase':
                                    self.df_chart = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'_Phase.pkz',compression='zip')
                                #
                                self.df_chart = self.df_chart[self.df_chart['Freq'] > 0.0]
                                if TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs PSD':
                                    pass
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs Amplitude':
                                    pass
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs LogAmpRatio':
                                    WaterSensor = TabFreqAnal.Combobox_TopSensor.currentText()
                                    WaterSensorAmplitude = self.df_chart[WaterSensor].to_numpy()
                                    Flag = 0
                                    df_chart_temp = pd.DataFrame()
                                    df_chart_temp['Freq'] = self.df_chart['Freq']
                                    for Sensor in (self.df_chart.columns.tolist())[1:]:                                        
                                        if Flag == 0:
                                            df_chart_temp[Sensor] = [np.nan for i in range(0,df_chart_temp.shape[0])]
                                        else:
                                            LogAmp = self.df_chart[Sensor].to_numpy() / WaterSensorAmplitude
                                            df_chart_temp[Sensor] = LogAmp.tolist()
                                        #
                                        if Sensor == WaterSensor:
                                            Flag = 1
                                    self.df_chart = df_chart_temp
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs DiffPhase':
                                    WaterSensor = TabFreqAnal.Combobox_TopSensor.currentText()
                                    WaterSensorPhase = self.df_chart[WaterSensor].to_numpy()
                                    Flag = 0
                                    df_chart_temp = pd.DataFrame()
                                    df_chart_temp['Freq'] = self.df_chart['Freq']
                                    for Sensor in (self.df_chart.columns.tolist())[1:]:
                                        if Flag == 0:
                                            df_chart_temp[Sensor] = [np.nan for i in range(0,df_chart_temp.shape[0])]
                                        else:
                                            DifPhase = self.df_chart[Sensor].to_numpy() - WaterSensorPhase
                                            df_chart_temp[Sensor] = DifPhase.tolist()
                                        #
                                        if Sensor == WaterSensor:
                                            Flag = 1
                                    self.df_chart = df_chart_temp
                                #
                                Freqs = np.array((self.df_chart['Freq'].tolist())[1:])
                                #
                                HarmonicHelp = []
                                for i,Harmonic in enumerate (OPT.GetHarmonics(OPT)):
                                    FreqCheck = (1.0/Freqs - Harmonic)**2
                                    HarmonicHelp.append(self.df_chart.iloc[np.argmin(FreqCheck)+1].tolist())
                                self.df_harmonics = pd.DataFrame(np.array(HarmonicHelp),columns=self.df_chart.columns.tolist())
                            # Sensors GroupBox
                            if Case != 10:
                                if TabFreqAnal.VBoxSensor is not None:
                                    while TabFreqAnal.VBoxSensor.count():
                                        item = TabFreqAnal.VBoxSensor.takeAt(0)
                                        widget = item.widget()
                                        if widget is not None:
                                            widget.deleteLater()
                                        else:
                                            self.clearLayout(item.layout())
                                #
                                contPos = 0
                                for Sensor in (self.df_chart.columns.tolist())[1:]:
                                    CheckBox = PQW.QCheckBox(Sensor)
                                    CheckBox.setChecked(True)
                                    CheckBox.toggled.connect(TabFreqAnal.SensorActiveChange)
                                    if contPos % 2 == 0:
                                        TabFreqAnal.VBoxSensor.addWidget(CheckBox,int(contPos/2),0,1,1)
                                    else:
                                        TabFreqAnal.VBoxSensor.addWidget(CheckBox,int(contPos/2),1,1,1)
                                    contPos = contPos + 1
                            # Chart
                            VAR.GetiFlowSelf(VAR).progress.setValue(80)
                            if Case != -1:
                                #
                                if Case == 10:
                                    Ylim = TabFreqAnal.ax.get_ylim()
                                    Xlim = TabFreqAnal.ax.get_xlim()
                                #
                                TabFreqAnal.Chart_Fig.clear()
                                TabFreqAnal.ax = TabFreqAnal.Chart_Fig.add_subplot(111)
                                if(VAR.GetChartColors(VAR) is None):
                                    Colors = []
                                else:
                                    Colors = VAR.GetChartColors(VAR)    #! To check if works
                                    if len(Colors) < len((self.df_chart.columns.tolist())[1:])-1:
                                        Colors = []
                                        VAR.SetChartColors(VAR,None)
                                #
                                if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                    pass
                                elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                    self.df_chart['Freq'] = self.df_chart['Freq'] * 86400.0
                                    self.df_harmonics['Freq'] = self.df_harmonics['Freq'] * 86400.0
                                elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                    self.df_chart['Freq'] = self.df_chart['Freq'] * 3600.0
                                    self.df_harmonics['Freq'] = self.df_harmonics['Freq'] * 3600.0
                                # Chart's Limits
                                if Case != 10:
                                    MAX = self.df_chart.max().tolist()
                                    MIN = self.df_chart.min().tolist()
                                    MAX = [x for x in MAX if str(x) != 'nan']
                                    MIN = [x for x in MIN if str(x) != 'nan']
                                    DeltaX = (MAX[0]-MIN[0])*0.1/2
                                    DeltaY = (max(MAX[1:])-min(MIN[1:]))*0.1/2
                                    self.xLimits = [MIN[0]-DeltaX,MAX[0]+DeltaX]
                                    self.yLimits = [min(MIN[1:])-DeltaY,max(MAX[1:])+DeltaY]
                                #
                                for i in range(0,len((self.df_chart.columns.tolist())[1:])):
                                    if TabFreqAnal.VBoxSensor.itemAt(i).widget().isChecked():
                                        if(VAR.GetChartColors(VAR) == None):
                                            plot = TabFreqAnal.ax.plot(self.df_chart['Freq'].to_numpy(), (self.df_chart[TabFreqAnal.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabFreqAnal.VBoxSensor.itemAt(i).widget().text())
                                            if OPT.GetHarmonicFlag(OPT) == 'True':
                                                plot = TabFreqAnal.ax.plot(self.df_harmonics['Freq'].to_numpy(), (self.df_harmonics[TabFreqAnal.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = 'Harm_'+TabFreqAnal.VBoxSensor.itemAt(i).widget().text())
                                            Colors.append(plot[0].get_color())
                                        else:
                                            plot = TabFreqAnal.ax.plot(self.df_chart['Freq'].to_numpy(), (self.df_chart[TabFreqAnal.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabFreqAnal.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                            if OPT.GetHarmonicFlag(OPT) == 'True':
                                                plot = TabFreqAnal.ax.plot(self.df_harmonics['Freq'].to_numpy(), (self.df_harmonics[TabFreqAnal.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), 'o', label = 'Harm_'+TabFreqAnal.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                #
                                if len((self.df_chart.columns.tolist())[1:]) > 5:
                                    TabFreqAnal.ax.legend(ncol=int(len((self.df_chart.columns.tolist())[1:])/5+1),fontsize=TabFreqAnal.MPL_Legend)
                                else:
                                    TabFreqAnal.ax.legend(ncol=len((self.df_chart.columns.tolist())[1:]),fontsize=TabFreqAnal.MPL_Legend)
                                # TabFreqAnal.ax.legend(loc=9, ncol=len((self.df_chart.columns.tolist())[1:]))
                                TabFreqAnal.ax.grid(True, which='both', axis='both', linestyle='--')
                                TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
                                #
                                if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                                    TabFreqAnal.ax.set_xlabel('Frequency (Hz)',fontsize=TabFreqAnal.MPL_AxisTitle)
                                elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                                    TabFreqAnal.ax.set_xlabel('Frequency (d$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                                elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                                    TabFreqAnal.ax.set_xlabel('Frequency (hr$^{-1}$)',fontsize=TabFreqAnal.MPL_AxisTitle)
                                #
                                if TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs PSD':
                                    TabFreqAnal.ax.set_ylabel('PSD',fontsize=TabFreqAnal.MPL_AxisTitle)
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs Amplitude':
                                    TabFreqAnal.ax.set_ylabel('Amplitude',fontsize=TabFreqAnal.MPL_AxisTitle)
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs LogAmpRatio':
                                    TabFreqAnal.ax.set_xscale('log')
                                    TabFreqAnal.ax.set_yscale('log')
                                    TabFreqAnal.ax.set_ylabel('LogAmpRatio',fontsize=TabFreqAnal.MPL_AxisTitle)
                                elif TabFreqAnal.Combobox_ChartType.currentText() == 'Frequecies vs DiffPhase':
                                    TabFreqAnal.ax.set_xscale('log')
                                    TabFreqAnal.ax.set_ylabel('DiffPhase',fontsize=TabFreqAnal.MPL_AxisTitle)
                                #
                                # if Case == 10:
                                #     TabFreqAnal.ax.set_ylim(Ylim)
                                #     TabFreqAnal.ax.set_xlim(Xlim)
                                # else:
                                #     TabFreqAnal.ax.set_ylim(self.yLimits)
                                #     TabFreqAnal.ax.set_xlim(self.xLimits)
                                #
                                TabFreqAnal.ax.tick_params(axis='both', labelsize=TabFreqAnal.MPL_AxisTick)
                                #
                                TabFreqAnal.Canvas.draw()
                                #
                                if(VAR.GetChartColors(VAR) is None):
                                    VAR.SetChartColors(VAR, Colors)
                            # Menu Update
                            if Case != -1:
                                VAR.GetiFlowSelf(VAR).Menu_RunFA.setEnabled(True)
                                VAR.GetiFlowSelf(VAR).Menu_FA_Export_PDA.setEnabled(True)
                                VAR.GetiFlowSelf(VAR).Menu_FA_Export_Amplitude.setEnabled(True)
                                VAR.GetiFlowSelf(VAR).Menu_FA_Export_Phase.setEnabled(True)
                                #
                                if OPT.GetHarmonicFlag(OPT) == 'True':
                                    VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Hide Harmonics')
                                else:
                                    VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Show Harmonics')
        # Connect all internal event
        TabFreqAnal.Combobox_FFTWin.currentIndexChanged.connect(TabFreqAnal.on_Combobox_FFTWin_change) # ComboBox event change item
        TabFreqAnal.Combobox_Analysis.currentIndexChanged.connect(TabFreqAnal.on_Combobox_Analysis_change) # ComboBox event change item
        TabFreqAnal.Combobox_TopSensor.currentIndexChanged.connect(TabFreqAnal.on_Combobox_TopSensor_change) # ComboBox event change item
        TabFreqAnal.Combobox_ChartType.currentIndexChanged.connect(TabFreqAnal.on_Combobox_ChartType_change) # ComboBox event change item
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        #
        return

    # @logger.catch
    def on_Button_FA_clicked(self):
        logger.debug('TabFreqAnal - on_Button_PE_clicked')
        # Lunch the wizard for Frequency analysis
        WizardFreqAnal = WFA.FrequencyAnalysis()
        WizardFreqAnal.exec_()
        #
        return

    # @logger.catch
    def on_Combobox_FFTWin_change(self):
        logger.debug('TabFreqAnal - on_Combobox_FFTWin_change')
        TFA.TabFreqAnal.Update(TFA,11)
        return

    # @logger.catch
    def on_Combobox_Analysis_change(self):
        logger.debug('TabFreqAnal - on_Combobox_Analysis_change')
        TFA.TabFreqAnal.Update(TFA,8)
        return
    
    # @logger.catch
    def on_Combobox_ChartType_change(self):
        logger.debug('TabFreqAnal - on_Combobox_ChartType_change')
        TFA.TabFreqAnal.Update(TFA,9)
        return

    # @logger.catch
    def SensorActiveChange(self):
        logger.debug('TabFreqAnal - SensorActiveChange')
        TFA.TabFreqAnal.Update(TFA,10)
        return

    # @logger.catch
    def on_Combobox_TopSensor_change(self):
        logger.debug('TabFreqAnal - on_Combobox_TopSensor_change')
        TFA.TabFreqAnal.Update(TFA,10)
        return

    # @logger.catch
    def on_Button_FA_Harmonics_Show_clicked(self):
        if OPT.GetHarmonicFlag(OPT) == 'True':
            OPT.SetHarmonicFlag(OPT,'False')
            VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Show Harmonics')
        else:
            OPT.SetHarmonicFlag(OPT,'True')
            VAR.GetiFlowSelf(VAR).Menu_FA_Harmonics_Show.setText('Hide Harmonics')
        #
        TFA.TabFreqAnal.Update(TFA,10)
        #
        return

    # @logger.catch
    def on_Button_FA_Export_PDA_clicked(self):
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export PSD to File', '../exports/' + TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_PSD_' +VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            # Load Data
            df_export = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_PSD.pkz',compression='zip')
            #
            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                df_export = df_export.rename(columns = {'Freq':'Freq (Hz)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                df_export['Freq'] = df_export['Freq'] * 86400.0
                df_export = df_export.rename(columns = {'Freq':'Freq (d^-1)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                df_export['Freq'] = df_export['Freq'] * 3600.0
                df_export = df_export.rename(columns = {'Freq':'Freq (hr^-1)'})
            #
            df_export.to_csv(file_export[0],index=False)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'PSD Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Button_FA_Export_Amplitude_clicked(self):
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Amplitude to File', '../exports/' + TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_Amplitude_' +VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            # Load Data
            df_export = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_Amplitude.pkz',compression='zip')
            #
            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                df_export = df_export.rename(columns = {'Freq':'Freq (Hz)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                df_export['Freq'] = df_export['Freq'] * 86400.0
                df_export = df_export.rename(columns = {'Freq':'Freq (d^-1)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                df_export['Freq'] = df_export['Freq'] * 3600.0
                df_export = df_export.rename(columns = {'Freq':'Freq (hr^-1)'})
            #
            ActiveRun = TabFreqAnal.Combobox_Analysis.currentText()
            HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+ActiveRun.replace('Run: ','')+'.run','r')
            Rows = HandleRun.readlines()
            HandleRun.close()
            FFTwinType = (Rows[0]).split(';')[0]
            if FFTwinType == 'Rectangular':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,0)
            elif FFTwinType == 'Triangular':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,1)
            elif FFTwinType == 'Bartlett':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,2)
            elif FFTwinType == 'Hanning':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,3)
            elif FFTwinType == 'Hamming':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,4)
            elif FFTwinType == 'Flat Top':
                FFTwinCor = OPT.GetFFTcorAMP(OPT,5)
            for Sensor in (df_export.columns.tolist())[1:]:
                df_export[Sensor] = df_export[Sensor] * FFTwinCor
            #
            df_export.to_csv(file_export[0],index=False)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Amplitude Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Button_FA_Export_Phase_clicked(self):
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Phase to File', '../exports/' + TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_Phase_' +VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            # Load Data
            df_export = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+TabFreqAnal.Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
            #
            if OPT.GetTFAxAxisUnit(OPT) == 'Hz':
                df_export = df_export.rename(columns = {'Freq':'Freq (Hz)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Day':
                df_export['Freq'] = df_export['Freq'] * 86400.0
                df_export = df_export.rename(columns = {'Freq':'Freq (d^-1)'})
            elif OPT.GetTFAxAxisUnit(OPT) == 'Hour':
                df_export['Freq'] = df_export['Freq'] * 3600.0
                df_export = df_export.rename(columns = {'Freq':'Freq (hr^-1)'})
            #
            df_export.to_csv(file_export[0],index=False)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Phase Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Button_FA_Harmonics_Manage_clicked(self):
        WizardHamonics = WMH.ManageHarmonics()
        WizardHamonics.exec_()
        TFA.TabFreqAnal.Update(TFA,10)
        return