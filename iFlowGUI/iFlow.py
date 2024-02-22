#-------------------------------------------------------------------------------
# Name:        iFlow
# Purpose:     Main file of the iFlow GUI
#
# Author:      Andrea Bertagnoli
#
# Created:     02/18/2021
# Copyright:   (c) user 2021
#              Center for Ecohydraulics
#              University of Idaho
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import standard library
import os,sys
# # import shutil
import PyQt5.QtWidgets as PQW
import PyQt5.QtGui as PQG
# # import PyQt5.QtCore as PQC
# import time
# # # Import custom library
from Variables import VAR
from Options import OPT
import TabProjProb as TPP
import TabFreqAnal as TFA
import TabSignProc as TSP
import TabParEst as TPE
import TabBrede as TB
from loguru import logger
#------------------------------------------------------------------------------#
'''
Main window of iFlow
'''
class iFlowApp(PQW.QMainWindow):
    def __init__(self):
        super().__init__()
        logger.debug("MainApp - Start the program")
        # Set window icon
        self.setWindowIcon(PQG.QIcon('iFlow.ico'))
        # Store class object
        VAR.SetiFlowSelf(VAR, self)
        # Set options Options #! Insert load parameter from file
        HandleConfig = open('../config/config.ini','r')
        OPT.SetHarmonicFlag(OPT,HandleConfig.readline().split(',')[0])
        OPT.SetTFAxAxisUnit(OPT,HandleConfig.readline().split(',')[0])
        HandleConfig.close()
        # Load and store the amplitude correction factor for the FFT window types
        HandleFFTconfig = open('../config/FFTcorAMP.txt')
        Rows = HandleFFTconfig.readlines()
        HandleFFTconfig.close()
        AmpCorrFFT = []
        for Row in Rows:
            AmpCorrFFT.append(float(Row.split(',')[0]))
        OPT.SetFFTcorAMP(OPT,AmpCorrFFT)
        # Load and store the hamonics for the Frequency Analysis  Tab
        HandleHarmonics = open('../harmonics/harmonics.hrm','r')
        Rows = HandleHarmonics.readlines()
        HandleHarmonics.close()
        ListHarminics = []
        for Row in Rows:
            ListHarminics.append(float(Row.replace('\n','')))
        OPT.SetHarmonics(OPT,ListHarminics)
        #
        OPT.SetBasicPeriod(OPT,24)
        # Load the projects crated from the file projects.ini
        try:
            HandleProjIni = open('../projects/projects.ini','r')
            ProjectList = HandleProjIni.readlines()
            HandleProjIni.close()
            #
            for pos,item in enumerate(ProjectList):
                ProjectList[pos] = item.replace('\n','')
        except:
            pass
        #
        if(len(ProjectList) == 0):
            # If No project set Projects List, Active Project, Probes List, Active Probe
            VAR.SetProjectsList(VAR,[])
            VAR.SetActiveProject(VAR,None)
            VAR.SetProbesList(VAR, [])
            VAR.SetActiveProbe(VAR, None)
        else:
            # Set Projects List
            VAR.SetProjectsList(VAR,ProjectList)
            # Set Active project
            VAR.SetActiveProject(VAR,ProjectList[0])
            # Load probes.ini
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
            # Set Color palette to None
            VAR.SetChartColors(VAR,None)
        # Set window title
        self.setWindowTitle(VAR.GetSoftwareName(VAR))
        # Create main widget of the window
        Widget_iFlow = PQW.QWidget()
        self.setCentralWidget(Widget_iFlow)
        # Create grid layot for the window
        Layout_iFlow = PQW.QGridLayout(Widget_iFlow)
        # Create tabwidget
        self.Tabs_iFlow = PQW.QTabWidget()
        # Add Tab Projects/Probes to TabWidget
        self.Tabs_iFlow.addTab(TPP.TabProjProb(), 'Projects/Probes')
        # # Add Tab Frequency Analysis to TabWidget
        self.Tabs_iFlow.addTab(TFA.TabFreqAnal(), 'Frequency analysis')
        # Add Tab Signal Processing to TabWidget
        self.Tabs_iFlow.addTab(TSP.TabSignProc(), 'Signal Processing')
        # Add Tab Parameter Estimation to TabWidget
        self.Tabs_iFlow.addTab(TPE.TabParEst(), 'Parameter Estimation')
        # Add Tab Bredehofet to TabWidget
        self.Tabs_iFlow.addTab(TB.TabBrede(), 'Bredehofet')
        # Insert TabWidget in the grid
        Layout_iFlow.addWidget(self.Tabs_iFlow, 0, 0)
        # Create the menubar of the main window
        Menu = self.menuBar()
        # Add menu Main to menubar
        Menu_Main = Menu.addMenu('Main')
        # Add menu Project to menu Main
        Menu_Project = PQW.QMenu('Project', self)
        # Add action New to menu Project
        Menu_Project_New = PQW.QAction('New', self)
        Menu_Project_New.triggered.connect(VAR.GetTabProjProb(VAR).on_Button_New_Project_clicked)
        # Add action Delete to menu Project
        self.Menu_Project_Del = PQW.QAction('Delete', self)
        self.Menu_Project_Del.triggered.connect(VAR.GetTabProjProb(VAR).on_Button_Del_Project_clicked)
        # Add action Rename to menu Project
        self.Menu_Project_Rename = PQW.QAction('Rename', self)
        self.Menu_Project_Rename.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Project_Rename_clicked)
        # Add action Export to menu Project
        self.Menu_Project_Exp = PQW.QAction('Export', self)
        self.Menu_Project_Exp.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Project_Export_clicked)
        # Add action Import to menu Project
        Menu_Project_Imp = PQW.QAction('Import', self)
        Menu_Project_Imp.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Project_Import_clicked)
        #
        Menu_Project.addAction(Menu_Project_New)
        Menu_Project.addAction(self.Menu_Project_Del)
        Menu_Project.addAction(self.Menu_Project_Rename)
        Menu_Project.addSeparator() # Separator
        Menu_Project.addAction(self.Menu_Project_Exp)
        Menu_Project.addAction(Menu_Project_Imp)
        # Add menu Probe to menu Main
        Menu_Probe = PQW.QMenu('Probe', self)
        self.Menu_Probe_Add = PQW.QAction('Add', self)
        self.Menu_Probe_Add.triggered.connect(VAR.GetTabProjProb(VAR).on_Button_Add_Probes_clicked)
        self.Menu_Probe_Del = PQW.QAction('Delete', self)
        self.Menu_Probe_Del.triggered.connect(VAR.GetTabProjProb(VAR).on_Button_Remove_Probes_clicked)
        self.Menu_Probe_Rename = PQW.QAction('Rename', self)
        self.Menu_Probe_Rename.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Probe_Rename_clicked)
        self.Menu_Probe_ExpData = PQW.QAction('Export Data', self)
        self.Menu_Probe_ExpData.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Probe_ExportData_clicked)
        self.Menu_Probe_Exp = PQW.QAction('Export', self)
        self.Menu_Probe_Exp.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Probe_Export_clicked)
        self.Menu_Probe_Imp = PQW.QAction('Import', self)
        self.Menu_Probe_Imp.triggered.connect(VAR.GetTabProjProb(VAR).on_Main_Menu_Probe_Import_clicked)
        Menu_Probe.addAction(self.Menu_Probe_Add)
        Menu_Probe.addAction(self.Menu_Probe_Del)
        Menu_Probe.addAction(self.Menu_Probe_Rename)
        Menu_Probe.addSeparator()
        Menu_Probe.addAction(self.Menu_Probe_ExpData)
        Menu_Probe.addAction(self.Menu_Probe_Exp)
        Menu_Probe.addAction(self.Menu_Probe_Imp)
        #
        Menu_Exit = PQW.QAction('Exit', self)
        #
        Menu_Main.addMenu(Menu_Project)
        Menu_Main.addMenu(Menu_Probe)
        Menu_Main.addAction(Menu_Exit)
        # Menu: FreqAnalysis
        Menu_Main = Menu.addMenu('Frequency analysis')
        self.Menu_RunFA = PQW.QAction('Run analysis', self)
        self.Menu_RunFA.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_clicked)
        # Menu: FreqAnalysis: Harmonics
        Menu_FA_Harmonics = PQW.QMenu('Harmonics', self)
        if OPT.GetHarmonicFlag(OPT):
            self.Menu_FA_Harmonics_Show = PQW.QAction('Hide Harmonics', self)
        else:
            self.Menu_FA_Harmonics_Show = PQW.QAction('Show Harmonics', self)
        self.Menu_FA_Harmonics_Show.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_Harmonics_Show_clicked)
        self.Menu_FA_Harmonics_Manage = PQW.QAction('Menage Harmonics', self)
        self.Menu_FA_Harmonics_Manage.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_Harmonics_Manage_clicked)
        #
        Menu_FA_Harmonics.addAction(self.Menu_FA_Harmonics_Show)
        Menu_FA_Harmonics.addAction(self.Menu_FA_Harmonics_Manage)
        # Menu: FreqAnalysis: Export
        Menu_FA_Export = PQW.QMenu('Export', self)
        self.Menu_FA_Export_PDA = PQW.QAction('Export PSD', self)
        self.Menu_FA_Export_PDA.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_Export_PDA_clicked)
        self.Menu_FA_Export_Amplitude = PQW.QAction('Export Amplitude', self)
        self.Menu_FA_Export_Amplitude.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_Export_Amplitude_clicked)
        self.Menu_FA_Export_Phase = PQW.QAction('Export Phase', self)
        self.Menu_FA_Export_Phase.triggered.connect(VAR.GetTabFreqAnal(VAR).on_Button_FA_Export_Phase_clicked)
        #
        Menu_FA_Export.addAction(self.Menu_FA_Export_PDA)
        Menu_FA_Export.addAction(self.Menu_FA_Export_Amplitude)
        Menu_FA_Export.addAction(self.Menu_FA_Export_Phase)
        #
        Menu_Main.addAction(self.Menu_RunFA)
        Menu_Main.addMenu(Menu_FA_Harmonics)
        Menu_Main.addMenu(Menu_FA_Export)
        # Menu: SignProce
        Menu_Main = Menu.addMenu('Signal processing')
        self.Menu_RunSP = PQW.QAction('Run analysis', self)
        self.Menu_RunSP.triggered.connect(VAR.GetTabSignProc(VAR).on_Button_SP_clicked)
        self.Menu_SP_Export = PQW.QAction('Export', self)
        self.Menu_SP_Export.triggered.connect(VAR.GetTabSignProc(VAR).on_Button_SPExport_clicked)
        #
        self.Menu_SP_PhaseCorr = PQW.QAction('Phase correction', self)
        self.Menu_SP_PhaseCorr.triggered.connect(VAR.GetTabSignProc(VAR).on_Button_SP_PhaseCorr_clicked)
        self.Menu_SP_BREcalc = PQW.QAction('Phase/Amplitude vs Depth', self)
        self.Menu_SP_BREcalc.triggered.connect(VAR.GetTabSignProc(VAR).on_Button_SP_BREcalc_clicked)
        #
        Menu_Main.addAction(self.Menu_RunSP)
        # Menu_Main.addMenu(Menu_SP_Export)
        Menu_Main.addAction(self.Menu_SP_Export)
        Menu_Main.addAction(self.Menu_SP_PhaseCorr)
        Menu_Main.addAction(self.Menu_SP_BREcalc)
        # Menu: ParEst
        Menu_Main = Menu.addMenu('Parameter estimation')
        self.Menu_RunPE = PQW.QAction('Run analysis', self)
        self.Menu_RunPE.triggered.connect(VAR.GetTabParEst(VAR).on_Button_PE_clicked)
        Menu_PE_Export = PQW.QMenu('Export', self)
        self.Menu_PE_Export_Eta = PQW.QAction('Eta', self)
        self.Menu_PE_Export_Eta.triggered.connect(VAR.GetTabParEst(VAR).on_Button_PE_Export_Eta_clicked)
        self.Menu_PE_Export_Ke = PQW.QAction('Ke', self)
        self.Menu_PE_Export_Ke.triggered.connect(VAR.GetTabParEst(VAR).on_Button_PE_Export_Ke_clicked)
        self.Menu_PE_Export_Flow = PQW.QAction('Flow', self)
        self.Menu_PE_Export_Flow.triggered.connect(VAR.GetTabParEst(VAR).on_Button_PE_Export_Flow_clicked)
        self.Menu_PE_Export_Height = PQW.QAction('Height', self)
        self.Menu_PE_Export_Height.triggered.connect(VAR.GetTabParEst(VAR).on_Button_PE_Export_Height_clicked)
        #
        Menu_PE_Export.addAction(self.Menu_PE_Export_Eta)
        Menu_PE_Export.addAction(self.Menu_PE_Export_Ke)
        Menu_PE_Export.addAction(self.Menu_PE_Export_Flow)
        Menu_PE_Export.addAction(self.Menu_PE_Export_Height)
        #
        # self.Menu_RunPE_Compare = PQW.QAction('Compare', self)
        # self.Menu_RunPE_Compare.triggered.connect(VAR.GetTabSignProc(VAR).on_Button_PE_Compare_clicked)
        #
        Menu_Main.addAction(self.Menu_RunPE)
        Menu_Main.addMenu(Menu_PE_Export)
        # Menu_Main.addAction(self.Menu_RunPE_Compare)
        # Menu: Bredehofet
        Menu_Main = Menu.addMenu('Bredehofet')
        self.Menu_RunBH = PQW.QAction('Run analysis', self)
        self.Menu_RunBH.triggered.connect(VAR.GetTabBrede(VAR).on_Button_BH_clicked)
        self.Menu_BH_Export = PQW.QAction('Export', self)
        self.Menu_BH_Export.triggered.connect(VAR.GetTabBrede(VAR).on_Button_BHExport_clicked)
        #
        Menu_Main.addAction(self.Menu_RunBH)
        Menu_Main.addAction(self.Menu_BH_Export)
        # # Menu: Functions
        # Menu_Main = Menu.addMenu('Functions')
        # # Menu: ?
        # Menu_Main = Menu.addMenu('?')
        # Status Bar
        self.statusBar = PQW.QStatusBar()
        #
        self.progress = PQW.QProgressBar(self)
        self.progress.setFormat('')
        self.progress.setValue(0)
        self.statusBar.addWidget(self.progress)
        #
        self.setStatusBar(self.statusBar)
        # Update Tabs
        TPP.TabProjProb.Update(TPP,0)
        TFA.TabFreqAnal.Update(TFA,0)
        TSP.TabSignProc.Update(TSP,0)
        TPE.TabParEst.Update(TPE,0)
        TB.TabBrede.Update(TB,0)

if __name__ == '__main__':
    logger.remove()
    logger.add(F"../logs/GUI.log", rotation="7 days")
    
    app = PQW.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    VAR.SetWindowsSize(VAR, width, height)
    iFlow = iFlowApp()
    iFlow.showMaximized()
    iFlow.show()
    sys.exit(app.exec_())
