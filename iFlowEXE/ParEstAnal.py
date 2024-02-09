################################# 
# 
# 
# 
# 
#
#     Probe name  [STRING] -p
#     Project name  [STRING] -j
#     Sensors [LIST] -s
#     Heights [LIST] -h
#     Run [STRING] -r
#     PeriodPos [INTEGER] -e
#     Period [FLOAT] -f
#     Bed Elevation [FLOAT] -z
#     Top Sensor [STRING] -u
#     dt [FLOAT] -d
############################### 

# Import the libraries
import sys#os,sys
import getopt
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import numpy as np
# import glob
# import scipy.stats
# import pickle

class ParEstAnal:
    def __init__(self,opts, args):
        #
        self.Sensors = []#['T0','T1','T2','T4','T6'] # Sensors List
        self.Heights = []#['0.0','-0.15','-0.3','-0.6','-0.9'] # Sensors height
        self.RunSP = '-9'#'0' # Signal processing run
        self.Period = np.nan#0 # Position Period to analyze 
        self.PeriodValue = np.nan#24.0 # Value Period to analyze
        self.BElev = np.nan#0.0 # Bed Elevetion
        self.TopSens = ''#'T0' # Sensor to use as water sensor
        self.dt = np.nan#900.0 #None # dt of the data
        self.OutputFolder = '../temp' # Output folder.
        self.InputFolder = '../temp' # Input folder.
        self.Version = False # Flag display version and stop the execution.
        self.FlagUpdate = False
        self.RunUpdate = '-9'
        #
        for opt, arg in opts:
            if opt in ('-s'):
                self.Sensors = []
                for item in arg.split(','):
                    self.Sensors.append(item)
            elif opt in ('-h'):
                self.Heights = []
                for item in arg.split(','):
                    self.Heights.append(item)
            elif opt in ('-r'):
                self.RunSP = arg
            elif opt in ('-e'):
                self.Period = int(arg)
            elif opt in ('-f'):
                self.PeriodValue = float(arg)
            elif opt in ('-z'):
                self.BElev = float(arg)
            elif opt in ('-u'):
                self.TopSens = arg
            elif opt in ('-d'):
                self.dt = float(arg)
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in ('-i'):
                self.InputFolder = arg
            elif opt in('--version'):
                self.Version = True
            elif opt in ('-c'):
                if arg == 'False':
                    self.FlagUpdate = False
                else:
                    self.FlagUpdate = True
            elif opt in ('-b'):
                self.RunUpdate = arg
        return

    def CheckOptions(self):
        '''CheckOptions [summary]
        [extended_summary]
        Returns:
            [type]: [description]
        '''
        print('CheckOptions...')
        try:
            #  
            FlagPreCheck = True
            # Check Options type
            if type(self.RunSP) != str : FlagPreCheck = False
            if type(self.Period) != int : FlagPreCheck = False
            if type(self.PeriodValue) != float : FlagPreCheck = False
            if type(self.BElev) != float : FlagPreCheck = False
            if type(self.TopSens) != str : FlagPreCheck = False
            if type(self.dt) != float : FlagPreCheck = False
            if type(self.OutputFolder) != str: FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
            if type(self.FlagUpdate) != bool : FlagPreCheck = False
            if type(self.RunUpdate) != str: FlagPreCheck = False
            #
            for item in self.Sensors:
                if type(item) != str:
                    FlagPreCheck = False
                    break
            #
            for item in self.Heights:
                if type(item) != str:
                    FlagPreCheck = False
                    break
            #
            if self.Version:
                print('Version 0.1')
                return False
            return FlagPreCheck
        except:
            return False

    def LoadData(self):
        '''LoadData [summary]
        [extended_summary]
        Returns:
            [type]: [description]
        '''
        print('LoadData...')
        try:
            # Load the Time
            self.MobTimeWin = pd.read_pickle(self.InputFolder+'/MobWinTime.pkz',compression='zip').to_numpy()
            #
            # Load the Amplitude
            Amplitude = pd.read_pickle(self.InputFolder+'/Amplitude.pkz',compression='zip')
            self.df_Amp = Amplitude[Amplitude['Freq'] == 1.0/float(self.PeriodValue)/3600.0]
            del self.df_Amp['Freq']
            #
            for item in self.df_Amp.columns.tolist()[1:]:
                if item in self.Sensors:
                    pass
                else:
                    del self.df_Amp[item]
            #
            self.ColName = self.df_Amp.columns.tolist()
            # Load Phase
            Phase = pd.read_pickle(self.InputFolder+'/Phase.pkz',compression='zip')
            self.df_Phase = Phase[Phase['Freq'] == 1.0/float(self.PeriodValue)/3600.0]
            del self.df_Phase['Freq']
            #
            for item in self.df_Phase.columns.tolist()[1:]:
                if item in self.Sensors:
                    pass
                else:
                    del self.df_Phase[item]
            #
            if self.FlagUpdate:
                pass
            else:
                self.MobTimeWinOld = []
            #
            return True
        except:
            return False

    def Processing(self):
        '''Processing [summary]
        [extended_summary]
        Returns:
            [type]: [description]
        '''
        print('Processing...')
        try:
            Omega = 2 * np.pi / (self.PeriodValue * 3600.0)
            #
            PosTopSens = self.Sensors.index(self.TopSens)
            # Check Bed Elevation
            if self.BElev > float(self.Heights[PosTopSens]):
                self.BElev = float(self.Heights[PosTopSens])
            # Eta
            self.df_eta = pd.DataFrame(columns = self.ColName)
            self.df_ke = pd.DataFrame(columns = self.ColName)
            #
            EtaBase = [np.nan for i in range(0,len(self.ColName))]
            KeBase = [np.nan for i in range(0,len(self.ColName))]
            #
            for t in range(0,self.MobTimeWin.shape[0]):
                print(t,self.MobTimeWin.shape[0])
                if self.MobTimeWin[t] in self.MobTimeWinOld:
                    pass
                else:
                    EtaTemp = EtaBase
                    KeTemp = KeBase
                    AmpTemp = (self.df_Amp.iloc[t]).tolist()
                    PhaseTemp = (self.df_Phase.iloc[t]).tolist()
                    EtaTemp[0] = AmpTemp[0]
                    KeTemp[0] = AmpTemp[0]
                    #
                    for i in range(PosTopSens+2,len(self.ColName)):
                        if PhaseTemp[i] < PhaseTemp[PosTopSens+1]:
                            EtaTemp[i] = np.nan
                            KeTemp[i] = np.nan
                        elif AmpTemp[i] > AmpTemp[PosTopSens+1]:
                            EtaTemp[i] = np.nan
                            KeTemp[i] = np.nan
                        elif (PhaseTemp[i]-PhaseTemp[PosTopSens+1]) > 2*np.pi:
                            try:
                                #
                                pos0 = int(np.floor(self.PeriodValue*3600.0/self.dt))
                                pos1 = int(np.ceil(self.PeriodValue*3600.0/self.dt))
                                #
                                p0 = ((self.df_Phase.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i]
                                p1 = ((self.df_Phase.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i]
                                #
                                if pos0 == pos1:
                                    PhaseInt = p0
                                else:
                                    PhaseInt = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (p1-p0) + p0
                                #
                                a0 = ((self.df_Amp.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i]
                                a1 = ((self.df_Amp.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i]
                                #
                                if pos0 == pos1:
                                    AmpInt = a0
                                else:
                                    AmpInt = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (a1-a0) + a0
                                #
                                if PhaseInt < PhaseTemp[PosTopSens+1]:
                                    EtaTemp[i] = np.nan
                                    KeTemp[i] = np.nan
                                elif AmpInt > AmpTemp[PosTopSens+1]:
                                    EtaTemp[i] = np.nan
                                    KeTemp[i] = np.nan
                                else:
                                    EtaTemp[i] = (-np.log(AmpInt/AmpTemp[PosTopSens+1]))/(PhaseInt-PhaseTemp[PosTopSens+1])
                                    KeTemp[i] = Omega * ((self.BElev - float(self.Heights[i-1])) ** 2) * EtaTemp[i] / ((PhaseInt-PhaseTemp[PosTopSens+1]) ** 2) / (1 + (EtaTemp[i] ** 2))
                            except:
                                EtaTemp[i] = np.nan
                                KeTemp[i] = np.nan
                        else:
                            EtaTemp[i] = (-np.log(AmpTemp[i]/AmpTemp[PosTopSens+1]))/(PhaseTemp[i]-PhaseTemp[PosTopSens+1])
                            KeTemp[i] = Omega * ((self.BElev - float(self.Heights[i-1])) ** 2) * EtaTemp[i] / ((PhaseTemp[i]-PhaseTemp[PosTopSens+1]) ** 2) / (1 + (EtaTemp[i] ** 2))
                    #
                    self.df_eta.loc[t] = EtaTemp
                    self.df_ke.loc[t] = KeTemp
#             #
            return True
        except:
            return False
            
    def SaveData(self):
        '''SaveData [summary]
        [extended_summary]
        Returns:
            [type]: [description]
        '''
        print('SaveData...')
        try:
#             self.MobTimeWin.to_pickle('../temp/MobWinTime.pkz', compression='zip')
            self.df_eta.to_pickle('../temp/Eta.pkz', compression='zip')
            self.df_ke.to_pickle('../temp/Ke.pkz', compression='zip')
            #
            return True
        except:
            return False

if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        opts, args = getopt.getopt(options,'p:j:s:r:e:z:u:h:f:d:o:i:',['version'])
        #
        StringError = 'No Error'
        PE = ParEstAnal(opts, args)
        result = PE.CheckOptions()
        if result:
            result = PE.LoadData()
            if result:
                result = PE.Processing()
                if result:
                    result = PE.SaveData()
                    if result:
                        # ImportLog
                        HandleRiassunto = open(PE.OutputFolder+'/XXX.run','w')
                        HandleRiassunto.write(','.join(PE.Sensors)+';SensorsKe\n')
                        HandleRiassunto.write(','.join(PE.Heights)+';HeightsKe\n')
                        HandleRiassunto.write(PE.RunSP+';RunSPKe\n')
                        HandleRiassunto.write(str(PE.Period)+';PeriodKe\n')
                        HandleRiassunto.write(str(PE.PeriodValue)+';PeriodValueKe\n')
                        HandleRiassunto.write(str(PE.BElev)+';BElevKe\n')
                        HandleRiassunto.write(PE.TopSens+';TopSensKe\n')
                        HandleRiassunto.write(str(PE.dt)+';dtKe\n')
                        HandleRiassunto.close()
                    else:
                        StringError = 'SaveData Error'
                else:
                    StringError = 'Processing Error'
            else:
                StringError = 'LoadData Error'
        else:
            StringError = 'CheckOptions Error'
        #
        HandleLog = open('../temp/EtaKe.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open('../temp/EtaKe.log','w')
        HandleLog.write('Options error')
        HandleLog.close()