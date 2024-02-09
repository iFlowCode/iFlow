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

#%%
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
        print('Next',self.currentId())
        # Check Mobile Window Lenght
        WinLenght = Page1.WinLen.text()
        try:
            float(WinLenght)
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
        if Page1.Combobox_MobWin.currentText() == 'Yes':
            stringEXE = stringEXE + ' -f True'
            # Mobile Window lenght [FLOAT] -s
            stringEXE = stringEXE + ' -s "' + Page1.WinLen.text() +'"'
        else:
            stringEXE = stringEXE + ' -f False'
        #
        if Page1.Combobox_Method.currentText() == 'LPM':
            # SensorRef [STRING] -q
            stringEXE = stringEXE + ' -q "' + Page1.Combobox_Tref.currentText() +'"'
            # # SensorUP [STRING] -w
            # stringEXE = stringEXE + ' -w "' + SensorUP +'"'
            # # SensorDOWN [STRING] -e
            # stringEXE = stringEXE + ' -e "' + SensorDOWN +'"'
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
        print(stringEXE)
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

#%%
    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
        #
        return
        
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
        # Method
        Label_Method = PQW.QLabel('Method:')
        Page1.Combobox_Method = PQW.QComboBox() # Combobox probe name
        #
        for item in VAR.GetProcessingMethod(VAR):
            if item != '':
                Page1.Combobox_Method.addItem(item)
        # Page1.Combobox_Method.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_Method.currentIndexChanged.connect(self.on_Combobox_Method_change) # ComboBox event change item
        # Groupbox Mobile Window
        self.GroupBox_MobWin = PQW.QGroupBox('Mobile Window:')
        self.HBoxMobWin = PQW.QHBoxLayout() # Create the Layout for the Groupbox 
        # Mobile Window
        Label_MobWin = PQW.QLabel('Mobile window:')
        # Label_MobWin.setFixedWidth(110) #!
        Page1.Combobox_MobWin = PQW.QComboBox() # Combobox probe name
        # Page1.Combobox_MobWin.setFixedWidth(110) #!
        Page1.Combobox_MobWin.addItem('Yes')
        Page1.Combobox_MobWin.addItem('No')
        # Page1.Combobox_MobWin.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_MobWin.currentIndexChanged.connect(self.on_Combobox_MobWin_change) # ComboBox event change item
        self.HBoxMobWin.addWidget(Label_MobWin) # Add element to the Layout
        self.HBoxMobWin.addWidget(Page1.Combobox_MobWin) # Add element to the Layout
        # Lenght
        Label_MobWinLenght = PQW.QLabel('Lenght (hr):')
        # Label_MobWinLenght.setFixedWidth(110) #!
        Page1.WinLen = PQW.QLineEdit(self)
        # Page1.WinLen.setFixedWidth(110) #!
        Page1.WinLen.setText('96')
        # Page1.WinLen.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        self.HBoxMobWin.addWidget(Label_MobWinLenght) # Add element to the Layout
        self.HBoxMobWin.addWidget(Page1.WinLen) # Add element to the Layout
        # Slider
        Label_Slider = PQW.QLabel('Slider (s):')
        # Label_Slider.setFixedWidth(110) #!
        Page1.Slider = PQW.QLineEdit(self)
        # Page1.Slider.setFixedWidth(110) #!
        Page1.Slider.setText(str(VAR.GetActiveParameters(VAR,3)))
        # Page1.Slider.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        self.HBoxMobWin.addWidget(Label_Slider) # Add element to the Layout
        self.HBoxMobWin.addWidget(Page1.Slider) # Add element to the Layout
        self.GroupBox_MobWin.setLayout(self.HBoxMobWin) # Add the Layout to the Groupbox 
        # Update
        Page1.Check_Update = PQW.QCheckBox('Update Run:')
        Page1.Check_Update.toggled.connect(self.UpdateChange) #!
        Page1.Combox_RunToUpdate = PQW.QComboBox()
        UpdateRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/*.run')
        for UpdateRun in UpdateRuns:
            Page1.Combox_RunToUpdate.addItem(UpdateRun.split('\\')[1].replace('.run','')) #!
        Page1.Combox_RunToUpdate.setEnabled(False)
        # FFT
        self.GroupBox_FFT = PQW.QGroupBox('FFT:')
        # self.GroupBox_FFT.setFixedWidth(120)
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
        # # Top sensors
        # Label_SensorUP = PQW.QLabel('Sensor UP:')
        # Page1.Combobox_SensorUP = PQW.QComboBox()
        # # Page1.Combobox_FFTwin.setToolTip('Filter results by FFT window') # Tooltip message
        # #
        # for item in Page1.Sensors:
        #     Page1.Combobox_SensorUP.addItem(item)
        # Page1.Combobox_SensorUP.setEnabled(False)
        # Page1.Combobox_SensorUP.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # Page1.Combobox_SensorUP.currentIndexChanged.connect(self.on_Combobox_SensorUP_change) # ComboBox event change item
        # # Bottom sensor
        # Label_SensorDOWN = PQW.QLabel('Sensor DOWN:')
        # Page1.Combobox_SensorDOWN = PQW.QComboBox()
        # # Page1.Combobox_FFTwin.setToolTip('Filter results by FFT window') # Tooltip message
        # #
        # for item in Page1.Sensors:
        #     Page1.Combobox_SensorDOWN.addItem(item)
        # Page1.Combobox_SensorDOWN.setCurrentText(item)
        # Page1.Combobox_SensorDOWN.setEnabled(False)
        # Page1.Combobox_SensorDOWN.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # Page1.Combobox_SensorDOWN.currentIndexChanged.connect(self.on_Combobox_SensorDOWN_change) # ComboBox event change item
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
        self.GroupBox_Sensors = PQW.QGroupBox('Sensors:')
        # self.GroupBox_Sensors.setFixedWidth(200)
        Page1.VBoxSensor = PQW.QGridLayout()
        self.GroupBox_Sensors.setLayout(Page1.VBoxSensor)
        print(VAR.GetActiveParameters(VAR,6))
        for Sensor in VAR.GetActiveParameters(VAR,6).split(','):
            CheckBox = PQW.QCheckBox(Sensor)
            CheckBox.setChecked(True)
            Page1.VBoxSensor.addWidget(CheckBox)
        #
        self.VBoxLPM.addWidget(Label_Tref)
        self.VBoxLPM.addWidget(Page1.Combobox_Tref)
        # self.VBoxLPM.addWidget(Label_SensorUP)
        # self.VBoxLPM.addWidget(Page1.Combobox_SensorUP)
        # self.VBoxLPM.addWidget(Label_SensorDOWN)
        # self.VBoxLPM.addWidget(Page1.Combobox_SensorDOWN)
        self.VBoxLPM.addWidget(Label_dof)
        self.VBoxLPM.addWidget(Page1.dof)
        self.VBoxLPM.addWidget(Label_order)
        self.VBoxLPM.addWidget(Page1.order)
        self.GroupBox_LPM.setLayout(self.VBoxLPM) # Add the Layout to the Groupbox 
        # Insert elements in the grid
        Layout_Page1.addWidget(Label_Method, 0, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_Method, 0, 1, 1, 1)
        Layout_Page1.addWidget(Page1.Check_Update,0,2,1,1)
        Layout_Page1.addWidget(Page1.Combox_RunToUpdate,0,3,1,1)
        Layout_Page1.addWidget(self.GroupBox_MobWin, 1, 0, 1, 4)
        Layout_Page1.addWidget(self.GroupBox_FFT, 3, 0, 1, 1)
        Layout_Page1.addWidget(self.GroupBox_LPM, 3, 1, 1, 1)
        Layout_Page1.addWidget(self.GroupBox_Sensors, 3, 2, 1, 2)
        # Show layout
        self.setLayout(Layout_Page1)

    def UpdateChange(self):
        print('UpdateChange')
        if Page1.Check_Update.isChecked():
            Page1.Combox_RunToUpdate.setEnabled(True)
            Page1.Combobox_Method.setEnabled(False)
            Page1.Combobox_MobWin.setEnabled(False)
            Page1.WinLen.setEnabled(False)
            Page1.Slider.setEnabled(False)
            Page1.Combobox_Detrending.setEnabled(False)
            Page1.Combobox_FFTwin.setEnabled(False)
            Page1.SavePer.setEnabled(False)
            Page1.Combobox_Tref.setEnabled(False)
            Page1.dof.setEnabled(False)
            Page1.order.setEnabled(False)
            print(Page1.Combox_RunToUpdate.currentText())
            print('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+Page1.Combox_RunToUpdate.currentText()+'.run')
            HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+Page1.Combox_RunToUpdate.currentText()+'.run','r')
            Run_AnalysisType = HandleRun.readline().replace('\n','').split(';')[0]
            if Run_AnalysisType == 'FFT':
                Run_MobileWin = HandleRun.readline().replace('\n','').split(';')[0]
                Run_MobileWinLenght = HandleRun.readline().replace('\n','').split(';')[0]
                Run_FFTwin = HandleRun.readline().replace('\n','').split(';')[0]
                Run_Detrending = HandleRun.readline().replace('\n','').split(';')[0]
                Run_Periods = HandleRun.readline().replace('\n','').split(';')[0]
            elif Run_AnalysisType == 'LPM':
                Run_MobWin = HandleRun.readline().replace('\n','').split(';')[0]
                Run_MobWinLen = HandleRun.readline().replace('\n','').split(';')[0]
                Run_SensorRef = HandleRun.readline().replace('\n','').split(';')[0]
                Run_SensorUP = HandleRun.readline().replace('\n','').split(';')[0]
                Run_SensorDOWN = HandleRun.readline().replace('\n','').split(';')[0]
                Run_dt = HandleRun.readline().replace('\n','').split(';')[0]
                Run_dof = HandleRun.readline().replace('\n','').split(';')[0]
                Run_order = HandleRun.readline().replace('\n','').split(';')[0]
                Run_Sensors = HandleRun.readline().replace('\n','').split(';')[0]
                Run_slider = HandleRun.readline().replace('\n','').split(';')[0]
            HandleRun.close()
        else:
            Page1.Combox_RunToUpdate.setEnabled(False)
            Page1.Combobox_Method.setEnabled(True)
            Page1.Combobox_MobWin.setEnabled(True)
            Page1.WinLen.setEnabled(True)
            Page1.Slider.setEnabled(True)
            if Page1.Combobox_Method.currentText() == 'FFT':
                Page1.Combobox_Detrending.setEnabled(True)
                Page1.Combobox_FFTwin.setEnabled(True)
                Page1.SavePer.setEnabled(True)
            elif Page1.Combobox_Method.currentText() == 'LPM':
                Page1.Combobox_Tref.setEnabled(True)
                Page1.dof.setEnabled(True)
                Page1.order.setEnabled(True)
        return

    def on_Combobox_Method_change(self):
        print('Page1 - on_Combobox_Method_change')
        if Page1.Combobox_Method.currentText() == 'LPM':
            Page1.Combobox_Detrending.setEnabled(False)
            Page1.Combobox_FFTwin.setEnabled(False)
            Page1.SavePer.setEnabled(False)
            Page1.Combobox_Tref.setEnabled(True)
            # Page1.Combobox_SensorUP.setEnabled(True)
            # Page1.Combobox_SensorDOWN.setEnabled(True)
            Page1.dof.setEnabled(True)
            Page1.order.setEnabled(True)
        elif Page1.Combobox_Method.currentText() == 'FFT':
            Page1.Combobox_Detrending.setEnabled(True)
            Page1.Combobox_FFTwin.setEnabled(True)
            Page1.SavePer.setEnabled(True)
            Page1.Combobox_Tref.setEnabled(False)
            # Page1.Combobox_SensorUP.setEnabled(False)
            # Page1.Combobox_SensorDOWN.setEnabled(False)
            Page1.dof.setEnabled(False)
            Page1.order.setEnabled(False)
        return

    def on_Combobox_MobWin_change(self):
        print('Page1 - on_Combobox_MobWin_change')
        if Page1.Combobox_MobWin.currentText() == 'Yes':
            Page1.WinLen.setEnabled(True)
        else:
            Page1.WinLen.setEnabled(False)
        return

    # def on_Combobox_SensorUP_change(self):
    #     Page1.dof.setText(str(Page1.Combobox_SensorDOWN.currentIndex()-Page1.Combobox_SensorUP.currentIndex()+2))
    #     return

    # def on_Combobox_SensorDOWN_change(self):
    #     Page1.dof.setText(str(Page1.Combobox_SensorDOWN.currentIndex()-Page1.Combobox_SensorUP.currentIndex()+2))
    #     return

#%%
'''
Page 2 of the wizard
'''
class Page2(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)