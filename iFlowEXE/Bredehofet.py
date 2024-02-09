################################# 
# Code to perform the modified Bredehofet - Papadopulos analysis (1965)
# 
# Parameters:
#   Sensors [LIST of STRING] -s
#   Heights [LIST of FLOAT] -h
#   SoilSens [STRING] -l
#   Threshold [FLOAT] -t
#   k [FLOAT] -k
#   WinLenght [INTEGER] -w
#   dt [FLOAT] -d
#   OutputFolder [STRING] -o
#   Version [BOOLEAN] --version
#   InputFolder [STRING] -i
#
# Input:
#   File of the temperature that must be located into the InputFolder.
#   The file must be a Pandas dataframe saved in pickle format with 'zip' compression and 
#   with a column named 'Time' containing the Unix timestamp of the records.
#
# Output:
#   File of the thermal velocity estimated located into the OutputFolder.
#   The output a Pandas dataframe saved in pickle format with 'zip' compression and 
#   with a column named 'Time' containing the Unix timestamp of the estimated velocitied.
############################### 
import sys
import getopt
import pandas as pd
import numpy as np
from scipy.optimize import least_squares

def fun(x,Temperature,HeightOr):
    Heights = HeightOr[0] - HeightOr
    #
    L = Heights[-1]
    #
    TL = Temperature[-1]
    T0 = Temperature[0]
    #
    Error = 0.0
    for i in range(1,len(Heights)-1):
        Error = Error + (np.exp(x[0]*Heights[i]/L)-1)/(np.exp(x[0])-1)-(Temperature[i]-T0)/(TL-T0)
    return Error

class Bredehofet:
    def __init__(self,opts, args):
        #
        self.Sensors = ['T0','T1','T2','T3','T4','T5','T6']#[]
        self.Heights = [0.0,-0.15,-0.3,-0.45,-0.6,-0.75,-0.9]#[]
        self.SoilSens = 'T0'#''
        self.Threshold = 0.0#np.nan
        self.k = 0.0000005#np.nan
        self.WinLenght = 30#np.nan
        self.dt = 900.0#np.nan
        self.OutputFolder = '../temp' # Output folder.
        self.Version = False # Flag display version and stop the execution.
        self.InputFolder = '../temp' # Input folder.
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
            elif opt in ('-l'):
                self.SoilSens = arg
            elif opt in ('-t'):
                self.Threshold = float(arg)
            elif opt in ('-k'):
                self.k = float(arg)
            elif opt in ('-w'):
                self.WinLenght = int(arg)
            elif opt in ('-d'):
                self.dt = float(arg)
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in ('-i'):
                self.InputFolder = arg
            elif opt in('--version'):
                self.Version = True
        #
        return
#%%
    def CheckOptions(self):
        print('CheckOptions...')
        try:
            #  
            FlagPreCheck = True
            # Check Options type
            if type(self.SoilSens) != str : FlagPreCheck = False
            if type(self.Threshold) != float : FlagPreCheck = False
            if type(self.k) != float : FlagPreCheck = False
            if type(self.WinLenght) != int : FlagPreCheck = False
            if type(self.dt) != float : FlagPreCheck = False
            if type(self.OutputFolder) != str : FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
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
            if self.Version:
                print('Version 0.1')
                return False
            return FlagPreCheck
        except:
            return False
#%%
    def LoadData(self):
        print('LoadData...')
        try:
            self.df_Data = pd.read_pickle(self.InputFolder+'/clean.pkz', compression = 'zip')
            # self.df_Data.to_csv(self.InputFolder+'/clean.csv')
            self.Columns = (self.df_Data.columns.tolist())[1:]
            #
            if self.Columns != self.Sensors:
                return False
            #
            return True
        except:
            return False
#%%
    def Processing(self):
        print('Processing...')
        try:
            self.Time = []
            self.Velocity = []
            Flag = []
            posSensor = self.Columns.index(self.SoilSens)
            #
            WorkHeights = np.array(self.Heights[posSensor:])
            #
            # Check Starting Time
            if (self.df_Data['Time'].loc[0]/86400.0)%1 != 0.0:
                StartTime = (((self.df_Data['Time'].loc[0]/86400.0)//1)+1)*86400.0
            else:
                StartTime = self.df_Data['Time'].loc[0]
            #
            dfWork = pd.DataFrame(columns=self.df_Data.columns)
            cont = 0
            while StartTime + self.WinLenght*24.0*3600.0 - self.dt <= self.df_Data['Time'].loc[self.df_Data.shape[0]-1]:
                dfTemp = self.df_Data.loc[(self.df_Data['Time'] >= StartTime) & (self.df_Data['Time'] < StartTime + self.WinLenght*24.0*3600.0)]
                Stats = dfTemp.describe()
                Data = Stats.loc['mean'].tolist()
                Data[0] = self.WinLenght*24.0*3600.0/2.0 + StartTime
                dfWork.loc[cont] = Data
                StartTime = StartTime + self.WinLenght*24.0*3600.0
                cont += 1
            #
            for t in range(0,dfWork.shape[0]):
                self.Time.append(dfWork.iloc[t].tolist()[0])
                TemperList = np.array(dfWork.iloc[t].tolist()[posSensor+1:])
                # Find min and max pos
                maxpos = np.argmax(TemperList)
                minpos = np.argmin(TemperList)
                #
                if (TemperList[maxpos]-TemperList[minpos]) < self.Threshold:
                    self.Velocity.append(np.nan)
                    Flag.append(TemperList[maxpos]-TemperList[minpos])
                else:
                    if (np.abs(maxpos-minpos)) < 2:
                        self.Velocity.append(np.nan)
                        Flag.append(TemperList[maxpos]-TemperList[minpos])
                    else:
                        if minpos < maxpos:
                            input = np.array([-2])
                            res = least_squares(fun, input, ftol=1e-8, method='lm', args=([TemperList[minpos:maxpos+1],WorkHeights[minpos:maxpos+1]]))
                            # self.Velocity.append(-self.k*res.x[0]/self.c0rho0/(WorkHeights[minpos]-WorkHeights[maxpos])/100)
                            self.Velocity.append(-self.k*res.x[0]/(WorkHeights[minpos]-WorkHeights[maxpos]))
                            Flag.append(TemperList[maxpos]-TemperList[minpos])
                        else:
                            input = np.array([2])
                            res = least_squares(fun, input, ftol=1e-8, method='lm', args=([TemperList[maxpos:minpos+1],WorkHeights[maxpos:minpos+1]]))
                            # self.Velocity.append(-self.k*res.x[0]/self.c0rho0/(WorkHeights[maxpos]-WorkHeights[minpos])/100)
                            self.Velocity.append(-self.k*res.x[0]/(WorkHeights[maxpos]-WorkHeights[minpos]))
                            Flag.append(TemperList[maxpos]-TemperList[minpos])
            #
            self.df_Velocity = pd.DataFrame()
            self.df_Velocity['Time'] = self.Time
            self.df_Velocity['Velocity'] = self.Velocity
            self.df_Velocity['Flag'] = Flag
            #
            return True
        except:
            return False
            
    def SaveData(self):
        print('SaveData...')
        try:
            #
            self.df_Velocity.to_pickle(self.OutputFolder+'/Velocity.pkz', compression='zip')
            self.df_Velocity.to_csv(self.OutputFolder+'/Velocity.csv')
            return True
        except:
            return False


if __name__ == '__main__':
    options = sys.argv[1:]
    '''
    Probe name  [STRING] -p
    Project name  [STRING] -j
    Sensors [LIST] -s
    Heights [LIST] -h
    Sensor in soil [STRING] -l
    Threshold [FLOAT] -t
    c0rho0 [FLOAT] -r
    k [FLOAT] -k
    window lenght [INTEGER] - w
    dt [FLOAT] -d
    '''
    #
    print('Start')
    try:
        opts, args = getopt.getopt(options,'s:h:l:t:k:w:d:o:i:',['version'])
        #
        StringError = 'No Error'
        BDH = Bredehofet(opts, args)
        result = BDH.CheckOptions()
        if result:
            result = BDH.LoadData()
            if result:
                result = BDH.Processing()
                if result:
                    result = BDH.SaveData()
                    if result:
                        # ImportLog
                        HandleRiassunto = open(BDH.OutputFolder+'/XXX.run','w')
                        HandleRiassunto.write(','.join(BDH.Sensors)+';Sensors\n')
                        HandleRiassunto.write(','.join([str(item) for item in BDH.Heights])+';Heights\n')
                        HandleRiassunto.write(BDH.SoilSens+';SoilSens\n')
                        HandleRiassunto.write(str(BDH.Threshold)+';Threshold\n')
                        # HandleRiassunto.write(str(BDH.c0rho0)+';c0rho0\n')
                        HandleRiassunto.write(str(BDH.k)+';k\n')
                        HandleRiassunto.write(str(BDH.WinLenght)+';WinLenght\n')
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
        HandleLog = open('../temp/BDH.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open('../temp/BDH.log','w')
        HandleLog.write('Options error')
        HandleLog.close()