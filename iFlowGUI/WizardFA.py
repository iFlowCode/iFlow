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
import os,sys
import PyQt5.QtWidgets as PQW
import PyQt5.QtGui as PQG
import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
# import pickle
from datetime import datetime
import numpy as np
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
import glob
from shutil import copy
# Import custom library
from Variables import VAR
# import WizEtaKeMean as WKE
#%%
'''
Wizzard Frequency Analisys Class
'''
class FrequencyAnalysis(PQW.QWizard):
    def __init__(self, parent=None):
        super(FrequencyAnalysis, self).__init__(parent)
        self.setWindowTitle('Signal Processing')
        #
        width = VAR.GetWindowsSize(VAR)[0] * 2 / 3 # Width of the window
        height = VAR.GetWindowsSize(VAR)[1] * 2 / 3 # Height of the window
        if width > 300:
            width = 300
        if height > 500:
            height = 500
        self.setMinimumSize(width,height) # Set the minimun size of the wondow
        #
        self.addPage(Page1(self)) # Add Page1
        #
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        #

#%%
    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
        #
        FFTWin = Page1.Combobox_WT.currentText()
        if Page1.Combobox_WT.currentText() == '':
            FFTWin = 'Rectangular'
        #
        stringEXE = 'FrequencyAnalysis.exe'
        # Probe name  [STRING] -p
        # stringEXE = stringEXE + ' -p "' + VAR.GetActiveProbe(VAR) +'"'
        # Project name  [STRING] -j
        # stringEXE = stringEXE + ' -j "' + VAR.GetActiveProject(VAR) +'"'
        # FFT Windows [STRING] -w
        stringEXE = stringEXE + ' -w "' + FFTWin +'"'
        # From [FLOAT] -f
        stringEXE = stringEXE + ' -f "' + str(Page1.From) +'"'
        # To [FLOAT] -t
        stringEXE = stringEXE + ' -t "' + str(Page1.To) +'"'
        # Sample Rate [FLOAT] -d
        stringEXE = stringEXE + ' -d "' + str(VAR.GetActiveParameters(VAR,3)) +'"'
        #
        FileDel = glob.glob('../temp/*.*')
        for File in FileDel:
            os.remove(File)
        # Move Datafile
        copy('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz','../temp/clean.pkz')
        # Call external program
        print(stringEXE)
        os.system(stringEXE)
        # # Check Run
        HandleLog = open('../temp/FrequencyAnalysis.log')
        Check = HandleLog.readline().replace('\n','')
        HandleLog.close()
        if Check == 'No Error':
            FilesRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/*.run')
            if len(FilesRuns) == 0:
                NewRun = '0'
            else:
                NewRun = -9
                for File in FilesRuns:
                    if NewRun < int((File.split('/')[-1]).replace('fft\\','').replace('.run','')):
                        NewRun = int((File.split('/')[-1]).replace('fft\\','').replace('.run',''))
                NewRun = str(NewRun+1)
            # Move the data
            os.remove('../temp/clean.pkz')
            os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+str(NewRun)+'.run')
            os.replace('../temp/Amplitude.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+str(NewRun)+'_Amplitude.pkz')
            os.replace('../temp/Phase.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+str(NewRun)+'_Phase.pkz')
            os.replace('../temp/PSD.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+str(NewRun)+'_PSD.pkz')
            os.replace('../temp/FrequencyAnalysis.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/fft/'+str(NewRun)+'_FrequencyAnalysis.log')
            #
            VAR.GetTabFreqAnal(VAR).Update(7)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Analysis Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        else:
            PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check+'. Error.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
#%%
'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
#%%
        # Create grid layot for the window
        Layout_Page1 = PQW.QGridLayout()
        # Load Probe Data
        df_data = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz', compression= 'zip')
        idx, idy = np.where(pd.isnull(df_data))
        idxUnique = np.unique(idx)
        Start = 0
        # # End = df.shape[0]
        Longs = []
        Starts = []
        Ends = []
        for n in idxUnique:
            Longs.append(n-Start)
            Starts.append(Start)
            Ends.append(n-1)
            Start = n+1
        Longs.append(df_data.shape[0]-Start)
        Starts.append(Start)
        Ends.append(df_data.shape[0]-1)
        maxValue = max(Longs)
        max_index = Longs.index(maxValue)
        #
        HandleLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/probe.ini')
        HandleLog.readline()
        HandleLog.readline()
        TimeType = HandleLog.readline().split(';')[0] #
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.close()
        # Data
        Label_Data = PQW.QLabel('Data')
        dt_object = pd.Timestamp(df_data['Time'].iloc[0], unit='s').strftime('%Y-%m-%d %H:%M:%S')
        Page1.From = df_data['Time'].iloc[Starts[max_index]]
        Page1.To = df_data['Time'].iloc[Ends[max_index]]
        if TimeType == 'Time':
            Label_DataFrom = PQW.QLabel('From: '+str(df_data['Time'].iloc[0])+' s')
            Label_DataTo = PQW.QLabel('To: '+str(df_data['Time'].iloc[df_data.shape[0]-1])+' s')
        else:
            Label_DataFrom = PQW.QLabel('From: '+pd.Timestamp(df_data['Time'].iloc[0], unit='s').strftime('%Y-%m-%d %H:%M:%S'))
            Label_DataTo = PQW.QLabel('To: '+pd.Timestamp(df_data['Time'].iloc[df_data.shape[0]-1], unit='s').strftime('%Y-%m-%d %H:%M:%S'))
        # Longest period
        LabelLP = PQW.QLabel('Longest period')
        if TimeType == 'Time':
            Label_LPFrom = PQW.QLabel('From: '+str(df_data['Time'].iloc[Starts[max_index]]))
            Label_LPTo = PQW.QLabel('To: '+str(df_data['Time'].iloc[Ends[max_index]]))
        else:
            Label_LPFrom = PQW.QLabel('From: '+pd.Timestamp(df_data['Time'].iloc[Starts[max_index]], unit='s').strftime('%Y-%m-%d %H:%M:%S'))
            Label_LPTo = PQW.QLabel('To: '+pd.Timestamp(df_data['Time'].iloc[Ends[max_index]], unit='s').strftime('%Y-%m-%d %H:%M:%S'))
        # Window type
        LabelWT = PQW.QLabel('Window type:')
        Page1.Combobox_WT = PQW.QComboBox() # Combobox
        for item in VAR.GetFFTWindowfunction(VAR):
            Page1.Combobox_WT.addItem(item)
# Insert elements in the grid
        Layout_Page1.addWidget(Label_Data, 0, 0, 1, 2)
        Layout_Page1.addWidget(Label_DataFrom, 1, 0, 1, 2)
        Layout_Page1.addWidget(Label_DataTo, 2, 0, 1, 2)
        Layout_Page1.addWidget(LabelLP, 3, 0, 1, 2)
        Layout_Page1.addWidget(Label_LPFrom, 4, 0, 1, 2)
        Layout_Page1.addWidget(Label_LPTo, 5, 0, 1, 2)
        Layout_Page1.addWidget(LabelWT, 6, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_WT, 7, 0, 1, 1)
# # Show layout
        self.setLayout(Layout_Page1)