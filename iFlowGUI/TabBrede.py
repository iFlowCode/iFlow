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
# # from mpl_toolkits.mplot3d import Axes3D  
import glob
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
import pandas as pd
# # import pickle
# # import datetime
# # import time
# # import numpy as np
# # from matplotlib import cm
# # Import custom library
from Variables import VAR
# # from Options import OPT
from ScrollLabel import ScrollLabel
# # import TabSignProc as TSP
# # import STabFFTAnal as STFA
# # import STabLPMAnal as STLA
import WizardBH as WBH
from loguru import logger
#------------------------------------------------------------------------------#
'''
TabBrede Class
'''
class TabBrede(PQW.QWidget):
    def __init__(self):
        super().__init__()
        logger.debug('TabBrede - Start Class')
        # Set Matplotlib fonts size
        TabBrede.MPL_AxisTitle = int(VAR.GetMPLAxisTitleFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabBrede.MPL_AxisTick = int(VAR.GetMPLAxisTickFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabBrede.MPL_Legend = int(VAR.GetMPLLegendFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # Store class object
        VAR.SetTabBrede(VAR, self)
        # Create grid layot for the window
        Layout_Tab_Brede = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Tab_Brede_left = PQW.QVBoxLayout()
        # Button Calculate
        TabBrede.Button_Brede = PQW.QPushButton('Run analysis')
        # TabBrede.Button_Brede.setFixedHeight(int(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR)))
        # TabSignProc.Button_SP.setToolTip('Launch Signal Processing Wizard') # Tooltip message
        TabBrede.Button_Brede.clicked.connect(self.on_Button_BH_clicked) # Button event Click on
        Layout_Tab_Brede_left.addWidget(TabBrede.Button_Brede)
        #
        Label_Analysis = PQW.QLabel('Analysis:')
        Layout_Tab_Brede_left.addWidget(Label_Analysis)
        #
        TabBrede.Analysis = PQW.QComboBox()
        Layout_Tab_Brede_left.addWidget(TabBrede.Analysis)
        TabBrede.Analysis.currentIndexChanged.connect(self.on_Combobox_Analysis_change) # ComboBox event change item
        # Groupbox Report
        self.GroupBox_Report = PQW.QGroupBox('Report:')
        # Create Layout for the Groupbox Report
        self.VBoxReport = PQW.QVBoxLayout()
        # Element EditLine
        TabBrede.Label_Report = ScrollLabel(self)
        TabBrede.Label_Report.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ')
        # Add elements to the Layout
        self.VBoxReport.addWidget(TabBrede.Label_Report)
        # Add the Layout to the Groupbox Report
        self.GroupBox_Report.setLayout(self.VBoxReport)
        #
        Layout_Tab_Brede_left.addWidget(self.GroupBox_Report)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Tab_Brede_left)
        # FFTChart
        container_right = PQW.QFrame()
        Layout_Tab_Brede_Right = PQW.QVBoxLayout()
        TabBrede.Chart_Fig = plt.figure()
        TabBrede.Canvas = FigureCanvas(TabBrede.Chart_Fig)
        self.Toolbar = NavigationToolbar(TabBrede.Canvas, self)
        TabBrede.Canvas.draw()
        Layout_Tab_Brede_Right.addWidget(self.Toolbar)
        Layout_Tab_Brede_Right.addWidget(TabBrede.Canvas)
        #
        container_right.setLayout(Layout_Tab_Brede_Right)
        #
        Layout_Tab_Brede.addWidget(container_left)
        Layout_Tab_Brede.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Tab_Brede)

    # @logger.catch
    def Update(self,Case):
        logger.debug(f"TabBrede Update - Case: {Case}")
        '''
        Case 0: Event generated by the starting of the GUI
        # Case 1: Event generated by on change project
        # Case 2: Event generated by button new project
        # Case 3: Event generated by button delete project
        # Case 4: Event generated by wizard AddProbe
        # Case 5: Event generated by Button Remove Probe
        Case 6: New analysis
        # Case 7: Change Analysis Change
        # Case 8: 
        # Case 9: 
        # Case 10:
        # Case 11: 
        # Case 12: 
        # Case 13:
        # Case 14: 
        '''
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        # Disconect all the internal events
        TabBrede.Analysis.currentIndexChanged.disconnect()
        #
        if(VAR.GetActiveProject(VAR) == None):
            TabBrede.Button_Brede.setEnabled(False)
            #
            TabBrede.Analysis.clear()
            # Report GroupBox
            TabBrede.Label_Report.setText('There isn\'t any Analysis\nRun one.')
            # Chart
            TabBrede.Chart_Fig.clear()
            TabBrede.ax = TabBrede.Chart_Fig.add_subplot(111)
            # TabFreqAnal.ax.legend()
            TabBrede.ax.grid(True, which='both', axis='both', linestyle='--')
            TabBrede.ax.set_ylabel('Velocity (m/s)',fontsize=TabBrede.MPL_AxisTitle)
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                pass
            elif VAR.GetActiveParameters(VAR,2) == 'Time':
                TabBrede.ax.set_xlabel('Time (s)',fontsize=TabBrede.MPL_AxisTitle)
            TabBrede.Canvas.draw()
            #
            VAR.GetiFlowSelf(VAR).Menu_RunBH.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_BH_Export.setEnabled(False)
        else:
            if(VAR.GetActiveProbe(VAR) == None):
                TabBrede.Button_Brede.setEnabled(False)
                #
                TabBrede.Analysis.clear()
                # Report GroupBox
                TabBrede.Label_Report.setText('There isn\'t any Analysis\nRun one.')
                # Chart
                TabBrede.Chart_Fig.clear()
                TabBrede.ax = TabBrede.Chart_Fig.add_subplot(111)
                # TabFreqAnal.ax.legend()
                TabBrede.ax.grid(True, which='both', axis='both', linestyle='--')
                TabBrede.ax.set_ylabel('Velocity ($m$ $s^-1$))',fontsize=TabBrede.MPL_AxisTitle)
                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                    pass
                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                    TabBrede.ax.set_xlabel('Time (s)',fontsize=TabBrede.MPL_AxisTitle)
                #
                TabBrede.Canvas.draw()
                #
                VAR.GetiFlowSelf(VAR).Menu_RunBH.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_BH_Export.setEnabled(False)
            else:
                TabBrede.Button_Brede.setEnabled(True)
                #
                Runs = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/*.run')
                #
                if len(Runs) == 0:
                    TabBrede.Analysis.clear()
                    # Report GroupBox
                    TabBrede.Label_Report.setText('There isn\'t any Analysis\nRun one.')
                    # Chart
                    TabBrede.Chart_Fig.clear()
                    TabBrede.ax = TabBrede.Chart_Fig.add_subplot(111)
                    # TabFreqAnal.ax.legend()
                    TabBrede.ax.grid(True, which='both', axis='both', linestyle='--')
                    TabBrede.ax.set_ylabel('Velocity (m/s)',fontsize=TabBrede.MPL_AxisTitle)
                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                        pass
                    elif VAR.GetActiveParameters(VAR,2) == 'Time':
                        TabBrede.ax.set_xlabel('Time (s)',fontsize=TabBrede.MPL_AxisTitle)
                    #
                    TabBrede.Canvas.draw()
                    #
                    VAR.GetiFlowSelf(VAR).Menu_RunBH.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_BH_Export.setEnabled(False)
                else:
                    if Case != 7:
                        TabBrede.Analysis.clear()
                        for item in Runs:
                            TabBrede.Analysis.addItem('Run: '+(item.replace('\\','/').split('/')[-1]).replace('.run',''))
                        TabBrede.Analysis.setCurrentIndex(len(Runs)-1)
                    if Case != -1:
                        Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/'+TabBrede.Analysis.currentText().replace('Run: ','')+'.run','r')
                        Handle.readline()
                        Handle.readline()
                        TopSensor = Handle.readline().split(';')[0]
                        Threshold = Handle.readline().split(';')[0]
                        c0rho0 = Handle.readline().split(';')[0]
                        k = Handle.readline().split(';')[0]
                        WinMean = Handle.readline().split(';')[0]
                        Handle.close()
                    if Case != -1:
                        Text = 'Top Sensor: '+TopSensor+'\n'
                        Text = Text + 'Threshold: '+Threshold+' C\n'
                        Text = Text + 'c0rho0: '+c0rho0+'\n'
                        Text = Text + 'k: '+k+'\n'
                        Text = Text + 'WinMean: '+WinMean+' days\n'
                        TabBrede.Label_Report.setText(Text)
                    if Case != -1:
                        TabBrede.df_chart_data = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/'+TabBrede.Analysis.currentText().replace('Run: ','')+'_Velocity.pkz',compression='zip')
                    if Case != -1:
                        TabBrede.Chart_Fig.clear()
                        TabBrede.ax = TabBrede.Chart_Fig.add_subplot(111)
                        if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                            plot = TabBrede.ax.plot(pd.to_datetime(TabBrede.df_chart_data['Time'],unit='s'), TabBrede.df_chart_data['Velocity'].to_numpy(), '-', color='b', label = 'Velocity')
                            plot = TabBrede.ax.plot(pd.to_datetime(TabBrede.df_chart_data['Time'],unit='s'), TabBrede.df_chart_data['Velocity'].to_numpy(), 'o', color='b', label = 'Velocity')
                        elif VAR.GetActiveParameters(VAR,2) == 'Time':
                            plot = TabBrede.ax.plot(TabBrede.df_chart_data['Time'].to_numpy(), TabBrede.df_chart_data['Velocity'].to_numpy(), '-', color='b', label = 'Velocity')
                            plot = TabBrede.ax.plot(TabBrede.df_chart_data['Time'].to_numpy(), TabBrede.df_chart_data['Velocity'].to_numpy(), 'o', color='b', label = 'Velocity')
                        TabBrede.ax.grid(True, which='both', axis='both', linestyle='--')
                        TabBrede.ax.set_ylabel('Velocity (m/s)')
                        if VAR.GetActiveParameters(VAR,2) == 'Time':
                            TabBrede.ax.set_xlabel('Time (s)')
                        else:
                            pass
                        #
                        TabBrede.Canvas.draw()
                        #
                    VAR.GetiFlowSelf(VAR).Menu_RunBH.setEnabled(True)
                    VAR.GetiFlowSelf(VAR).Menu_BH_Export.setEnabled(True)
        # Connect all internal event
        TabBrede.Analysis.currentIndexChanged.connect(TabBrede.on_Combobox_Analysis_change) # ComboBox event change item
        #
        return

    # @logger.catch
    def on_Button_BH_clicked(self):
        logger.debug('TabBrede - on_Button_BH_clicked')
        # Lunch the wizard for importing a new probe
        WizardBred = WBH.Brede()
        WizardBred.exec_()
        # TSP.TabSignProc.Update(TSP,9)
        return

    # @logger.catch
    def on_Button_BHExport_clicked(self):
        logger.debug('TabBrede - on_Button_BHExport_clicked')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Data to File', '../exports/Bredehofet_' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            # df_export = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
            TabBrede.df_chart_data.to_csv(file_export[0],index=False)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Breddhofet Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Combobox_Analysis_change(self):
        logger.debug('TabBrede - on_Combobox_Analysis_change')
        TabBrede.Update(TabBrede,7)
        return