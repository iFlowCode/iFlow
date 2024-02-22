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
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import datetime
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import subprocess
import glob

# Import custom library
from Variables import VAR
from loguru import logger

'''
Wizzard Add Probe Class
'''
class SignalProcessing(PQW.QWizard):
    def __init__(self, parent=None):
        super(SignalProcessing, self).__init__(parent)
        self.setWindowTitle('Signal Processing')
        #
        self.addPage(Page1(self)) # Add Page1
        self.addPage(Page2(self)) # Add Page1
        #
        self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print) # Click event on Next Page of the wizard
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        
    def next_print(self):
        # Check Mobile Window Lenght
        if Page1.Checkbox_MobWin:
            try:
                float(Page1.WinLen.text())
            except:
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'The Mobile Window lenght is\'t a number.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
                return
        #
        if Page1.Combobox_Method.currentText() == 'FFT':
            # Check FFT Window
            if Page1.Combobox_FFTwin.currentText() == '':
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'FFT window not choosen', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
                return
            # Check FFT Window
            if Page1.Combobox_Detrending.currentText() == '':
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'Detrending not choosen', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
                return
        elif Page1.Combobox_Method.currentText() == 'LPM':
            # Check Number of sensors
            nSensors = 0
            Sensors = VAR.GetActiveParameters(VAR,6).split(',')
            FlagFirst = True
            for i in range(0,len(VAR.GetActiveParameters(VAR,6).split(','))):
                if Page1.VBoxSensor.itemAt(i).widget().isChecked():
                    nSensors += 1
                    if FlagFirst:
                        SensorUP = Sensors[i]
                        FlagFirst = False
                    SensorDOWN = Sensors[i]
            #
            if nSensors < 2:
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'Too few sensors to perform MLEn', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
                return
            elif nSensors < 3:
                PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Too few sensors to perform MLEn Boundaries', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        # Filter data
        df = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
        dfwork = pd.DataFrame()
        dfwork['Time'] = df['Time']
        SensorActive = VAR.GetActiveParameters(VAR,6).split(',')
        HeightActive = VAR.GetActiveParameters(VAR,7).split(',')
        SensorWork = []
        HeightWork = []
        for i in range(0,len(VAR.GetActiveParameters(VAR,6).split(','))):
            if Page1.VBoxSensor.itemAt(i).widget().isChecked():
                SensorWork.append(SensorActive[i])
                HeightWork.append(HeightActive[i])
            else:
                if Page1.Combobox_Tref.currentText() == Page1.VBoxSensor.itemAt(i).widget().text():
                    pass
                else:
                    df = df.drop(columns=[Page1.VBoxSensor.itemAt(i).widget().text()])
        #
        FileDel = glob.glob('../temp/*.*')
        for File in FileDel:
            os.remove(File)
        #
        df.to_pickle('../temp/clean.pkz',compression='zip')
        #
        if Page1.Combobox_Method.currentText() == 'FFT':
            stringEXE = 'SignalProcessingFFT.exe'
        elif Page1.Combobox_Method.currentText() == 'LPM':
            stringEXE = 'SignalProcessingLPM.exe'
        # Mobile Window [BOOLEAN] -f
        if Page1.Checkbox_MobWin:
            stringEXE = stringEXE + ' -f True'
            # Mobile Window lenght [FLOAT] -s
            stringEXE = stringEXE + ' -s "' + Page1.WinLen.text() +'"'
        else:
            stringEXE = stringEXE + ' -f False'
        #
        if Page1.Combobox_Method.currentText() == 'LPM':
            # SensorRef [STRING] -q
            stringEXE = stringEXE + ' -q "' + Page1.Combobox_Tref.currentText() +'"'
            # Degree of freedom
            stringEXE = stringEXE + ' -o "' + Page1.dof.text() +'"'
            # Order
            stringEXE = stringEXE + ' -m "' + Page1.order.text() +'"'
        elif Page1.Combobox_Method.currentText() == 'FFT':
            # FFT window [STRING] -t
            stringEXE = stringEXE + ' -t "' + Page1.Combobox_FFTwin.currentText() +'"'
            # Detrending [BOOLEAN] -r
            if Page1.Combobox_Detrending.currentText() == 'Yes':
                stringEXE = stringEXE + ' -r True'
            else:
                stringEXE = stringEXE + ' -r False'
            # Period to Extract [LIST] -XXXX
            stringEXE = stringEXE + ' -a "' + Page1.SavePer.text() +'"'
        # dt [FLOAT] -d
        stringEXE = stringEXE + ' -d "' + VAR.GetActiveParameters(VAR,3) +'"'
        # Call external program
        logger.debug(stringEXE)
        os.system(stringEXE)
        # Check Run
        HandleLog = open('../temp/SignalProcessing.log','r')
        Check = HandleLog.readline().replace('\n','')
        HandleLog.close()
        #
        if Check == 'No Error':
            FilesRun = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/*.run')
            NewRun = '-1'
            for FileRun in FilesRun:
                if int(FileRun.split('\\')[1].split('.')[0]) > int(NewRun):
                    NewRun = FileRun.split('\\')[1].split('.')[0]
            NewRun = str(int(NewRun)+1)
            if Page1.Combobox_Method.currentText() == 'LPM':
                # Move the data
                os.remove('../temp/clean.pkz')
                os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'.run')
                os.replace('../temp/MobWinTime.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_MobWinTime.pkz')
                os.replace('../temp/Amplitude.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_Amplitude.pkz')
                os.replace('../temp/Phase.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_Phase.pkz')
                os.replace('../temp/SRN.PdList','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_SRN.PdList')
                os.replace('../temp/Y.PdList','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_Y.PdList')
                CYFiles = glob.glob('../temp/*.CY_m_nt')
                for CYFile in CYFiles:
                    os.replace(CYFile,'../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_'+CYFile.split('\\')[1])
                os.replace('../temp/SignalProcessing.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_SignalProcessing.log')
            elif Page1.Combobox_Method.currentText() == 'FFT':
                # Move the data
                os.remove('../temp/clean.pkz')
                os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'.run')
                os.replace('../temp/Amplitude.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_Amplitude.pkz')
                os.replace('../temp/Phase.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_Phase.pkz')
                os.replace('../temp/MobWinTime.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_MobWinTime.pkz')
                os.replace('../temp/SignalProcessing.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+str(NewRun)+'_SignalProcessing.log')
            #
            VAR.GetTabSignProc(VAR).Update(7)
            VAR.GetTabParEst(VAR).Update(7)
            #
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Signal Processing Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        else:
            PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    def finish_print(self):
        logger.debug("Signal processing End")
        #
        return

'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        #
        Page1.Sensors = (VAR.GetActiveParameters(VAR,6)).split(',')
        Page1.Heights = (VAR.GetActiveParameters(VAR,7)).split(',')
        # Create grid layot for the window
        Layout_Page1 = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Page1_Left = PQW.QVBoxLayout()
        #
        Layout_Page1_Left_1 = PQW.QHBoxLayout()
        #
        Label_Method = PQW.QLabel('Method:')
        Layout_Page1_Left_1.addWidget(Label_Method)
        Page1.Combobox_Method = PQW.QComboBox() # Combobox probe name
        for item in VAR.GetProcessingMethod(VAR):
            if item != '':
                Page1.Combobox_Method.addItem(item)
        # Page1.Combobox_Method.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_Method.currentIndexChanged.connect(self.on_Combobox_Method_change) # ComboBox event change item
        Layout_Page1_Left_1.addWidget(Page1.Combobox_Method)
        #
        Layout_Page1_Left.addLayout(Layout_Page1_Left_1)
        # FFT
        self.GroupBox_FFT = PQW.QGroupBox('FFT:')
#         # self.GroupBox_FFT.setFixedWidth(120)
        self.VBoxFFT = PQW.QVBoxLayout() # Create the Layout for the Groupbox
        Label_Detrending = PQW.QLabel('Detrending:')
        Page1.Combobox_Detrending = PQW.QComboBox()
        Page1.Combobox_Detrending.setToolTip('Filter results by detrending') # Tooltip message
        # Page1.Combobox_Detrending.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        #
        for item in VAR.GetDetrending(VAR):
            Page1.Combobox_Detrending.addItem(item)
        #
        Label_FFTwin = PQW.QLabel('FFT Window:')
        Page1.Combobox_FFTwin = PQW.QComboBox()
        Page1.Combobox_FFTwin.setToolTip('Filter results by FFT window') # Tooltip message
        # Page1.Combobox_FFTwin.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        #
        for item in VAR.GetFFTWindowfunction(VAR):
            Page1.Combobox_FFTwin.addItem(item)
        #
        Label_SavePer = PQW.QLabel('Period to extract:')
        Page1.SavePer = PQW.QLineEdit(self)
        Page1.SavePer.setText('24')
        Page1.SavePer.setToolTip('Period to extract') # Tooltip message
        # Page1.SavePer.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        #
        self.VBoxFFT.addWidget(Label_Detrending)
        self.VBoxFFT.addWidget(Page1.Combobox_Detrending)
        self.VBoxFFT.addWidget(Label_FFTwin)
        self.VBoxFFT.addWidget(Page1.Combobox_FFTwin)
        self.VBoxFFT.addWidget(Label_SavePer)
        self.VBoxFFT.addWidget(Page1.SavePer)
        self.GroupBox_FFT.setLayout(self.VBoxFFT) # Add the Layout to the Groupbox 
        Layout_Page1_Left.addWidget(self.GroupBox_FFT)
        # LPM
        self.GroupBox_LPM = PQW.QGroupBox('LPM:')
        # self.GroupBox_LPM.setFixedWidth(120)
        self.VBoxLPM = PQW.QVBoxLayout() # Create the Layout for the Groupbox
        # Reference sensor
        Label_Tref = PQW.QLabel('Tref Sensor:')
        Page1.Combobox_Tref = PQW.QComboBox()
        # Page1.Combobox_Detrending.setToolTip('Filter results by detrending') # Tooltip message
        #
        for item in Page1.Sensors:
            Page1.Combobox_Tref.addItem(item)
        #
        Page1.Combobox_Tref.setEnabled(False)
        # Page1.Combobox_Tref.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # dof
        Label_dof = PQW.QLabel('Degree of freedom:')
        Page1.dof = PQW.QLineEdit(self)
        # Page1.dof.setText(str(Page1.Combobox_SensorDOWN.currentIndex()-Page1.Combobox_SensorUP.currentIndex()+2))
        Page1.dof.setText(str(len(VAR.GetActiveParameters(VAR,6).split(','))+1))
        Page1.dof.setEnabled(False)
        # Page1.dof.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # order
        Label_order = PQW.QLabel('Order: ')
        Page1.order = PQW.QLineEdit(self)
        Page1.order.setText('2')
        Page1.order.setEnabled(False)
        # Page1.order.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # LPM
        self.VBoxLPM.addWidget(Label_Tref)
        self.VBoxLPM.addWidget(Page1.Combobox_Tref)
        self.VBoxLPM.addWidget(Label_dof)
        self.VBoxLPM.addWidget(Page1.dof)
        self.VBoxLPM.addWidget(Label_order)
        self.VBoxLPM.addWidget(Page1.order)
        self.GroupBox_LPM.setLayout(self.VBoxLPM) # Add the Layout to the Groupbox 
        #
        Layout_Page1_Left.addWidget(self.GroupBox_LPM)
        #
        container_left.setLayout(Layout_Page1_Left)
        #
        container_right = PQW.QFrame()
        Layout_Page1_Right = PQW.QVBoxLayout()
        #
        Layout_Page1_Right_1 = PQW.QHBoxLayout()
        #
        Page1.Checkbox_MobWin = PQW.QCheckBox("Mobile window lenght (hr):")
        Page1.Checkbox_MobWin.toggled.connect(self.UpdateMobWin)
        Layout_Page1_Right_1.addWidget(Page1.Checkbox_MobWin)
        Page1.WinLen = PQW.QLineEdit(self)
        # Page1.WinLen.setFixedWidth(110) #!
        Page1.WinLen.setText('96')
        Page1.WinLen.setEnabled(False)
        Layout_Page1_Right_1.addWidget(Page1.WinLen)
        #
        Layout_Page1_Right.addLayout(Layout_Page1_Right_1)
        #
        self.GroupBox_Sensors = PQW.QGroupBox('Sensors:')
        # self.GroupBox_Sensors.setFixedWidth(200)
        Page1.VBoxSensor = PQW.QGridLayout()
        self.GroupBox_Sensors.setLayout(Page1.VBoxSensor)
        #
        for Sensor in VAR.GetActiveParameters(VAR,6).split(','):
            CheckBox = PQW.QCheckBox(Sensor)
            CheckBox.setChecked(True)
            Page1.VBoxSensor.addWidget(CheckBox)
        #
        Layout_Page1_Right.addWidget(self.GroupBox_Sensors)
        #
        container_right.setLayout(Layout_Page1_Right)
        #
        Layout_Page1.addWidget(container_left)
        Layout_Page1.addWidget(container_right)
        #
        self.setLayout(Layout_Page1)

    def UpdateMobWin(self, state):
        if state:
            Page1.WinLen.setEnabled(True)
        else:
            Page1.WinLen.setEnabled(False)
        return

    def on_Combobox_Method_change(self):
        logger.debug('Page1 - on_Combobox_Method_change')
        if Page1.Combobox_Method.currentText() == 'LPM':
            Page1.Combobox_Detrending.setEnabled(False)
            Page1.Combobox_FFTwin.setEnabled(False)
            Page1.SavePer.setEnabled(False)
            Page1.Combobox_Tref.setEnabled(True)
            Page1.dof.setEnabled(True)
            Page1.order.setEnabled(True)
        elif Page1.Combobox_Method.currentText() == 'FFT':
            Page1.Combobox_Detrending.setEnabled(True)
            Page1.Combobox_FFTwin.setEnabled(True)
            Page1.SavePer.setEnabled(True)
            Page1.Combobox_Tref.setEnabled(False)
            Page1.dof.setEnabled(False)
            Page1.order.setEnabled(False)
        return

'''
Page 2 of the wizard
'''
class Page2(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)