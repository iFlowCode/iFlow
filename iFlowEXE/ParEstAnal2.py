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
#     dt [FLOAT] -d
#     Bed Elevation [FLOAT] -z
#     Gamma [FLOAT] -g
#     From [FLOAT] -f
#     To [FLOAT] -t
#     ke [LIST] -k
#     Run [STRING] -r
#     PeriodPos [INTEGER] -e
#     Period [FLOAT] -x
############################### 

# Import the libraries
import os,sys
import getopt
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import numpy as np
import pickle

class ParEstAnal2:
    def __init__(self,opts, args):
        #
        self.Sensors = []#['T0','T1','T2','T4','T6']
        self.Heights = []#[0.0,-0.15,-0.3,-0.6,-0.9]
        self.Gamma = 1.0
        self.From = np.nan#86400.0
        self.To = np.nan#2331900.0
        self.RunSP = ''#'0'
        self.Period = np.nan#0
        self.PeriodValue = np.nan#24.0
        self.BRE = np.nan#0.0
        self.Ke = []#[5.004792e-07,5.004792e-07,4.996599e-07,4.994111e-07,4.993549e-07,4.993936e-07,4.996401e-07]
        self.dt = np.nan#900.0
        self.OutputFolder = '../temp' # Output folder.
        self.Version = False # Flag display version and stop the execution.
        self.InputFolder = '../temp' # Input folder.
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
                    self.Heights.append(float(item))
            elif opt in ('-d'):
                self.dt = float(arg)
            elif opt in ('-z'):
                self.BRE = float(arg)
            elif opt in ('-g'):
                self.Gamma = float(arg)
            elif opt in ('-f'):
                self.From = float(arg)
            elif opt in ('-t'):
                self.To = float(arg)
            elif opt in ('-e'):
                self.Period = int(arg)
            elif opt in ('-x'):
                self.PeriodValue = float(arg)
            elif opt in ('-r'):
                self.RunSP = arg
            elif opt in ('-k'):
                self.Ke = []
                for item in arg.split(','):
                    self.Ke.append(float(item))
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in ('-i'):
                self.InputFolder = arg
            elif opt in ('-c'):
                if arg == 'False':
                    self.FlagUpdate = False
                else:
                    self.FlagUpdate = True
            elif opt in ('-b'):
                self.RunUpdate = arg

            elif opt in('--version'):
                self.Version = True
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
            if type(self.dt) != float : FlagPreCheck = False
            if type(self.BRE) != float : FlagPreCheck = False
            if type(self.Gamma) != float : FlagPreCheck = False
            if type(self.From) != float : FlagPreCheck = False
            if type(self.RunSP) != str : FlagPreCheck = False
            if type(self.To) != float : FlagPreCheck = False
            if type(self.Period) != int : FlagPreCheck = False
            if type(self.PeriodValue) != float : FlagPreCheck = False
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
                if type(item) != float:
                    FlagPreCheck = False
                    break
            #
            for item in self.Ke:
                if type(item) != float:
                    FlagPreCheck = False
                    break
            #
            self.From = np.ceil(self.From / self.dt) * self.dt
            self.To = np.floor(self.To / self.dt) * self.dt
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
            self.ColName = ['Time']
            for item in self.Sensors:
                self.ColName.append(item)
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
            # Calculate Omega
            Omega = 2 * np.pi / (self.PeriodValue * 3600.0)
            # Initialize Dataframe
            self.eta = pd.DataFrame(np.nan, index=[i for i in range(0,len(self.MobTimeWin))], columns=self.ColName)
            self.heigths = pd.DataFrame(np.nan, index=[i for i in range(0,len(self.MobTimeWin))], columns=self.ColName)
            self.velocity = pd.DataFrame(np.nan, index=[i for i in range(0,len(self.MobTimeWin))], columns=self.ColName)
            self.q = pd.DataFrame(np.nan, index=[i for i in range(0,len(self.MobTimeWin))], columns=self.ColName)
            #
            self.eta['Time'] = self.MobTimeWin
            self.heigths['Time'] = self.MobTimeWin
            self.velocity['Time'] = self.MobTimeWin
            self.q['Time'] = self.MobTimeWin
            #
            # StartIndex = (self.MobTimeWin['Time'].index[self.MobTimeWin['Time']==self.From].tolist())[0]
            # EndIndex = (self.MobTimeWin['Time'].index[self.MobTimeWin['Time']==self.To].tolist())[0]
            StartIndex = (self.eta['Time'].index[self.eta['Time']>=self.From].tolist())[0]
            EndIndex = (self.eta['Time'].index[self.eta['Time']<=self.To].tolist())[len((self.eta['Time'].index[self.eta['Time']<=self.To].tolist()))-1]
            # Costant Period
            for t in range(StartIndex,EndIndex):
                if self.MobTimeWin[t] in self.MobTimeWinOld:
                    pass
                else:
                    if t == StartIndex:
                        if self.Heights[0] < self.BRE:
                            heightsWork = self.Heights[0]
                            SensWater = 0
                        else:
                            heightsWork = self.BRE
                            for j in range(0,len(self.Heights)):
                                if heightsWork > self.Heights[j]:
                                    SensWater = j-1
                                    break
                        HiniBack = heightsWork
                    else:
                        if self.Heights[0] < heightsWork:
                            heightsWork = self.Heights[0]
                            SensWater = 0
                        else:
                            for j in range(0,len(self.Heights)):
                                if heightsWork > self.Heights[j]:
                                    SensWater = j-1
                                    break
                    # Check SensWater
                    if np.isnan(self.df_Amp.iloc[t,SensWater+1]) or np.isnan(self.df_Phase.iloc[t,SensWater+1]):
                        for Sens in range(SensWater-1,-1,-1):
                            if np.isnan(self.df_Amp.iloc[t,Sens+1])  or np.isnan(self.df_Phase.iloc[t,Sens+1]):
                                pass
                            else:
                                SensWater = Sens
                                break
                    #
                    for i in range(len(self.ColName[1:])):
                        if i <= SensWater:
                            self.eta[self.ColName[i+1]].loc[t] = np.nan
                            self.heigths[self.ColName[i+1]].loc[t] = np.nan
                            self.velocity[self.ColName[i+1]].loc[t] = np.nan
                            self.q[self.ColName[i+1]].loc[t] = np.nan
                        else:
                            AmpWater = self.df_Amp.iloc[t,SensWater+1]
                            PhaseWater = self.df_Phase.iloc[t,SensWater+1]
                            AmpSoil = self.df_Amp.iloc[t,i+1]
                            PhaseSoil = self.df_Phase.iloc[t,i+1]
                            # check next day
                            if PhaseSoil-PhaseWater > 2*np.pi:
                                try:
                                    pos0 = int(np.floor(self.PeriodValue*3600.0/self.dt))
                                    pos1 = int(np.ceil(self.PeriodValue*3600.0/self.dt))
                                    #
                                    p0 = ((self.df_Phase.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    p1 = ((self.df_Phase.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        PhaseSoil = p0
                                    else:
                                        PhaseSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (p1-p0) + p0
                                    #
                                    a0 = ((self.df_Amp.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    a1 = ((self.df_Amp.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        AmpSoil = a0
                                    else:
                                        AmpSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (a1-a0) + a0
                                except:
                                    PhaseSoil = np.nan
                                    AmpSoil = np.nan
                            #
                            if AmpWater < AmpSoil:
                                self.eta[self.ColName[i+1]].loc[t] = np.nan
                                self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                self.q[self.ColName[i+1]].loc[t] = np.nan
                            else:
                                if PhaseSoil < PhaseWater:
                                    self.eta[self.ColName[i+1]].loc[t] = np.nan
                                    self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                    self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                    self.q[self.ColName[i+1]].loc[t] = np.nan
                                else:
                                    dPhaseWork = PhaseSoil-PhaseWater
                                    etaWork = -np.log(AmpSoil/AmpWater)/dPhaseWork
                                    dzWork = dPhaseWork*((self.Ke[i]/Omega*(etaWork+1/etaWork))**(0.5))
                                    qWork = -self.Gamma*Omega*dzWork/dPhaseWork*(1-etaWork**2)/(1+etaWork**2)
                                    self.eta[self.ColName[i+1]].loc[t] = etaWork
                                    self.heigths[self.ColName[i+1]].loc[t] = heightsWork
                                    self.velocity[self.ColName[i+1]].loc[t] = qWork/self.Gamma
                                    self.q[self.ColName[i+1]].loc[t] = qWork

            # forward
            for t in range(EndIndex,len(self.MobTimeWin)):
                if self.MobTimeWin[t] in self.MobTimeWinOld:
                    pass
                else:
                    if self.Heights[0] < heightsWork:
                        heightsWork = self.Heights[0]
                        SensWater = 0
                    else:
                        for j in range(0,len(self.Heights)):
                            if heightsWork > self.Heights[j]:
                                SensWater = j-1
                                break
                    # Check SensWater
                    if np.isnan(self.df_Amp.iloc[t,SensWater+1]) or np.isnan(self.df_Phase.iloc[t,SensWater+1]):
                        for Sens in range(SensWater-1,-1,-1):
                            if np.isnan(self.df_Amp.iloc[t,Sens+1])  or np.isnan(self.df_Phase.iloc[t,Sens+1]):
                                pass
                            else:
                                SensWater = Sens
                                break
                    #
                    FlagHeight = True
                    FlagHeightSens = False
                    for i in range(len(self.ColName[1:])):
                        if i <= SensWater:
                            self.eta[self.ColName[i+1]].loc[t] = np.nan
                            self.heigths[self.ColName[i+1]].loc[t] = np.nan
                            self.velocity[self.ColName[i+1]].loc[t] = np.nan
                            self.q[self.ColName[i+1]].loc[t] = np.nan
                        else:
                            AmpWater = self.df_Amp.iloc[t,SensWater+1]
                            PhaseWater = self.df_Phase.iloc[t,SensWater+1]
                            AmpSoil = self.df_Amp.iloc[t,i+1]
                            PhaseSoil = self.df_Phase.iloc[t,i+1]
                            # check next day
                            if PhaseSoil-PhaseWater > 2*np.pi:
                                try:
                                    pos0 = int(np.floor(self.PeriodValue*3600.0/self.dt))
                                    pos1 = int(np.ceil(self.PeriodValue*3600.0/self.dt))
                                    #
                                    p0 = ((self.df_Phase.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    p1 = ((self.df_Phase.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        PhaseSoil = p0
                                    else:
                                        PhaseSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (p1-p0) + p0
                                    #
                                    a0 = ((self.df_Amp.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    a1 = ((self.df_Amp.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        AmpSoil = a0
                                    else:
                                        AmpSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (a1-a0) + a0
                                except:
                                    PhaseSoil = np.nan
                                    AmpSoil = np.nan
                            #
                            if AmpWater < AmpSoil:
                                self.eta[self.ColName[i+1]].loc[t] = np.nan
                                self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                self.q[self.ColName[i+1]].loc[t] = np.nan
                            else:
                                if PhaseSoil < PhaseWater:
                                    self.eta[self.ColName[i+1]].loc[t] = np.nan
                                    self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                    self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                    self.q[self.ColName[i+1]].loc[t] = np.nan
                                else:
                                    dPhaseWork = PhaseSoil-PhaseWater
                                    etaWork = -np.log(AmpSoil/AmpWater)/dPhaseWork
                                    dzWork = dPhaseWork*(self.Ke[i]/Omega*(etaWork+1/etaWork))**(0.5)
                                    qWork = -self.Gamma*Omega*dzWork/dPhaseWork*(1-etaWork**2)/(1+etaWork**2)
                                    self.eta[self.ColName[i+1]].loc[t] = etaWork
                                    self.heigths[self.ColName[i+1]].loc[t] = self.Heights[i] + dzWork
                                    self.velocity[self.ColName[i+1]].loc[t] = qWork/self.Gamma
                                    self.q[self.ColName[i+1]].loc[t] = qWork
                                    #
                                    heightsWorkTemp = self.Heights[i] + dzWork
                                    if heightsWorkTemp > self.Heights[0]:
                                        heightsWorkTemp = self.Heights[0]
                                    #
                                    FlagHeightSens = True
                        #
                        if FlagHeight:
                            if FlagHeightSens:
                                if np.isnan(heightsWorkTemp):
                                    pass
                                else:
                                    heightsWork = heightsWorkTemp
                                    FlagHeight = False

            # backward
            heightsWork = HiniBack
            for t in range(StartIndex-1,-1,-1):
                if self.MobTimeWin[t] in self.MobTimeWinOld:
                    pass
                else:
                    if self.Heights[0] < heightsWork:
                        heightsWork = self.Heights[0]
                        SensWater = 0
                    else:
                        for j in range(0,len(self.Heights)):
                            if heightsWork > self.Heights[j]:
                                SensWater = j-1
                                break
                    # Check SensWater
                    if np.isnan(self.df_Amp.iloc[t,SensWater+1]) or np.isnan(self.df_Phase.iloc[t,SensWater+1]):
                        for Sens in range(SensWater-1,-1,-1):
                            if np.isnan(self.df_Amp.iloc[t,Sens+1])  or np.isnan(self.df_Phase.iloc[t,Sens+1]):
                                pass
                            else:
                                SensWater = Sens
                                break
                    #
                    FlagHeight = True
                    FlagHeightSens = False
                    for i in range(len(self.ColName[1:])):
                        if i <= SensWater:
                            self.eta[self.ColName[i+1]].loc[t] = np.nan
                            self.heigths[self.ColName[i+1]].loc[t] = np.nan
                            self.velocity[self.ColName[i+1]].loc[t] = np.nan
                            self.q[self.ColName[i+1]].loc[t] = np.nan
                        else:
                            AmpWater = self.df_Amp.iloc[t,SensWater+1]
                            PhaseWater = self.df_Phase.iloc[t,SensWater+1]
                            AmpSoil = self.df_Amp.iloc[t,i+1]
                            PhaseSoil = self.df_Phase.iloc[t,i+1]
                            # check next day
                            if PhaseSoil-PhaseWater > 2*np.pi:
                                try:
                                    pos0 = int(np.floor(self.PeriodValue*3600.0/self.dt))
                                    pos1 = int(np.ceil(self.PeriodValue*3600.0/self.dt))
                                    #
                                    p0 = ((self.df_Phase.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    p1 = ((self.df_Phase.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        PhaseSoil = p0
                                    else:
                                        PhaseSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (p1-p0) + p0
                                    #
                                    a0 = ((self.df_Amp.iloc[t+int(np.floor(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    a1 = ((self.df_Amp.iloc[t+int(np.ceil(self.PeriodValue*3600.0/self.dt))]).tolist())[i+1]
                                    #
                                    if pos0 == pos1:
                                        AmpSoil = a0
                                    else:
                                        AmpSoil = (self.PeriodValue*3600.0/self.dt - np.floor(self.PeriodValue*3600.0/self.dt)) / (np.ceil(self.PeriodValue*3600.0/self.dt) - np.floor(self.PeriodValue*3600.0/self.dt)) * (a1-a0) + a0
                                except:
                                    PhaseSoil = np.nan
                                    AmpSoil = np.nan
                            #
                            if AmpWater < AmpSoil:
                                self.eta[self.ColName[i+1]].loc[t] = np.nan
                                self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                self.q[self.ColName[i+1]].loc[t] = np.nan
                            else:
                                if PhaseSoil < PhaseWater:
                                    self.eta[self.ColName[i+1]].loc[t] = np.nan
                                    self.heigths[self.ColName[i+1]].loc[t] = np.nan
                                    self.velocity[self.ColName[i+1]].loc[t] = np.nan
                                    self.q[self.ColName[i+1]].loc[t] = np.nan
                                else:
                                    dPhaseWork = PhaseSoil-PhaseWater
                                    etaWork = -np.log(AmpSoil/AmpWater)/dPhaseWork
                                    dzWork = dPhaseWork*(self.Ke[i]/Omega*(etaWork+1/etaWork))**(0.5)
                                    # heightsWork = self.Heights[i] + dzWork
                                    # if heightsWork > self.Heights[0]:
                                    #     heightsWork = self.Heights[0]
                                    qWork = -self.Gamma*Omega*dzWork/dPhaseWork*(1-etaWork**2)/(1+etaWork**2)
                                    self.eta[self.ColName[i+1]].loc[t] = etaWork
                                    self.heigths[self.ColName[i+1]].loc[t] = self.Heights[i] + dzWork
                                    self.velocity[self.ColName[i+1]].loc[t] = qWork/self.Gamma
                                    self.q[self.ColName[i+1]].loc[t] = qWork
                                    #
                                    heightsWorkTemp = self.Heights[i] + dzWork
                                    if heightsWorkTemp > self.Heights[0]:
                                        heightsWorkTemp = self.Heights[0]
                                    #
                                    FlagHeightSens = True
                        #
                        if FlagHeight:
                            if FlagHeightSens:
                                if np.isnan(heightsWorkTemp):
                                    pass
                                else:
                                    heightsWork = heightsWorkTemp
                                    FlagHeight = False
            #
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
            self.eta.to_pickle('../temp/eta2.pkz', compression='zip')
            self.heigths.to_pickle('../temp/BEC.pkz', compression='zip')
            self.q.to_pickle('../temp/Q.pkz', compression='zip')
            self.velocity.to_pickle('../temp/Velocity.pkz', compression='zip')
            #
            return True
        except:
            return False

if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        opts, args = getopt.getopt(options,'p:j:s:h:d:z:g:f:t:k:r:x:e:i:o:',['version'])
        #
        StringError = 'No Error'
        PE2 = ParEstAnal2(opts, args)
        result = PE2.CheckOptions()
        if result:
            result = PE2.LoadData()
            if result:
                result = PE2.Processing()
                if result:
                    result = PE2.SaveData()
                    if result:
                        HandlePre = open(PE2.OutputFolder+'/XXX.run','r')
                        Rows = HandlePre.readlines()
                        HandlePre.close()
                        # ImportLog
                        HandleRiassunto = open(PE2.OutputFolder+'/XXX.run','w')
                        HandleRiassunto.write('Analytical;SimType\n')
                        HandleRiassunto.write(Rows[2])
#                         HandleRiassunto.write(Rows[0])
#                         HandleRiassunto.write(Rows[1])
                        HandleRiassunto.write(Rows[3])
                        HandleRiassunto.write(Rows[4])
                        HandleRiassunto.write(Rows[5])
                        HandleRiassunto.write(Rows[6])
                        HandleRiassunto.write(','.join(PE2.Sensors)+';SensorsPE\n')
                        HandleRiassunto.write(','.join([str(item) for item in PE2.Heights])+';HeightsPE\n')
                        HandleRiassunto.write(str(PE2.dt)+';dtPE\n')
                        HandleRiassunto.write(str(PE2.BRE)+';BREPE\n')
                        HandleRiassunto.write(str(PE2.Gamma)+';GammaPE\n')
                        HandleRiassunto.write(str(PE2.From)+';FromPE\n')
                        HandleRiassunto.write(str(PE2.To)+';ToPE\n')
                        HandleRiassunto.write(','.join([str(item) for item in PE2.Ke])+';KePE\n')
#                         HandleRiassunto.write(str(PE2.Period)+';Period\n')
#                         HandleRiassunto.write(str(PE2.PeriodValue)+';PeriodValue\n')
#                         HandleRiassunto.write(str(PE2.Run)+';RunSP\n')
#                         # HandleRiassunto.write(FA.FFTWin+';FFTwin\n')
#                         # HandleRiassunto.write(str(FA.From)+';From\n')
#                         # HandleRiassunto.write(str(FA.To)+';To\n')
#                         # HandleRiassunto.write(str(FA.dt)+';dt\n')
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
        HandleLog = open('../temp/Flux.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open('../temp/Flux.log','w')
        HandleLog.write('Options error')
        HandleLog.close()