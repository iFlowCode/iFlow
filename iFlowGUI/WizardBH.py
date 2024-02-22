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
import os#,sys
import PyQt5.QtWidgets as PQW
# import PyQt5.QtGui as PQG
# import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
# import datetime
import numpy as np
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
import glob
from shutil import copyfile

# Import custom library
from Variables import VAR
from loguru import logger

'''
Wizzard Add Probe Class
'''
class Brede(PQW.QWizard):
    def __init__(self, parent=None):
        super(Brede, self).__init__(parent)
        self.setWindowTitle('Bredehofet')
        #
        self.addPage(Page1(self)) # Add Page1
        #
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        
    def next_print(self):
        return

    def finish_print(self):
        logger.debug("Bred End")
        # Input Files
        FileDel = glob.glob('../temp/*.*')
        for File in FileDel:
            os.remove(File)
        #
        copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz', '../temp/clean.pkz')
        #
        stringEXE = 'Bredehofet.exe'
        # Sensors [LIST] -s
        stringEXE = stringEXE + ' -s "' + ','.join(Page1.Sensors) +'"'
        # Heights [LIST] -h
        stringEXE = stringEXE + ' -h "' + ','.join(Page1.Heights) +'"'
        # Sensor in soil [STRING] -l
        stringEXE = stringEXE + ' -l "' + Page1.Combobox_TopSensor.currentText() +'"'
        # Threshold [FLOAT] -t
        stringEXE = stringEXE + ' -t "' + Page1.Threshold.text() +'"'
        # c0rho0 [FLOAT] -r
        # stringEXE = stringEXE + ' -r "' + Page1.c0rho0.text() +'"'
        # k [FLOAT] -k
        stringEXE = stringEXE + ' -k "' + Page1.k.text() +'"'
        # window lenght [INTEGER] - w
        stringEXE = stringEXE + ' -w "' + Page1.WinMean.currentText() +'"'
        # dt [FLOAT] -d
        stringEXE = stringEXE + ' -d "' + VAR.GetActiveParameters(VAR,3) +'"'
        # Call external program
        logger.debug(stringEXE)
        os.system(stringEXE)
        # Check Run
        HandleLog = open('../temp/BDH.log','r')
        Check = HandleLog.readline().replace('\n','')
        HandleLog.close()
        #
        FilesRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/*.run')
        if len(FilesRuns) == 0:
            NewRun = '0'
        else:
            NewRun = -9
            for File in FilesRuns:
                if NewRun < int((File.split('/')[-1]).replace('Bredehofet\\','').replace('.run','')):
                    NewRun = int((File.split('/')[-1]).replace('Bredehofet\\','').replace('.run',''))
            NewRun = str(NewRun+1)
        #
        if Check == 'No Error':
            # Move the data
            os.remove('../temp/clean.pkz')
            os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/'+str(NewRun)+'.run')
            os.replace('../temp/Velocity.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/'+str(NewRun)+'_Velocity.pkz')
            os.replace('../temp/BDH.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/Bredehofet/'+str(NewRun)+'_BDH.log')
            #
            VAR.GetTabBrede(VAR).Update(6)
            #
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Bredehofet Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        else:
            PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)

'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        # Load Probe.init
        HandleProbIni = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/probe.ini','r')
        HandleProbIni.readline()
        HandleProbIni.readline()
        Page1.TimeType = HandleProbIni.readline().split(';')[0]
        HandleProbIni.readline()
        HandleProbIni.readline()
        HandleProbIni.readline()
        Page1.Sensors = (HandleProbIni.readline().split(';')[0]).split(',')
        Page1.SensorsHeight = (HandleProbIni.readline().split(';')[0]).split(',')
        HandleProbIni.readline()
        HandleProbIni.readline()
        HandleProbIni.readline()
        HandleProbIni.readline()
        HandleProbIni.readline()
        HandleProbIni.close()
        #
        Page1.Sensors = (VAR.GetActiveParameters(VAR,6)).split(',')
        Page1.Heights = (VAR.GetActiveParameters(VAR,7)).split(',')
        # Create grid layot for the window
        Layout_Page1 = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Page1_Left = PQW.QVBoxLayout()
        # Top Sensor
        Layout_Page1_Left_1 = PQW.QHBoxLayout()
        Label_TopSensor = PQW.QLabel('Top Sensor:')
        Layout_Page1_Left_1.addWidget(Label_TopSensor)
        Page1.Combobox_TopSensor = PQW.QComboBox() # Combobox probe name
        for item in Page1.Sensors:
            Page1.Combobox_TopSensor.addItem(item)
        Layout_Page1_Left_1.addWidget(Page1.Combobox_TopSensor)
        Layout_Page1_Left.addLayout(Layout_Page1_Left_1)
        #
        Layout_Page1_Left_2 = PQW.QHBoxLayout()
        Label_Threshold = PQW.QLabel("Threshold ()"+u"\N{DEGREE SIGN}"+"C):")
        Layout_Page1_Left_2.addWidget(Label_Threshold)
        Page1.Threshold = PQW.QLineEdit(self)
        Page1.Threshold.setText('0.0')
        Layout_Page1_Left_2.addWidget(Page1.Threshold)
        Layout_Page1_Left.addLayout(Layout_Page1_Left_2)
        #
        Layout_Page1_Left_3 = PQW.QHBoxLayout()
        Label_k = PQW.QLabel('k (m<sup>2</sup> s<sup>-1</sup>):')
        Layout_Page1_Left_3.addWidget(Label_k)
        Page1.k = PQW.QLineEdit(self)
        Page1.k.setText('0.002')
        Layout_Page1_Left_3.addWidget(Page1.k)
        Layout_Page1_Left.addLayout(Layout_Page1_Left_3)
        #
        Layout_Page1_Left_4 = PQW.QHBoxLayout()
        Label_WinMean = PQW.QLabel('Mean window (d):')
        Layout_Page1_Left_4.addWidget(Label_WinMean)
        Page1.WinMean = PQW.QComboBox()
        Page1.WinMean.addItem('1')
        Page1.WinMean.addItem('2')
        Page1.WinMean.addItem('3')
        Page1.WinMean.addItem('4')
        Page1.WinMean.addItem('5')
        Page1.WinMean.addItem('6')
        Page1.WinMean.addItem('7')
        Layout_Page1_Left_4.addWidget(Page1.WinMean)
        Layout_Page1_Left.addLayout(Layout_Page1_Left_4)
        # Chart column
        container_right = PQW.QFrame()
        Layout_Page1_Right = PQW.QVBoxLayout()
        Page1.Chart_Fig = plt.figure()
        Page1.Canvas = FigureCanvas(self.Chart_Fig)
        self.Toolbar = NavigationToolbar(self.Canvas, self)
        Layout_Page1_Right.addWidget(self.Toolbar)
        Layout_Page1_Right.addWidget(Page1.Canvas)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Page1_Left)
        container_right.setLayout(Layout_Page1_Right)
        #
        Layout_Page1.addWidget(container_left)
        Layout_Page1.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Page1)
        #
        df_Clean = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
        ChartColumns = (df_Clean.columns).tolist()
        Page1.Chart_Fig.clear()
        Page1.ax = Page1.Chart_Fig.add_subplot(111)
        #
        VAR.SetChartColors(VAR,None)
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        #
        for i in range(1,len(ChartColumns)): #!
            if(VAR.GetChartColors(VAR) == None):
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page1.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                elif Page1.TimeType == 'Time':
                    plot = Page1.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                Colors.append(plot[0].get_color())
            else:
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page1.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
                elif Page1.TimeType == 'Time':
                    plot = Page1.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
        #
        if(VAR.GetChartColors(VAR) is None):
            VAR.SetChartColors(VAR, Colors)
        #
        Page1.ax.legend(loc=9, ncol=len(ChartColumns)) # Add legend to the chart
        #
        Page1.ax.grid(True, which='both', axis='both', linestyle='--')
        Page1.ax.set_ylabel('Temperature')
        #
        if Page1.TimeType == 'Time':
            Page1.ax.set_xlabel('Time (s)')
        else:
            pass
        Page1.Canvas.draw()