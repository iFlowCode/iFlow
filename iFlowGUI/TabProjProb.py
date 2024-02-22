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
# # # from PyQt5 import QtCore, QtWidgets
import PyQt5.QtWidgets as PQW
# # import PyQt5.QtGui as PQG
import PyQt5.QtCore as PQC
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import shutil
# # import numpy.random.common
# # import numpy.random.bounded_integers
# # import numpy.random.entropy
import pandas as pd
import datetime
# # Import custom library
from Variables import VAR
from ScrollLabel import ScrollLabel
import TabProjProb as TPP
import TabSignProc as TSP
import TabFreqAnal as TFA
import TabParEst as TPE
import TabBrede as TBH
import WizardAP as WAP
from loguru import logger

'''
TabProjStac Class
'''
class TabProjProb(PQW.QWidget):
    def __init__(self):
        super().__init__()
        logger.debug("TabProjProb - Start Class")
        # Set Matplotlib fonts size
        TabProjProb.MPL_AxisTitle = int(VAR.GetMPLAxisTitleFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.MPL_AxisTick = int(VAR.GetMPLAxisTickFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.MPL_Legend = int(VAR.GetMPLLegendFontSizeReference(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        # Store class object
        VAR.SetTabProjProb(VAR, self)
        # Create grid layot for the window
        Layout_Tab_ProjStac = PQW.QHBoxLayout()
        container_left = PQW.QFrame()
        Layout_Tab_ProjStac_left = PQW.QVBoxLayout()
        # Groupbox Project
        self.GroupBox_Projects = PQW.QGroupBox('Projects:')
        # Create the Layout for the Groupbox Project
        self.VBoxProjects = PQW.QVBoxLayout()
        # Element ComboBox Active Project
        TabProjProb.Combobox_Active_Project = PQW.QComboBox()
        # TabProjProb.Combobox_Active_Project.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Combobox_Active_Project.setToolTip('Choose Active Project') # Tooltip message
        TabProjProb.Combobox_Active_Project.currentIndexChanged.connect(self.on_Combobox_Active_Project_change) # ComboBox event change item
        # Element Button Create Project
        TabProjProb.Button_New_Project = PQW.QPushButton('New Project')
        # TabProjProb.Button_New_Project.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Button_New_Project.setToolTip('Create a New Project') # Tooltip message
        TabProjProb.Button_New_Project.clicked.connect(self.on_Button_New_Project_clicked) # Button event Click on
        # Element Button Delete Project
        TabProjProb.Button_Del_Project = PQW.QPushButton('Delete Project')
        # TabProjProb.Button_Del_Project.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Button_Del_Project.setToolTip('Delete the Active Project') # Tooltip message
        TabProjProb.Button_Del_Project.clicked.connect(self.on_Button_Del_Project_clicked) # Button event Click on
        # Add elements to the Layout
        self.VBoxProjects.addWidget(TabProjProb.Combobox_Active_Project)
        self.VBoxProjects.addWidget(TabProjProb.Button_New_Project)
        self.VBoxProjects.addWidget(TabProjProb.Button_Del_Project)
        # Add the Layout to the Groupbox Project
        self.GroupBox_Projects.setLayout(self.VBoxProjects)
        #
        Layout_Tab_ProjStac_left.addWidget(self.GroupBox_Projects)
        # Groupbox Probes
        self.GroupBox_Probes = PQW.QGroupBox('Probes:')
        # Create the Layout for the Groupbox Probes
        self.VBoxProbes = PQW.QVBoxLayout() 
        # Element ComboBox Active Probes
        TabProjProb.Combobox_Active_Probes = PQW.QComboBox()
        # TabProjProb.Combobox_Active_Probes.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Combobox_Active_Probes.setToolTip('Choose Active Probes') # Tooltip message
        TabProjProb.Combobox_Active_Probes.currentIndexChanged.connect(self.on_Combobox_Active_Probes_change) # ComboBox event change item
        # Element Button Add Probes
        TabProjProb.Button_Add_Probes = PQW.QPushButton('Add Probes')
        # TabProjProb.Button_Add_Probes.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Button_Add_Probes.setToolTip('Add Probes to the Project') # Tooltip message
        self.Button_Add_Probes.clicked.connect(self.on_Button_Add_Probes_clicked) # Button event Click on
        # Element Button Remove Probes
        TabProjProb.Button_Remove_Probes = PQW.QPushButton('Remove Probes')
        # TabProjProb.Button_Remove_Probes.setFixedHeight(VAR.GetConboBoxHeight(VAR)/VAR.GetWindowHeightReference(VAR)*VAR.GetWindowsHeight(VAR))
        TabProjProb.Button_Remove_Probes.setToolTip('Remove the Active Probes') # Tooltip message
        TabProjProb.Button_Remove_Probes.clicked.connect(self.on_Button_Remove_Probes_clicked) # Button event Click on
        # Add element to the Layout
        self.VBoxProbes.addWidget(TabProjProb.Combobox_Active_Probes)
        self.VBoxProbes.addWidget(TabProjProb.Button_Add_Probes)
        self.VBoxProbes.addWidget(TabProjProb.Button_Remove_Probes)
        # Add the Layout to the Groupbox Probes
        self.GroupBox_Probes.setLayout(self.VBoxProbes)
        #
        Layout_Tab_ProjStac_left.addWidget(self.GroupBox_Probes)
        # Groupbox Report
        self.GroupBox_Report = PQW.QGroupBox('Report:')
        # Create Layout for the Groupbox Report
        self.VBoxReport = PQW.QVBoxLayout()
        # Element EditLine
        TabProjProb.Label_Report = ScrollLabel(self)
        TabProjProb.Label_Report.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\nUt enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ')
        # Add elements to the Layout
        self.VBoxReport.addWidget(TabProjProb.Label_Report)
        # Add the Layout to the Groupbox Report
        self.GroupBox_Report.setLayout(self.VBoxReport)
        #
        Layout_Tab_ProjStac_left.addWidget(self.GroupBox_Report)
        # Element Checkbox display interpolated data
        TabProjProb.CheckBox_DispInter = PQW.QCheckBox('Display interpolated data')
        TabProjProb.CheckBox_DispInter.stateChanged.connect(self.ChartChanged)
        #
        Layout_Tab_ProjStac_left.addWidget(TabProjProb.CheckBox_DispInter)
        # Groupbox Sensors
        self.GroupBox_Sensors = PQW.QGroupBox("Sensors:")
        TabProjProb.VBoxSensor = PQW.QGridLayout()
        self.GroupBox_Sensors.setLayout(TabProjProb.VBoxSensor)
        #
        Layout_Tab_ProjStac_left.addWidget(self.GroupBox_Sensors)
        #
        container_left.setMaximumWidth(int(VAR.GetWindowsSize(VAR)[0] * 2 / 3 / 4))
        container_left.setLayout(Layout_Tab_ProjStac_left)
        # Chart column
        container_right = PQW.QFrame()
        Layout_Tab_ProjStac_Right = PQW.QVBoxLayout()
        TabProjProb.Chart_Fig = plt.figure()
        TabProjProb.Canvas = FigureCanvas(TabProjProb.Chart_Fig)
        self.Toolbar = NavigationToolbar(TabProjProb.Canvas, self)
        TabProjProb.Canvas.draw()
        #
        Layout_Tab_ProjStac_Right.addWidget(self.Toolbar)
        Layout_Tab_ProjStac_Right.addWidget(TabProjProb.Canvas)
        #
        container_right.setLayout(Layout_Tab_ProjStac_Right)
        #
        Layout_Tab_ProjStac.addWidget(container_left)
        Layout_Tab_ProjStac.addWidget(container_right)
        # Show layout
        self.setLayout(Layout_Tab_ProjStac)

    # @logger.catch
    def on_Main_Menu_Project_Export_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Project_Export_clicked')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Project to File', '../exports/' + VAR.GetActiveProject(VAR), 'Project Export (*.pkr)')
        if file_export[0]:
            shutil.make_archive(file_export[0], 'zip', '../projects/' + str(VAR.GetActiveProject(VAR)))
            shutil.move(file_export[0] + '.zip', file_export[0])
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Project Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Main_Menu_Project_Import_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Project_Import_clicked')
        file_import = PQW.QFileDialog.getOpenFileName(self, 'Select project file to import...', '../exports/', 'Project Import(*.pkr)')
        if file_import[0]:
            if os.path.isdir('../projects/' +(file_import[0].split('/')[-1]).replace('.pkr','')):
                flag = True
                cont = 1
                while flag:
                    if os.path.isdir('../projects/' +(file_import[0].split('/')[-1]).replace('.pkr','(' + str(cont) +')')):
                        cont = cont + 1
                    else:
                        flag = False
                        target_folder = '../projects/' +(file_import[0].split('/')[-1]).replace('.pkr','(' + str(cont) +')')
                        project = (file_import[0].split('/')[-1]).replace('.pkr','(' + str(cont) +')')
            else:
                target_folder = '../projects/' + (file_import[0].split('/')[-1]).replace('.pkr','')
                project = (file_import[0].split('/')[-1]).replace('.pkr','')
            #
            shutil.move(file_import[0], file_import[0] + '.zip')
            shutil.unpack_archive(file_import[0] + '.zip', target_folder, 'zip')
            shutil.move(file_import[0] + '.zip', file_import[0])
            # Set Active Project
            VAR.SetActiveProject(VAR,project)
            # Get Projects list
            projects_list = VAR.GetProjectsList(VAR)
            # Update list of projects
            projects_list.append(str(project))
            # Update the file with the list of projects
            Handle = open('../projects/projects.ini','w')
            for item in projects_list:
                Handle.write(item+'\n')
            Handle.close()
            # Store updated list of projects
            VAR.SetProjectsList(VAR, projects_list)
            # load probes list
            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/probes.ini','r')
            list_probes = Handle.readlines()
            Handle.close()
            #
            if len(list_probes) == 0:
                VAR.SetProbesList(VAR,None)
                #
                VAR.SetActiveProbe(VAR,None)
            else:
                VAR.SetProbesList(VAR,list_probes)
                #
                VAR.SetActiveProbe(VAR,list_probes[0].replace('\n',''))
            #
            TPP.TabProjProb.Update(TPP,2)
            TSP.TabSignProc.Update(TSP,2)
            TFA.TabFreqAnal.Update(TFA,2)
            TPE.TabParEst.Update(TPE,2)
            TBH.TabBrede.Update(TBH,2)
        #
        return

    # @logger.catch
    def on_Main_Menu_Project_Rename_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Project_Rename_clicked')
        new_name, okPressed = PQW.QInputDialog.getText(None,'Rename Project','Project Name:',PQW.QLineEdit.Normal,'')
        if okPressed and new_name != '':
            if os.path.isdir('../projects/'+new_name):
                PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR)+' message', 'Project already exixst.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
            else:
                List = VAR.GetProjectsList(VAR)
                pos = List.index(VAR.GetActiveProject(VAR))
                List[pos] = new_name
                VAR.SetProjectsList(VAR,List)
                Handle = open('../projects/projects.ini','w')
                for item in List:
                    Handle.write(item+'\n')
                Handle.close()
                os.rename('../projects/'+VAR.GetActiveProject(VAR),'../projects/'+new_name)
                VAR.SetActiveProject(VAR,new_name)
                #
                TPP.TabProjProb.Update(TPP,2)
                TSP.TabSignProc.Update(TSP,2)
                TFA.TabFreqAnal.Update(TFA,2)
                TPE.TabParEst.Update(TPE,2)
                TBH.TabBrede.Update(TBH,2)
        #
        return

    # @logger.catch
    def on_Main_Menu_Probe_Rename_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Probe_Rename_clicked')
        new_name, okPressed = PQW.QInputDialog.getText(None,'Rename Probe','Probe Name:',PQW.QLineEdit.Normal,'')
        if okPressed and new_name != '':
            if os.path.isdir('../projects/'+VAR.GetActiveProject(VAR)+'/'+new_name):
                PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR)+' message', 'Probe already exixst.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
            else:
                List = VAR.GetProbesList(VAR)
                #
                pos = List.index(VAR.GetActiveProbe(VAR))
                List[pos] = new_name
                VAR.SetProbesList(VAR,List)
                Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+'probes.ini','w')
                for item in List:
                    Handle.write(item+'\n')
                Handle.close()
                os.rename('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR),'../projects/'+VAR.GetActiveProject(VAR)+'/'+new_name)
                VAR.SetActiveProbe(VAR,new_name)
                #
                TPP.TabProjProb.Update(TPP,4)
                TSP.TabSignProc.Update(TSP,4)
                TFA.TabFreqAnal.Update(TFA,4)
                TPE.TabParEst.Update(TPE,4)
                TBH.TabBrede.Update(TBH,4)
        #
        return

    # @logger.catch
    def ChartChanged(self):
        logger.debug('TabProjProb - ChartChanged')
        TPP.TabProjProb.Update(TPP,6)
        return

    # @logger.catch
    def SensorActiveChange(self):
        logger.debug('TabProjProb - SensorActiveChange')
        TPP.TabProjProb.Update(TPP,7)
        return

    # @logger.catch
    def Update(self,Case):
        logger.debug(f"TabProjProb Update - Case: {Case}")
        '''
        Case 0: Event generated by the starting of the GUI
        Case 1: Event generated by Combobox Active Project
        Case 2: Event generated by Create New Project or Project imported or Change Project Name
        Case 3: Event generated by Delete Active Project
        Case 4: Event generated by Import New Probe or Project imported or Change Project Name
        Case 5: Event generated by Delete Probe
        Case 6: Event generated by Combobox Active Probe
        Case 7: Event generated by Activete/deactivete Sensors CheckBox
        '''
        # VAR.GetiFlowSelf(VAR).progress.setFormat('Update Tab Projects/Probes')
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        # Disconect all the internal events
        TabProjProb.Combobox_Active_Project.currentIndexChanged.disconnect()
        TabProjProb.Button_New_Project.clicked.disconnect()
        TabProjProb.Button_Del_Project.clicked.disconnect()
        TabProjProb.Combobox_Active_Probes.currentIndexChanged.disconnect()
        TabProjProb.Button_Add_Probes.clicked.disconnect()
        TabProjProb.Button_Remove_Probes.clicked.disconnect()
        # Load Probe configuration
        if(VAR.GetActiveProject(VAR) == None):
            VAR.SetActiveParameters(VAR,['None','None','None','None','None','None','None','None','None','None','None','None','None'])
            # Window Title
            string = VAR.GetSoftwareName(VAR) + ' - Create a Project'
            VAR.GetiFlowSelf(VAR).setWindowTitle(string)
            # Project GroupoBox
            TabProjProb.Combobox_Active_Project.clear()
            TabProjProb.Button_Del_Project.setEnabled(False)
            # Probe GroupoBox
            TabProjProb.Combobox_Active_Probes.clear()
            TabProjProb.Button_Add_Probes.setEnabled(False)
            TabProjProb.Button_Remove_Probes.setEnabled(False)
            # Report GroupoBox
            TabProjProb.Label_Report.setText('There isn\'t any Project\nCreate one.')
            # Sensors GroupoBox
            TabProjProb.CheckBox_DispInter.setEnabled(False)
            if TabProjProb.VBoxSensor is not None:
                while TabProjProb.VBoxSensor.count():
                    item = TabProjProb.VBoxSensor.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        self.clearLayout(item.layout())
            # Chart
            TabProjProb.Chart_Fig.clear()
            TabProjProb.ax = TabProjProb.Chart_Fig.add_subplot(111)
            # TabProjProb.ax.legend()
            TabProjProb.ax.grid(True, which='both', axis='both', linestyle='--')
            TabProjProb.ax.set_ylabel('Temperature')
            #
            TabProjProb.ax.set_xlabel('Time')
            TabProjProb.Canvas.draw()
            # Menu Update
            VAR.GetiFlowSelf(VAR).Menu_Project_Del.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Project_Rename.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Project_Exp.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_Add.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_Del.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_Rename.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_ExpData.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_Exp.setEnabled(False)
            VAR.GetiFlowSelf(VAR).Menu_Probe_Imp.setEnabled(False)
        else:
            if(VAR.GetActiveProbe(VAR) == None):
                VAR.SetActiveParameters(VAR,['None','None','None','None','None','None','None','None','None','None','None','None','None'])
                # Window Title
                string = VAR.GetSoftwareName(VAR) + ' - Active Project: ' + VAR.GetActiveProject(VAR) + ' - Add Probe to the Project'
                VAR.GetiFlowSelf(VAR).setWindowTitle(string)
                # Project GroupoBox
                TabProjProb.Combobox_Active_Project.clear()
                for item in VAR.GetProjectsList(VAR):
                    TabProjProb.Combobox_Active_Project.addItem(item)
                #
                index = TabProjProb.Combobox_Active_Project.findText(VAR.GetActiveProject(VAR), PQC.Qt.MatchFixedString)
                if index >= 0:
                    TabProjProb.Combobox_Active_Project.setCurrentIndex(index)
                #
                TabProjProb.Button_Del_Project.setEnabled(True)
                # Probe GroupoBox
                TabProjProb.Combobox_Active_Probes.clear()
                TabProjProb.Button_Add_Probes.setEnabled(True)
                TabProjProb.Button_Remove_Probes.setEnabled(False)
                # Report GroupoBox
                TabProjProb.Label_Report.setText('There isn\'t any Probe\nImport one.')
                # Sensors GroupoBox
                TabProjProb.CheckBox_DispInter.setEnabled(False)
                if TabProjProb.VBoxSensor is not None:
                    while TabProjProb.VBoxSensor.count():
                        item = TabProjProb.VBoxSensor.takeAt(0)
                        widget = item.widget()
                        if widget is not None:
                            widget.deleteLater()
                        else:
                            self.clearLayout(item.layout())
                # Chart
                TabProjProb.Chart_Fig.clear()
                TabProjProb.ax = TabProjProb.Chart_Fig.add_subplot(111)
                # TabProjProb.ax.legend()
                TabProjProb.ax.grid(True, which='both', axis='both', linestyle='--')
                TabProjProb.ax.set_ylabel('Temperature')
                TabProjProb.ax.set_xlabel('Time')
                TabProjProb.Canvas.draw()
                # Menu Update
                VAR.GetiFlowSelf(VAR).Menu_Project_Del.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Project_Rename.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Project_Exp.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Add.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Del.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Rename.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_Probe_ExpData.setEnabled(False)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Exp.setEnabled(False)
            else:
                # Load Probe.ini file
                if Case != 7:
                    ProbeIniList = []
                    HandleProbIni = open('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/probe.ini','r')
                    Rows = HandleProbIni.readlines()
                    HandleProbIni.close()
                    for Row in Rows:
                        ProbeIniList.append(Row.split(';')[0])
                    VAR.SetActiveParameters(VAR,ProbeIniList)
                VAR.GetiFlowSelf(VAR).progress.setValue(20)
                # Load data of probe
                if Case != 7:
                    self.Data_Columns = []
                    self.df_Data = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz', compression = 'zip')
                    self.Data_Columns = self.df_Data.columns.tolist()
                    del self.Data_Columns[0]
                    self.df_Mark = pd.read_pickle('../projects/' + VAR.GetActiveProject(VAR) + '/' + VAR.GetActiveProbe(VAR) + '/data/miss.pkz', compression = 'zip')
                # Chart's Limits
                if Case != 7:
                    MAX = self.df_Data.max().tolist()
                    MIN = self.df_Data.min().tolist()
                    DeltaX = (MAX[0]-MIN[0])*0.1/2
                    DeltaY = (max(MAX[1:])-min(MIN[1:]))*0.1/2
                    # self.xLimits = [MIN[0]-DeltaX,MAX[0]+DeltaX]
                    self.xLimits = [self.df_Data['Time'].iloc[0],self.df_Data['Time'].iloc[self.df_Data.shape[0]-1]]
                    self.yLimits = [min(MIN[1:])-DeltaY,max(MAX[1:])+DeltaY]
                # Change Window Title
                if Case != 7:
                    string = VAR.GetSoftwareName(VAR) + ' - Active Project: ' + VAR.GetActiveProject(VAR) + ' - Active Probe: ' + VAR.GetActiveProbe(VAR)
                    VAR.GetiFlowSelf(VAR).setWindowTitle(string)
                # Project GroupoBox
                if Case != 7:
                    TabProjProb.Combobox_Active_Project.clear()
                    for item in VAR.GetProjectsList(VAR):
                        TabProjProb.Combobox_Active_Project.addItem(item)
                    #
                    index = TabProjProb.Combobox_Active_Project.findText(VAR.GetActiveProject(VAR), PQC.Qt.MatchFixedString)
                    if index >= 0:
                        TabProjProb.Combobox_Active_Project.setCurrentIndex(index)
                    #
                    TabProjProb.Button_Del_Project.setEnabled(True)
                VAR.GetiFlowSelf(VAR).progress.setValue(40)
                # Probe GroupoBox
                if Case != 7:
                    TabProjProb.Combobox_Active_Probes.clear()
                    for item in VAR.GetProbesList(VAR):
                        TabProjProb.Combobox_Active_Probes.addItem(item)
                    #
                    index = TabProjProb.Combobox_Active_Probes.findText(VAR.GetActiveProbe(VAR), PQC.Qt.MatchFixedString)
                    if index >= 0:
                        TabProjProb.Combobox_Active_Probes.setCurrentIndex(index)
                    #
                    TabProjProb.Button_Add_Probes.setEnabled(True)
                    TabProjProb.Button_Remove_Probes.setEnabled(True)
                # Report GroupoBox
                if Case != 7:
                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                        StartTime = datetime.datetime.utcfromtimestamp(int(self.df_Data['Time'].iloc[0])).strftime('%Y-%m-%d %H:%M:%S')
                        EndTime = datetime.datetime.utcfromtimestamp(int(self.df_Data['Time'].iloc[self.df_Data.shape[0]-1])).strftime('%Y-%m-%d %H:%M:%S')
                    elif VAR.GetActiveParameters(VAR,2) == 'Time':
                        StartTime = str(self.df_Data['Time'].iloc[0])
                        EndTime = str(self.df_Data['Time'].iloc[self.df_Data.shape[0]-1])
                    #
                    Text = 'Last file imported:\n'+VAR.GetActiveParameters(VAR,0)+'\n'+'Sample rate: '+VAR.GetActiveParameters(VAR,3)+' s\n'+'Sample frequency: '+str("%.2E" % (1/float(VAR.GetActiveParameters(VAR,3))))+' Hz\n'
                    # Text = 'Last file imported:\n'+VAR.GetActiveParameters(VAR,0)+'\n'+'Sample rate: '+VAR.GetActiveParameters(VAR,3)+' s\n'+'Sample frequency: '+str(1/float(VAR.GetActiveParameters(VAR,3)))+' Hz\n'
                    if VAR.GetActiveParameters(VAR,4) == 'True':
                        Text = Text + 'The missing data were imterpolated\n'
                    if VAR.GetActiveParameters(VAR,5) == 'True':
                        Text = Text + 'The Time serie was rebuilded with the Sample rate\n'
                    Text = Text + 'Data from: ' + StartTime + '\nData to: '+ EndTime+'\n'
                    Text = Text + 'Sensor\'s geometry:\n'
                    #
                    Heights = VAR.GetActiveParameters(VAR,7).split(',')
                    for i,item in enumerate(VAR.GetActiveParameters(VAR,6).split(',')):
                        Text = Text + '\t' + item + ' is at ' + Heights[i] + ' m\n'
                    TabProjProb.Label_Report.setText(Text)
                # Sensors GroupoBox
                VAR.GetiFlowSelf(VAR).progress.setValue(60)
                if Case != 7:
                    TabProjProb.CheckBox_DispInter.setEnabled(True)
                    if TabProjProb.VBoxSensor is not None:
                        while TabProjProb.VBoxSensor.count():
                            item = TabProjProb.VBoxSensor.takeAt(0)
                            widget = item.widget()
                            if widget is not None:
                                widget.deleteLater()
                            else:
                                self.clearLayout(item.layout())
                    contPos = 0
                    for Sensor in self.Data_Columns:
                        CheckBox = PQW.QCheckBox(Sensor)
                        CheckBox.setChecked(True)
                        CheckBox.toggled.connect(TabProjProb.SensorActiveChange)
                        if contPos % 2 == 0:
                            TabProjProb.VBoxSensor.addWidget(CheckBox,int(contPos/2),0,1,1)
                        else:
                            TabProjProb.VBoxSensor.addWidget(CheckBox,int(contPos/2),1,1,1)
                        contPos = contPos + 1
                # Chart
                if Case != -1:
                    #
                    if Case == 7:
                        Ylim = TabProjProb.ax.get_ylim()
                        Xlim = TabProjProb.ax.get_xlim()
                    #
                    TabProjProb.Chart_Fig.clear()
                    TabProjProb.ax = TabProjProb.Chart_Fig.add_subplot(111)
                    #
                    if(VAR.GetChartColors(VAR) is None):
                        Colors = []
                    else:
                        Colors = VAR.GetChartColors(VAR)    #! To check if works
                        if len(Colors) < len(self.Data_Columns):
                            Colors = []
                            VAR.SetChartColors(VAR,None)
                    #
                    Min = 9999
                    for Sens in self.Data_Columns:
                        MinTemp = (self.df_Data[Sens]).min(axis = 0)
                        if Min > MinTemp:
                            Min = MinTemp
                    #
                    for i in range(0,len(self.Data_Columns)):
                        if TabProjProb.VBoxSensor.itemAt(i).widget().isChecked():
                            if(VAR.GetChartColors(VAR) == None):
                                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                    plot = TabProjProb.ax.plot(pd.to_datetime(self.df_Data['Time'],unit='s').to_numpy(), (self.df_Data[TabProjProb.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabProjProb.VBoxSensor.itemAt(i).widget().text())
                                    if TabProjProb.CheckBox_DispInter.isChecked():
                                        plot = TabProjProb.ax.plot(pd.to_datetime(self.df_Mark['Time'],unit='s').to_numpy(), (self.df_Mark[TabProjProb.VBoxSensor.itemAt(i).widget().text()].replace(-9999.0,Min)).to_numpy(), 'o', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                    plot = TabProjProb.ax.plot(self.df_Data['Time'].to_numpy(), (self.df_Data[TabProjProb.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabProjProb.VBoxSensor.itemAt(i).widget().text())
                                    if TabProjProb.CheckBox_DispInter.isChecked():
                                        plot = TabProjProb.ax.plot(self.df_Mark['Time'].to_numpy(), (self.df_Mark[TabProjProb.VBoxSensor.itemAt(i).widget().text()].replace(-9999.0,Min)).to_numpy(), 'o', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                Colors.append(plot[0].get_color())
                            else:
                                if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                                    plot = TabProjProb.ax.plot(pd.to_datetime(self.df_Data['Time'],unit='s').to_numpy(), (self.df_Data[TabProjProb.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                    if TabProjProb.CheckBox_DispInter.isChecked():
                                        plot = TabProjProb.ax.plot(pd.to_datetime(self.df_Mark['Time'],unit='s').to_numpy(), (self.df_Mark[TabProjProb.VBoxSensor.itemAt(i).widget().text()].replace(-9999.0,Min)).to_numpy(), 'o', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                elif VAR.GetActiveParameters(VAR,2) == 'Time':
                                    plot = TabProjProb.ax.plot(self.df_Data['Time'].to_numpy(), (self.df_Data[TabProjProb.VBoxSensor.itemAt(i).widget().text()]).to_numpy(), '-', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                                    if TabProjProb.CheckBox_DispInter.isChecked():
                                        plot = TabProjProb.ax.plot(self.df_Mark['Time'].to_numpy(), (self.df_Mark[TabProjProb.VBoxSensor.itemAt(i).widget().text()].replace(-9999.0,Min)).to_numpy(), 'o', label = TabProjProb.VBoxSensor.itemAt(i).widget().text(), color=Colors[i])
                    #
                    VAR.GetiFlowSelf(VAR).progress.setValue(80)
                    if len(self.Data_Columns) > 5:
                        TabProjProb.ax.legend(ncol=int(len(self.Data_Columns)/5+1),fontsize=TabProjProb.MPL_Legend)
                    else:
                        TabProjProb.ax.legend(ncol=len(self.Data_Columns),fontsize=TabProjProb.MPL_Legend)
                    TabProjProb.ax.grid(True, which='both', axis='both', linestyle='--')
                    TabProjProb.ax.set_ylabel('Temperature ('+u'\N{DEGREE SIGN}'+'C)',fontsize=TabProjProb.MPL_AxisTitle)
                    TabProjProb.ax.tick_params(axis='both', labelsize=TabProjProb.MPL_AxisTick)
                    if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                        TabProjProb.ax.set_xlabel('Date',fontsize=TabProjProb.MPL_AxisTitle)
                    elif VAR.GetActiveParameters(VAR,2) == 'Time':
                        TabProjProb.ax.set_xlabel('Time (s)',fontsize=TabProjProb.MPL_AxisTitle)
                    #
                    # if Case == 7:
                    #     if VAR.GetActiveParameters(VAR,2) == 'yyyy-mm-dd h24:min:sec':
                    #         Xlim = ((Xlim[0]-719165) * 24.0 * 3600.0,(Xlim[1]-719165) * 24.0 * 3600.0)
                    #     TabProjProb.ax.set_ylim(Ylim)
                    #     TabProjProb.ax.set_xlim(Xlim)
                    # else:
                    #     TabProjProb.ax.set_ylim(self.yLimits)
                    #     TabProjProb.ax.set_xlim(self.xLimits)
                    #
                    TabProjProb.Canvas.draw()
                    #
                    if(VAR.GetChartColors(VAR) is None):
                        VAR.SetChartColors(VAR, Colors)
                # Menu Update
                VAR.GetiFlowSelf(VAR).Menu_Project_Del.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Project_Rename.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Project_Exp.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Add.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Del.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Rename.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_ExpData.setEnabled(True)
                VAR.GetiFlowSelf(VAR).Menu_Probe_Exp.setEnabled(True)
        # Reconect all the internal events  
        TabProjProb.Combobox_Active_Project.currentIndexChanged.connect(TabProjProb.on_Combobox_Active_Project_change) # ComboBox event change item      
        TabProjProb.Button_New_Project.clicked.connect(TabProjProb.on_Button_New_Project_clicked) # Button event Click on
        TabProjProb.Button_Del_Project.clicked.connect(TabProjProb.on_Button_Del_Project_clicked) # Button event Click on
        TabProjProb.Combobox_Active_Probes.currentIndexChanged.connect(TabProjProb.on_Combobox_Active_Probes_change) # ComboBox event change item
        TabProjProb.Button_Add_Probes.clicked.connect(TabProjProb.on_Button_Add_Probes_clicked) # Button event Click on
        TabProjProb.Button_Remove_Probes.clicked.connect(TabProjProb.on_Button_Remove_Probes_clicked) # Button event Click on
        VAR.GetiFlowSelf(VAR).progress.setValue(0)
        #
        return

    # @logger.catch
    def on_Combobox_Active_Project_change(self):
        logger.debug('TabProjProb - on_Combobox_Active_Project_change')
        # Set the choosed project as active
        VAR.SetActiveProject(VAR,TabProjProb.Combobox_Active_Project.currentText())
        # Load probes list of the new active project
        try:            
            HandleProbIni = open('../projects/'+VAR.GetActiveProject(VAR)+'/probes.ini','r')
            ProbesList = HandleProbIni.readlines()
            HandleProbIni.close()
            for pos,item in enumerate(ProbesList):
                ProbesList[pos] = item.replace('\n','')
            if(len(ProbesList) == 0):
                # Set Probes List
                VAR.SetProbesList(VAR,[])
                # Set Active Probe
                VAR.SetActiveProbe(VAR,None)
            else:
                # Set Probes List
                VAR.SetProbesList(VAR,ProbesList)
                # Set Active Probe
                VAR.SetActiveProbe(VAR,ProbesList[0])
        except:
            # Set Probes List
            VAR.SetProbesList(VAR,[])
            # Set Active Probe
            VAR.SetActiveProbe(VAR,None)
        # Update Tabs
        TPP.TabProjProb.Update(TPP,1)
        TSP.TabSignProc.Update(TSP,1)
        TFA.TabFreqAnal.Update(TFA,1)
        TPE.TabParEst.Update(TPE,1)
        TBH.TabBrede.Update(TBH,1)
        #
        return

    # @logger.catch
    def on_Button_New_Project_clicked(self):
        logger.debug('TabProjProb - on_Button_New_Project_clicked')
        new_project, okPressed = PQW.QInputDialog.getText(None,'Create New Project','Project Name:',PQW.QLineEdit.Normal,'')
        if okPressed and new_project != '':
            # Check if the name of new project already exist
            if(new_project in VAR.GetProjectsList(VAR)):
                PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR)+' message', 'A project with this name\nalready exist.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
            else:
                # Set Updated ProjectsList
                VAR.SetProjectsList(VAR,VAR.GetProjectsList(VAR)+[new_project])
                # Set the new project as Active Project
                VAR.SetActiveProject(VAR,new_project)
                # Set ProbesList
                VAR.SetProbesList(VAR,[])
                # Set ActiveProbe
                VAR.SetActiveProbe(VAR,None)
                # Create the folder and the file for the new project
                os.mkdir('../projects/' + new_project)
                HandleProbIni = open('../projects/' + new_project + '/probes.ini', 'w')
                HandleProbIni.close()
                # Update List in file projects.ini
                HandleProjIni = open('../projects/projects.ini','w')
                String = '\n'.join(VAR.GetProjectsList(VAR))
                HandleProjIni.write(String)
                HandleProjIni.close()
                # Update Tabs
                TPP.TabProjProb.Update(TPP,2)
                TSP.TabSignProc.Update(TSP,2)
                TFA.TabFreqAnal.Update(TFA,2)
                TPE.TabParEst.Update(TPE,2)
                TBH.TabBrede.Update(TBH,2)
        # 
        return

    # @logger.catch
    def on_Button_Del_Project_clicked(self):
        logger.debug('TabProjProb - on_Button_Del_Project_clicked')
        # Get the project to delete
        active_project = VAR.GetActiveProject(VAR)
        # Get the list of projects created
        project_list = VAR.GetProjectsList(VAR)
        string = 'You are deleting the project: ' + VAR.GetActiveProject(VAR) + '. Continue?'
        Reply = PQW.QMessageBox.warning(None, VAR.GetSoftwareName(VAR)+' message', string, PQW.QMessageBox.Yes|PQW.QMessageBox.No, PQW.QMessageBox.Yes)
        if(Reply == PQW.QMessageBox.Yes):
            # Delete the project from the list
            project_list.remove(active_project)
            # Delete Project folder
            try:
                shutil.rmtree('../projects/' + str(active_project))
                #
                if(len(project_list) == 0):
                    # Save the new list to projects.ini
                    HandleProjIni = open('../projects/projects.ini','w')
                    HandleProjIni.close()
                    # Set Active Project
                    VAR.SetActiveProject(VAR,None)
                    # Set Projects List
                    VAR.SetProjectsList(VAR,[])
                    # Set Active Probe
                    VAR.SetActiveProbe(VAR,None)
                    # Set Probes List
                    VAR.SetProbesList(VAR,[])
                else:
                    # Save the new list to projects.ini
                    HandleProjIni = open('../projects/projects.ini','w')
                    String = '\n'.join(project_list)
                    HandleProjIni.write(String)
                    HandleProjIni.close()
                    # Set Active Project
                    VAR.SetActiveProject(VAR,project_list[0])
                    # Set Projects List
                    VAR.SetProjectsList(VAR,project_list)
                    # Load Probes for the Active Project
                    try:
                        HandleProbIni = open('../projects/' + project_list[0] + '/probes.ini', 'r')
                        ProbesList = HandleProbIni.readlines()
                        HandleProbIni.close()
                        for pos,item in enumerate(ProbesList):
                            ProbesList[pos] = item.replace('\n','')
                        if(len(ProbesList) == 0):
                            # Set Active Probe
                            VAR.SetActiveProbe(VAR,None)
                            # Set Probes List
                            VAR.SetProbesList(VAR,[])
                        else:
                            # Set Active Probe
                            VAR.SetActiveProbe(VAR,ProbesList[0])
                            # Set Probes List
                            VAR.SetProbesList(VAR,ProbesList)
                    except:
                        PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR) + ' message', 'Error while loading new project.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
                # Update Tabs
                TPP.TabProjProb.Update(TPP,3)
                TSP.TabSignProc.Update(TSP,3)
                TFA.TabFreqAnal.Update(TFA,3)
                TPE.TabParEst.Update(TPE,3)
                TBH.TabBrede.Update(TBH,3)
            except:
                PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR) + ' message', 'Error while deleting project.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        #
        return

    # @logger.catch
    def on_Combobox_Active_Probes_change(self):
        logger.debug('TabProjProb - on_Combobox_Active_Probes_change')
        if(os.path.isdir('../projects/'+VAR.GetActiveProject(VAR)+'/'+TabProjProb.Combobox_Active_Probes.currentText())):
            # Set the choosed probe as active
            VAR.SetActiveProbe(VAR,TabProjProb.Combobox_Active_Probes.currentText())
        else:
            # Error/Issue Message
            PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR)+' message', 'The folder for the choosen probe seems doesn\'t exist.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        # Update Tabs
        TPP.TabProjProb.Update(TPP,6)
        TSP.TabSignProc.Update(TSP,6)
        TFA.TabFreqAnal.Update(TFA,6)
        TPE.TabParEst.Update(TPE,6)
        TBH.TabBrede.Update(TBH,6)
        return

    # @logger.catch
    def on_Button_Add_Probes_clicked(self):
        logger.debug('TabProjProb - on_Button_Add_Probes_clicked')
        # Lunch the wizard for importing a new probe
        WizardAddProbe = WAP.AddProbe()
        WizardAddProbe.exec_()
        TPP.TabProjProb.Update(TPP,4)
        TSP.TabSignProc.Update(TSP,4)
        TFA.TabFreqAnal.Update(TFA,4)
        TPE.TabParEst.Update(TPE,4)
        TBH.TabBrede.Update(TBH,4)
        TFA.TabFreqAnal.Button_FA.setEnabled(True)
        return

    # @logger.catch
    def on_Button_Remove_Probes_clicked(self):
        logger.debug('TabProjProb - on_Button_Remove_Probes_clicked')
        # Delete Check
        string = 'You are deleting the probe: ' + VAR.GetActiveProbe(VAR) + ' from the project '+VAR.GetActiveProject(VAR)+'. Continue?'
        Reply = PQW.QMessageBox.warning(None, VAR.GetSoftwareName(VAR)+' message', string, PQW.QMessageBox.Yes|PQW.QMessageBox.No, PQW.QMessageBox.Yes)
        if(Reply == PQW.QMessageBox.Yes):
            # Update probe list
            probe_list = VAR.GetProbesList(VAR)
            probe_list.remove(VAR.GetActiveProbe(VAR))
            # Delete Project folder
            try:
                shutil.rmtree('../projects/' + str(VAR.GetActiveProject(VAR)) + '/' + str(VAR.GetActiveProbe(VAR)))
                if(len(probe_list) == 0):
                    # Save the new list to projects.ini
                    Handle = open('../projects/'+str(VAR.GetActiveProject(VAR))+'/probes.ini','w')
                    Handle.close()
                    # Set Active Probe
                    VAR.SetActiveProbe(VAR,None)
                    # Set Probe List
                    VAR.SetProbesList(VAR,[])
                else:
                    # Save the new list to probes.ini
                    Handle = open('../projects/'+str(VAR.GetActiveProject(VAR))+'/probes.ini','w')
                    for item in probe_list:
                        Handle.write(item+'\n')
                    Handle.close()
                    # Set Active Probe
                    VAR.SetActiveProbe(VAR,probe_list[0])
                    # Set Probes List
                    VAR.SetProbesList(VAR,probe_list)
            except:
                PQW.QMessageBox.information(None, VAR.GetSoftwareName(VAR) + ' message', 'Error while deleting project.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        # Update
        TPP.TabProjProb.Update(TPP,5)
        TSP.TabSignProc.Update(TSP,5)
        TFA.TabFreqAnal.Update(TSP,5)
        TPE.TabParEst.Update(TSP,5)
        TBH.TabBrede.Update(TBH,5)
        return

    # @logger.catch
    def on_Main_Menu_Probe_Export_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Probe_Export_clicked')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Probe to File', '../exports/' + VAR.GetActiveProbe(VAR), 'Probe Export (*.pbr)')
        if file_export[0]:
            shutil.make_archive(file_export[0], 'zip', '../projects/' + str(VAR.GetActiveProject(VAR))+'/'+str(VAR.GetActiveProbe(VAR)))
            shutil.move(file_export[0] + '.zip', file_export[0])
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Project Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return

    # @logger.catch
    def on_Main_Menu_Probe_Import_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Probe_Import_clicked')
        file_import = PQW.QFileDialog.getOpenFileName(self, 'Select probe file to import...', '../exports/', 'File Probe(*.pbr)')
        if file_import[0]:
            if os.path.isdir('../projects/' + VAR.GetActiveProject(VAR) + '/' + (file_import[0].split('/')[-1]).replace('.pbr','')):
                flag = True
                cont = 1
                while flag:
                    if os.path.isdir('../projects/' + VAR.GetActiveProject(VAR) + '/' + (file_import[0].split('/')[-1]).replace('.pbr','(' + str(cont) +')')):
                        pass
                    else:
                        flag = False
                        target_folder = '../projects/' + VAR.GetActiveProject(VAR) + '/' + (file_import[0].split('/')[-1]).replace('.pbr','(' + str(cont) +')')
                        probe = (file_import[0].split('/')[-1]).replace('.pbr','(' + str(cont) +')')
            else:
                target_folder = '../projects/' + VAR.GetActiveProject(VAR) + '/' +  (file_import[0].split('/')[-1]).replace('.pbr','')
                probe = (file_import[0].split('/')[-1]).replace('.pbr','')
            #
            shutil.move(file_import[0], file_import[0] + '.zip')
            shutil.unpack_archive(file_import[0] + '.zip', target_folder, 'zip')
            shutil.move(file_import[0] + '.zip', file_import[0])
            #
            VAR.SetActiveProbe(VAR,probe)
            probe_list  =VAR.GetProbesList(VAR)
            probe_list.append(probe)
            VAR.SetProbesList(VAR,probe_list)
            Handle = open('../projects/'+VAR.GetActiveProject(VAR)+'/probes.ini','w')
            for item in probe_list:
                Handle.write(item+'\n')
            Handle.close()
            #
            TPP.TabProjProb.Update(TPP,4)
            TSP.TabSignProc.Update(TSP,4)
            TFA.TabFreqAnal.Update(TFA,4)
            TPE.TabParEst.Update(TPE,4)
            TBH.TabBrede.Update(TBH,4)
        #
        return

    # @logger.catch
    def on_Main_Menu_Probe_ExportData_clicked(self):
        logger.debug('TabProjProb - on_Main_Menu_Probe_ExportData_clicked')
        file_export = PQW.QFileDialog.getSaveFileName(self, 'Export Data to File', '../exports/' + VAR.GetActiveProbe(VAR), 'CSV (*.csv)')
        if file_export[0]:
            df_export = pd.read_pickle('../projects/'+VAR.GetActiveProject(VAR)+'/'+VAR.GetActiveProbe(VAR)+'/data/clean.pkz',compression='zip')
            df_export.to_csv(file_export[0],index=False)
            PQW.QMessageBox.information(self, VAR.GetSoftwareName(VAR)+' message', 'Project Export Completed.', PQW.QMessageBox.Ok, PQW.QMessageBox.Ok)
        return