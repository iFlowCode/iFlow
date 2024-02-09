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
# import os#,sys
import PyQt5.QtWidgets as PQW
# import PyQt5.QtGui as PQG
# import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from numpy.lib.function_base import append
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
from scipy import stats
# import datetime
import numpy as np
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
# import glob
import pickle
# from shutil import copyfile

# Import custom library
from Variables import VAR
from Options import OPT
#%%
'''
Wizzard Add Probe Class
'''
class BREcalc(PQW.QWizard):
    def __init__(self, parent=None):
        super(BREcalc, self).__init__(parent)
        self.setWindowTitle('Bed river elevation estimation - '+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText())
        #
        width = int(VAR.GetWindowsSize(VAR)[0] * 0.8) # Width of the window
        height = int(VAR.GetWindowsSize(VAR)[1] * 0.8) # Height of the window
        self.setMinimumSize(width,height)
        #
        self.addPage(Page1(self)) # Add Page1
        #
        # self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print) # Click event on Next Page of the wizard
        self.button(PQW.QWizard.CancelButton).clicked.connect(self.cancel_print) # Click event on Finish the wizard
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        



    def cancel_print(self):
        print('Cancel')
        #
        return
#%%
    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
        #
        result =PQW.QMessageBox.question(self, VAR.GetSoftwareName(VAR)+' message', 'Do you want to save a report?', PQW.QMessageBox.Yes|PQW.QMessageBox.No, PQW.QMessageBox.Yes)
        if result == PQW.QMessageBox.Yes:
            file_report = PQW.QFileDialog.getSaveFileName(self, 'Save Report to File', '../exports/Report_' + VAR.GetActiveProbe(VAR), 'txt (*.txt)')
            if file_report[0]:
                Handle = open(file_report[0],'w')
                Handle.write('Estimated height:'+Page1.Elevation.text()+' m\n')
                Handle.write('Period used:'+Page1.Combobox_Freq.currentText()+'\n')
                Handle.write('Phase:\n')
                Handle.write('      rsquare:'+"{:.2f}".format(Page1.resPhase.rvalue**2)+'\n')
                Handle.write('      slope:'+str(Page1.resPhase.slope)+'\n')
                Handle.write('      intercept:'+str(Page1.resPhase.intercept)+'\n')
                Handle.write('Amplitude:\n')
                Handle.write('      rsquare:'+"{:.2f}".format(Page1.resAmplitude.rvalue**2)+'\n')
                Handle.write('      slope:'+str(Page1.resAmplitude.slope)+'\n')
                Handle.write('      intercept:'+str(Page1.resAmplitude.intercept)+'\n')
                Handle.close()
        return
        
#%%
'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        #
        Page1.Heights = VAR.GetActiveParameters(VAR,7).split(',')
        # Load Data
        # Time
        Page1.df_Time = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_MobWinTime.pkz',compression='zip')
        # Phase
        Page1.Phase = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
        # Amplitude
        Page1.Amplitude = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Amplitude.pkz',compression='zip')
        #
        Page1.Columns = (Page1.Phase.columns.tolist())[2:]
        #
        Label_Freq = PQW.QLabel('Freq: ')
        Page1.Combobox_Freq = PQW.QComboBox()
        Freq = Page1.Phase['Freq'].drop_duplicates()
        Periods = (1.0/Freq/3600.0).tolist()
        for item in Periods:
            Page1.Combobox_Freq.addItem(str(item))
        Periods = (np.array(Periods) - OPT.GetBasicPeriod(OPT))**2
        pos = np.argmin(Periods)
        Page1.Combobox_Freq.setCurrentIndex(pos)
        Page1.Combobox_Freq.currentIndexChanged.connect(self.Update)
        #
        Label_Time = PQW.QLabel('Time: ')
        Page1.Combobox_Time = PQW.QComboBox()
        # # Page1.Combobox_Time.clear()
        for item in Page1.df_Time['Time'].tolist():
            if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                Page1.Combobox_Time.addItem(str(pd.to_datetime(item,unit='s')))
            else:
                Page1.Combobox_Time.addItem(str(item))
        Page1.Combobox_Freq.currentIndexChanged.connect(self.Update)
        #
        Label_Elev = PQW.QLabel('Height (m):')
        Page1.Elevation = PQW.QLineEdit()
        Page1.Elevation.setText(self.Heights[0])
        Page1.Elevation.setFocus()
        Page1.Elevation.textChanged.connect(self.Update)
        #
        Page1.Label_r2Phase = PQW.QLabel('Label_r2Phase')
        Page1.Label_r2Ampl = PQW.QLabel('Label_r2Ampl')
        Page1.VBoxSensor = PQW.QVBoxLayout()
        for Sensor in (Page1.Columns):
            CheckBox = PQW.QCheckBox(Sensor)
            CheckBox.setChecked(True)
            CheckBox.toggled.connect(self.Update)
            Page1.VBoxSensor.addWidget(CheckBox)
        # Chart Phase
        Page1.Chart_Fig_Phase = plt.figure()
        Page1.Canvas_Phase = FigureCanvas(self.Chart_Fig_Phase)
        Page1.Toolbar_Phase = NavigationToolbar(self.Canvas_Phase, self)
        # Chart Amp
        Page1.Chart_Fig_Amp = plt.figure()
        Page1.Canvas_Amp = FigureCanvas(self.Chart_Fig_Amp)
        Page1.Toolbar_Amp = NavigationToolbar(self.Canvas_Amp, self)
        # Create grid layot for the window
        Layout_Page1 = PQW.QGridLayout()
        Layout_Page1.addWidget(Label_Freq, 0, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_Freq, 0, 1, 1, 1)
        Layout_Page1.addWidget(Label_Time, 0, 2, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_Time, 0, 3, 1, 1)
        Layout_Page1.addWidget(Label_Elev, 0, 4, 1, 1)
        Layout_Page1.addWidget(Page1.Elevation, 0, 5, 1, 1)
        Layout_Page1.addWidget(Page1.Label_r2Phase, 1, 0, 1, 2)
        Layout_Page1.addWidget(Page1.Label_r2Ampl, 1, 4, 1, 2)
        Layout_Page1.addLayout(Page1.VBoxSensor, 1, 2, 5, 2)
        Layout_Page1.addWidget(Page1.Toolbar_Phase, 2, 0, 1, 2)
        Layout_Page1.addWidget(Page1.Canvas_Phase, 3, 0, 2, 2)
        Layout_Page1.addWidget(Page1.Toolbar_Amp, 2, 4, 1, 4)
        Layout_Page1.addWidget(Page1.Canvas_Amp, 3, 4, 2, 2)
        # Show layout
        self.setLayout(Layout_Page1)
        # Update
        self.Update()

    def Update(self):
        print('Update')
        #
        # PhaseChart = (Page1.Phase[Page1.Combobox_Time.currentIndex()].iloc[Page1.Combobox_Freq.currentIndex()]).tolist()[1:]
        PhaseChart = ((Page1.Phase[(Page1.Phase['Time'] == Page1.df_Time.loc[Page1.Combobox_Time.currentIndex()].values[0]) & (Page1.Phase['Freq'] == 1.0/float(Page1.Combobox_Freq.currentText())/3600.0)]).values.tolist()[0])[2:]
        # AmpChart = (Page1.Amplitude[Page1.Combobox_Time.currentIndex()].iloc[Page1.Combobox_Freq.currentIndex()]).tolist()[1:]
        AmpChart = ((Page1.Amplitude[(Page1.Amplitude['Time'] == Page1.df_Time.loc[Page1.Combobox_Time.currentIndex()].values[0]) & (Page1.Amplitude['Freq'] == 1.0/float(Page1.Combobox_Freq.currentText())/3600.0)]).values.tolist()[0])[2:]
        #
        AmpChart = np.log(AmpChart)
        #
        Flag = 0
        WorkHeights = []
        WorkPhase = []
        WorkAmp = []
        #
        for i in range(0,len(Page1.Heights)):
            if Page1.VBoxSensor.itemAt(i).widget().isChecked():
                if Flag == 0:
                    WorkHeights.append(float(Page1.Elevation.text()))
                    Flag = 1
                else:
                    WorkHeights.append(float(Page1.Heights[i]))
                WorkPhase.append(float(PhaseChart[i]))
                WorkAmp.append(AmpChart[i])
        #
        Page1.resPhase = stats.linregress(np.array(WorkPhase), np.array(WorkHeights))
        Page1.resAmplitude = stats.linregress(np.array(WorkAmp), np.array(WorkHeights))
        #
        Page1.Label_r2Phase.setText('Phase rSquare: '+"{:.2f}".format(Page1.resPhase.rvalue**2))#str(resPhase.rvalue**2))
        Page1.Label_r2Ampl.setText('Amplitude rSquare: '+"{:.2f}".format(Page1.resAmplitude.rvalue**2))#str(resAmplitude.rvalue**2))
        LinePhase = []
        LineAmp = []
        LineHeight = []
        for i in range(0,len(Page1.Heights)):
            LinePhase.append((float(Page1.Heights[i])-Page1.resPhase.intercept)/Page1.resPhase.slope)
            LineAmp.append((float(Page1.Heights[i])-Page1.resAmplitude.intercept)/Page1.resAmplitude.slope)
            LineHeight.append(float(Page1.Heights[i]))
        # Chart
        # Phase
        Page1.Chart_Fig_Phase.clear()
        Page1.axPhase = Page1.Chart_Fig_Phase.add_subplot(111)
        #
        for i in range(0,len(Page1.Heights)):
            plotPhase = Page1.axPhase.plot(PhaseChart[i], float(Page1.Heights[i]), 'o', label = 'Data', color='b')
        #
        for i in range(0,len(WorkHeights)):
            plotPhase = Page1.axPhase.plot(WorkPhase[i], float(WorkHeights[i]), 'o', label = 'Work', color='r')
        #
        plotPhase = Page1.axPhase.plot(LinePhase, LineHeight, '--', label = 'Int', color='k')
        #
        Page1.axPhase.grid(True, which='both', axis='both', linestyle='--')
        Page1.axPhase.set_ylabel('z (m)')
        Page1.axPhase.set_xlabel('Phase')
        Page1.Canvas_Phase.draw()
        Page1.Canvas_Phase.flush_events()
        # Amp
        Page1.Chart_Fig_Amp.clear()
        Page1.axAmp = Page1.Chart_Fig_Amp.add_subplot(111)
        #
        for i in range(0,len(Page1.Heights)):
            plotAmp = Page1.axAmp.plot(AmpChart[i], float(Page1.Heights[i]), 'o', label = 'Data', color='b')
        #
        for i in range(0,len(WorkHeights)):
            plotAmp = Page1.axAmp.plot(WorkAmp[i], float(WorkHeights[i]), 'o', label = 'Work', color='r')
        #
        plotAmp = Page1.axAmp.plot(LineAmp, LineHeight, '--', label = 'Int', color='k')
        #
        Page1.axAmp.grid(True, which='both', axis='both', linestyle='--')
        Page1.axAmp.set_ylabel('z (m)')
        Page1.axAmp.set_xlabel('Amplitude')
        Page1.Canvas_Amp.draw()
        Page1.Canvas_Amp.flush_events()
        #
        return