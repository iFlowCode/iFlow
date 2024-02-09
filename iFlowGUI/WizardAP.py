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
import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import numpy.random.common
# import numpy.random.bounded_integers
from shutil import copy
import pandas as pd
import datetime
import numpy as np
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
import glob

# Import custom library
from Variables import VAR

#%%
'''
Wizzard Add Probe Class
'''
class AddProbe(PQW.QWizard):
    def __init__(self, parent=None):
        super(AddProbe, self).__init__(parent)
        self.setWindowTitle('Add probe to Project')
        #
        # print('Windows size',VAR.GetWindowsSize(VAR)[0],VAR.GetWindowsSize(VAR)[1])
        # if VAR.GetWindowsSize(VAR)[0] < 800:
        #     width = VAR.GetWindowsSize(VAR)[0]
        # else:
        #     width = 800
        # if VAR.GetWindowsSize(VAR)[1] < 600:
        #     height = VAR.GetWindowsSize(VAR)[1]
        # else:
        #     height = 600
        width = VAR.GetWindowsSize(VAR)[0] * 2 / 3 # Width of the window
        height = VAR.GetWindowsSize(VAR)[1] * 2 / 3 # Height of the window
        self.setMinimumSize(width,height) # Set the minimun size of the wondow
        #
        Page1.Flag_Update = False # Set False the Flag_Update
        #
        VAR.SetChartColors(VAR,None) # Reset the chart's colors
        #
        self.addPage(Page1(self)) # Add Page1
        self.addPage(Page2(self)) # Add Page2
        self.addPage(Page3(self)) # Add Page3
        self.addPage(Page4(self)) # Add Page4
        self.addPage(Page5(self)) # Add Page5
        #
        self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print) # Click event on Next Page of the wizard
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        
    def next_print(self):
        print('Next',self.currentId())
        Flag_Error = 0
        if(self.currentId() == 1):
            # Check the user input
            try:
                if((Page1.Combobox_ProbName.currentText())  != ''):
                    pass
                else:
                    Flag_Error = 1
            except:
                Flag_Error = 1
            #
            try:
                if not os.path.exists(Page1.Data_File.text()) and Flag_Error == 0:
                    Flag_Error = 2
            except:
                Flag_Error = 2
            #
            try:
                if(Page1.Combobox_TimeSerie.currentText() != '' and Flag_Error == 0):
                    pass
                else:
                    Flag_Error = 3
            except:
                Flag_Error = 3
            #
            try:
                if(Page1.Combobox_TimeType.currentText() != '' and Flag_Error == 0):
                    pass
                else:
                    Flag_Error = 4
            except:
                Flag_Error = 4
            #
            try:
                float(Page1.SampleRate.text())
                pass
            except:
                if(Flag_Error == 0):
                    Flag_Error = 5
            # Error Message
            if(Flag_Error == 1):
                string = 'Probe\'s name not setted.'
            elif(Flag_Error == 2):
                string = 'Data file of the probe not setted.'
            elif(Flag_Error == 3):
                string = 'Time serie of the probe not setted.'
            elif(Flag_Error == 4):
                string = 'Time serie\'s type not setted.'
            elif(Flag_Error == 5):
                string = 'dt setted is a string not a number.'
            # Popup an error message if needed
            if(Flag_Error != 0):
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', string, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
            else: # to new page
                if Page1.Flag_Update: #! To finish
                    pass
                else:
                    Page2.List_Sensor_File.clear() # Reset List of sensor in file
                    Page2.List_Sensor_Impo.clear() # Reset list of sensor to import
                    if Page1.Flag_Update: #! To finish
                        pass
                    else:    
                        for i, Sensor in enumerate(Page1.DataNow.columns.tolist()):
                            if(Sensor == Page1.Combobox_TimeSerie.currentText()):
                                pass
                            else:
                                Page2.List_Sensor_File.addItem(Sensor) # Add the sensor, except the timeserie, to the list of sensor in file
            #
            Page2.UpdateChart(self)
        elif(self.currentId() == 2):
            if(Page2.List_Sensor_Impo.count() == 0): # Popup message if there isn't any sensor choosen to import
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'No sensor to import.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
            else: # to new page
                if Page1.Flag_Update: #! To finish
                    pass
                else:
                    Page3.Table_Height.setColumnCount(2)
                    Page3.Table_Height.setHorizontalHeaderLabels(['Sensor', 'Height (m asl)'])
                    Page3.Table_Height.setRowCount(Page2.List_Sensor_Impo.count())
                    #
                    for i in range(0,Page2.List_Sensor_Impo.count()):
                        item = PQW.QTableWidgetItem(Page2.List_Sensor_Impo.item(i).text())
                        item2 = PQW.QTableWidgetItem('')
                        item.setFlags(PQC.Qt.ItemIsEnabled)
                        Page3.Table_Height.setItem(i,0, item)
                        Page3.Table_Height.setItem(i,1, item2)
            #
            Page3.UpdateChart(self)
        elif(self.currentId() == 3):
            Page4.UpdateChart(self)
            #
            Flag_Error = False
            BackValue = None
            for i in range(0,Page3.Table_Height.rowCount()):
                try:
                    Value = float(Page3.Table_Height.item(i, 1).text())
                    if(BackValue == None):
                        BackValue == Value
                    else:
                        if(BackValue > Value):
                            BackValue == Value
                        else:
                            Flag_Error = True
                except:
                    Flag_Error = True
            #
            if Flag_Error:
                PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'Sensors\'s position not correct .', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                self.back()
                return
            #
            if(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'):
                Page4.ImpoFromDateTime.setEnabled(True)
                Page4.ImpoFromTime.setEnabled(False)
                Page4.ImpoToDateTime.setEnabled(True)
                Page4.ImpoToTime.setEnabled(False)
                #
                Page4.ImpoToDateTime.setHidden(False)
                Page4.ImpoFromTime.setHidden(True)
                Page4.ImpoToDateTime.setHidden(False)
                Page4.ImpoToTime.setHidden(True)
                # if Page1.Flag_Update: #! To finish
                #     pass
                # else:
                DataFrom = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[0]
                DataTo = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[Page1.DataNow.shape[0]-1]
                DTfrom = PQC.QDateTime(int(DataFrom[0:4]),int(DataFrom[5:7]),int(DataFrom[8:10]),int(DataFrom[11:13]),int(DataFrom[14:16]),int(DataFrom[17:19]))
                DTto = PQC.QDateTime(int(DataTo[0:4]),int(DataTo[5:7]),int(DataTo[8:10]),int(DataTo[11:13]),int(DataTo[14:16]),int(DataTo[17:19]))
                Page4.ImpoFromDateTime.setDateTime(DTfrom)
                Page4.ImpoFromDateTime.setDisplayFormat('yyyy-MM-dd hh:mm:ss')
                Page4.ImpoToDateTime.setDateTime(DTto)
                Page4.ImpoToDateTime.setDisplayFormat('yyyy-MM-dd hh:mm:ss')
            elif(Page1.Combobox_TimeType.currentText() == 'Time'):
                Page4.ImpoFromDateTime.setEnabled(False)
                Page4.ImpoFromTime.setEnabled(True)
                Page4.ImpoToDateTime.setEnabled(False)
                Page4.ImpoToTime.setEnabled(True)
                #
                Page4.ImpoFromDateTime.setHidden(True)
                Page4.ImpoFromTime.setHidden(False)
                Page4.ImpoToDateTime.setHidden(True)
                Page4.ImpoToTime.setHidden(False)
                # if Page1.Flag_Update: #! To finish
                #     pass
                # else:
                if Page1.Flag_TimeSerie == PQW.QMessageBox.No:
                    DataFrom = 0.0
                    DataTo = 9999.0
                    Page4.ImpoFromTime.setEnabled(True)
                    Page4.ImpoToTime.setEnabled(False)
                else:
                    DataFrom = int(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[0])
                    DataTo = int(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[Page1.DataNow.shape[0]-1])
                    Page4.ImpoFromTime.setEnabled(True)
                    Page4.ImpoToTime.setEnabled(True)
                Page4.ImpoFromTime.setRange(DataFrom,DataTo)
                Page4.ImpoToTime.setRange(DataFrom,DataTo)
                Page4.ImpoFromTime.setValue(DataFrom)
                Page4.ImpoToTime.setValue(DataTo)
            else:
                pass
        elif(self.currentId() == 4):
            # Check start date/time and end date/time
            if(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'):
                dtFrom = Page4.ImpoFromDateTime.dateTime()
                dtTo = Page4.ImpoToDateTime.dateTime()
                #
                if(dtFrom >= dtTo):
                    PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'From date > To date.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                    self.back()
                    return
                # else:
                #     dtFrom_string = dtFrom.toString(Page4.ImpoFromDateTime.displayFormat())
                #     dtTo_string = dtTo.toString(Page4.ImpoToDateTime.displayFormat())
            elif(Page1.Combobox_TimeType.currentText() == 'Time'):
                dtFrom = Page4.ImpoFromTime.value()
                dtTo = Page4.ImpoToTime.value()
                if(dtFrom >= dtTo):
                    PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'From date > To date.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                    self.back()
                    return

    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
        #
        stringEXE = 'DataImport.exe'
        stringLog = ''
        # Probe name  [STRING] -p
        # stringEXE = stringEXE + ' -p "' + Page1.Combobox_ProbName.currentText() +'"'
        # stringLog = stringLog + Page1.Combobox_ProbName.currentText() + ';ProbeName\n'
        # Project name  [STRING] -j
        # stringEXE = stringEXE + ' -j "' + VAR.GetActiveProject(VAR) +'"'
        # stringLog = stringLog + VAR.GetActiveProject(VAR) + ';ProjectName\n'
        # FileIn  [STRING] -f
        stringEXE = stringEXE + ' -f "' + Page1.Data_File.text() +'"'
        stringLog = stringLog + Page1.Data_File.text() + ';LastDatafile\n'
        # TimeSerie  [STRING] -s
        stringEXE = stringEXE + ' -s "' + Page1.Combobox_TimeSerie.currentText() +'"'
        stringLog = stringLog + Page1.Combobox_TimeSerie.currentText() + ';TimeSerieName\n'
        # TimeType  [STRING] -t
        stringEXE = stringEXE + ' -t "' + Page1.Combobox_TimeType.currentText() +'"'
        stringLog = stringLog + Page1.Combobox_TimeType.currentText() + ';TimeType\n'
        # SampleRate [FLOAT] -r
        stringEXE = stringEXE + ' -r ' + Page1.SampleRate.text()
        stringLog = stringLog + Page1.SampleRate.text() + ';SampleRate\n'
        # Interpolate missing data  [BOOLEAN] -i
        if Page1.CheckIMD.isChecked():
            stringEXE = stringEXE + ' -i True'
            stringLog = stringLog + 'True;IMD\n'
        else:
            stringLog = stringLog + 'False;IMD\n'
        # Rebuild time serie  [BOOLEAN] -e
        if Page1.CheckRTS.isChecked():
            stringEXE = stringEXE + ' -e True'
            stringLog = stringLog + 'True;RTS\n'
        else:
            stringLog = stringLog + 'False;RTS\n'
        # Sensors to import  [LIST] -n
        stringHelp = ''
        for i in range(0,Page3.Table_Height.rowCount()):
            stringHelp = stringHelp + Page3.Table_Height.item(i, 0).text() + ','
        stringEXE = stringEXE + ' -n "' + stringHelp[0:-1] +'"'
        stringLog = stringLog + stringHelp[0:-1] + ';SensorsName\n'
        # Sensors heights  [LIST]????? -h
        stringHelp = ''
        for i in range(0,Page3.Table_Height.rowCount()):
            stringHelp = stringHelp + Page3.Table_Height.item(i, 1).text() + ','
        stringEXE = stringEXE + ' -h "' + stringHelp[0:-1] + '"'
        stringLog = stringLog + stringHelp[0:-1] + ';SensorsHeight\n'
        # From  [STRING] -a
        if(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'):
            stringEXE = stringEXE + ' -a "' + Page4.ImpoFromDateTime.dateTime().toString(Page4.ImpoFromDateTime.displayFormat()) + '"'
            stringLog = stringLog + Page4.ImpoFromDateTime.dateTime().toString(Page4.ImpoFromDateTime.displayFormat()) + ';From\n'
        elif(Page1.Combobox_TimeType.currentText() == 'Time'):
            stringEXE = stringEXE + ' -a "' + str(Page4.ImpoFromTime.value()) + '"'
            stringLog = stringLog + str(Page4.ImpoFromTime.value()) + ';From\n'
        # To  [STRING] -b
        if(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'):
            stringEXE = stringEXE + ' -b "' + Page4.ImpoToDateTime.dateTime().toString(Page4.ImpoFromDateTime.displayFormat()) + '"'
            stringLog = stringLog + Page4.ImpoToDateTime.dateTime().toString(Page4.ImpoFromDateTime.displayFormat()) + ';To\n'
        elif(Page1.Combobox_TimeType.currentText() == 'Time'):
            stringEXE = stringEXE + ' -b "' + str(Page4.ImpoToTime.value()) + '"'
            stringLog = stringLog + str(Page4.ImpoToTime.value()) + ';To\n'
        # Update [BOOLEAN] -u
        if Page1.Flag_Update:
            stringEXE = stringEXE + ' -u True'
            stringLog = stringLog + 'True;FlagUpdate\n'
        else:
            stringLog = stringLog + 'False;FlagUpdate\n'
        # FlagHeader [BOOLEAN] -g
        if Page1.Flag_TimeSerie == PQW.QMessageBox.Yes:
            stringEXE = stringEXE + ' -g True'
            stringLog = stringLog + 'True;FlagTimeSerie\n'
        else:
            stringEXE = stringEXE + ' -g False'
            stringLog = stringLog + 'False;FlagTimeSerie\n'
        # Page1.Flag_Header
        if Page1.Flag_Header == PQW.QMessageBox.Yes:
            stringEXE = stringEXE + ' -l True'
            stringLog = stringLog + 'True;FlagHeader'
        else:
            stringEXE = stringEXE + ' -l False'
            stringLog = stringLog + 'False;FlagHeader'
        #
        FileDel = glob.glob('../temp/*.*')
        for File in FileDel:
            os.remove(File)
        # Move Datafile
        # copy('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz','../temp/clean_old.pkz')
        # copy('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/DataImport.log','../temp/DataImport_old.log')
        # copy('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/miss.pkz','../temp/miss_old.pkz')
        # Call external program
        print(stringEXE)
        os.system(stringEXE)
        # Check Run
        HandleLog = open('../temp/DataImport.log')
        Check = HandleLog.readline().replace('\n','')
        HandleLog.close()
        #
        if Check == 'No Error':
            # Create the folders
            ProbeFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()
            if not os.path.exists(ProbeFolder):
                os.makedirs(ProbeFolder)
            # Create Data Folder
            DataFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data'
            if not os.path.exists(DataFolder):
                os.makedirs(DataFolder)
            # Create FFT Folder
            FFTFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/fft'
            if not os.path.exists(FFTFolder):
                os.makedirs(FFTFolder)
            # Create SPdata Folder
            SPdataFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/SPdata'
            if not os.path.exists(SPdataFolder):
                os.makedirs(SPdataFolder)
            # Create PEdata Folder
            PEdataFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/PEdata'
            if not os.path.exists(PEdataFolder):
                os.makedirs(PEdataFolder)
            # Create Seepage Folder
            BredehofetFolder = '../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/Bredehofet'
            if not os.path.exists(BredehofetFolder):
                os.makedirs(BredehofetFolder)
            # Update probes.ini
            if Page1.Flag_Update:
                pass
                
            else:
                HandleProbe = open('../projects/'+VAR.GetActiveProject(VAR)+'/probes.ini','r')
                Rows = HandleProbe.readlines()
                HandleProbe.close()
                Rows.append(Page1.Combobox_ProbName.currentText())
                HandleProbe = open('../projects/'+VAR.GetActiveProject(VAR)+'/probes.ini','w')
                for item in Rows:
                    HandleProbe.write(item)
                HandleProbe.write('\n')
                HandleProbe.close()
            # Move the data
            os.replace('../temp/probe.ini','../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/probe.ini')
            os.replace('../temp/clean.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/clean.pkz')
            os.replace('../temp/miss.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/miss.pkz')
            os.replace('../temp/DataImport.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/DataImport.log')
            # Files = glob.glob('../temp/*.*')
            # for File in Files:
            #     os.replace(File,'../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/'+File.split('\\')[-1])
            # # Probe Log
            # HandleProbeLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/probe.ini','w')
            # HandleProbeLog.write(stringLog)
            # HandleProbeLog.close()
            #
            VAR.SetActiveProbe(VAR,Page1.Combobox_ProbName.currentText())
            #
            if Page1.Flag_Update:
                pass
            else:
                ListProbes = VAR.GetProbesList(VAR)
                ListProbes.append(Page1.Combobox_ProbName.currentText())
                VAR.SetProbesList(VAR,ListProbes)
            #
            (VAR.GetTabProjProb(VAR)).Update(4)
            (VAR.GetTabSignProc(VAR)).Update(4)
            (VAR.GetTabParEst(VAR)).Update(4)
            (VAR.GetTabSignProc(VAR)).Update(4)
            (VAR.GetTabBrede(VAR)).Update(4)
            #
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Import Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        else:
            PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        #
        return
#%%
'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
#
        Page1.Flag_Update = False
# Create grid layot for the window
        Layout_Page1 = PQW.QGridLayout()
# Probe name
        Label_FileName = PQW.QLabel('Probe name:')
        Label_FileName.setFixedWidth(60)
        Page1.Combobox_ProbName = PQW.QComboBox() # Combobox probe name
        Page1.Combobox_ProbName.setEditable(True)
        Page1.Combobox_ProbName.addItem('')
        for item in VAR.GetProbesList(VAR): # Add elements to the combobox
            HandleLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+item+'/probe.ini')
            # HandleLog.readline()
            # HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            RTStemp = HandleLog.readline().split(';')[0] #
            HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            HandleLog.readline()
            FlagTS = HandleLog.readline().split(';')[0] #
            HandleLog.readline()
            HandleLog.close()
            if RTStemp == 'False' or FlagTS == 'True':
                Page1.Combobox_ProbName.addItem(item)
        Page1.Combobox_ProbName.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_ProbName.setFixedWidth(135)
        Page1.Combobox_ProbName.currentIndexChanged.connect(self.on_Combobox_ProbName_change) # ComboBox event change item
# Groupbox DataFile
        self.GroupBox_DataFile = PQW.QGroupBox('File Data:')
        self.HBoxDataFile = PQW.QHBoxLayout() # Create the Layout for the Groupbox DataFile
        Page1.Data_File = PQW.QLineEdit() # Data File  field
        Page1.Data_File.setEnabled(False) # Setted as not modificable (Feature)
        Page1.Data_File.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Button_Select_File = PQW.QPushButton('Select') # Button select data file
        Button_Select_File.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Button_Select_File.clicked.connect(self.on_Button_Select_File_clicked) # Button event Click on
        self.HBoxDataFile.addWidget(Page1.Data_File) # Add element to the Layout
        self.HBoxDataFile.addWidget(Button_Select_File) # Add element to the Layout
        self.GroupBox_DataFile.setLayout(self.HBoxDataFile) # Add the Layout to the Groupbox Probes
        self.GroupBox_DataFile.setFixedWidth(200)
# Groupbox Time
        self.GroupBox_Time = PQW.QGroupBox('Time:')
        self.VBoxTime = PQW.QVBoxLayout() # Create the Layout for the Groupbox DataFile
        # Time serie
        self.HBoxTimeSerie = PQW.QHBoxLayout() # Layout
        Label_TimeSerie = PQW.QLabel('Time serie:') # Label
        Page1.Combobox_TimeSerie = PQW.QComboBox() # Combobox TimeSerie
        Page1.Combobox_TimeSerie.setEnabled(False) # disable the combobox
        Page1.Combobox_TimeSerie.currentIndexChanged.connect(self.on_Combobox_TimeSerie_change) # ComboBox event change item
        self.HBoxTimeSerie.addWidget(Label_TimeSerie) # Add Element to the Layout
        self.HBoxTimeSerie.addWidget(Page1.Combobox_TimeSerie) # Add Element to the Layout
        # Time Format
        self.HBoxTimeType = PQW.QHBoxLayout() # Layout
        Label_TimeType = PQW.QLabel('Time Format') # Label
        Page1.Combobox_TimeType = PQW.QComboBox() # Combobox TimeType
        for item in VAR.GetTimeserieTypeString(VAR): # Add elements to the combobox
            Page1.Combobox_TimeType.addItem(item)
        Page1.Combobox_TimeType.currentIndexChanged.connect(self.on_Combobox_TimeType_change) # ComboBox event change item
        Page1.Combobox_TimeType.setEnabled(False) # disable the combobox
        self.HBoxTimeType.addWidget(Label_TimeType) # Add Element to the Layout
        self.HBoxTimeType.addWidget(Page1.Combobox_TimeType) # Add Element to the Layout
        # Sample Rate
        self.HBoxSampleRate = PQW.QHBoxLayout() # Layout
        Page1.RadioBot_SampleRate = PQW.QRadioButton('Sample rate  [s]   ') # Radiobutton SampleRate
        Page1.RadioBot_SampleRate.setEnabled(False) # disable the radiobutton
        Page1.RadioBot_SampleRate.toggled.connect(self.on_RadioBot_SampleRate_Clicked) # Radiobutton event click
        Page1.SampleRate = PQW.QLineEdit() # Text SampleRate
        Page1.SampleRate.setEnabled(False) # disable SampleRate field
        Page1.SampleRate.textChanged.connect(self.on_SampleRate_Change)
        self.HBoxSampleRate.addWidget(Page1.RadioBot_SampleRate) # Add Element to the Layout
        self.HBoxSampleRate.addWidget(self.SampleRate) # Add Element to the Layout
        # Sample Frequency
        self.HBoxSampleFreq = PQW.QHBoxLayout() # Layout
        Page1.RadioBot_SampleFreq = PQW.QRadioButton('Sample frequency  [Hz]') # Radiobutton SampleFreq
        Page1.RadioBot_SampleFreq.setEnabled(False) # disable the radiobutton
        Page1.RadioBot_SampleFreq.toggled.connect(self.on_RadioBot_SampleFreq_Clicked) # Radiobutton event click
        Page1.SampleFreq = PQW.QLineEdit() # Text SampleFrequency
        Page1.SampleFreq.textChanged.connect(self.on_SampleFreq_Change)
        Page1.SampleFreq.setEnabled(False) # disable SampleFreq field
        self.HBoxSampleFreq.addWidget(Page1.RadioBot_SampleFreq) # Add Element to the Layout
        self.HBoxSampleFreq.addWidget(Page1.SampleFreq)
        self.VBoxTime.addLayout(self.HBoxTimeSerie) # Add element to the Layout
        self.VBoxTime.addLayout(self.HBoxTimeType) # Add Element to the Layout
        self.VBoxTime.addLayout(self.HBoxSampleRate) # Add Element to the Layout
        self.VBoxTime.addLayout(self.HBoxSampleFreq) # Add Element to the Layout
        self.GroupBox_Time.setLayout(self.VBoxTime) # Add the Layout to the Groupbox Probes
        self.GroupBox_Time.setFixedWidth(200)
# Groupbox Options
        self.GroupBox_Options = PQW.QGroupBox('Options:')
        self.VBoxOpttions = PQW.QVBoxLayout() # Create the Layout for the Groupbox DataFile
        Page1.CheckIMD = PQW.QCheckBox('Interpolate missing data') # Checkbox Interpolate missing data
        Page1.CheckIMD.setEnabled(False) # disable the checkbox
        Page1.CheckRTS = PQW.QCheckBox('Rebuilt time serie with\ncostant sample rate/Frequency') # Checkbox Rebuil Time serie
        Page1.CheckRTS.setEnabled(False) # disable the checkbox
        self.VBoxOpttions.addWidget(Page1.CheckIMD) # Add element to the Layout
        self.VBoxOpttions.addWidget(Page1.CheckRTS) # Add element to the Layout
        self.GroupBox_Options.setLayout(self.VBoxOpttions) # Add the Layout to the Groupbox Probes
        self.GroupBox_Options.setFixedWidth(200)
# DataChart
        Page1.Chart_Fig = plt.figure()
        Page1.Canvas = FigureCanvas(Page1.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page1.Canvas, self)
        Page1.Canvas.draw()
# Insert elements in the grid
        Layout_Page1.addWidget(Label_FileName, 0, 0, 1, 1)
        Layout_Page1.addWidget(self.Combobox_ProbName, 0, 1, 1, 1)
        Layout_Page1.addWidget(self.GroupBox_DataFile, 1, 0, 1, 2)
        Layout_Page1.addWidget(self.GroupBox_Time, 2, 0, 1, 2)
        Layout_Page1.addWidget(self.GroupBox_Options, 3, 0, 1, 2)
        Layout_Page1.addWidget(self.Toolbar,0,2,1,8)
        Layout_Page1.addWidget(Page1.Canvas,1,2,9,8)
# Show layout
        self.setLayout(Layout_Page1)
        #
        # Page1.UpdateChart(self) # Call update charts
#
    def on_SampleRate_Change(self):
        print('Page1 - on_SampleRate_Change')
        # Update fields SampleRate and SampleFreq
        try:
            if(float(Page1.SampleRate.text()) == 0.0):
                Page1.SampleFreq.setText('Infinity')
            elif(float(Page1.SampleRate.text()) < 0.0):
                Page1.SampleFreq.setText('NaN')
            else:
                Page1.SampleFreq.setText(str(1/float(Page1.SampleRate.text())))
        except:
            Page1.SampleRate.setText('NaN')
            Page1.SampleFreq.setText('NaN')
        #
        Page1.UpdateChart(self) # Call update charts
        return

    def on_SampleFreq_Change(self):
        print('Page1 - on_SampleFreq_Change')
        # Update fields SampleRate and SampleFreq
        try:
            if(float(Page1.SampleFreq.text()) == 0.0):
                Page1.SampleRate.setText('Infinity')
            elif(float(Page1.SampleFreq.text()) < 0.0):
                Page1.SampleRate.setText('NaN')
            else:
                Page1.SampleRate.setText(str(1/float(Page1.SampleFreq.text())))
        except:
            Page1.SampleRate.setText('NaN')
            Page1.SampleFreq.setText('NaN')
        #
        Page1.UpdateChart(self) # Call update charts
        return
#
    def UpdateChart(self):
        print('Page1 - Update Chart')
        # Reset chart
        Page1.Chart_Fig.clear()
        Page1.ax = Page1.Chart_Fig.add_subplot(111)
        #
        FlagLegend = False
        # Check if chart color palette exist or not
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        # Update the chart
        if Page1.Flag_Update: # Update the data of probe #! To finish
            pass
        else: # Create a new probe
            if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes):
                if(Page1.Combobox_TimeType.currentText() == 'Time'): # Timeserie is timestamp format
                    TimeStamp = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].to_numpy()
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor != Page1.Combobox_TimeSerie.currentText():
                            if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                try:
                                    plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                    Colors.append(plot[0].get_color())
                                    FlagLegend = True
                                except:
                                    pass
                            else: # Chart colors setted
                                try:
                                    plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                    FlagLegend = True
                                except:
                                    pass
                elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'): # Timeserie is datetime format
                    TimeStamp = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor != Page1.Combobox_TimeSerie.currentText():
                            if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                try:
                                    plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                    Colors.append(plot[0].get_color())
                                    FlagLegend = True
                                except:
                                    pass
                            else: # Chart colors setted
                                try:
                                    plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                    FlagLegend = True
                                except:
                                    pass




            else:
                TimeStamp = np.array([i*float(Page1.SampleRate.text()) for i in range(0,Page1.DataNow.shape[0])])
                #
                for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                    if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                        try:
                            plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                            Colors.append(plot[0].get_color())
                            FlagLegend = True
                        except:
                            pass
                    else: # Chart colors setted
                        try:
                            plot = Page1.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i]) # Plot
                            FlagLegend = True
                        except:
                            pass

            # if hasattr(Page1, 'DataNow'): # Data loaded from file
            #     if(Page1.Combobox_TimeType.currentText() == 'Time'): # Timeserie is timestamp format
            #         if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes): # Timeserie not exist in the data loaded
            #             TimeStamp = pd.to_numeric(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
            #         else:  # Timeserie exist in the data loaded
            #             TimeStamp = pd.Series([i*float(Page1.SampleRate.text()) for i in range(0,Page1.DataNow.shape[0])]) # Create the timeserie
            #         #
            #         for i, Sensor in enumerate(Page1.SensorsNow):
            #             if(Sensor == Page1.Combobox_TimeSerie.currentText()): # Not to plot the timeserie if exist in the data loaded
            #                 pass
            #             else:
            #                 if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
            #                     try:
            #                         plot = Page1.ax.plot(TimeStamp, pd.to_numeric(Page1.DataNow[Sensor]), '-', label = str(Sensor)) # Plot
            #                         Colors.append(plot[0].get_color())
            #                         FlagLegend = True
            #                     except:
            #                         pass
            #                 else: # Chart colors setted
            #                     try:
            #                         plot = Page1.ax.plot(TimeStamp, pd.to_numeric(Page1.DataNow[Sensor]), '-', label = str(Sensor), color=Colors[i-1]) # Plot
            #                         FlagLegend = True
            #                     except:
            #                         pass
            #     elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'): # Timeserie is datetime format
            #         TimeStamp = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
            #         for i, Sensor in enumerate(Page1.SensorsNow):
            #             if(Sensor == Page1.Combobox_TimeSerie.currentText()):
            #                 pass
            #             else:
            #                 if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
            #                     try:
            #                         plot = Page1.ax.plot(TimeStamp, pd.to_numeric(Page1.DataNow[Sensor]), '-', label = str(Sensor)) # Plot
            #                         Colors.append(plot[0].get_color())
            #                         FlagLegend = True
            #                     except:
            #                         pass
            #                 else: # Chart colors  setted
            #                     try:
            #                         plot = Page1.ax.plot(TimeStamp, pd.to_numeric(Page1.DataNow[Sensor]), '-', label = str(Sensor), color=Colors[i-1]) # Plot
            #                         FlagLegend = True
            #                     except:
            #                         pass
            #     else:
            #         pass
            # else: # Data not loaded from file
            #     pass
        #
        if(VAR.GetChartColors(VAR) is None and len(Colors) != 0):
            VAR.SetChartColors(VAR, Colors) # Store the colors use for the chart
        #
        if FlagLegend:
            Page1.ax.legend(loc=9, ncol=4) # Add legend to the chart
        #
        Page1.ax.grid(True, which='both', axis='both', linestyle='--') # Add grid to the chart
        Page1.Canvas.draw() # Redraw the chart
        return
# #%%
    def on_Combobox_ProbName_change(self):
        print('Page1 - on_Combobox_ProbName_change')
        # Check if data update
        if os.path.exists('../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/clean.pkz'):
            Page1.Flag_Update = True
            # Load old data
            Page1.df_DataOld = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/data/clean.pkz', compression='zip')
            # load Probe config probe.ini and update Page1
            HandleProbeLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+Page1.Combobox_ProbName.currentText()+'/probe.ini','r')
            Old_LastDatafile = HandleProbeLog.readline().split(';')[0]
            Old_TimeSerieName = HandleProbeLog.readline().split(';')[0]
            Old_TimeType = HandleProbeLog.readline().split(';')[0]
            Old_SampleRate = HandleProbeLog.readline().split(';')[0]
            Old_IMD = HandleProbeLog.readline().split(';')[0]
            Old_RTS = HandleProbeLog.readline().split(';')[0]
            Old_SensorsName = HandleProbeLog.readline().split(';')[0]
            Old_SensorsHeight = HandleProbeLog.readline().split(';')[0]
            Old_From = HandleProbeLog.readline().split(';')[0]
            Old_To = HandleProbeLog.readline().split(';')[0]
            Old_FlagUpdate = HandleProbeLog.readline().split(';')[0]
            Old_FlagTimeSerie = HandleProbeLog.readline().split(';')[0]
            Old_FlagHeader = HandleProbeLog.readline().split(';')[0]
            HandleProbeLog.close()


            # HandleProbeLog.readline()# D:/Lavoro/PhD/iFlow/Data/DateTime_Header.csv;LastDatafile
            # TimeSerieName
            Page1.Combobox_TimeSerie.currentIndexChanged.disconnect()
            Page1.Combobox_TimeSerie.addItem(Old_TimeSerieName)
            Page1.Combobox_TimeSerie.setEnabled(False) # disable the combobox
            Page1.Combobox_TimeSerie.currentIndexChanged.connect(self.on_Combobox_TimeSerie_change) # ComboBox event change item
            # # TimeType
            Page1.Combobox_TimeType.currentIndexChanged.disconnect()
            Page1.Combobox_TimeType.setCurrentText(Old_TimeType)
            Page1.Combobox_TimeType.setEnabled(False) # disable the combobox
            Page1.Combobox_TimeType.currentIndexChanged.connect(self.on_Combobox_TimeType_change) # ComboBox event change item
            # SampleRate and SampleFreq
            Page1.RadioBot_SampleRate.toggled.disconnect()
            Page1.SampleRate.textChanged.disconnect()
            Page1.RadioBot_SampleFreq.toggled.disconnect()
            Page1.SampleFreq.textChanged.disconnect()
            Page1.RadioBot_SampleRate.setEnabled(False) # disable the radiobutton
            Page1.RadioBot_SampleFreq.setEnabled(False) # disable the radiobutton
            # TempText = (HandleProbeLog.readline().split(';'))[0]
            Page1.SampleRate.setText(Old_SampleRate)
            Page1.SampleFreq.setText(str(1.0/float(Old_SampleRate)))
            Page1.RadioBot_SampleRate.toggled.connect(self.on_RadioBot_SampleRate_Clicked) # Radiobutton event click
            Page1.SampleRate.textChanged.connect(self.on_SampleRate_Change)
            Page1.RadioBot_SampleFreq.toggled.connect(self.on_RadioBot_SampleFreq_Clicked) # Radiobutton event click
            Page1.SampleFreq.textChanged.connect(self.on_SampleFreq_Change)
            # IMD
            if Old_IMD == 'True':
                Page1.CheckIMD.setEnabled(True) # enable the checkbox
            else:
                Page1.CheckIMD.setEnabled(False) # disable the checkbox
            # RTS
            if Old_RTS == 'True':
                Page1.CheckRTS.setEnabled(True) # enable the checkbox
            else:
                Page1.CheckRTS.setEnabled(False) # disable the checkbox
            # SensorsName
            Page1.SensorsNow = Old_SensorsName.split(',')
            TempList = Old_SensorsHeight.split(',')
            # #
            Page2.List_Sensor_File.disconnect()
            Page2.List_Sensor_Impo.disconnect()
            Page2.Button_Add_All.disconnect()
            Page2.Button_Remove_All.clicked.disconnect()
            Page3.Button_Imp_Geo.clicked.disconnect()
            Page3.Button_Gen_Geo.clicked.disconnect()
            # #
            Page2.List_Sensor_File.clear()
            Page2.List_Sensor_Impo.clear()
            Page3.Table_Height.setRowCount(0)
            Page3.Table_Height.setRowCount(len(Page1.SensorsNow))
            Page3.Table_Height.setColumnCount(2)
            Page3.Table_Height.setHorizontalHeaderLabels(['Sensor', 'Height (m asl)'])
            # #
            for i,Sensor in enumerate(Page1.SensorsNow):
                Page2.List_Sensor_Impo.addItem(Sensor)
                item = PQW.QTableWidgetItem(Sensor)
                item2 = PQW.QTableWidgetItem(TempList[i])
                item.setFlags(PQC.Qt.ItemIsEnabled)
                item2.setFlags(PQC.Qt.ItemIsEnabled)
                Page3.Table_Height.setItem(i,0, item)
                Page3.Table_Height.setItem(i,1, item2)
            #
            Page2.List_Sensor_File.setEnabled(False)
            Page2.List_Sensor_Impo.setEnabled(False)
            Page2.Button_Add_All.setEnabled(False)
            Page2.Button_Remove_All.setEnabled(False)
            Page3.Button_Imp_Geo.setEnabled(False)
            Page3.Button_Gen_Geo.setEnabled(False)
            #
            # Page2.List_Sensor_File.itemActivated.connect(Page2.on_List_Sensor_File_event)
            # Page2.List_Sensor_Impo.itemActivated.connect(Page2.on_List_Sensor_Impo_event)
            # Page2.Button_Add_All.clicked.connect(Page2.on_Button_Add_All_clicked)
            # Page2.Button_Remove_All.clicked.connect(Page2.on_Button_Remove_All_clicked)
            # Page3.Button_Imp_Geo.clicked.connect(Page3.on_Button_Imp_Geo_clicked)
            # Page3.Button_Gen_Geo.clicked.connect(Page3.on_Button_Gen_Geo_clicked)
            # #
            # HandleProbeLog.readline() # From
            # HandleProbeLog.readline() # To
            # HandleProbeLog.readline() # FlagUpdate
            # if (HandleProbeLog.readline().split(';'))[0] == 'True':
            #     Page1.Flag_TimeSerie = PQW.QMessageBox.Yes
                
            # else:
            #     Page1.Flag_TimeSerie = PQW.QMessageBox.No
            # if (HandleProbeLog.readline().split(';'))[0] == 'True':
            #     Page1.Flag_Header = PQW.QMessageBox.Yes
            # else:
            #     Page1.Flag_Header = PQW.QMessageBox.No
            # HandleProbeLog.close()
        else:
            Page1.Flag_Update = False
        #
        Page1.UpdateChart(self) # Call update charts
        #
        return
        
    def on_Combobox_TimeSerie_change(self):
        print('Page1 - on_Combobox_TimeSerie_change')
        # Disconnect events
        Page1.Combobox_TimeType.currentIndexChanged.disconnect() # ComboBox disconnect event change item
        Page1.SampleRate.textChanged.disconnect() # Filed disconnect change text
        Page1.SampleFreq.textChanged.disconnect() # Filed disconnect change text
        # Reset
        Page1.Combobox_TimeType.setCurrentText('') # TimeType Combobox
        Page1.SampleRate.setText('') # SampleRate field
        Page1.SampleFreq.setText('') # SampleFreq field
        #
        Page1.SampleRate.setEnabled(False) # Disable SampleRate field
        Page1.SampleFreq.setEnabled(False) # Disable SampleFrea field
        Page1.RadioBot_SampleRate.setEnabled(False) # Disable RadioButton SampleRate
        Page1.RadioBot_SampleFreq.setEnabled(False) # Disable RadioButton SampleFreq
        # Reconnect events
        Page1.Combobox_TimeType.currentIndexChanged.connect(self.on_Combobox_TimeType_change) # ComboBox event change item
        Page1.SampleRate.textChanged.connect(self.on_SampleRate_Change) # Field SampleRate event changed text
        Page1.SampleFreq.textChanged.connect(self.on_SampleFreq_Change) # Field SampleFreq event changed text
        #
        Page1.UpdateChart(self) # Call update charts
        return
        
    def on_Combobox_TimeType_change(self):
        print('Page1 - on_Combobox_TimeType_change')
        # Disconect events
        Page1.SampleRate.textChanged.disconnect() # Text field event change disconnect
        Page1.SampleFreq.textChanged.disconnect() # Text field event change disconnect
        Page1.RadioBot_SampleRate.toggled.disconnect() # Radiobutton event click disconnect
        Page1.Combobox_TimeType.currentIndexChanged.disconnect() # ComboBox disconnect event change item
        # Check if the format of timeserie data is congruent with the format choosen by the user
        if(Page1.Combobox_TimeType.currentText() == 'Time'):
            try:
                datetime_test = float(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[0]) # Check the type of time
                # Calculate dt of the time serie
                DatetimeNow = pd.to_numeric(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
                data_dt = DatetimeNow - DatetimeNow.shift()
                # Remove duplicate from dt previously calculated
                data_dt_unique = data_dt[1:].drop_duplicates().dropna()
                list_temp = data_dt_unique.dropna().to_numpy() # Convert to numpy array
                list_temp = np.where(list_temp <= 0.0, np.nan, list_temp) # Remove negative dt
                # Calculate the occurance of every unique dt
                list_temp_occur = np.zeros(shape=list_temp.shape)
                for i,value in enumerate(list_temp):
                    list_temp_occur[i] = np.count_nonzero(data_dt[1:] == value)
                # In the case of multiple dt check which type of hole is
                Page1.FlagHole = 0
                if(data_dt_unique.size > 1):
                    Page1.FlagHole = 1
                    for value in data_dt_unique:
                        if((value/data_dt_unique.min()).is_integer()):
                            pass
                        else:
                            Page1.FlagHole = 2
                # In case of multiple dt popup a message for the user
                if(Page1.FlagHole == 1):
                    PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Found multiple dt compatible\nwith holes in the time serie.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                elif(Page1.FlagHole == 2):
                    PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Found multiple dt not compatible\nwith holes in the time serie.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                #
                Page1.RadioBot_SampleRate.setEnabled(True) # Enable SampleRate radiobutton
                Page1.RadioBot_SampleFreq.setEnabled(True) # Enable SampleFreq radiobutton
                Page1.SampleRate.setEnabled(True) # Enable SampleRate field
                Page1.SampleFreq.setEnabled(False) # Disable SampleFreq field
                # Check that the fields SampleRate and SampleFreq is a number
                try:
                    Page1.SampleRate.setText(str(list_temp[np.argmax(list_temp_occur)]))
                except:
                    Page1.SampleRate.setText('NaN')
                try:
                    Page1.SampleFreq.setText(str(np.format_float_scientific(1.0 / list_temp[np.argmax(list_temp_occur)])))
                except:
                    Page1.SampleFreq.setText('NaN')
                #
                Page1.RadioBot_SampleRate.setChecked(True) # Set Checked Sample Rate radiobutton
            except:
                # Popup massage for user that the timeserie data don't match the timetype choosen
                PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Time serie\'s values incompatible with Time serie\'s type choose.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                Page1.Combobox_TimeType.setCurrentText('') # Reset the TimeType combobox
                Page1.RadioBot_SampleRate.setEnabled(False) # Disable SampleRate radiobutton
                Page1.RadioBot_SampleFreq.setEnabled(False) # Disable SampleFreq radiobutton
                Page1.SampleRate.setEnabled(False) # Disable SampleRate field
                Page1.SampleFreq.setEnabled(False) # Disable SampleFreq field
                Page1.SampleRate.setText('') # Disable SampleRate field
                Page1.SampleFreq.setText('') # Disable SampleFreq field
        elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'):
            try:
                datetime_test = datetime.datetime.strptime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].iloc[0],'%Y-%m-%d %H:%M:%S') # Check the type of time
                # Calculate dt of the time serie
                DatetimeNow = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()]) #!
                data_dt = DatetimeNow - DatetimeNow.shift()
                # Remove duplicate from dt previously calculated
                data_dt_unique = data_dt[1:].drop_duplicates().dt.total_seconds().dropna()
                list_temp = data_dt_unique.dropna().to_numpy() # Convert to numpy array
                list_temp = np.where(list_temp <= 0.0, np.nan, list_temp) # Remove negative dt
                # Calculate the occurance of every unique dt
                list_temp_occur = np.zeros(shape=list_temp.shape)
                for i,value in enumerate(list_temp):
                    list_temp_occur[i] = np.count_nonzero(data_dt[1:].dt.total_seconds() == value)
                # In the case of multiple dt check which type of hole is
                Page1.FlagHole = 0
                if(data_dt_unique.size > 1):
                    Page1.FlagHole = 1
                    for value in data_dt_unique:
                        if((value/data_dt_unique.min()).is_integer()):
                            pass
                        else:
                            Page1.FlagHole = 2
                # In case of multiple dt popup a message for the user
                if(Page1.FlagHole == 1):
                    PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Found multiple dt compatible\nwith holes in the time serie.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                elif(Page1.FlagHole == 2):
                    PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Found multiple dt not compatible\nwith holes in the time serie.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                #
                Page1.RadioBot_SampleRate.setEnabled(True) # Enable SampleRate radiobutton
                Page1.RadioBot_SampleFreq.setEnabled(True) # Enable SampleFreq radiobutton
                Page1.SampleRate.setEnabled(True) # Enable SampleRate field
                Page1.SampleFreq.setEnabled(False) # Disable SampleFreq field
                # Check that the fields SampleRate and SampleFreq is a number
                try:
                    Page1.SampleRate.setText(str(list_temp[np.argmax(list_temp_occur)]))
                except:
                    Page1.SampleRate.setText('NaN')
                try:
                    Page1.SampleFreq.setText(str(np.format_float_scientific(1.0 / list_temp[np.argmax(list_temp_occur)])))
                except:
                    Page1.SampleFreq.setText('NaN')
                #
                Page1.RadioBot_SampleRate.setChecked(True) # Set Checked Sample Rate radiobutton
            except:
                # Popup massage for user that the timeserie data don't match the timetype choosen
                PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Time serie\'s values incompatible with Time serie\'s type choose.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                Page1.Combobox_TimeType.setCurrentText('') # Reset the TimeType combobox
                Page1.RadioBot_SampleRate.setEnabled(False) # Disable SampleRate radiobutton
                Page1.RadioBot_SampleFreq.setEnabled(False) # Disable SampleFreq radiobutton
                Page1.SampleRate.setEnabled(False) # Disable SampleRate field
                Page1.SampleFreq.setEnabled(False) # Disable SampleFreq field
                Page1.SampleRate.setText('') # Reset SampleRate field
                Page1.SampleFreq.setText('') # Reset SampleFreq field
        else:
            print('No choice')
        # Reconnect events
        Page1.SampleRate.textChanged.connect(self.on_SampleRate_Change) # Text field event change
        Page1.SampleFreq.textChanged.connect(self.on_SampleFreq_Change) # Text field event change
        Page1.RadioBot_SampleRate.toggled.connect(self.on_RadioBot_SampleRate_Clicked) # Radiobutton event click
        Page1.Combobox_TimeType.currentIndexChanged.connect(self.on_Combobox_TimeType_change) # ComboBox event change item
        #
        Page1.UpdateChart(self) # Call update charts
        return

    def on_Button_Select_File_clicked(self):
        print('Page1 - on_Button_Select_File_clicked')
        # Disconect events
        Page1.Combobox_TimeSerie.currentIndexChanged.disconnect() # ComboBox disconnect event change item
        Page1.Combobox_TimeType.currentIndexChanged.disconnect() # ComboBox disconnect event change item
        Page1.RadioBot_SampleRate.toggled.disconnect() # Radiobutton event click disconnect
        Page1.SampleRate.textChanged.disconnect() # SampleRate field text change event disconnect
        Page1.SampleFreq.textChanged.disconnect() # SampleFreq field text change event disconnect
        # Sensor names are in the first row?
        if Page1.Flag_Update: #! To finish
            pass#Page1.Flag_Header = PQW.QMessageBox.No #TODO
        else:
            Page1.Flag_Header = PQW.QMessageBox.question(self, VAR.GetSoftwareName(VAR)+' message', 'Are the sensor name in the first row of the datafile?', PQW.QMessageBox.Yes|PQW.QMessageBox.No, PQW.QMessageBox.Yes)
        # Time serie is present in the file?
        if Page1.Flag_Update: #! To finish
            pass#Page1.Flag_TimeSerie = PQW.QMessageBox.No #TODO
        else:
            Page1.Flag_TimeSerie = PQW.QMessageBox.question(self, VAR.GetSoftwareName(VAR)+' message', 'Are present a time serie in the datafile?', PQW.QMessageBox.Yes|PQW.QMessageBox.No, PQW.QMessageBox.Yes)
        # Select the path of the datafile
        Options = PQW.QFileDialog.Options()
        Options |= PQW.QFileDialog.DontUseNativeDialog
        file_name, _ = PQW.QFileDialog.getOpenFileName(self, 'Select data file...', VAR.DefaultFolderFileDialog(VAR), 'CSV Files (*.csv);;All Files (*);;Text Files (*.txt)', options = Options)  
        #
        if file_name:
            Page1.Data_File.setText(file_name) # Update DataFile
            #
            if Page1.Flag_Update: #! To finish
                pass
                # if(Page1.Flag_Header == PQW.QMessageBox.Yes): # There is sensor's name in the datafile
                #     Page1.DataNow = pd.read_csv(file_name, error_bad_lines=False, index_col=False, dtype='unicode') # Load Data
                # else:  # There is not sensor's name in the datafile
                #     Page1.DataNow = pd.read_csv(file_name,header=None) # Load Data
                #     Page1.SensorsNow = []
                #     for i in range(0,Page1.DataNow.shape[1]):
                #         Page1.SensorsNow.append('Sensor'+str(i))
                #         Page1.Combobox_TimeSerie.addItem('Sensor'+str(i))
                #     Page1.DataNow.columns = Page1.SensorsNow
                # Page1.UpdateChart(self) # Call update charts
            else:
                # Reset fields SampleRate and SampleFreq
                Page1.SampleRate.setText('')
                Page1.SampleFreq.setText('')
                #
                if(Page1.Flag_Header == PQW.QMessageBox.Yes): # There is sensor's name in the datafile
                    Page1.DataNow = pd.read_csv(file_name)#, error_bad_lines=False, index_col=False, dtype='unicode') # Load Data
                    # # Page1.DataNow = pd.read_csv(file_name)
                    # # print(Page1.DataNow)
                    # Page1.SensorsNow = Page1.DataNow.columns.tolist() # Sensors name in datafile
                    # Update Combobox_TimeSerie with the name of the sensors
                    # Page1.Combobox_TimeSerie.clear()
                    # for item in Page1.DataNow.columns.tolist():
                    #     Page1.Combobox_TimeSerie.addItem(item)
                    #
                    if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes): # The data is marked with Time
                        Page1.Combobox_TimeSerie.clear()
                        for item in Page1.DataNow.columns.tolist():
                            Page1.Combobox_TimeSerie.addItem(item)
                        pass
                        Page1.Combobox_TimeSerie.setEnabled(True) # Set Enable TimeSerie combobox
                        Page1.Combobox_TimeType.setEnabled(True) # Set Enable TimeType combobox
                        Page1.SampleRate.setEnabled(False) # Disable Sample Rate field
                        Page1.SampleFreq.setEnabled(False) # Disable Frequency Rate field
                        Page1.RadioBot_SampleFreq.setEnabled(False) # Set Disable Sample Frequency radiobutton
                        Page1.RadioBot_SampleRate.setEnabled(False) # Set Disable Sample Rate radiobutton
                        # Reset Time type
                        Page1.Combobox_TimeType.setCurrentText('')
                        #
                        Page1.CheckIMD.setEnabled(True) # Enable IMD checkbutton
                        Page1.CheckRTS.setEnabled(True) # Enable RTS checkbutton
                        Page1.CheckIMD.setChecked(False) # Decheck IMD checkbutton
                        Page1.CheckRTS.setChecked(False) # Decheck RTS checkbutton
                    else: # The data is not marked with Time
                        pass
                        Page1.Combobox_TimeSerie.clear()
                        Page1.Combobox_TimeSerie.addItem('Time')
                        # Set Timetype to Time by default
                        Page1.Combobox_TimeType.setCurrentText('Time')
                        #
                        Page1.Combobox_TimeSerie.setEnabled(False) # Set Disable TimeSerie combobox
                        Page1.Combobox_TimeType.setEnabled(False) # Set Disable TimeType combobox
                        #
                        Page1.SampleRate.setEnabled(True) # Enable Sample Rate field
                        Page1.SampleFreq.setEnabled(False) # Disable Frequency Rate field
                        Page1.RadioBot_SampleFreq.setEnabled(True) # Set Enable Sample Frequency radiobutton
                        Page1.RadioBot_SampleRate.setEnabled(True) # Set Enable Sample Rate radiobutton
                        #
                        Page1.RadioBot_SampleRate.setChecked(True) # Set Checked Sample Rate radiobutton
                        #
                        Page1.CheckIMD.setEnabled(False) # Disable IMD checkbutton
                        Page1.CheckRTS.setEnabled(False) # Disable RTS checkbutton
                        Page1.CheckIMD.setChecked(False) # Decheck IMD checkbutton
                        Page1.CheckRTS.setChecked(True) # Check RTS checkbutton
                        #
                        Page1.SampleRate.setText('900')
                        Page1.SampleFreq.setText(str(np.format_float_scientific(1.0 / 900.0)))
                        #
                        Page1.UpdateChart(self) # Call update charts
                else:  # There is not sensor's name in the datafile
                    Page1.DataNow = pd.read_csv(file_name,header=None) # Load Data
                    # Update Combobox_TimeSerie
                    Page1.Combobox_TimeSerie.clear()
                    SensorsNow = []
                    #
                    # Page1.DataNow.columns = Page1.SensorsNow
                    #
                    if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes): # The data is marked with Time
                        for i in range(0,Page1.DataNow.shape[1]):
                            SensorsNow.append('Sensor'+str(i))
                            Page1.Combobox_TimeSerie.addItem('Sensor'+str(i))
                        Page1.DataNow.columns = SensorsNow
                        Page1.Combobox_TimeSerie.setEnabled(True) # Set Enable TimeSerie combobox
                        Page1.Combobox_TimeType.setEnabled(True) # Set Enable TimeType combobox
                        Page1.SampleRate.setEnabled(False) # Disable Sample Rate field
                        Page1.SampleFreq.setEnabled(False) # Disable Sample Frequency field
                        Page1.RadioBot_SampleFreq.setEnabled(False) # Set Disable Sample Frequency radiobutton
                        Page1.RadioBot_SampleRate.setEnabled(False) # Set Enable Sample Rate radiobutton
                        # Reset Time type
                        Page1.Combobox_TimeType.setCurrentText('')
                        #
                        Page1.CheckIMD.setEnabled(True) # Enable IMD checkbutton
                        Page1.CheckRTS.setEnabled(True) # Enable RTS checkbutton
                        Page1.CheckIMD.setChecked(False) # Decheck IMD checkbutton
                        Page1.CheckRTS.setChecked(False) # Decheck RTS checkbutton
                    else: # The data is not marked with Time
                        for i in range(0,Page1.DataNow.shape[1]):
                            SensorsNow.append('Sensor'+str(i))
                        Page1.DataNow.columns = SensorsNow
                        # Update Combobox_TimeSerie
                        Page1.Combobox_TimeSerie.addItem('Time')
                        Page1.Combobox_TimeSerie.setCurrentText('Time')
                        # Update Combobox_TimeType
                        Page1.Combobox_TimeType.setCurrentText('Time')
                        Page1.Combobox_TimeSerie.setEnabled(False) # Disable TimeSerie combobox
                        Page1.Combobox_TimeType.setEnabled(False) # Disable TimeType combobox
                        #
                        Page1.SampleRate.setEnabled(True) # Enable Sample Rate field
                        Page1.SampleFreq.setEnabled(False) # Disable Frequency Rate field
                        Page1.RadioBot_SampleFreq.setEnabled(True) # Set Enable Sample Frequency radiobutton
                        Page1.RadioBot_SampleRate.setChecked(True)
                        Page1.RadioBot_SampleRate.setEnabled(True) # Set Enable Sample Frequency radiobutton
                        #
                        Page1.CheckIMD.setEnabled(False) # Disable IMD checkbutton
                        Page1.CheckRTS.setEnabled(False) # Disable RTS checkbutton
                        Page1.CheckIMD.setChecked(False) # Decheck IMD checkbutton
                        Page1.CheckRTS.setChecked(True) # Check RTS checkbutton
                        #
                        Page1.SampleRate.setText('900')
                        Page1.SampleFreq.setText(str(np.format_float_scientific(1.0 / 900.0)))
                        #
                        Page1.UpdateChart(self) # Call update charts
        # Reconnect events
        Page1.Combobox_TimeSerie.currentIndexChanged.connect(self.on_Combobox_TimeSerie_change) # ComboBox event change item
        Page1.Combobox_TimeType.currentIndexChanged.connect(self.on_Combobox_TimeType_change) # ComboBox event change item
        Page1.RadioBot_SampleRate.toggled.connect(self.on_RadioBot_SampleRate_Clicked) # Radiobutton event click
        Page1.SampleRate.textChanged.connect(self.on_SampleRate_Change) # Text event change
        Page1.SampleFreq.textChanged.connect(self.on_SampleFreq_Change) # Text event change
        #
        return

    def on_RadioBot_SampleFreq_Clicked(self):
        print('Page1 - on_RadioBot_SampleFreq_Clicked')
        Page1.SampleRate.setEnabled(False)
        Page1.SampleFreq.setEnabled(True)
        return
            
    def on_RadioBot_SampleRate_Clicked(self):
        print('Page1 - on_RadioBot_SampleRate_Clicked')
        Page1.SampleRate.setEnabled(True)
        Page1.SampleFreq.setEnabled(False)
        return
#%%
'''
Page 2 of the wizard
'''
class Page2(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
# Create grid layot for the window
        Layout_Page2 = PQW.QGridLayout()
# Label Sensor in file
        Label_SensFile = PQW.QLabel('S\ne\nn\ns\no\nr\ns\n \ni\nn\n \nd\na\nt\na\n \nf\ni\nl\ne')
# Label Sensor to import
        Label_SensImpo = PQW.QLabel('S\ne\nn\ns\no\nr\ns\n \nt\no\n \ni\nm\np\no\nr\nt')
# List of Sensor in file
        Page2.List_Sensor_File = PQW.QListWidget()
        Page2.List_Sensor_File.setFixedWidth(205)
        Page2.List_Sensor_File.itemActivated.connect(self.on_List_Sensor_File_event)
# List of Sensor to import
        Page2.List_Sensor_Impo = PQW.QListWidget()
        Page2.List_Sensor_Impo.setFixedWidth(205)
        Page2.List_Sensor_Impo.itemActivated.connect(self.on_List_Sensor_Impo_event)
# Button Add all
        Page2.Button_Add_All = PQW.QPushButton('Add all sensors')
        Page2.Button_Add_All.setFixedWidth(100)
        Page2.Button_Add_All.clicked.connect(self.on_Button_Add_All_clicked)
# Button Remove all
        Page2.Button_Remove_All = PQW.QPushButton('Remove all sensors')
        Page2.Button_Remove_All.setFixedWidth(100)
        Page2.Button_Remove_All.clicked.connect(self.on_Button_Remove_All_clicked)
# DataChart
        Page2.Chart_Fig = plt.figure()
        Page2.Canvas = FigureCanvas(Page2.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page2.Canvas, self)
        Page2.Canvas.draw()
# Insert elements in the grid
        Layout_Page2.addWidget(Label_SensFile, 0,0,3,1)
        Layout_Page2.addWidget(Label_SensImpo, 4,0,3,1)
        Layout_Page2.addWidget(Page2.List_Sensor_File, 0,1,3,2)
        Layout_Page2.addWidget(Page2.Button_Add_All, 3,1,1,1)
        Layout_Page2.addWidget(Page2.Button_Remove_All, 3,2,1,1)
        Layout_Page2.addWidget(Page2.List_Sensor_Impo, 4,1,3,2)
        Layout_Page2.addWidget(self.Toolbar, 0,3,1,1)
        Layout_Page2.addWidget(Page2.Canvas, 1,3,6,1)
# Show layout
        self.setLayout(Layout_Page2)
        #
        # Page2.UpdateChart(self) # Call update charts

    def UpdateChart(self):
        print('Page2 - Update Chart')
        # Reset chart
        Page2.Chart_Fig.clear()
        Page2.ax = Page2.Chart_Fig.add_subplot(111)
        #
        FlagLegend = False
        # Check if chart color palette exist or not
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        # Update the chart
        if Page1.Flag_Update: # Update the data of probe #! To finish
            pass
        else: # Create a new probe
            if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes):
                if(Page1.Combobox_TimeType.currentText() == 'Time'): # Timeserie is timestamp format
                    TimeStamp = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].to_numpy()
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor != Page1.Combobox_TimeSerie.currentText():
                            if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                try:
                                    plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                    Colors.append(plot[0].get_color())
                                    FlagLegend = True
                                except:
                                    pass
                            else: # Chart colors setted
                                try:
                                    plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                    FlagLegend = True
                                except:
                                    pass
                elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'): # Timeserie is datetime format
                    TimeStamp = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor != Page1.Combobox_TimeSerie.currentText():
                            if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                try:
                                    plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                    Colors.append(plot[0].get_color())
                                    FlagLegend = True
                                except:
                                    pass
                            else: # Chart colors setted
                                try:
                                    plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                    FlagLegend = True
                                except:
                                    pass
            else:
                TimeStamp = np.array([i*float(Page1.SampleRate.text()) for i in range(0,Page1.DataNow.shape[0])])
                #
                for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                    if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                        try:
                            plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                            Colors.append(plot[0].get_color())
                            FlagLegend = True
                        except:
                            pass
                    else: # Chart colors setted
                        try:
                            plot = Page2.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i]) # Plot
                            FlagLegend = True
                        except:
                            pass
        #
        if(VAR.GetChartColors(VAR) is None and len(Colors) != 0):
            VAR.SetChartColors(VAR, Colors) # Store the colors use for the chart
        #
        if FlagLegend:
            Page1.ax.legend(loc=9, ncol=4) # Add legend to the chart
        #
        Page2.ax.grid(True, which='both', axis='both', linestyle='--') # Add grid to the chart
        Page2.Canvas.draw() # Redraw the chart
        #
        return

    def on_List_Sensor_File_event(self,item):
        print('Page2 - on_List_Sensor_File_event')
        Page2.List_Sensor_Impo.addItem(item.text())
        Page2.List_Sensor_File.takeItem(Page2.List_Sensor_File.row(item))
        return

    def on_List_Sensor_Impo_event(self,item):
        print('Page2 - on_List_Sensor_Impo_event')
        Page2.List_Sensor_File.addItem(item.text())
        Page2.List_Sensor_Impo.takeItem(Page2.List_Sensor_Impo.row(item))
        return

    def on_Button_Add_All_clicked(self):
        print('Page2 - on_Button_Add_All_clicked')
        n_item = Page2.List_Sensor_File.count()
        list_item = [Page2.List_Sensor_File.item(i) for i in range(n_item)]
        for item in list_item:
            Page2.List_Sensor_Impo.addItem(item.text())
        Page2.List_Sensor_File.clear()
        return

    def on_Button_Remove_All_clicked(self):
        print('Page2 - on_Button_Remove_All_clicked')
        n_item = Page2.List_Sensor_Impo.count()
        list_item = [Page2.List_Sensor_Impo.item(i) for i in range(n_item)]
        for item in list_item:
            Page2.List_Sensor_File.addItem(item.text())
        Page2.List_Sensor_Impo.clear()
        return
#%%
'''
Page 3 of the wizard
'''
class Page3(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
# Create grid layot for the window
        Layout_Page3 = PQW.QGridLayout()
# Table of sensor and relative height
        Page3.Table_Height = PQW.QTableWidget()
        Page3.Table_Height.setFixedWidth(230)
        Page3.Table_Height.setFixedHeight(500)
# Button Import Geometry
        Page3.Button_Imp_Geo = PQW.QPushButton('Import Geometry')
        Page3.Button_Imp_Geo.setFixedWidth(110)
        Page3.Button_Imp_Geo.clicked.connect(self.on_Button_Imp_Geo_clicked)
# Button Generate Geometry
        Page3.Button_Gen_Geo = PQW.QPushButton('Generate Geometry')
        Page3.Button_Gen_Geo.setFixedWidth(110)
        Page3.Button_Gen_Geo.clicked.connect(self.on_Button_Gen_Geo_clicked)
# DataChart
        Page3.Chart_Fig = plt.figure()
        Page3.Canvas = FigureCanvas(Page3.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page3.Canvas, self)
        Page3.Canvas.draw()
# Insert elements in the grid
        Layout_Page3.addWidget(Page3.Table_Height,0,0,3,2)
        Layout_Page3.addWidget(Page3.Button_Imp_Geo,4,0,1,1)
        Layout_Page3.addWidget(Page3.Button_Gen_Geo,4,1,1,1)
        Layout_Page3.addWidget(self.Toolbar,0,2,1,1)
        Layout_Page3.addWidget(Page3.Canvas,1,2,6,1)
# Show layout
        self.setLayout(Layout_Page3)
        #
        # Page3.UpdateChart(self) # Call update charts
#%%
    def UpdateChart(self):
        print('Page3 - Update Chart')
        SensorToImport =  [str(Page2.List_Sensor_Impo.item(i).text()) for i in range(Page2.List_Sensor_Impo.count())]
        # Reset chart
        Page3.Chart_Fig.clear()
        Page3.ax = Page3.Chart_Fig.add_subplot(111)
        #
        FlagLegend = False
        # Check if chart color palette exist or not
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        # Update the chart
        if Page1.Flag_Update: # Update the data of probe #! To finish
            pass
        else: # Create a new probe
            if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes):
                if(Page1.Combobox_TimeType.currentText() == 'Time'): # Timeserie is timestamp format
                    TimeStamp = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].to_numpy()
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor in SensorToImport:
                            if Sensor != Page1.Combobox_TimeSerie.currentText():
                                if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                    try:
                                        plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                        Colors.append(plot[0].get_color())
                                        FlagLegend = True
                                    except:
                                        pass
                                else: # Chart colors setted
                                    try:
                                        plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                        FlagLegend = True
                                    except:
                                        pass
                elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'): # Timeserie is datetime format
                    TimeStamp = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor in SensorToImport:
                            if Sensor != Page1.Combobox_TimeSerie.currentText():
                                if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                    try:
                                        plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                        Colors.append(plot[0].get_color())
                                        FlagLegend = True
                                    except:
                                        pass
                                else: # Chart colors setted
                                    try:
                                        plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                        FlagLegend = True
                                    except:
                                        pass
            else:
                TimeStamp = np.array([i*float(Page1.SampleRate.text()) for i in range(0,Page1.DataNow.shape[0])])
                #
                for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                    if Sensor in SensorToImport:
                        if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                            try:
                                plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                Colors.append(plot[0].get_color())
                                FlagLegend = True
                            except:
                                pass
                        else: # Chart colors setted
                            try:
                                plot = Page3.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i]) # Plot
                                FlagLegend = True
                            except:
                                pass
        #
        if(VAR.GetChartColors(VAR) is None and len(Colors) != 0):
            VAR.SetChartColors(VAR, Colors) # Store the colors use for the chart
        #
        if FlagLegend:
            Page3.ax.legend(loc=9, ncol=4) # Add legend to the chart
        #
        Page3.ax.grid(True, which='both', axis='both', linestyle='--') # Add grid to the chart
        Page3.Canvas.draw() # Redraw the chart
        #
        return

    def on_Button_Imp_Geo_clicked(self):
        print('Page2 - on_Button_Imp_Geo_clicked')
        # Select the path of the datafile
        Options = PQW.QFileDialog.Options()
        Options |= PQW.QFileDialog.DontUseNativeDialog
        file_name, _ = PQW.QFileDialog.getOpenFileName(self, 'Select geometry file...', VAR.DefaultFolderFileDialog(VAR), 'CSV Files (*.csv);;All Files (*);;Text Files (*.txt)', options = Options)  
        #
        if file_name:
            # Load the geometry
            df_Geom = pd.read_csv(file_name,header=None)
            #
            if(df_Geom.shape[1] == 1): # Check dimension of geometry data: only z present
                for i in range(0,Page2.List_Sensor_Impo.count()):
                    try:
                        item = PQW.QTableWidgetItem(str(df_Geom[0].iloc[i]))
                        Page3.Table_Height.setItem(i,1, item)
                    except:
                        pass
            elif(df_Geom.shape[1] == 2): # Check dimension of geometry data: Sensor name and z present
                for i in range(0,Page2.List_Sensor_Impo.count()):
                    try:
                        index = df_Geom.index[df_Geom[0] == Page2.List_Sensor_Impo.item(i).text()].tolist()
                        item = PQW.QTableWidgetItem(str(df_Geom[1].loc[index[0]]))
                        Page3.Table_Height.setItem(i,1, item)
                    except:
                        pass
            else:
                pass
        #
        return

    def on_Button_Gen_Geo_clicked(self):
        print('Page2 - on_Button_Gen_Geo_clicked')
        dz_text, okPressed = PQW.QInputDialog.getText(None,'Create Probe Geometry','dz between the sensors:',PQW.QLineEdit.Normal,'')
        if okPressed and dz_text != '':
            try:
                dz = float(dz_text)
                for i in range(0,Page2.List_Sensor_Impo.count()):
                    item = PQW.QTableWidgetItem(str(round(-i*dz,3)))
                    Page3.Table_Height.setItem(i,1, item)
            except:
                pass
        #
        return
#%%
'''
Page 4 of the wizard
'''
class Page4(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page4, self).__init__(parent)
# Create grid layot for the window
        Layout_Page4 = PQW.QGridLayout()
# Label Import From
        Label_ImpoFrom = PQW.QLabel('Import from:')
        Label_ImpoFrom.setFixedWidth(110)
# 
        Page4.ImpoFromDateTime = PQW.QDateTimeEdit(self)
        Page4.ImpoFromDateTime.setFixedWidth(110)
        Page4.ImpoFromDateTime.setDisplayFormat('yyyy-mm-dd hh:mm:ss') 
        Page4.ImpoFromTime = PQW.QSpinBox(self)
        Page4.ImpoFromTime.setFixedWidth(110)
# Label Import To
        Label_ImpoTo = PQW.QLabel('Import to:')
        Label_ImpoTo.setFixedWidth(110)
# 
        Page4.ImpoToDateTime = PQW.QDateTimeEdit(self)
        Page4.ImpoToDateTime.setFixedWidth(110)
        Page4.ImpoToDateTime.setDisplayFormat('yyyy-mm-dd hh:mm:ss') 
        Page4.ImpoToTime = PQW.QSpinBox(self)
        Page4.ImpoToTime.setFixedWidth(110)
# DataChart
        Page4.Chart_Fig = plt.figure()
        Page4.Canvas = FigureCanvas(Page4.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page4.Canvas, self)
        Page4.Canvas.draw()
# Insert elements in the grid
        Layout_Page4.addWidget(Label_ImpoFrom,0,0,1,1)
        Layout_Page4.addWidget(Page4.ImpoFromDateTime,1,0,1,1)
        Layout_Page4.addWidget(Page4.ImpoFromTime,2,0,1,1)
        Layout_Page4.addWidget(Label_ImpoTo,3,0,1,1)
        Layout_Page4.addWidget(Page4.ImpoToDateTime,4,0,1,1)
        Layout_Page4.addWidget(Page4.ImpoToTime,5,0,1,1)
        Layout_Page4.addWidget(self.Toolbar,0,1,1,1)
        Layout_Page4.addWidget(Page4.Canvas,1,1,6,1)
# Show layout
        self.setLayout(Layout_Page4)
        #
        # Page4.UpdateChart(self) # Call update charts
#
    def UpdateChart(self):
        print('Page4 - Update Chart')
        SensorToImport =  [str(Page2.List_Sensor_Impo.item(i).text()) for i in range(Page2.List_Sensor_Impo.count())]
        # Reset chart
        Page4.Chart_Fig.clear()
        Page4.ax = Page4.Chart_Fig.add_subplot(111)
        #
        FlagLegend = False
        # Check if chart color palette exist or not
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        # Update the chart
        if Page1.Flag_Update: # Update the data of probe #! To finish
            pass
        else: # Create a new probe
            if(Page1.Flag_TimeSerie == PQW.QMessageBox.Yes):
                if(Page1.Combobox_TimeType.currentText() == 'Time'): # Timeserie is timestamp format
                    TimeStamp = Page1.DataNow[Page1.Combobox_TimeSerie.currentText()].to_numpy()
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor in SensorToImport:
                            if Sensor != Page1.Combobox_TimeSerie.currentText():
                                if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                    try:
                                        plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                        Colors.append(plot[0].get_color())
                                        FlagLegend = True
                                    except:
                                        pass
                                else: # Chart colors setted
                                    try:
                                        plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                        FlagLegend = True
                                    except:
                                        pass
                elif(Page1.Combobox_TimeType.currentText() == 'yyyy-mm-dd h24:min:sec'): # Timeserie is datetime format
                    TimeStamp = pd.to_datetime(Page1.DataNow[Page1.Combobox_TimeSerie.currentText()])
                    for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                        if Sensor in SensorToImport:
                            if Sensor != Page1.Combobox_TimeSerie.currentText():
                                if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                                    try:
                                        plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                        Colors.append(plot[0].get_color())
                                        FlagLegend = True
                                    except:
                                        pass
                                else: # Chart colors setted
                                    try:
                                        plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i-1]) # Plot
                                        FlagLegend = True
                                    except:
                                        pass
            else:
                TimeStamp = np.array([i*float(Page1.SampleRate.text()) for i in range(0,Page1.DataNow.shape[0])])
                #
                for i,Sensor in enumerate(Page1.DataNow.columns.tolist()):
                    if Sensor in SensorToImport:
                        if(VAR.GetChartColors(VAR) == None): # Chart colors not setted
                            try:
                                plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor)) # Plot
                                Colors.append(plot[0].get_color())
                                FlagLegend = True
                            except:
                                pass
                        else: # Chart colors setted
                            try:
                                plot = Page4.ax.plot(TimeStamp, Page1.DataNow[Sensor].to_numpy(), '-', label = str(Sensor), color=Colors[i]) # Plot
                                FlagLegend = True
                            except:
                                pass
        #
        if(VAR.GetChartColors(VAR) is None and len(Colors) != 0):
            VAR.SetChartColors(VAR, Colors) # Store the colors use for the chart
        #
        if FlagLegend:
            Page4.ax.legend(loc=9, ncol=4) # Add legend to the chart
        #
        Page4.ax.grid(True, which='both', axis='both', linestyle='--') # Add grid to the chart
        Page4.Canvas.draw() # Redraw the chart
        #
        return

'''
Page 5 of the wizard
'''
class Page5(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page5, self).__init__(parent)
# Create grid layot for the window
        Layout_Page5 = PQW.QGridLayout()
# Label Import From
        Label_Text = PQW.QLabel('Press FINISH to import the data')
# Insert elements in the grid
        Layout_Page5.addWidget(Label_Text,0,0,1,1)
# Show layout
        self.setLayout(Layout_Page5)
