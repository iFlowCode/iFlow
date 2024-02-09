#-----------------------------------------------------------------------------#
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
#-----------------------------------------------------------------------------#
class VAR():

    # def SetLoguru(self, object):
    #     self.loguru_log = object
    #     return
    
    # def GetLoguru(self):
    #     return self.loguru_log



#-----------------------------------------------------------------------------#
    '''
    Name of software
    '''
    def GetSoftwareName(self):
        return 'iFLOW' #Ondo kara no nagare - Flusso della temperatura
#-----------------------------------------------------------------------------#
    '''
    Monitor resolution in pixels - Set and Get procedure
    '''
    def SetWindowsSize(self,WidthPX,HeightPX):
        self.WidthPX = WidthPX
        self.HeightPX = HeightPX
        return
    def GetWindowsSize(self):
        return self.WidthPX,self.HeightPX
    def GetWindowsWidth(self):
        return self.WidthPX
    def GetWindowsHeight(self):
        return self.HeightPX
#-----------------------------------------------------------------------------#
    '''
    Projects List
    Empty list if there is not project created 
    '''
    def SetProjectsList(self,ProjectsList):
        self.ProjectsList = ProjectsList
        return
    def GetProjectsList(self):
        return self.ProjectsList
#-----------------------------------------------------------------------------#
    '''
    Active Project
    None if there is not an active project
    '''
    def SetActiveProject(self,ActiveProject):
        self.ActiveProject = ActiveProject
        return
    def GetActiveProject(self):
        return self.ActiveProject
#-----------------------------------------------------------------------------#
    '''
    Probes List
    Empty list if there is not probe in the active project
    '''
    def SetProbesList(self,ProbesList):
        self.ProbesList = ProbesList
        return
    def GetProbesList(self):
        return self.ProbesList
#-----------------------------------------------------------------------------#
    '''
    Active Probe
    None if there is not an active probe
    '''
    def SetActiveProbe(self,ActiveProbe):
        self.ActiveProbe = ActiveProbe
        return
    def GetActiveProbe(self):
        return self.ActiveProbe
#-----------------------------------------------------------------------------#
    '''
    Active probe's parameters
    '''
    def SetActiveParameters(self,List):
        self.LastFile = List[0]
        self.TimeserieSerieName = List[1]
        self.TimeType = List[2]
        self.SampleRate = List[3]
        self.IMD = List[4]
        self.RTS = List[5]
        self.SensorsList = List[6]
        self.SensorsHeight = List[7]
        self.From = List[8]
        self.To = List[9]
        self.FlagUpdate = List[10]
        self.FlagTimeSerie = List[11]
        self.FlagHeader = List[12]
        return

    def GetActiveParameters(self,Code):
        if Code == 0:
            return self.LastFile
        elif Code == 1:
            return self.TimeserieSerieName
        elif Code == 2:
            return self.TimeType
        elif Code == 3:
            return self.SampleRate
        elif Code == 4:
            return self.IMD
        elif Code == 5:
            return self.RTS
        elif Code == 6:
            return self.SensorsList
        elif Code == 7:
            return self.SensorsHeight
        elif Code == 8:
            return self.From
        elif Code == 9:
            return self.To
        elif Code == 10:
            return self.FlagUpdate
        elif Code == 11:
            return self.FlagTimeSerie
        elif Code == 12:
            return self.FlagHeader


#%%-----------------------------------------------------------------------------#
    '''
    Main self
    '''
    def SetiFlowSelf(self, iFlow_self):
        self.iFlow_self = iFlow_self
        return
    def GetiFlowSelf(self):
        return self.iFlow_self 
#-----------------------------------------------------------------------------#
    '''
    TabBrede self
    '''
    def SetTabBrede(self, TabBrede_self):
        self.TabBrede_self = TabBrede_self
        return
    def GetTabBrede(self):
        return self.TabBrede_self 
#-----------------------------------------------------------------------------#
    '''
    TabProjProb self
    '''
    def SetTabProjProb(self, TabProjProb_self):
        self.TabProjProb_self = TabProjProb_self
        return
    def GetTabProjProb(self):
        return self.TabProjProb_self 
#-----------------------------------------------------------------------------#
    '''
    TabFreqAnal self
    '''
    def SetTabFreqAnal(self, TabFreqAnal_self):
        self.TabFreqAnal_self = TabFreqAnal_self
        return
    def GetTabFreqAnal(self):
        return self.TabFreqAnal_self 
#-----------------------------------------------------------------------------#
    '''
    TabSignProc self
    '''
    def SetTabSignProc(self, TabSignProc_self):
        self.TabSignProc_self = TabSignProc_self
        return
    def GetTabSignProc(self):
        return self.TabSignProc_self 
#-----------------------------------------------------------------------------#
    '''
    TabParEst self
    '''
    def SetTabParEst(self, TabParEst_self):
        self.TabParEst_self = TabParEst_self
        return
    def GetTabParEst(self):
        return self.TabParEst_self 






#-----------------------------------------------------------------------------#   
    '''
    List of time format
    '''
    def GetTimeserieTypeString(self):
        self.types = ['','Time', 'yyyy-mm-dd h24:min:sec']
        return self.types
#-----------------------------------------------------------------------------#
    '''
    Windows function for FFT
    '''
    def GetFFTWindowfunction(self):
        return ['','Rectangular','Triangular','Bartlett','Hanning','Hamming','FlatTop']
#-----------------------------------------------------------------------------#
    '''
    Processing Methods
    '''
    def GetProcessingMethod(self):
        return ['','FFT','LPM']
#-----------------------------------------------------------------------------#
    '''
    Processing Methods
    '''
    def GetEstimationMethod(self):
        return ['','Analytical','MLEn']
#-----------------------------------------------------------------------------#
    '''
    Detrending Methods
    '''
    def GetDetrending(self):
        return ['','Yes','No']
#-----------------------------------------------------------------------------#
    '''
    Chart Type Signal Processing
    '''
    def GetChartTypeSignalProcessin(self):
        return ['SNR heatmap','SNR vs Time','Phase vs Time','Amplitude vs Time','Amplitude vs Frequency','Phase vs Frequency']
#-----------------------------------------------------------------------------#
    '''
    Chart Type Parameter Estimation
    '''
    def GetChartTypeParameterEstimation(self):
        return ['Eta','Ke','Heights','Flux','K','Q']
#-----------------------------------------------------------------------------#
    '''
    Chart Type Frequency Analysis
    '''
    def GetChartTypeFrequecyAnalysis(self):
        return ['Frequecies vs PSD','Frequecies vs Amplitude','Frequecies vs LogAmpRatio','Frequecies vs DiffPhase']
#-----------------------------------------------------------------------------#   
    '''
    Default folder for file dialog
    '''
    def DefaultFolderFileDialog(self):
        return '../'
#------------------------------------------------------------------------------#
    '''
    Data chart colors
    '''
    def SetChartColors(self, colors):
        self.chart_colors = colors
        return

    def GetChartColors(self):
        return self.chart_colors
#%% 
    '''
    Window height reference 
    '''
    def GetWindowHeightReference(self):
        return 1080
#------------------------------------------------------------------------------#
    '''
    Window width reference 
    '''
    def GetWindowWidthReference(self):
        return 1920
#------------------------------------------------------------------------------#
    '''
    Font Titles size for Matplotlib
    '''
    def GetMPLAxisTitleFontSizeReference(self):
        return 12
#------------------------------------------------------------------------------#
    '''
    Font Axis size for Matplotlib
    '''
    def GetMPLAxisTickFontSizeReference(self):
        return 10

#------------------------------------------------------------------------------#
    '''
    Font Legend size for Matplotlib
    '''
    def GetMPLLegendFontSizeReference(self):
        return 10

#------------------------------------------------------------------------------#
    '''
    Height of Comboboxs
    '''
    def GetConboBoxHeight(self):
        return 20