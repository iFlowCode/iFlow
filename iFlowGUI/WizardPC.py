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
import matplotlib
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
import pytz
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()
# import subprocess
# import glob
import pickle
import time
from shutil import copyfile
import datetime
# Import custom library
from Variables import VAR
from Options import OPT
# from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
#                             MONTHS_PER_YEAR, DAYS_PER_WEEK,
#                             SEC_PER_HOUR, SEC_PER_DAY,
#                             num2date, rrulewrapper, YearLocator,
#                             MicrosecondLocator, warnings)
#%%
'''
Wizzard Add Probe Class
'''
class Phase(PQW.QWizard):
    def __init__(self, parent=None):
        super(Phase, self).__init__(parent)
        self.setWindowTitle('Phase Correction - '+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText())
        #
        width = int(VAR.GetWindowsSize(VAR)[0] * 0.9) # Width of the window
        height = int(VAR.GetWindowsSize(VAR)[1] * 0.9) # Height of the window
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
        copyfile('../temp/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz','../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz')
        os.remove('../temp/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz')
        return
#%%
    def finish_print(self):
        print("Action:finish Page: " + str(self.currentId()))
        #
        Page1.Phase.to_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
        os.remove('../temp/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz')
        return
        
#%%
'''
Page 1 of the wizard
'''
class Page1(PQW.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        # Copy file
        copyfile('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz','../temp/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz')
        # Load Data
        Page1.Phase = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.pkz',compression='zip')
    #     with open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/SPdata/'+VAR.GetTabSignProc(VAR).Combobox_Analysis.currentText().replace('Run: ','')+'_Phase.PdList','rb') as fPha:
    #         self.Phase = pickle.load(fPha)
    #     fPha.close()
        Columns = (Page1.Phase.columns.tolist())[1:]
        Freq = Page1.Phase['Freq'].drop_duplicates()
        Periods = (1.0/Freq/3600.0).tolist()
        # Page1.Time = Page1.Phase['Time'].drop_duplicates()
        #
        Label_Freq = PQW.QLabel('Freq:')
        Page1.Combobox_Freq = PQW.QComboBox()
        #
        for item in Periods:
            Page1.Combobox_Freq.addItem(str(item))
        Page1.Combobox_Freq.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_Freq.setFixedWidth(VAR.GetWindowsWidth(VAR)*0.2)
        Periods = (np.array(Periods) - OPT.GetBasicPeriod(OPT))**2
        pos = np.argmin(Periods)
        Page1.Combobox_Freq.setCurrentIndex(pos)
        Page1.Combobox_Freq.currentIndexChanged.connect(self.on_Combobox_Freq_change)
        Label_Threshold = PQW.QLabel('Threshold:')
        Page1.Threshold_Value = PQW.QLineEdit()
        Page1.Threshold_Value.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Threshold_Value.setFixedWidth(VAR.GetWindowsWidth(VAR)*0.2)
        Label_WorkSens = PQW.QLabel('WorkSens:')
        Page1.Combobox_WorkSens = PQW.QComboBox()
        for Col in Columns[1:]:
            Page1.Combobox_WorkSens.addItem(Col)
        Page1.Combobox_WorkSens.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_WorkSens.setFixedWidth(VAR.GetWindowsWidth(VAR)*0.2)
        Page1.Combobox_WorkSens.currentIndexChanged.connect(self.on_Combobox_WorkSens_change)
        Label_UPDown = PQW.QLabel('Move UP/DOWN:')
        Page1.Combobox_UPDown = PQW.QComboBox()
        Page1.Combobox_UPDown.addItem('UP')
        Page1.Combobox_UPDown.addItem('DOWN')
        Page1.Combobox_UPDown.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Combobox_UPDown.setFixedWidth(VAR.GetWindowsWidth(VAR)*0.2)
        Page1.Button_Apply = PQW.QPushButton('Apply')
        Page1.Button_Apply.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        Page1.Button_Apply.setFixedWidth(VAR.GetWindowsWidth(VAR)*0.2)
        Page1.Button_Apply.clicked.connect(self.on_Button_Apply_clicked) # Button event Click on
        # Chart
        Page1.Chart_Fig = plt.figure()
        Page1.Canvas = FigureCanvas(Page1.Chart_Fig)
        Page1.Canvas.setFixedHeight(VAR.GetWindowsHeight(VAR)*0.7)
        self.Toolbar = NavigationToolbar(Page1.Canvas, self)
        Page1.ax = Page1.Chart_Fig.add_subplot(111)
        Page1.Canvas.draw()
        # Create grid layot for the window
        Layout_Page1 = PQW.QGridLayout()
        Layout_Page1.addWidget(Label_Freq, 0, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_Freq, 1, 0, 1, 1)
        Layout_Page1.addWidget(Label_Threshold, 2, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Threshold_Value, 3, 0, 1, 1)
        Layout_Page1.addWidget(Label_WorkSens, 4, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_WorkSens, 5, 0, 1, 1)
        Layout_Page1.addWidget(Label_UPDown, 6, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Combobox_UPDown, 7, 0, 1, 1)
        Layout_Page1.addWidget(Page1.Button_Apply, 8, 0, 2, 2)
        Layout_Page1.addWidget(self.Toolbar, 0, 1, 1, 1)
        Layout_Page1.addWidget(Page1.Canvas, 1, 1, 8, 1)
        # Show layout
        self.setLayout(Layout_Page1)

        self.Update()

    def Update(self):
        print('Update')
        #
        self.df_chart_data = Page1.Phase[Page1.Phase['Freq'] == 1.0/(float(Page1.Combobox_Freq.currentText())*3600.0)]
        # Chart
        Page1.Chart_Fig.clear()
        Page1.ax = Page1.Chart_Fig.add_subplot(111)
        #
        print(Page1.Combobox_WorkSens.currentText())
        # for item in self.Phase.columns.tolist()[2:]:
        #     if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
        #         if self.df_chart_data.shape[0] == 1:
        #             plot = Page1.ax.plot(pd.to_datetime(self.df_chart_data['Time'],unit='s').to_numpy(), self.df_chart_data[item].to_numpy(), 'o', label = item)
        #         else:
        #             plot = Page1.ax.plot(pd.to_datetime(self.df_chart_data['Time'],unit='s').to_numpy(), self.df_chart_data[item].to_numpy(), '-', label = item)
        #     elif VAR.GetActiveParameters(VAR,2) == 'Time':
        #         if self.df_chart_data.shape[0] == 1:
        #             plot = Page1.ax.plot(self.df_chart_data['Time'].to_numpy(), self.df_chart_data[item].to_numpy(), 'o', label = item)
        #         else:
        #             plot = Page1.ax.plot(self.df_chart_data['Time'].to_numpy(), self.df_chart_data[item].to_numpy(), '-', label = item)
        if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
            if self.df_chart_data.shape[0] == 1:
                plot = Page1.ax.plot(pd.to_datetime(self.df_chart_data['Time'],unit='s').to_numpy(), self.df_chart_data[Page1.Combobox_WorkSens.currentText()].to_numpy(), 'o', label = Page1.Combobox_WorkSens.currentText())
            else:
                plot = Page1.ax.plot(pd.to_datetime(self.df_chart_data['Time'],unit='s').to_numpy(), self.df_chart_data[Page1.Combobox_WorkSens.currentText()].to_numpy(), '-', label = Page1.Combobox_WorkSens.currentText())
        elif VAR.GetActiveParameters(VAR,2) == 'Time':
            if self.df_chart_data.shape[0] == 1:
                plot = Page1.ax.plot(self.df_chart_data['Time'].to_numpy(), self.df_chart_data[Page1.Combobox_WorkSens.currentText()].to_numpy(), 'o', label = Page1.Combobox_WorkSens.currentText())
            else:
                plot = Page1.ax.plot(self.df_chart_data['Time'].to_numpy(), self.df_chart_data[Page1.Combobox_WorkSens.currentText()].to_numpy(), '-', label = Page1.Combobox_WorkSens.currentText())
        #
        Page1.ax.legend(loc=9, ncol=len(self.Phase.columns.tolist()[2:])) # Add legend to the chart
        #
        Page1.ax.grid(True, which='both', axis='both', linestyle='--')
        Page1.ax.set_ylabel('Phase')
        if VAR.GetActiveParameters(VAR,2) == 'Time':
            Page1.ax.set_xlabel('Time (s)')
        else:
            pass
        Page1.Canvas.draw()

    def on_Combobox_Freq_change(self):
        self.Update()
        return

    def on_Combobox_WorkSens_change(self):
        self.Update()
        return

    def on_Button_Apply_clicked(self):
        Xlim = Page1.ax.get_xlim()
        print(Xlim)
        #
        if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
            # Xlim = ((Xlim[0]*24.0*3600.0)-62135683200,(Xlim[1]*24.0*3600.0)-62135683200)
            Xlim = ((Xlim[0]*24.0*3600.0),(Xlim[1]*24.0*3600.0))
        print(Xlim)
        #
        # print(Xlim)
        Time = (Page1.Phase['Time'])[(Page1.Phase['Time'] >= Xlim[0]) & (Page1.Phase['Time'] <= Xlim[1])].drop_duplicates().tolist()
        print(Page1.Phase['Time'].iloc[0])
        print(Page1.Phase['Time'].iloc[-1])
        # print(type(Time))
        # StartTime = datetime.datetime.utcfromtimestamp(int(self.df_Data['Time'].iloc[0])).strftime('%Y-%m-%d %H:%M:%S')
        # EndTime = datetime.datetime.utcfromtimestamp(int(self.df_Data['Time'].iloc[self.df_Data.shape[0]-1])).strftime('%Y-%m-%d %H:%M:%S')
        # print(Page1.Time[(Page1.Time['Time'] >= Xlim[0]) & (Page1.Time['Time'] <= Xlim[1])])
        for item in Time:
            dfTemp = Page1.Phase[(Page1.Phase['Time'] == float(item)) & (Page1.Phase['Freq'] == 1.0/(float(Page1.Combobox_Freq.currentText())*3600.0))]
            # print(dfTemp)
            #
            index = dfTemp.index.values[0]
            # print(index)
            Value = Page1.Phase[Page1.Combobox_WorkSens.currentText()].loc[index]
            # print(Value)
            if Page1.Combobox_UPDown.currentText() == 'UP':
                if Value < float(Page1.Threshold_Value.text()):
                    Value = Value + 2 * np.pi
            elif Page1.Combobox_UPDown.currentText() == 'DOWN':
                if Value > float(Page1.Threshold_Value.text()):
                    Value = Value - 2 * np.pi
            # print(Value)
            Page1.Phase[Page1.Combobox_WorkSens.currentText()].loc[index] = Value
        #
        self.Update()