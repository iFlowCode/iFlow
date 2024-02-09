#------------------------------------------------------------------------------#
# Name:        software
# Purpose:
#
# Author:      Bert8301
#
# Created:     01/27/2020
# Copyright:   (c) Bert8301 2020
#              Center for Ecohydraulics Research
#              University of Idaho
# Licence:     <your licence>
#------------------------------------------------------------------------------#
# Import standard library
# import os,sys
import PyQt5.QtWidgets as PQW
# import PyQt5.QtGui as PQG
import PyQt5.QtCore as PQC
# from PyQt5.QtWidgets import QMessageBox
# import numpy as np
##from sklearn.linear_model import LinearRegression

# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
# import pandas as pd
# import datetime
# import shutil
# import math
# import glob
# Import custom library

# import TabKeMean as TKM

from Variables import VAR
from Options import OPT
# from TabProbeVariable import TPVAR
# from WFLVariables import WFLVAR
# from TabKeMeanVaraibles import TKMVAR

class ManageHarmonics(PQW.QWizard):
    def __init__(self, parent=None):
        super(ManageHarmonics, self).__init__(parent)
        self.addPage(Page1(self))
        #self.addPage(Page2(self))
        self.setWindowTitle('Manage Harmonics')

        self.resize(800,600)

        # self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print)
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print)


#------------------------------------------------------------------------------#
    # def next_print(self):
    #     print('Next',self.currentId())
    #     #


    #     #
    #     return

#------------------------------------------------------------------------------#
    def finish_print(self):
        print('finish_print')
        #TKM.TabKeMean.TKMUpdate(TKM.TabKeMean)
        return


#------------------------------------------------------------------------------#
'''
First page of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        # Create grid layot for the window
        Layout = PQW.QGridLayout()
        self.GroupBox_Add = PQW.QGroupBox('Add Harmonic')
        self.HBoxAdd = PQW.QHBoxLayout()
        Page1.HarmAdd_Value = PQW.QLineEdit()
        Page1.Combobox_HarmAdd_Unit = PQW.QComboBox()
        Page1.Combobox_HarmAdd_Unit.addItem('day')
        Page1.Combobox_HarmAdd_Unit.addItem('hour')
        Page1.Combobox_HarmAdd_Unit.addItem('minute')
        Page1.Combobox_HarmAdd_Unit.addItem('second')
        Page1.Button_AddHarm = PQW.QPushButton('Add Harmonic')
        Page1.Button_AddHarm.clicked.connect(self.on_Button_AddHarm_clicked) # Button event Click on
        self.HBoxAdd.addWidget(Page1.HarmAdd_Value)
        self.HBoxAdd.addWidget(Page1.Combobox_HarmAdd_Unit)
        self.HBoxAdd.addWidget(Page1.Button_AddHarm)
        self.GroupBox_Add.setLayout(self.HBoxAdd)
        #
        self.GroupBox_Del = PQW.QGroupBox('Delete Harmonic')
        self.HBoxDel = PQW.QHBoxLayout()
        Page1.Combobox_HarmDel_Value = PQW.QComboBox()
        Page1.Button_DelHarm = PQW.QPushButton('Delete Harmonic')
        Page1.Button_DelHarm.clicked.connect(self.on_Button_DelHarm_clicked) # Button event Click on
        self.HBoxDel.addWidget(Page1.Combobox_HarmDel_Value)
        self.HBoxDel.addWidget(Page1.Button_DelHarm)
        self.GroupBox_Del.setLayout(self.HBoxDel)
        #
        self.GroupBox_LaS = PQW.QGroupBox('Load/Save Harmonic')
        self.HBoxLaS = PQW.QHBoxLayout()
        Page1.Button_LoadHarm = PQW.QPushButton('Load Harmonic')
        Page1.Button_LoadHarm.clicked.connect(self.on_Button_LoadHarm_clicked) # Button event Click on
        Page1.Button_SaveHarm = PQW.QPushButton('Save Harmonic')
        Page1.Button_SaveHarm.clicked.connect(self.on_Button_SaveHarm_clicked) # Button event Click on
        self.HBoxLaS.addWidget(Page1.Button_LoadHarm)
        self.HBoxLaS.addWidget(Page1.Button_SaveHarm)
        self.GroupBox_LaS.setLayout(self.HBoxLaS)
        #
        Page1.Table_Harmonic = PQW.QTableWidget()
        Page1.Table_Harmonic.setRowCount(0)
        Page1.Table_Harmonic.setColumnCount(2)
        Page1.Table_Harmonic.setHorizontalHeaderLabels(['n', 'Harmonic'])
        # Insert element in the grid
        Layout.addWidget(self.GroupBox_Add,0,0,2,2)
        Layout.addWidget(self.GroupBox_Del,2,0,2,2)
        Layout.addWidget(self.GroupBox_LaS,4,0,2,2)
        Layout.addWidget(Page1.Table_Harmonic,0,2,6,3)
        # Set layout of tab
        self.setLayout(Layout)
        #
        self.Update()

    def Update(self):
        #
        print('Update')
        # Load Harmonics
        Harmonics = OPT.GetHarmonics(OPT)
        # GroupBox DELETE
        Page1.Combobox_HarmDel_Value.clear()
        if len(Harmonics) != 0:
            for Harm in Harmonics:
                Page1.Combobox_HarmDel_Value.addItem(str(Harm))
        #
        Page1.Table_Harmonic.setRowCount(0)
        Page1.Table_Harmonic.setRowCount(len(Harmonics))
        Page1.Table_Harmonic.setColumnCount(2)
        Page1.Table_Harmonic.setHorizontalHeaderLabels(['n', 'Harmonic (s)'])
        if len(Harmonics) != 0:
            for i,Harm in enumerate(Harmonics):
                item = PQW.QTableWidgetItem(str(i))
                item2 = PQW.QTableWidgetItem(str(Harm))
                item.setFlags(PQC.Qt.ItemIsEnabled)
                item2.setFlags(PQC.Qt.ItemIsEnabled)
                Page1.Table_Harmonic.setItem(i,0, item)
                Page1.Table_Harmonic.setItem(i,1, item2)
        #
        return

    def on_Button_AddHarm_clicked(self):
        # Check if number
        NewHarm = float(Page1.HarmAdd_Value.text())
        HarmList = OPT.GetHarmonics(OPT)
        # Units
        if Page1.Combobox_HarmAdd_Unit.currentText() == 'day':
            NewHarm = NewHarm * 24.0 * 3600.0
        elif Page1.Combobox_HarmAdd_Unit.currentText() == 'hour':
            NewHarm = NewHarm * 3600.0
        elif Page1.Combobox_HarmAdd_Unit.currentText() == 'minute':
            NewHarm = NewHarm * 60.0
        elif Page1.Combobox_HarmAdd_Unit.currentText() == 'second':
            pass
        # Check if already insert
        try:
            pos = HarmList.index(NewHarm)
            Page1.HarmAdd_Value.setText('')
        except:
            HarmList.append(NewHarm)
            HarmList.sort(reverse=True)
            # Store in OPT
            OPT.SetHarmonics(OPT,HarmList)
            # Store in File
            Handle = open('../harmonics/harmonics.hrm','w')
            for Harm in HarmList:
                Handle.write(str(Harm)+'\n')
            Handle.close()
            # Clear field
            Page1.HarmAdd_Value.setText('')
            # Update
            self.Update()
        #
        return

    def on_Button_DelHarm_clicked(self):
        HarmList = OPT.GetHarmonics(OPT)
        try:
            pos = HarmList.index(float(Page1.Combobox_HarmDel_Value.currentText()))
            #
            del HarmList[pos]
            # Store in OPT
            OPT.SetHarmonics(OPT,HarmList)
            # Store in File
            Handle = open('../harmonics/harmonics.hrm','w')
            for Harm in HarmList:
                Handle.write(str(Harm)+'\n')
            Handle.close()
            # Clear field
            Page1.HarmAdd_Value.setText('')
            # Update
            self.Update()
        except:
            pass
        
        return

    def on_Button_LoadHarm_clicked(self):
        file_import = PQW.QFileDialog.getOpenFileName(self, 'Select harmonics file to load', '../exports/', 'HRM (*.hrm)')
        if file_import[0]:
            Handle = open(file_import[0],'r')
            Rows = Handle.readlines()
            Handle.close()
            #
            HarmList = []
            for Row in Rows:
                HarmList.append(float(Row.replace('\n','')))
            #
            OPT.SetHarmonics(OPT,HarmList)
            #
            self.Update()
        return

    def on_Button_SaveHarm_clicked(self):
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Save harmonic to File', '../exports/harmonics', 'HRM (*.hrm)')
        if file_export[0]:
            HarmList = OPT.GetHarmonics(OPT)
            Handle = open(file_export[0],'w')
            for Harm in HarmList:
                Handle.write(str(Harm)+'\n')
            Handle.close()
        return