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
# import matplotlib.pyplot as plt
# # import matplotlib.ticker as ticker
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# # from mpl_toolkits.mplot3d import Axes3D  
# import glob
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
# import pandas as pd
# # import pickle
# # import datetime
# # import time
# # import numpy as np
# # from matplotlib import cm
# # Import custom library
from Units import UNIT
from Variables import VAR
# # from Options import OPT
# from ScrollLabel import ScrollLabel
import TabSignProc as TSP
import TabProjProb as TPP
import TabFreqAnal as TFA
import TabParEst as TPE
import TabBrede as TB
# # import STabFFTAnal as STFA
# # import STabLPMAnal as STLA
# import WizardBH as WBH
from loguru import logger
#------------------------------------------------------------------------------#
'''
TabOptions Class
'''
class TabOptions(PQW.QWidget):
    def __init__(self):
        super().__init__()
        logger.debug('TabBrede - Start Class')
        # # Store class object
        # VAR.SetTabBrede(VAR, self)
        # Create grid layot for the window
        Layout_Tab_Options = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Tab_Options_left = PQW.QVBoxLayout()
        # Groupbox Project
        self.GroupBox_Units = PQW.QGroupBox('Units:')
        # Create the Layout for the Groupbox Project
        self.VBoxUnits = PQW.QVBoxLayout()
        # 
        self.HBoxTime = PQW.QHBoxLayout()
        Label_Time = PQW.QLabel("Time units:")
        TabOptions.Combobox_Time_Units = PQW.QComboBox()
        TabOptions.Combobox_Time_Units.addItem("s")
        TabOptions.Combobox_Time_Units.addItem("min")
        TabOptions.Combobox_Time_Units.addItem("h")
        TabOptions.Combobox_Time_Units.addItem("d")
        TabOptions.Combobox_Time_Units.setCurrentText(UNIT.GetTime(UNIT))
        TabOptions.Combobox_Time_Units.currentIndexChanged.connect(self.on_Combobox_Time_Units_change)
        self.HBoxTime.addWidget(Label_Time)
        self.HBoxTime.addWidget(TabOptions.Combobox_Time_Units)
        self.VBoxUnits.addLayout(self.HBoxTime)
        # 
        self.HBoxTemperature = PQW.QHBoxLayout()
        Label_Temperature = PQW.QLabel("Temperature units:")
        TabOptions.Combobox_Temperature_Units = PQW.QComboBox()
        TabOptions.Combobox_Temperature_Units.addItem("C")
        TabOptions.Combobox_Temperature_Units.addItem("K")
        TabOptions.Combobox_Temperature_Units.addItem("F")
        TabOptions.Combobox_Temperature_Units.setCurrentText(UNIT.GetTemperature(UNIT))
        TabOptions.Combobox_Temperature_Units.currentIndexChanged.connect(self.on_Combobox_Temperature_Units_change)
        self.HBoxTemperature.addWidget(Label_Temperature)
        self.HBoxTemperature.addWidget(TabOptions.Combobox_Temperature_Units)
        self.VBoxUnits.addLayout(self.HBoxTemperature)
        # 
        self.HBoxFrequency = PQW.QHBoxLayout()
        Label_Frequency = PQW.QLabel("Frequency units:")
        TabOptions.Combobox_Frequency_Units = PQW.QComboBox()
        TabOptions.Combobox_Frequency_Units.addItem("Hz")
        TabOptions.Combobox_Frequency_Units.addItem("d")
        TabOptions.Combobox_Frequency_Units.addItem("h")
        TabOptions.Combobox_Frequency_Units.setCurrentText(UNIT.GetFrequency(UNIT))
        TabOptions.Combobox_Frequency_Units.currentIndexChanged.connect(self.on_Combobox_Frequency_Units_change)
        self.HBoxFrequency.addWidget(Label_Frequency)
        self.HBoxFrequency.addWidget(TabOptions.Combobox_Frequency_Units)
        self.VBoxUnits.addLayout(self.HBoxFrequency)
        # 
        self.HBoxAngle = PQW.QHBoxLayout()
        Label_Angle = PQW.QLabel("Angle units:")
        TabOptions.Combobox_Angle_Units = PQW.QComboBox()
        TabOptions.Combobox_Angle_Units.addItem("rad")
        TabOptions.Combobox_Angle_Units.addItem("degree")
        TabOptions.Combobox_Angle_Units.setCurrentText(UNIT.GetAngle(UNIT))
        TabOptions.Combobox_Angle_Units.currentIndexChanged.connect(self.on_Combobox_Angle_Units_change)
        self.HBoxAngle.addWidget(Label_Angle)
        self.HBoxAngle.addWidget(TabOptions.Combobox_Angle_Units)
        self.VBoxUnits.addLayout(self.HBoxAngle)
        # 
        self.HBoxLenght = PQW.QHBoxLayout()
        Label_Lenght = PQW.QLabel("Lenght units:")
        TabOptions.Combobox_Lenght_Units = PQW.QComboBox()
        TabOptions.Combobox_Lenght_Units.addItem("m")
        TabOptions.Combobox_Lenght_Units.addItem("cm")
        TabOptions.Combobox_Lenght_Units.addItem("mm")
        TabOptions.Combobox_Lenght_Units.addItem("in")
        TabOptions.Combobox_Lenght_Units.addItem("ft")
        TabOptions.Combobox_Lenght_Units.setCurrentText(UNIT.GetLenght(UNIT))
        TabOptions.Combobox_Lenght_Units.currentIndexChanged.connect(self.on_Combobox_Lenght_Units_change)
        self.HBoxLenght.addWidget(Label_Lenght)
        self.HBoxLenght.addWidget(TabOptions.Combobox_Lenght_Units)
        self.VBoxUnits.addLayout(self.HBoxLenght)
        # Add the Layout to the Groupbox Project
        self.GroupBox_Units.setLayout(self.VBoxUnits)
        Layout_Tab_Options_left.addWidget(self.GroupBox_Units)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Tab_Options_left)
        #
        Layout_Tab_Options.addWidget(container_left)
        # Layout_Tab_ProjStac.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Tab_Options)

    def on_Combobox_Time_Units_change(self):
        UNIT.SetTime(UNIT,TabOptions.Combobox_Time_Units.currentText())
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)
        self.File_Update()
        #
        return
    
    def on_Combobox_Temperature_Units_change(self):
        UNIT.SetTemperature(UNIT,TabOptions.Combobox_Temperature_Units.currentText())
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)
        self.File_Update()
        #
        return
    
    def on_Combobox_Frequency_Units_change(self):
        UNIT.SetFrequency(UNIT,TabOptions.Combobox_Frequency_Units.currentText())
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)
        self.File_Update()
        #
        return
    
    def on_Combobox_Angle_Units_change(self):
        UNIT.SetAngle(UNIT,TabOptions.Combobox_Angle_Units.currentText())
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)
        self.File_Update()
        #
        return
    
    def on_Combobox_Lenght_Units_change(self):
        UNIT.SetLenght(UNIT,TabOptions.Combobox_Lenght_Units.currentText())
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)
        self.File_Update()
        #
        return
    
    def File_Update(self):
        print("UpdateFile")
        with open("../config/config.ini","r") as reader:
            lines = reader.readlines()
        #
        new_string = f""
        for i in range(0,9):
            new_string += lines[i]
        #
        new_string += f"{TabOptions.Combobox_Time_Units.currentText()},Time unit [s,min,h,d]\n"
        new_string += f"{TabOptions.Combobox_Temperature_Units.currentText()},Temperature unit [C,F,K]\n"
        new_string += f"{TabOptions.Combobox_Frequency_Units.currentText()},Frequency unit [Hz,d,h]\n"
        new_string += f"{TabOptions.Combobox_Angle_Units.currentText()},Angle unit [rad,degree]\n"
        new_string += f"{TabOptions.Combobox_Lenght_Units.currentText()},Lenght unit [m,cm,mm,in,ft]"
        #
        with open("../config/config.ini","w") as reader:
            reader.write(new_string)
        #
        return