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
import os,sys
import PyQt5.QtWidgets as PQW
import PyQt5.QtGui as PQG
import PyQt5.QtCore as PQC
# from PyQt5.QtWidgets import QMessageBox
# import numpy as np
##from sklearn.linear_model import LinearRegression

# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import datetime
# import shutil
# import math
# import glob
# Import custom library

# import TabKeMean as TKM

from Variables import VAR
# from TabProbeVariable import TPVAR
# from WFLVariables import WFLVAR
# from TabKeMeanVaraibles import TKMVAR

class EtaKeMeanCalc(PQW.QWizard):
    def __init__(self, parent=None):
        super(EtaKeMeanCalc, self).__init__(parent)
        self.addPage(Page1(self))
        #self.addPage(Page2(self))
        self.setWindowTitle('FFT Calculate')

        self.resize(800,600)

        self.button(PQW.QWizard.NextButton).clicked.connect(self.next_print)
        self.button(PQW.QWizard.FinishButton).clicked.connect(self.finish_print)


#------------------------------------------------------------------------------#
    def next_print(self):
        # print('Next',self.currentId())
        #


        #
        return

#------------------------------------------------------------------------------#
    def finish_print(self):
        # print('finish_print')
        #TKM.TabKeMean.TKMUpdate(TKM.TabKeMean)
        return


#------------------------------------------------------------------------------#
'''
First page of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        #
        HandleLog = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/probe.ini')
        HandleLog.readline()
        HandleLog.readline()
        self.TimeType = HandleLog.readline().split(';')[0] #
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
        #
        Page1.df_Ke = pd.read_pickle('../temp/Ke.pkz',compression='zip')
        #
        Label_From = PQW.QLabel('From:')
        if self.TimeType == 'Time':
            # If timeserie is Time format
            Page1.FromDateTime = PQW.QDoubleSpinBox()
            Page1.FromDateTime.setMinimum(Page1.df_Ke['Time'].min())
            Page1.FromDateTime.setMaximum(Page1.df_Ke['Time'].max())
            Page1.FromDateTime.setValue(Page1.df_Ke['Time'].min())
            Label_To = PQW.QLabel('To:')
            Page1.ToDateTime = PQW.QDoubleSpinBox()
            Page1.ToDateTime.setMinimum(Page1.df_Ke['Time'].min())
            Page1.ToDateTime.setMaximum(Page1.df_Ke['Time'].max())
            Page1.ToDateTime.setValue(Page1.df_Ke['Time'].max())
            Page1.FromDateTime.valueChanged.connect(Page1.Update)
            Page1.ToDateTime.valueChanged.connect(Page1.Update)
        else:
            # If timeserie is DateTime format
            Page1.FromDateTime = PQW.QDateTimeEdit()
            Page1.FromDateTime.setCalendarPopup(True)
            Page1.FromDateTime.setDateTime(pd.to_datetime(Page1.df_Ke['Time'].min(), unit='s'))
            Page1.FromDateTime.dateTimeChanged.connect(Page1.Update)
            Label_To = PQW.QLabel('To:')
            Page1.ToDateTime = PQW.QDateTimeEdit()
            Page1.ToDateTime.setCalendarPopup(True)
            Page1.ToDateTime.setDateTime(pd.to_datetime(Page1.df_Ke['Time'].max(), unit='s'))
            Page1.ToDateTime.dateTimeChanged.connect(Page1.Update)
        #
        Page1.Table_Stat = PQW.QTableWidget()
        Page1.Table_Stat.setColumnCount(3)
        Page1.Table_Stat.setHorizontalHeaderLabels(['Sensor', 'Mean', 'Std'])
        #
        Page1.Label_KeMean = PQW.QLabel('Ke Mean:')
        # Create layout and add element to the layout
        Layout = PQW.QGridLayout()
        Layout.addWidget(Label_From,0,0)
        Layout.addWidget(Page1.FromDateTime,0,1)
        Layout.addWidget(Label_To,1,0)
        Layout.addWidget(Page1.ToDateTime,1,1)
        Layout.addWidget(Page1.Label_KeMean,2,0,1,2)
        Layout.addWidget(Page1.Table_Stat,0,3,3,1)
        # Show layout
        self.setLayout(Layout)
        #
        self.Update()

    def Update(self):
        #
        # print('Update')
        Handle = open('../temp/Ke.log','w')
        Page1.Table_Stat.setRowCount(0)
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
        if TimeType == 'Time':
            # from_date = pd.Timestamp(Page1.FromDateTime.value(), unit='s')
            # to_date = pd.Timestamp(Page1.ToDateTime.value(), unit='s')
            from_date = Page1.FromDateTime.value()
            to_date = Page1.ToDateTime.value()
            Handle.write(str(from_date)+','+str(to_date)+'\n')
        else:
            from_date = datetime.datetime.timestamp(Page1.FromDateTime.dateTime().toPyDateTime())
            to_date = datetime.datetime.timestamp(Page1.ToDateTime.dateTime().toPyDateTime())
            Handle.write(str(from_date)+','+str(to_date)+'\n')
        #
        # print(Page1.df_Ke)
        df_Ke_Rid = Page1.df_Ke.loc[(Page1.df_Ke['Time'] >= from_date) & (Page1.df_Ke['Time'] <= to_date)]
        # print(df_Ke_Rid)
        stats = df_Ke_Rid.describe()
        # print(stats)
        #
        Page1.Table_Stat.setRowCount(len(df_Ke_Rid.describe().columns)-1)
        Mean = 0.0
        for i,item in enumerate(df_Ke_Rid.describe().columns):
            if i == 0:
                pass
            else:
                itemTable = PQW.QTableWidgetItem(item)
                itemTable.setFlags(PQC.Qt.ItemIsEnabled)
                Page1.Table_Stat.setItem(i-1,0, itemTable)
                Handle.write(item+',')
                #
                itemTable = PQW.QTableWidgetItem(str("{:e}".format(stats.loc['mean' , item])))
                itemTable.setFlags(PQC.Qt.ItemIsEnabled)
                Page1.Table_Stat.setItem(i-1,1, itemTable)
                Handle.write(str("{:e}".format(stats.loc['mean' , item]))+',')
                Mean = Mean + stats.loc['mean' , item]
                itemTable = PQW.QTableWidgetItem(str("{:e}".format(stats.loc['std' , item])))
                itemTable.setFlags(PQC.Qt.ItemIsEnabled)
                Page1.Table_Stat.setItem(i-1,2, itemTable)
                Handle.write(str("{:e}".format(stats.loc['std' , item]))+'\n')
        #
        Mean = Mean / (len(df_Ke_Rid.describe().columns)-1)
        Page1.Label_KeMean.setText('Ke Mean: '+str("{:e}".format(Mean)))
        Handle.write(str("{:e}".format(Mean))+'\n')
        #
        Handle.close()
        #
        return

'''
Second page of the wizard
'''
class Page2(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        Page2.Label1 = PQW.QLabel('Finish')
        # Create layout and add element to the layout
        Layout = PQW.QGridLayout()
        Layout.addWidget(self.Label1,0,0)
        # Show layout
        self.setLayout(Layout)







