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
import os
import sys
import PyQt5.QtWidgets as PQW
import PyQt5.QtGui as PQG
import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from numpy.lib.function_base import append
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import pickle
import datetime
from shutil import copyfile
# import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# import subprocess
import glob
from loguru import logger

# Import custom library
from Variables import VAR
import WizEtaKeMean as WKE

'''
Wizzard Add Probe Class
'''
class ParameterEstimation(PQW.QWizard):
    def __init__(self, parent=None):
        logger.debug(F"Variable estimation Wizard started")
        super(ParameterEstimation, self).__init__(parent)
        self.setWindowTitle('Parameter Estimation')
        #
        self.width = VAR.GetWindowsSize(VAR)[0] * 2 / 3 # Width of the window
        height = VAR.GetWindowsSize(VAR)[1] * 2 / 3 # Height of the window
        #
        self.setMinimumSize(self.width,height) # Set the minimun size of the wondow
        #
        HandleLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/probe.ini')
        HandleLog.readline()
        HandleLog.readline()
        self.TimeType = HandleLog.readline().split(';')[0] #
        self.dt = HandleLog.readline().split(';')[0] #
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.readline()
        HandleLog.close()
        #
        self.addPage(Page1(self)) # Add Page1
        self.addPage(Page2(self)) # Add Page2
        self.addPage(Page3(self)) # Add Page3
        self.addPage(Page4(self)) # Add Page4
        self.addPage(Page5(self)) # Add Page5
        #
        self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print) # Click event on Next Page of the wizard
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print) # Click event on Finish the wizard
        # self.button(PQW.QWizard.BackButton).clicked.connect(self.back_print) # Click event on Finish the wizard
        #
        self.OldPage = 0

    # def back_print(self):
    #     print('QUI')
    #     print('Back',self.currentId())
    #     self.back()
    #     self.back()

    @logger.catch
    def next_print(self):
        if self.currentId() == 1:
            if Page1.CheckUpdate.isChecked():
                HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+Page1.Combobox_RunEst.currentText()+'.run','r')
                Run_Analysis = HandleRun.readline().replace('\n','').split(';')[0]
                if Run_Analysis == 'MLEn':
                    Run_LPMRun = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Sensors = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Heights = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_FreqOK = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_MethodDV = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_D = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_V = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Method = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_SRNLimit = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_FreqLimit = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_MinMaxSRN = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_cw_x_rhow = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_c_x_rho = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_IniFlag = HandleRun.readline().replace('\n','').split(';')[0]
                elif Run_Analysis == 'MLEnZ':
                    Run_LPMRun = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Sensors = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Heights = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_FreqOK = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_MethodDV = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_D = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_V = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Method = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_SRNLimit = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_FreqLimit = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_MinMaxSRN = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_cw_x_rhow = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_c_x_rho = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_IniFlag = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_d50 = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Zuser = HandleRun.readline().replace('\n','').split(';')[0]
                elif Run_Analysis == 'Analytical':
                    Run_RunSP = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Sensors = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Heights = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_PeriodValue = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_BElev = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_TopSens = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_dt = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_BRE = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Gamma = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_From = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_To = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Ke = HandleRun.readline().replace('\n','').split(';')[0]
                    Run_Period = HandleRun.readline().replace('\n','').split(';')[0]
                HandleRun.close()
            else:   
            #
                if Page1.Combobox_Method.currentText() == 'Analytical':
                    # Project and Probe Active
                    dfx = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+Page1.Combobox_Run.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
                    # with open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+Page1.Combobox_Run.currentText().replace('Run: ','')+'_Phase.PdList','rb') as f:
                    #     dfx = pickle.load(f)
                    # #
                    Columns = (dfx.columns.tolist())[2:]
                    #
                    for item in dfx['Freq'].drop_duplicates().tolist():
                        try:
                            Page3.Combobox_Period.addItem(str(1/float(item)/3600.0))
                        except:
                            Page3.Combobox_Period.addItem('Inf')
                    #
                    try:
                        pos = Page1.Sensors.index(Columns[0])
                        Page3.BedElev.setText(Page1.SensorsHeight[pos])
                    except:
                        pass
                    #
                    for item in Columns:
                        Page3.Combobox_TopSensor.addItem(item)
                    #
                    if Page3.VBoxSensor is not None:
                        while Page3.VBoxSensor.count():
                            item = Page3.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    #
                    for sensor in Columns:
                        CheckBox = PQW.QCheckBox(sensor)
                        CheckBox.setChecked(True)
                        Page3.VBoxSensor.addWidget(CheckBox)
                    #
                    # df_Clean = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
                    # ChartColumns = (df_Clean.columns).tolist()
                    # Page3.Chart_Fig.clear()
                    # Page3.ax = Page3.Chart_Fig.add_subplot(111)
                    # #
                    # VAR.SetChartColors(VAR,None)
                    # if(VAR.GetChartColors(VAR) is None):
                    #     Colors = []
                    # else:
                    #     Colors = VAR.GetChartColors(VAR)
                    # #
                    # for i in range(1,len(ChartColumns)):
                    #     if(VAR.GetChartColors(VAR) == None):
                    #         if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    #             plot = Page3.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s'), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                    #         elif Page1.TimeType == 'Time':
                    #             plot = Page3.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                    #         Colors.append(plot[0].get_color())
                    #     else:
                    #         if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    #             plot = Page3.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s'), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
                    #         elif Page1.TimeType == 'Time':
                    #             plot = Page3.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
                    # #
                    # if(VAR.GetChartColors(VAR) is None):
                    #     VAR.SetChartColors(VAR, Colors)
                    # #
                    # Page3.ax.legend(loc=9, ncol=len(ChartColumns)) # Add legend to the chart
                    # #
                    # Page3.ax.grid(True, which='both', axis='both', linestyle='--')
                    # Page3.ax.set_ylabel('Temperature')
                    # #
                    # if Page1.TimeType == 'Time':
                    #     Page3.ax.set_xlabel('Time (s)')
                    # else:
                    #     pass
                    # Page3.Canvas.draw()
                    self.next()
                else:
                    df_Temp = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+Page1.Combobox_Run.currentText().replace('Run: ','')+'_Amplitude.pkz',compression='zip')
                    #
                    if Page2.VBoxSensor is not None:
                        while Page2.VBoxSensor.count():
                            item = Page2.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    for sensor in df_Temp.columns.tolist()[2:]:
                        CheckBox = PQW.QCheckBox(sensor)
                        CheckBox.setChecked(True)
                        Page2.VBoxSensor.addWidget(CheckBox)
        if self.currentId() == 2:
            if Page1.Combobox_Method.currentText() == 'Analytical':
                pass
                # self.next()
            else:
                # Input Files
                FileDel = glob.glob('../temp/*.*')
                for File in FileDel:
                    os.remove(File)
                #
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_MobWinTime.pkz', '../temp/MobWinTime.pkz')
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_SRN.PdList', '../temp/SRN.PdList')
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_Y.PdList', '../temp/Y.PdList')
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_Amplitude.pkz', '../temp/Amplitude.pkz')
                #
                FileCYmnt = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_*.CY_m_nt')
                for File in FileCYmnt:
                    copyfile(File, File.replace('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata\\'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_','../temp/'))
                # SensorOk
                dfTemp = pd.read_pickle('../temp/Amplitude.pkz',compression='zip')
                SensorOk = (dfTemp.columns.tolist())[2:]
                # HeightOk
                HeightOk = []
                SensActive = VAR.GetActiveParameters(VAR,6).split(',')
                HeightActive = VAR.GetActiveParameters(VAR,7).split(',')
                for item in SensorOk:
                    try:
                        pos = SensActive.index(item)
                        HeightOk.append(HeightActive[pos])
                    except:
                        pass
                #
                if Page2.CheckBox_MLEnZ.isChecked():
                    stringEXE = 'ParEstMLEnZ.exe'
                else:
                    stringEXE = 'ParEstMLEn.exe'
                #
                SensorOkFin = []
                HeightOkFin = []
                for i in range(0,Page2.VBoxSensor.count()):
                    if Page2.VBoxSensor.itemAt(i).widget().isChecked():
                        SensorOkFin.append(SensorOk[i])
                        HeightOkFin.append(HeightOk[i])
                # Sensors [LIST] -s
                stringEXE = stringEXE + ' -s "' + ','.join(SensorOkFin) +'"'
                # Height [LIST] -h
                stringEXE = stringEXE + ' -h "' + ','.join(HeightOkFin) +'"'
                # FreqType [INTEGER] -f
                stringEXE = stringEXE + ' -f "' + str(Page2.Combobox_Frequency.currentIndex()) +'"'
                # Run [STRING] -r
                stringEXE = stringEXE + ' -r "' + (Page1.Combobox_Run.currentText()).replace('Run: ','') +'"'
                # MethodDV [STRING] -t
                if Page2.Combobox_Estimate.currentText() == 'D and V':
                    stringEXE = stringEXE + ' -t "DV"'
                elif Page2.Combobox_Estimate.currentText() == 'D':
                    stringEXE = stringEXE + ' -t "D"'
                elif Page2.Combobox_Estimate.currentText() == 'V':
                    stringEXE = stringEXE + ' -t "V"'
                # D [FLOAT] -d
                stringEXE = stringEXE + ' -d "' + Page2.Diffusivity.text() +'"'
                # V [FLOAT] -v
                stringEXE = stringEXE + ' -v "' + Page2.Velocity.text() +'"'
                # Method [STRING] -m
                stringEXE = stringEXE + ' -m "' + Page2.Combobox_Method.currentText() +'"'
                # SRN Limit [FLOAT] -n
                stringEXE = stringEXE + ' -n "' + Page2.SNRLimit.text() +'"'
                # Freq Limit [FLOAT] -n
                stringEXE = stringEXE + ' -l "' + Page2.FreqLimit.text() +'"'
                # cxrho [FLOAT] -n
                stringEXE = stringEXE + ' -z "' + Page2.cxrho.text() +'"'
                # cwxrhow [FLOAT] -n
                stringEXE = stringEXE + ' -x "' + Page2.cwxrhow.text() +'"'
                # SRNmixmax [INTEGER] -a
                if Page2.Combobox_SRNminmax.currentText() == 'Max':
                    stringEXE = stringEXE + ' -a "0"'
                elif Page2.Combobox_SRNminmax.currentText() == 'Min':
                    stringEXE = stringEXE + ' -a "1"'
                # InitialCond [INTEGER] -i
                if Page2.Combobox_InitialCond.currentText() == 'First':
                    stringEXE = stringEXE + ' -i "1"'
                elif Page2.Combobox_InitialCond.currentText() == 'Every':
                    stringEXE = stringEXE + ' -i "0"'
                #
                if Page2.CheckBox_MLEnZ.isChecked():
                    stringEXE = stringEXE + ' -p "' + Page2.d50.text() +'"'
                    stringEXE = stringEXE + ' -j "' + Page2.BedRiv.text() +'"'
                # Call external program
                logger.info(stringEXE)
                os.system(stringEXE)
                #
                # Check Run
                HandleLog = open('../temp/MLEn.log')
                Check = HandleLog.readline().replace('\n','')
                HandleLog.close()
                if Check == 'No Error':
                    FilesRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/*.run')
                    if len(FilesRuns) == 0:
                        NewRun = '0'
                    else:
                        NewRun = -9
                        for File in FilesRuns:
                            if NewRun < int((File.split('/')[-1]).replace('PEdata\\','').replace('.run','')):
                                NewRun = int((File.split('/')[-1]).replace('PEdata\\','').replace('.run',''))
                        NewRun = str(NewRun+1)
                    # Move the data
                    os.remove('../temp/Amplitude.pkz')
                    os.remove('../temp/SRN.PdList')
                    os.remove('../temp/Y.PdList')
                    FileCYmnt = glob.glob('../temp/*.CY_m_nt')
                    for File in FileCYmnt:
                        os.remove(File)
                    #
                    os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'.run')
                    os.replace('../temp/Diffusivity.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Diffusivity.pkz')
                    os.replace('../temp/K.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_K.pkz')
                    os.replace('../temp/Pearson.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Pearson.pkz')
                    os.replace('../temp/Q.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Q.pkz')
                    os.replace('../temp/PearsonQ.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_PearsonQ.pkz')
                    os.replace('../temp/Velocity.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Velocity.pkz')
                    os.replace('../temp/MobWinTime.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_MobWinTime.pkz')
                    os.replace('../temp/MLEn.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_MLEn.log')
                    os.replace('../temp/CostBest.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_CostBest.pkz')
                    if Page2.CheckBox_MLEnZ.isChecked():
                        os.replace('../temp/Heights.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Heights.pkz')
                    #
                    self.next()
                    self.next()
                else:
                    PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        if self.currentId() == 3:
            if Page1.Combobox_Method.currentText() == 'MLEn':
                self.next()
            else:
                # Checks
                try:
                    if float(Page1.SensorsHeight[Page1.Sensors.index(Page3.Combobox_TopSensor.currentText())]) < float(Page3.BedElev.text()):
                        FlagBed = True
                    else:
                        FlagBed = False
                except:
                    PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'Insert wrong elevation.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                    self.back()
                    return
                #
                if FlagBed:
                    result =PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'Top sensor in the bedriver. Continue?', PQW.QMessageBox.Ok|PQW.QMessageBox.No, PQW.QMessageBox.Ok)
                    if result == PQW.QMessageBox.No:
                        self.back()
                        return
                # Input Files
                FileDel = glob.glob('../temp/*.*')
                for File in FileDel:
                    os.remove(File)
                #
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_MobWinTime.pkz', '../temp/MobWinTime.pkz')
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_Phase.pkz', '../temp/Phase.pkz')
                copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'_Amplitude.pkz', '../temp/Amplitude.pkz')
                # SensorOk
                dfTemp = pd.read_pickle('../temp/Amplitude.pkz',compression='zip')
                SensorOk = (dfTemp.columns.tolist())[2:]
                # HeightOk
                HeightOk = []
                SensActive = VAR.GetActiveParameters(VAR,6).split(',')
                HeightActive = VAR.GetActiveParameters(VAR,7).split(',')
                for item in SensorOk:
                    try:
                        pos = SensActive.index(item)
                        HeightOk.append(HeightActive[pos])
                    except:
                        pass
                #
                stringEXE = 'ParEstAnal.exe'
                #
                SensorOkFin = []
                HeightOkFin = []
                for i in range(0,Page3.VBoxSensor.count()):
                    if Page3.VBoxSensor.itemAt(i).widget().isChecked():
                        SensorOkFin.append(SensorOk[i])
                        HeightOkFin.append(HeightOk[i])
                # # Probe name  [STRING] -p
                # stringEXE = stringEXE + ' -p "' + VAR.GetActiveProbe(VAR) +'"'
                # # Project name  [STRING] -j
                # stringEXE = stringEXE + ' -j "' + VAR.GetActiveProject(VAR) +'"'

                # AllItems = [Page3.Combobox_TopSensor.itemText(i) for i in range(Page3.Combobox_TopSensor.count())]
                # AllItems2 = []
                # for Sens in AllItems:
                #     try:
                #         pos = Page1.Sensors.index(Sens)
                #         AllItems2.append(Page1.SensorsHeight[pos])
                #     except:
                #         print('Error')
                # Sensors [LIST] -s
                stringEXE = stringEXE + ' -s "' + ','.join(SensorOkFin) +'"'
                # Height [LIST] -h
                stringEXE = stringEXE + ' -h "' + ','.join(HeightOkFin) +'"'
                # Run [STRING] -r
                stringEXE = stringEXE + ' -r "' + (Page1.Combobox_Run.currentText()).replace('Run: ','') +'"'
                # Period [INTEGER] -e
                stringEXE = stringEXE + ' -e "' + str(Page3.Combobox_Period.currentIndex()) +'"'
                # Period [FLOAT] -f
                stringEXE = stringEXE + ' -f "' + str(Page3.Combobox_Period.currentText()) +'"'
                # Bed Elevation [FLOAT] -z
                stringEXE = stringEXE + ' -z "' + Page3.BedElev.text() +'"'
                # Top Sensor [STRING] -u
                stringEXE = stringEXE + ' -u "' + Page3.Combobox_TopSensor.currentText() +'"'
                # dt [FLOAT] -d
                stringEXE = stringEXE + ' -d "' + self.dt +'"'
                #
                # FileDel = glob.glob('../temp/*.*')
                # for File in FileDel:
                #     os.remove(File)
                # Call external program
                logger.info(stringEXE)
                os.system(stringEXE)
                # Check Run
                HandleLog = open('../temp/EtaKe.log')
                Check = HandleLog.readline().replace('\n','')
                HandleLog.close()
                #
                try:
                    Page4.BRE2.setText(Page3.BedElev.text())
                    #
                    Page4.df_Ke = pd.read_pickle('../temp/Ke.pkz',compression='zip')
                    #
                    if Page1.TimeType == 'Time':
                        Page4.ImpoFrom.setMinimum(Page4.df_Ke['Time'].min())
                        Page4.ImpoFrom.setMaximum(Page4.df_Ke['Time'].max())
                        Page4.ImpoTo.setMinimum(Page4.df_Ke['Time'].min())
                        Page4.ImpoTo.setMaximum(Page4.df_Ke['Time'].max())
                        Page4.ImpoFrom.setValue(Page4.df_Ke['Time'].min())
                        Page4.ImpoTo.setValue(Page4.df_Ke['Time'].max())
                    else:
                        Page4.ImpoFrom.setDateTime(pd.to_datetime(Page4.df_Ke['Time'].min(), unit='s'))
                        Page4.ImpoTo.setDateTime(pd.to_datetime(Page4.df_Ke['Time'].max(), unit='s'))
                except:
                    pass
                #
                if Check != 'No Error':
                    self.back()
                else:
                    Page4.Chart(Page4)
        if self.currentId() == 4:
            if Page1.Combobox_Method.currentText() == 'MLEn':
                self.next()
            else:
                # Checks
                KeMean = []
                Sensors = []
                Heights = []
                for row in range(0,Page4.Table_Stat.rowCount()):
                    Value = Page4.Table_Stat.item(row,1).text()
                    try:
                        float(Value)
                        if Value == 'nan':
                            PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'One or more values of Ke aren\'t a number.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                            self.back()
                            return
                        else:
                            Sensors.append(Page4.Table_Stat.item(row,0).text())
                            try:
                                pos = Page1.Sensors.index(Page4.Table_Stat.item(row,0).text())
                                Heights.append(Page1.SensorsHeight[pos])
                            except:
                                pass
                            KeMean.append(Value)
                    except:
                        PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', 'One or more values of Ke aren\'t a number.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                        self.back()
                        return
                # SensorOk
                dfTemp = pd.read_pickle('../temp/Amplitude.pkz',compression='zip')
                SensorOk = (dfTemp.columns.tolist())[2:]
                # HeightOk
                HeightOk = []
                SensActive = VAR.GetActiveParameters(VAR,6).split(',')
                HeightActive = VAR.GetActiveParameters(VAR,7).split(',')
                for item in SensorOk:
                    try:
                        pos = SensActive.index(item)
                        HeightOk.append(HeightActive[pos])
                    except:
                        pass
                #
                stringEXE = 'ParEstAnal2.exe'
                #
                SensorOkFin = []
                HeightOkFin = []
                for i in range(0,Page3.VBoxSensor.count()):
                    if Page3.VBoxSensor.itemAt(i).widget().isChecked():
                        SensorOkFin.append(SensorOk[i])
                        HeightOkFin.append(HeightOk[i])
                # Sensors [LIST] -s
        #         # stringEXE = stringEXE + ' -s "' + ','.join(Page1.Sensors) +'"'
                stringEXE = stringEXE + ' -s "' + ','.join(SensorOkFin) +'"'
                # Height [LIST] -h
        #         # stringEXE = stringEXE + ' -h "' + ','.join(Page1.SensorsHeight) +'"'
                stringEXE = stringEXE + ' -h "' + ','.join(HeightOkFin) +'"'
                # Gamma [FLOAT] -g
                stringEXE = stringEXE + ' -g "' + Page4.Gamma.text() +'"'
                # Import from and to [FLOAT] -f and -t
                if Page1.TimeType == 'Time':
                    stringEXE = stringEXE + ' -f "' + str(Page4.ImpoFrom.value()) +'"'
                    stringEXE = stringEXE + ' -t "' + str(Page4.ImpoTo.value()) +'"'
                else:
                    stringEXE = stringEXE + ' -f "' + str(datetime.datetime.timestamp(Page4.ImpoFrom.dateTime().toPyDateTime())) +'"'
                    stringEXE = stringEXE + ' -t "' + str(datetime.datetime.timestamp(Page4.ImpoTo.dateTime().toPyDateTime())) +'"'
                # # Run [STRING] -r
                stringEXE = stringEXE + ' -r "' + (Page1.Combobox_Run.currentText()).replace('Run: ','') +'"'
                # Period [INTEGER] -e
                stringEXE = stringEXE + ' -e "' + str(Page3.Combobox_Period.currentIndex()) +'"'
                # Period [FLOAT] -f
                stringEXE = stringEXE + ' -x "' + str(Page3.Combobox_Period.currentText()) +'"'
                # Bed Elevation [FLOAT] -z
                stringEXE = stringEXE + ' -z "' + Page4.BRE2.text() +'"'
                # Top Sensor [STRING] -k
                stringEXE = stringEXE + ' -k "' + ','.join(KeMean) +'"'
                # dt [FLOAT] -d
                stringEXE = stringEXE + ' -d "' + self.dt +'"'
                # Call external program
                logger.info(stringEXE)
                os.system(stringEXE)
                # Check Run
                HandleLog = open('../temp/Flux.log')
                Check = HandleLog.readline().replace('\n','')
                HandleLog.close()
                if Check == 'No Error':
                    FilesRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/*.run')
                    if len(FilesRuns) == 0:
                        NewRun = '0'
                    else:
                        NewRun = -9
                        for File in FilesRuns:
                            if NewRun < int((File.split('/')[-1]).replace('PEdata\\','').replace('.run','')):
                                NewRun = int((File.split('/')[-1]).replace('PEdata\\','').replace('.run',''))
                        NewRun = str(NewRun+1)
                    # Move the data
                    os.remove('../temp/Amplitude.pkz')
                    os.remove('../temp/Phase.pkz')
                    #
                    os.replace('../temp/XXX.run','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'.run')
                    os.replace('../temp/BEC.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_BEC.pkz')
                    os.replace('../temp/Eta.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Eta.pkz')
                    os.replace('../temp/eta2.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_eta2.pkz')
                    os.replace('../temp/Ke.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Ke.pkz')
                    os.replace('../temp/MobWinTime.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_MobWinTime.pkz')
                    os.replace('../temp/Q.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Q.pkz')
                    os.replace('../temp/Velocity.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Velocity.pkz')
                    os.replace('../temp/EtaKe.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_EtaKe.log')
                    os.replace('../temp/Ke.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Ke.log')
                    os.replace('../temp/Flux.log','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/'+str(NewRun)+'_Flux.log')
                else:
                    PQW.QMessageBox.critical(self, VAR.GetSoftwareName(VAR)+' message', Check, PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)

    @logger.catch
    def finish_print(self):
        logger.debug("Action:finish Page: " + str(self.currentId()))
        return

'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        # Create grid layot for the window
        Layout_Page1 = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Page1_Left = PQW.QVBoxLayout()
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
        # Project and Probe Active
        Label_PP1 = PQW.QLabel('Project: '+VAR.GetActiveProject(VAR))
        Layout_Page1_Left.addWidget(Label_PP1)
        Label_PP2 = PQW.QLabel('Probe: '+VAR.GetActiveProbe(VAR))
        Layout_Page1_Left.addWidget(Label_PP2)
        # Signal Processing Runs
        Label_Run = PQW.QLabel('Signal processing Run:')
        Layout_Page1_Left.addWidget(Label_Run)
        Page1.Combobox_Run = PQW.QComboBox() # Combobox Signal processing Runs
        #
        Files = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/*.run')
        # RunList = []
        for File in Files:
            # RunList.append('Run: '+File.split('\\')[-1].replace('.run',''))
            Page1.Combobox_Run.addItem('Run: '+File.split('\\')[-1].replace('.run',''))
        #
        Page1.Combobox_Run.currentIndexChanged.connect(self.on_Combobox_Run_change) # ComboBox event change item
        Layout_Page1_Left.addWidget(Page1.Combobox_Run)
        #
        HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'.run','r')
        Rows = HandleRun.readlines()
        HandleRun.close()
        # Method
        Label_Method = PQW.QLabel('Method:')
        Layout_Page1_Left.addWidget(Label_Method)
        Page1.Combobox_Method = PQW.QComboBox() # Combobox 
        #
        for item in VAR.GetEstimationMethod(VAR):
            if item == 'MLEn':
                if Rows[0].split(';')[0] == 'FFT':
                    pass
                else:
                    Page1.Combobox_Method.addItem(item)
            elif item == 'MLEnZ':
                if Rows[0].split(';')[0] == 'FFT':
                    pass
                else:
                    Page1.Combobox_Method.addItem(item)
            else:
                Page1.Combobox_Method.addItem(item)
        Layout_Page1_Left.addWidget(Page1.Combobox_Method)
        # Update?
        #! Page1.CheckUpdate = PQW.QCheckBox('Update Run') #!
        #! Page1.CheckUpdate.toggled.connect(self.UpdateChange) #!
        #! Page1.Combobox_RunEst = PQW.QComboBox() #!
        #! #
        #! EstRuns = glob.glob('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/PEdata/*.run') #!
        #! #
        #! for EstRun in EstRuns: #!
        #!     Page1.Combobox_RunEst.addItem(EstRun.split('\\')[1].replace('.run','')) #!
        #! Page1.Combobox_RunEst.setEnabled(False) #!
        #! Page1.Combobox_RunEst.currentIndexChanged.connect(self.on_Combobox_RunEst_change) #!
        #
        container_left.setLayout(Layout_Page1_Left)
        # Chart column
        container_right = PQW.QFrame()
        Layout_Page1_Right = PQW.QVBoxLayout()
        Page1.Chart_Fig = plt.figure()
        Page1.Canvas = FigureCanvas(self.Chart_Fig)
        self.Toolbar = NavigationToolbar(self.Canvas, self)
        Layout_Page1_Right.addWidget(self.Toolbar)
        Layout_Page1_Right.addWidget(Page1.Canvas)
        #
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

    @logger.catch
    def UpdateChange(self): #!
#        print('UpdateChange') #!
#         if Page1.CheckUpdate.isChecked(): #!
#             Page1.Combobox_RunEst.setEnabled(True) #!
#         else: #!
#             Page1.Combobox_RunEst.setEnabled(False) #!
#         return #!
        return

    @logger.catch
    def on_Combobox_RunEst_change(self): #!
#        print('on_Combobox_RunEst_change') #!
        return #!

    @logger.catch
    def on_Combobox_Run_change(self):
        logger.debug('Page1 - on_Combobox_Run_change')
        #
        Page1.Combobox_Run.currentIndexChanged.disconnect()
        #
        HandleRun = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+(Page1.Combobox_Run.currentText()).replace('Run: ','')+'.run','r')
        Rows = HandleRun.readlines()
        HandleRun.close()
        #
        Page1.Combobox_Method.clear()
        for item in VAR.GetEstimationMethod(VAR):
            if item == 'MLEn':
                if Rows[0].split(';')[0] == 'FFT':
                    pass
                else:
                    Page1.Combobox_Method.addItem(item)
            elif item == 'MLEnZ':
                if Rows[0].split(';')[0] == 'FFT':
                    pass
                else:
                    Page1.Combobox_Method.addItem(item)
            else:
                Page1.Combobox_Method.addItem(item)
        #
        df_Clean = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
        ChartColumns = (df_Clean.columns).tolist()
        Page1.Chart_Fig.clear()
        Page1.ax = Page1.Chart_Fig.add_subplot(111)
        #
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        #
        for i in range(1,len(ChartColumns)-1):
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
        Page1.ax.legend()
        #
        Page1.ax.grid(True, which='both', axis='both', linestyle='--')
        Page1.ax.set_ylabel('Temperature')
        #
        if Page1.TimeType == 'Time':
            Page1.ax.set_xlabel('Time (s)')
        else:
            pass
        Page1.Canvas.draw()
        #
        Page1.Combobox_Run.currentIndexChanged.connect(self.on_Combobox_Run_change) # ComboBox event change item

'''
Page 2 of the wizard
'''
class Page2(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        # Create grid layot for the window
        # Layout_Page2 = PQW.QGridLayout()
        Layout_Page2 = PQW.QHBoxLayout()
        # Left Column
        container_left = PQW.QFrame()
        Layout_Page2_Left = PQW.QVBoxLayout()
        #
        Layout_Page2_Left_1 = PQW.QHBoxLayout()
        Label_Method = PQW.QLabel('Method:')
        Layout_Page2_Left_1.addWidget(Label_Method)
        Page2.Combobox_Method = PQW.QComboBox()
        Page2.Combobox_Method.addItem('infinite')
        Page2.Combobox_Method.addItem('boundaries')
        Layout_Page2_Left_1.addWidget(Page2.Combobox_Method)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_1)
        #
        Layout_Page2_Left_2 = PQW.QHBoxLayout()
        Label_Estimate = PQW.QLabel('Estimate:')
        Layout_Page2_Left_2.addWidget(Label_Estimate)
        Page2.Combobox_Estimate = PQW.QComboBox()
        Page2.Combobox_Estimate.addItem('D and V')
        Page2.Combobox_Estimate.addItem('D')
        Page2.Combobox_Estimate.addItem('V')
        # Page2.Combobox_Estimate.currentIndexChanged.connect(self.on_Combobox_Estimate_change) # ComboBox event change item
        Layout_Page2_Left_2.addWidget(Page2.Combobox_Estimate)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_2)
        #
        Layout_Page2_Left_3 = PQW.QHBoxLayout()
        Label_Frequency = PQW.QLabel('Frequency:')
        Layout_Page2_Left_3.addWidget(Label_Frequency)
        Page2.Combobox_Frequency = PQW.QComboBox()
        Page2.Combobox_Frequency.addItem('Best Frequency')
        Page2.Combobox_Frequency.addItem('Best 5 Frequencies')
        Page2.Combobox_Frequency.addItem('All Frequencies >')
        Page2.Combobox_Frequency.currentIndexChanged.connect(self.on_Combobox_Frequency_change) # ComboBox event change item
        Layout_Page2_Left_3.addWidget(Page2.Combobox_Frequency)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_3)
        #
        Layout_Page2_Left_4 = PQW.QHBoxLayout()
        Label_SNRLimitUnit = PQW.QLabel('dB:')
        Layout_Page2_Left_4.addWidget(Label_SNRLimitUnit)
        Page2.SNRLimit = PQW.QLineEdit()
        Page2.SNRLimit.setText('20')
        Page2.SNRLimit.setEnabled(False)
        Layout_Page2_Left_4.addWidget(Page2.SNRLimit)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_4)
        #
        Layout_Page2_Left_5 = PQW.QHBoxLayout()
        Label_SNRminmax = PQW.QLabel('SNRminmax:')
        Layout_Page2_Left_5.addWidget(Label_SNRminmax)
        Page2.Combobox_SNRminmax = PQW.QComboBox()
        Page2.Combobox_SNRminmax.addItem('Max')
        Page2.Combobox_SNRminmax.addItem('Min')
        Layout_Page2_Left_5.addWidget(Page2.Combobox_SNRminmax)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_5)
        #
        Layout_Page2_Left_6 = PQW.QHBoxLayout()
        Label_FreqLimit = PQW.QLabel('FreqLimit (d):')
        Layout_Page2_Left_6.addWidget(Label_FreqLimit)
        Page2.FreqLimit = PQW.QLineEdit()
        Page2.FreqLimit.setText('5')
        Layout_Page2_Left_6.addWidget(Page2.FreqLimit)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_6)
        #
        Layout_Page2_Left_7 = PQW.QHBoxLayout()
        Label_InitialCond = PQW.QLabel('InitialCondition:')
        Layout_Page2_Left_7.addWidget(Label_InitialCond)
        Page2.Combobox_InitialCond = PQW.QComboBox()
        Page2.Combobox_InitialCond.addItem('First')
        Page2.Combobox_InitialCond.addItem('Every')
        Layout_Page2_Left_7.addWidget(Page2.Combobox_InitialCond)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_7)
        #
        Page2.CheckBox_Calculate_Gamma = PQW.QCheckBox("Calculate \u03B3")
        Page2.CheckBox_Calculate_Gamma.stateChanged.connect(self.on_checkbox_changed)
        Layout_Page2_Left.addWidget(Page2.CheckBox_Calculate_Gamma)
        #
        Layout_Page2_Left_8 = PQW.QHBoxLayout()
        Label_Cpw = PQW.QLabel(f"c<sub>w</sub> (J kg<sup>-1</sup> K<sup>-1</sup>):")
        Page2.cp_w = PQW.QLineEdit(self)
        Page2.cp_w.setText("4183")
        Page2.cp_w.textChanged.connect(self.CalculateGamma)
        Page2.cp_w.setEnabled(False)
        Layout_Page2_Left_8.addWidget(Label_Cpw)
        Layout_Page2_Left_8.addWidget(Page2.cp_w)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_8)
        #
        Layout_Page2_Left_9 = PQW.QHBoxLayout()
        Label_Cps = PQW.QLabel(f"c<sub>s</sub> (J kg<sup>-1</sup> K<sup>-1</sup>):")
        Page2.cp_s = PQW.QLineEdit(self)
        Page2.cp_s.setText("800")
        Page2.cp_s.textChanged.connect(self.CalculateGamma)
        Page2.cp_s.setEnabled(False)
        Layout_Page2_Left_9.addWidget(Label_Cps)
        Layout_Page2_Left_9.addWidget(Page2.cp_s)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_9)
        #
        Layout_Page2_Left_10 = PQW.QHBoxLayout()
        Label_Rhow = PQW.QLabel(f"ρ<sub>w</sub> (kg m<sup>-3</sup>):")
        Page2.rho_w = PQW.QLineEdit(self)
        Page2.rho_w.setText("998")
        Page2.rho_w.textChanged.connect(self.CalculateGamma)
        Page2.rho_w.setEnabled(False)
        Layout_Page2_Left_10.addWidget(Label_Rhow)
        Layout_Page2_Left_10.addWidget(Page2.rho_w)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_10)
        #
        Layout_Page2_Left_11 = PQW.QHBoxLayout()
        Label_Rhos = PQW.QLabel(f"ρ<sub>s</sub> (kg m<sup>-3</sup>):")
        Page2.rho_s = PQW.QLineEdit(self)
        Page2.rho_s.setText("2650")
        Page2.rho_s.textChanged.connect(self.CalculateGamma)
        Page2.rho_s.setEnabled(False)
        Layout_Page2_Left_11.addWidget(Label_Rhos)
        Layout_Page2_Left_11.addWidget(Page2.rho_s)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_11)
        #
        Layout_Page2_Left_12 = PQW.QHBoxLayout()
        Label_poros = PQW.QLabel(f"n:")
        Page2.poros = PQW.QLineEdit(self)
        Page2.poros.setText("0.32")
        Page2.poros.textChanged.connect(self.CalculateGamma)
        Page2.poros.setEnabled(False)
        Layout_Page2_Left_12.addWidget(Label_poros)
        Layout_Page2_Left_12.addWidget(Page2.poros)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_12)
        #
        Layout_Page2_Left_12 = PQW.QHBoxLayout()
        Label_Gamma = PQW.QLabel('\u03B3:')
        Page2.Gamma = PQW.QLineEdit(self)
        Page2.Gamma.setText('0.6653')
        Layout_Page2_Left_12.addWidget(Label_Gamma)
        Layout_Page2_Left_12.addWidget(Page2.Gamma)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_12)
        #
        Layout_Page2_Left_13 = PQW.QHBoxLayout()
        Label_Diffusivity = PQW.QLabel('Diffusivity (m<sup>2</sup> s<sup>-1</sup>):')
        Layout_Page2_Left_13.addWidget(Label_Diffusivity)
        Page2.Diffusivity = PQW.QLineEdit()
        Page2.Diffusivity.setText('5e-07')
        Page2.Diffusivity.setEnabled(False)
        Layout_Page2_Left_13.addWidget(Page2.Diffusivity)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_13)
        #
        Layout_Page2_Left_14 = PQW.QHBoxLayout()
        Label_Velocity = PQW.QLabel('Velocity (m s<sup>-1</sup>):')
        Layout_Page2_Left_14.addWidget(Label_Velocity)
        Page2.Velocity = PQW.QLineEdit()
        Page2.Velocity.setText('6e-06')
        Page2.Velocity.setEnabled(False)
        Layout_Page2_Left_14.addWidget(Page2.Velocity)
        Layout_Page2_Left.addLayout(Layout_Page2_Left_14)
        #
        #! Page2.CheckBox_MLEnZ = PQW.QCheckBox('Use MLEnZ')
        #! Page2.CheckBox_MLEnZ.toggled.connect(Page2.MLEnZChange)
        #! Label_BedRiv = PQW.QLabel('Ber-River:')
        #! Page2.BedRiv = PQW.QLineEdit()
        #! Page2.BedRiv.setText('0.0')
        #! Page2.BedRiv.setEnabled(False)
        #! Label_BedRivUnit = PQW.QLabel('m')
        #! Label_d50 = PQW.QLabel('d50:')
        #! Page2.d50 = PQW.QLineEdit()
        #! Page2.d50.setText('0.001')
        #! Page2.d50.setEnabled(False)
        #! Label_d50Unit = PQW.QLabel('m')
        # Groupbox Sensors
        Page2.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
        # Create Layout for the Groupbox Sensor
        Page2.VBoxSensor = PQW.QGridLayout()
        Page2.GroupBox_Sensors.setLayout(Page2.VBoxSensor)
        Layout_Page2_Left.addWidget(Page2.GroupBox_Sensors)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Page2_Left)
        # Chart column
        container_right = PQW.QFrame()
        Layout_Page2_Right = PQW.QVBoxLayout()
        Page2.Chart_Fig = plt.figure()
        Page2.Canvas = FigureCanvas(self.Chart_Fig)
        self.Toolbar = NavigationToolbar(self.Canvas, self)
        Layout_Page2_Right.addWidget(self.Toolbar)
        Layout_Page2_Right.addWidget(Page2.Canvas)
        #
        container_right.setLayout(Layout_Page2_Right)
        #
        Layout_Page2.addWidget(container_left)
        Layout_Page2.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Page2)
        #
        df_Clean = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
        ChartColumns = (df_Clean.columns).tolist()
        Page2.Chart_Fig.clear()
        Page2.ax = Page2.Chart_Fig.add_subplot(111)
        #
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
            if len(Colors) != len(ChartColumns):
                Colors = []
                VAR.SetChartColors(VAR,None)
        #
        for i in range(1,len(ChartColumns)): #!
            if(VAR.GetChartColors(VAR) == None):
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page2.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                elif Page1.TimeType == 'Time':
                    plot = Page2.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                Colors.append(plot[0].get_color())
            else:
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page2.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
                elif Page1.TimeType == 'Time':
                    plot = Page2.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
        #
        if(VAR.GetChartColors(VAR) is None):
            VAR.SetChartColors(VAR, Colors)
        #
        Page2.ax.legend(loc=9, ncol=len(ChartColumns)) # Add legend to the chart
        #
        Page2.ax.grid(True, which='both', axis='both', linestyle='--')
        Page2.ax.set_ylabel('Temperature')
        #
        if Page1.TimeType == 'Time':
            Page2.ax.set_xlabel('Time (s)')
        else:
            pass
        Page2.Canvas.draw()

    @logger.catch
    def MLEnZChange(self):
#         if Page2.CheckBox_MLEnZ.isChecked():
#             Page2.BedRiv.setEnabled(True)
#             Page2.d50.setEnabled(True)
#             Page2.Combobox_Estimate.setCurrentText('D and V')
#             Page2.Combobox_Estimate.setEnabled(False)
#         else:
#             Page2.BedRiv.setEnabled(False)
#             Page2.d50.setEnabled(False)
#             Page2.Combobox_Estimate.setEnabled(True)
        return

    @logger.catch
    def on_Combobox_Estimate_change(self):
        logger.debug('Page1 - on_Combobox_Estimate_change')
        if Page2.Combobox_Estimate.currentText() == 'D and V':
            Page2.Diffusivity.setEnabled(False)
            Page2.Velocity.setEnabled(False)
        elif Page2.Combobox_Estimate.currentText() == 'D':
            Page2.Diffusivity.setEnabled(False)
            Page2.Velocity.setEnabled(True)
        elif Page2.Combobox_Estimate.currentText() == 'V':
            Page2.Diffusivity.setEnabled(True)
            Page2.Velocity.setEnabled(False)

    @logger.catch
    def on_Combobox_Frequency_change(self):
        logger.debug('Page1 - on_Combobox_Frequency_change')
        if Page2.Combobox_Frequency.currentText() == 'Best Frequency':
            Page2.SNRLimit.setEnabled(False)
        elif Page2.Combobox_Frequency.currentText() == 'Best 5 Frequencies':
            Page2.SNRLimit.setEnabled(False)
        elif Page2.Combobox_Frequency.currentText() == 'All Frequencies >':
            Page2.SNRLimit.setEnabled(True)

    @logger.catch
    def on_checkbox_changed(self,state):
        if state == 2: # Checked
            Page2.cp_w.setEnabled(True)
            Page2.cp_s.setEnabled(True)
            Page2.rho_w.setEnabled(True)
            Page2.rho_s.setEnabled(True)
            Page2.poros.setEnabled(True)
            Page2.Gamma.setEnabled(False)
        else:
            Page2.cp_w.setEnabled(False)
            Page2.cp_s.setEnabled(False)
            Page2.rho_w.setEnabled(False)
            Page2.rho_s.setEnabled(False)
            Page2.poros.setEnabled(False)
            Page2.Gamma.setEnabled(True)
        return

    @logger.catch
    def CalculateGamma(self):
        Page2.cp_w.textChanged.disconnect(self.CalculateGamma)
        Page2.cp_s.textChanged.disconnect(self.CalculateGamma)
        Page2.rho_w.textChanged.disconnect(self.CalculateGamma)
        Page2.rho_s.textChanged.disconnect(self.CalculateGamma)
        Page2.poros.textChanged.disconnect(self.CalculateGamma)
        try:
            cpw = float(Page2.cp_w.text())
            cps = float(Page2.cp_s.text())
            row = float(Page2.rho_w.text())
            ros = float(Page2.rho_s.text())
            n = float(Page2.poros.text())
        except:
            logger.critical("Error")
        #
        if cpw < 0.0:
            cpw = 0.0
            Page2.cp_w.setText(f"{cpw}")
        if cps < 0.0:
            cps = 0.0
            Page2.cp_s.setText(f"{cps}")
        if row < 0.0:
            row = 0.0
            Page2.rho_w.setText(f"{row}")
        if ros < 0.0:
            ros = 0.0
            Page2.rho_s.setText(f"{ros}")
        if n < 0.0:
            n = 0.0
            Page2.poros.setText(f"{n}")
        if n > 1.0:
            n = 1.0
            Page2.poros.setText(f"{n}")
        #
        Page2.Gamma.setText(f"{(n * cpw * row + (1 - n) * cps * ros) /(cpw * row)}")
        #
        Page2.cp_w.textChanged.connect(self.CalculateGamma)
        Page2.cp_s.textChanged.connect(self.CalculateGamma)
        Page2.rho_w.textChanged.connect(self.CalculateGamma)
        Page2.rho_s.textChanged.connect(self.CalculateGamma)
        Page2.poros.textChanged.connect(self.CalculateGamma)
        return

'''
Page 3 of the wizard
'''
class Page3(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page3, self).__init__(parent)
        # Create grid layot for the window
        Layout_Page3 = PQW.QHBoxLayout()
        # Left column
        container_left = PQW.QFrame()
        Layout_Page3_Left = PQW.QVBoxLayout()
        #
        Label_Period = PQW.QLabel('Period:')
        Layout_Page3_Left.addWidget(Label_Period)
        Page3.Combobox_Period = PQW.QComboBox() # Combobox period
        Layout_Page3_Left.addWidget(Page3.Combobox_Period)
        # 
        Label_BRE = PQW.QLabel('Ber river elevation (m):')
        Layout_Page3_Left.addWidget(Label_BRE)
        Page3.BedElev = PQW.QLineEdit(self)
        Layout_Page3_Left.addWidget(Page3.BedElev)
        Label_TopSens = PQW.QLabel('TopSensor:')
        Layout_Page3_Left.addWidget(Label_TopSens)
        Page3.Combobox_TopSensor = PQW.QComboBox() # Combobox TopSensor
        Layout_Page3_Left.addWidget(Page3.Combobox_TopSensor)
        # Groupbox Sensors
        Page3.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
        # Create Layout for the Groupbox Sensor
        Page3.VBoxSensor = PQW.QGridLayout()
        Page3.GroupBox_Sensors.setLayout(Page3.VBoxSensor)
        Layout_Page3_Left.addWidget(Page3.GroupBox_Sensors)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Page3_Left)
        # Chart Column
        container_right = PQW.QFrame()
        Layout_Page3_Right = PQW.QVBoxLayout()
        Page3.Chart_Fig = plt.figure()
        Page3.Canvas = FigureCanvas(Page3.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page3.Canvas, self)
        Layout_Page3_Right.addWidget(self.Toolbar)
        Layout_Page3_Right.addWidget(Page3.Canvas)
        #
        container_right.setLayout(Layout_Page3_Right)
        #
        Layout_Page3.addWidget(container_left)
        Layout_Page3.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Page3)
        #
        df_Clean = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
        ChartColumns = (df_Clean.columns).tolist()
        Page3.Chart_Fig.clear()
        Page3.ax = Page3.Chart_Fig.add_subplot(111)
        #
        if(VAR.GetChartColors(VAR) is None):
            Colors = []
        else:
            Colors = VAR.GetChartColors(VAR)
        #
        for i in range(1,len(ChartColumns)-1):
            if(VAR.GetChartColors(VAR) == None):
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page3.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                elif Page1.TimeType == 'Time':
                    plot = Page3.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i])
                Colors.append(plot[0].get_color())
            else:
                if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                    plot = Page3.ax.plot(pd.to_datetime(df_Clean['Time'],unit='s').to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
                elif Page1.TimeType == 'Time':
                    plot = Page3.ax.plot(df_Clean['Time'].to_numpy(), df_Clean[ChartColumns[i]].to_numpy(), '-', label = ChartColumns[i], color=Colors[i])
        #
        if(VAR.GetChartColors(VAR) is None):
            VAR.SetChartColors(VAR, Colors)
        #
        Page3.ax.legend()
        #
        Page3.ax.grid(True, which='both', axis='both', linestyle='--')
        Page3.ax.set_ylabel('Temperature')
        #
        if Page1.TimeType == 'Time':
            Page3.ax.set_xlabel('Time (s)')
        else:
            pass
        Page3.Canvas.draw()

'''
Page 4 of the wizard
'''
# The above class is a Python class that represents a page in a wizard interface,
# specifically Page 4, which contains various widgets and functionality related to
# charting and calculating the value of Ke.
class Page4(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page4, self).__init__(parent)
        # Create layot for the window
        Layout_Page4 = PQW.QHBoxLayout()
        # Left column
        container_left = PQW.QFrame()
        Layout_Page4_Left = PQW.QVBoxLayout()
        #
        Layout_Page4_Left_1 = PQW.QHBoxLayout()
        Label_Chart = PQW.QLabel('Chart:')
        Page4.Combobox_Chart = PQW.QComboBox() # Combobox period
        Page4.Combobox_Chart.addItem('Ke')
        Page4.Combobox_Chart.addItem('Eta')
        # Page4.Combobox_Chart.currentIndexChanged.connect(self.Chart) # ComboBox event change item
        Layout_Page4_Left_1.addWidget(Label_Chart)
        Layout_Page4_Left_1.addWidget(Page4.Combobox_Chart)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_1)
        #
        Page4.CheckBox_Calculate_Gamma = PQW.QCheckBox("Calculate \u03B3")
        Page4.CheckBox_Calculate_Gamma.stateChanged.connect(self.on_checkbox_changed)
        Layout_Page4_Left.addWidget(Page4.CheckBox_Calculate_Gamma)
        #
        Layout_Page4_Left_2 = PQW.QHBoxLayout()
        Label_Cpw = PQW.QLabel(f"c<sub>w</sub> (J kg<sup>-1</sup> K<sup>-1</sup>):")
        Page4.cp_w = PQW.QLineEdit(self)
        Page4.cp_w.setText("4183")
        Page4.cp_w.textChanged.connect(self.CalculateGamma)
        Page4.cp_w.setEnabled(False)
        Layout_Page4_Left_2.addWidget(Label_Cpw)
        Layout_Page4_Left_2.addWidget(Page4.cp_w)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_2)
        #
        Layout_Page4_Left_3 = PQW.QHBoxLayout()
        Label_Cps = PQW.QLabel(f"c<sub>s</sub> (J kg<sup>-1</sup> K<sup>-1</sup>):")
        Page4.cp_s = PQW.QLineEdit(self)
        Page4.cp_s.setText("800")
        Page4.cp_s.textChanged.connect(self.CalculateGamma)
        Page4.cp_s.setEnabled(False)
        Layout_Page4_Left_3.addWidget(Label_Cps)
        Layout_Page4_Left_3.addWidget(Page4.cp_s)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_3)
        #
        Layout_Page4_Left_4 = PQW.QHBoxLayout()
        Label_Rhow = PQW.QLabel(f"ρ<sub>w</sub> (kg m<sup>-3</sup>):")
        Page4.rho_w = PQW.QLineEdit(self)
        Page4.rho_w.setText("998")
        Page4.rho_w.textChanged.connect(self.CalculateGamma)
        Page4.rho_w.setEnabled(False)
        Layout_Page4_Left_4.addWidget(Label_Rhow)
        Layout_Page4_Left_4.addWidget(Page4.rho_w)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_4)
        #
        Layout_Page4_Left_5 = PQW.QHBoxLayout()
        Label_Rhos = PQW.QLabel(f"ρ<sub>s</sub> (kg m<sup>-3</sup>):")
        Page4.rho_s = PQW.QLineEdit(self)
        Page4.rho_s.setText("2650")
        Page4.rho_s.textChanged.connect(self.CalculateGamma)
        Page4.rho_s.setEnabled(False)
        Layout_Page4_Left_5.addWidget(Label_Rhos)
        Layout_Page4_Left_5.addWidget(Page4.rho_s)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_5)
        #
        Layout_Page4_Left_6 = PQW.QHBoxLayout()
        Label_poros = PQW.QLabel(f"n:")
        Page4.poros = PQW.QLineEdit(self)
        Page4.poros.setText("0.32")
        Page4.poros.textChanged.connect(self.CalculateGamma)
        Page4.poros.setEnabled(False)
        Layout_Page4_Left_6.addWidget(Label_poros)
        Layout_Page4_Left_6.addWidget(Page4.poros)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_6)
        #
        Layout_Page4_Left_7 = PQW.QHBoxLayout()
        Label_Gamma = PQW.QLabel('\u03B3:')
        Page4.Gamma = PQW.QLineEdit(self)
        Page4.Gamma.setText('0.6653')
        Layout_Page4_Left_7.addWidget(Label_Gamma)
        Layout_Page4_Left_7.addWidget(Page4.Gamma)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_7)
        #
        Layout_Page4_Left_8 = PQW.QHBoxLayout()
        Label_BRE2 = PQW.QLabel('Bed River Elevation:')
        Page4.BRE2 = PQW.QLineEdit(self)
        # Page4.BRE2.setText(Page1.SensorsHeight[0])
        Layout_Page4_Left_8.addWidget(Label_BRE2)
        Layout_Page4_Left_8.addWidget(Page4.BRE2)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_8)
        #
        Label_SBR = PQW.QLabel('Fixed bedriver')
        Layout_Page4_Left.addWidget(Label_SBR)
        #
        Label_From = PQW.QLabel('From:')
        Label_To = PQW.QLabel('To:')
        #
        if Page1.TimeType == 'Time':
            Page4.ImpoFrom = PQW.QSpinBox(self)
            Page4.ImpoTo = PQW.QSpinBox(self)
        else:
            Page4.ImpoFrom = PQW.QDateTimeEdit(self)
            Page4.ImpoTo = PQW.QDateTimeEdit(self)
        #
        Layout_Page4_Left_9 = PQW.QHBoxLayout()
        Layout_Page4_Left_10 = PQW.QHBoxLayout()
        Layout_Page4_Left_9.addWidget(Label_From)
        Layout_Page4_Left_9.addWidget(Page4.ImpoFrom)
        Layout_Page4_Left_10.addWidget(Label_To)
        Layout_Page4_Left_10.addWidget(Page4.ImpoTo)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_9)
        Layout_Page4_Left.addLayout(Layout_Page4_Left_10)
        # 
        Label_Ke = PQW.QLabel('Ke:')
        Layout_Page4_Left.addWidget(Label_Ke)
        #
        Page4.Button_KE = PQW.QPushButton('Calculate Ke')
        # Page4.Button_KE.setToolTip('Launch Calculate Ke') # Tooltip message
        Page4.Button_KE.clicked.connect(self.on_Button_KE_clicked) # Button event Click on
        Layout_Page4_Left.addWidget(Page4.Button_KE)
        #
        Page4.Table_Stat = PQW.QTableWidget()
        Page4.Table_Stat.setColumnCount(2)
        Page4.Table_Stat.setHorizontalHeaderLabels(['Sensor', 'Ke'])
        Layout_Page4_Left.addWidget(Page4.Table_Stat)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Page4_Left)
        # Chart Columns
        container_right = PQW.QFrame()
        Layout_Page4_Right = PQW.QVBoxLayout()
        Page4.Chart_Fig = plt.figure()
        Page4.Canvas = FigureCanvas(Page4.Chart_Fig)
        self.Toolbar = NavigationToolbar(Page4.Canvas, self)
        Layout_Page4_Right.addWidget(self.Toolbar)
        Layout_Page4_Right.addWidget(Page4.Canvas)
        #
        container_right.setLayout(Layout_Page4_Right)
        #
        Layout_Page4.addWidget(container_left)
        Layout_Page4.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Page4)
        #
        self.Chart()

    @logger.catch
    def on_checkbox_changed(self,state):
        if state == 2: # Checked
            Page4.cp_w.setEnabled(True)
            Page4.cp_s.setEnabled(True)
            Page4.rho_w.setEnabled(True)
            Page4.rho_s.setEnabled(True)
            Page4.poros.setEnabled(True)
            Page4.Gamma.setEnabled(False)
        else:
            Page4.cp_w.setEnabled(False)
            Page4.cp_s.setEnabled(False)
            Page4.rho_w.setEnabled(False)
            Page4.rho_s.setEnabled(False)
            Page4.poros.setEnabled(False)
            Page4.Gamma.setEnabled(True)
        return

    @logger.catch
    def CalculateGamma(self):
        Page4.cp_w.textChanged.disconnect(self.CalculateGamma)
        Page4.cp_s.textChanged.disconnect(self.CalculateGamma)
        Page4.rho_w.textChanged.disconnect(self.CalculateGamma)
        Page4.rho_s.textChanged.disconnect(self.CalculateGamma)
        Page4.poros.textChanged.disconnect(self.CalculateGamma)
        try:
            cpw = float(Page4.cp_w.text())
            cps = float(Page4.cp_s.text())
            row = float(Page4.rho_w.text())
            ros = float(Page4.rho_s.text())
            n = float(Page4.poros.text())
        except:
            logger.critical("Error")
        #
        if cpw < 0.0:
            cpw = 0.0
            Page4.cp_w.setText(f"{cpw}")
        if cps < 0.0:
            cps = 0.0
            Page4.cp_s.setText(f"{cps}")
        if row < 0.0:
            row = 0.0
            Page4.rho_w.setText(f"{row}")
        if ros < 0.0:
            ros = 0.0
            Page4.rho_s.setText(f"{ros}")
        if n < 0.0:
            n = 0.0
            Page4.poros.setText(f"{n}")
        if n > 1.0:
            n = 1.0
            Page4.poros.setText(f"{n}")
        #
        Page4.Gamma.setText(f"{(n * cpw * row + (1 - n) * cps * ros) /(cpw * row)}")
        #
        Page4.cp_w.textChanged.connect(self.CalculateGamma)
        Page4.cp_s.textChanged.connect(self.CalculateGamma)
        Page4.rho_w.textChanged.connect(self.CalculateGamma)
        Page4.rho_s.textChanged.connect(self.CalculateGamma)
        Page4.poros.textChanged.connect(self.CalculateGamma)
        return

    @logger.catch
    def on_Button_KE_clicked(self):
        """
        The function `on_Button_KE_clicked` opens a dialog window, reads data from a
        log file, and populates a table with the data.
        """
        logger.debug('on_Button_KE_clicked')
        WizardKe = WKE.EtaKeMeanCalc()
        WizardKe.exec_()
        #
        Handle = open('../temp/Ke.log','r')
        Rows = Handle.readlines()
        Handle.close()
        #
        Page4.Table_Stat.setRowCount(len(Rows)-2)
        #
        for i in range(1,len(Rows)-1):
            itemTable = PQW.QTableWidgetItem(Rows[i].split(',')[0])
            itemTable.setFlags(PQC.Qt.ItemIsEnabled)
            Page4.Table_Stat.setItem(i-1,0, itemTable)
            itemTable = PQW.QTableWidgetItem(Rows[i].split(',')[1])
            Page4.Table_Stat.setItem(i-1,1, itemTable)

    @logger.catch
    def Chart(self):
        """
        The function `Chart` updates a chart based on the selected option in a combo
        box and displays it.
        """
        logger.debug('Update Chart')
        #
        Page4.Chart_Fig.clear()
        Page4.ax = Page4.Chart_Fig.add_subplot(111)
        #
        try:
            if Page4.Combobox_Chart.currentText() == 'Eta':
                df_Chart = pd.read_pickle('../temp/Eta.pkz',compression='zip')
            elif Page4.Combobox_Chart.currentText() == 'Ke':
                df_Chart = pd.read_pickle('../temp/Ke.pkz',compression='zip')
            #
            Columns = ((df_Chart.columns).tolist())[1:]
            #
            if(VAR.GetChartColors(VAR) is None):
                Colors = []
            else:
                Colors = VAR.GetChartColors(VAR)
                #
            for i in range(1,len(Columns)):
                if(VAR.GetChartColors(VAR) == None):
                    if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                        plot = Page4.ax.plot(pd.to_datetime(df_Chart['Time'],unit='s').to_numpy(), df_Chart[Columns[i]].to_numpy(), '-', label = Columns[i])
                    elif Page1.TimeType == 'Time':
                        plot = Page4.ax.plot(df_Chart['Time'].to_numpy(), df_Chart[Columns[i]].to_numpy(), '-', label = Columns[i])
                    Colors.append(plot[0].get_color())
                else:
                    if Page1.TimeType == 'yyyy-mm-dd h24:min:sec':
                        plot = Page4.ax.plot(pd.to_datetime(df_Chart['Time'],unit='s').to_numpy(), df_Chart[Columns[i]].to_numpy(), '-', label = Columns[i], color=Colors[i])
                    elif Page1.TimeType == 'Time':
                        plot = Page4.ax.plot(df_Chart['Time'].to_numpy(), df_Chart[Columns[i]].to_numpy(), '-', label = Columns[i], color=Colors[i])
                #
            if(VAR.GetChartColors(VAR) is None):
                VAR.SetChartColors(VAR, Colors)
            #
            Page4.ax.legend(loc=9, ncol=len(Columns)) # Add legend to the chart
        except:
            pass
        #
        Page4.ax.grid(True, which='both', axis='both', linestyle='--')
        #
        if Page4.Combobox_Chart.currentText() == 'Eta':
            Page4.ax.set_ylabel('Eta')
        elif Page4.Combobox_Chart.currentText() == 'Ke':
            Page4.ax.set_ylabel('Ke')
        #
        if Page1.TimeType == 'Time':
            Page4.ax.set_xlabel('Time (s)')
        else:
            pass
        Page4.Canvas.draw()

'''
Page 5 of the wizard
'''
# The above class is a subclass of PQW.QWizardPage and it creates a grid layout
# for the window with a QLabel displaying "Page5 Finish".
class Page5(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page5, self).__init__(parent)
        # Create grid layot for the window
        Layout_Page5 = PQW.QGridLayout()
        # Project and Probe Active
        Label_PP5 = PQW.QLabel('Page5 Finish')
        # Insert elements in the grid
        Layout_Page5.addWidget(Label_PP5, 0, 0, 1, 1)