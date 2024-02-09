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
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
# import pandas as pd
# import datetime
# import numpy as np
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
import glob
from shutil import copyfile

# Import custom library
from Variables import VAR

#%%
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
        print('Next',self.currentId())
        return

    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
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
        print(stringEXE)
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
#%%
'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        # Create grid layot for the window
        Layout_Page1 = PQW.QGridLayout()
        #
        Page1.Sensors = (VAR.GetActiveParameters(VAR,6)).split(',')
        Page1.Heights = (VAR.GetActiveParameters(VAR,7)).split(',')
        # Top Sensor
        Label_TopSensor = PQW.QLabel('Top Sensor:')
        Page1.Combobox_TopSensor = PQW.QComboBox() # Combobox probe name
        for item in Page1.Sensors:
            Page1.Combobox_TopSensor.addItem(item)
        #
        Label_Threshold = PQW.QLabel('Threshold:')
        Page1.Threshold = PQW.QLineEdit(self)
        Page1.Threshold.setText('0.0')
        Label_Threshold_unit = PQW.QLabel(u"\N{DEGREE SIGN}"+'C')
        #
        Label_k = PQW.QLabel('k:')
        Page1.k = PQW.QLineEdit(self)
        Page1.k.setText('0.002')
        Label_k_unit = PQW.QLabel('m<sup>2</sup> s<sup>-1</sup>')
        #
        Label_WinMean = PQW.QLabel('Mean window:')
        Page1.WinMean = PQW.QComboBox()
        Page1.WinMean.addItem('1')
        Page1.WinMean.addItem('2')
        Page1.WinMean.addItem('3')
        Page1.WinMean.addItem('4')
        Page1.WinMean.addItem('5')
        Page1.WinMean.addItem('6')
        Page1.WinMean.addItem('7')
        Label_WinMean_unit = PQW.QLabel('days')
        # Insert elements in the grid
        Layout_Page1.addWidget(Label_TopSensor, 0, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_TopSensor, 0, 1, 1, 2)
        Layout_Page1.addWidget(Label_Threshold, 1, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Threshold, 1, 1, 1, 1)
        Layout_Page1.addWidget(Label_Threshold_unit, 1, 2, 1, 1)

        Layout_Page1.addWidget(Label_k, 2, 0, 1, 1)
        Layout_Page1.addWidget(Page1.k, 2, 1, 1, 1)
        Layout_Page1.addWidget(Label_k_unit, 2, 2, 1, 1)

        Layout_Page1.addWidget(Label_WinMean, 4, 0, 1, 1)
        Layout_Page1.addWidget(Page1.WinMean, 4, 1, 1, 1)
        Layout_Page1.addWidget(Label_WinMean_unit, 4, 2, 1, 1)

        # Show layout
        self.setLayout(Layout_Page1)
# #%%
# '''
# Page 2 of the wizard
# '''
# class Page2(PQW.QWizardPage):
#     def __init__(self, parent=None):
#         super(Page2, self).__init__(parent)