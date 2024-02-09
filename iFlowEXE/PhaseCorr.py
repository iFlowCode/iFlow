################################# 
# 
# 
# 
# 
#
############################### 

# Import the libraries
import os,sys
import numpy as np
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import pandas as pd
import getopt
import pickle


class PhaseCorr:
    def __init__(self,opts, args):
        # Initialize parameters
        self.Project = 'Uwe'
        self.Probe = 'Probe'
        self.Opp = 'dw'
        self.Sensor = 'Sensor2'
        self.From = '0.0'#'1590710400.0'
        self.To = '7500000.0'#1591142400.0'
        self.Run = '9'
        self.FreqPos = '7'
        self.Threshold = '7'
        #
        for opt, arg in opts:
            if opt in ('-j'):
                self.Project = arg
            elif opt in ('-p'):
                self.Probe = arg
            elif opt in ('-o'):
                self.Opp = arg
            elif opt in ('-s'):
                self.Sensor = arg
            elif opt in ('-f'):
                self.From = arg
            elif opt in ('-t'):
                self.To = arg
            elif opt in ('-r'):
                self.Run = arg
            elif opt in ('-q'):
                self.FreqPos = arg
            elif opt in ('-h'):
                self.Threshold = arg

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
            if type(self.Project) != str : FlagPreCheck = False
            if type(self.Probe) != str : FlagPreCheck = False
            if type(self.Opp) != str : FlagPreCheck = False
            if type(self.From) != str : FlagPreCheck = False
            if type(self.To) != str : FlagPreCheck = False
            if type(self.Run) != str : FlagPreCheck = False
            if type(self.FreqPos) != str : FlagPreCheck = False
            if type(self.Threshold) != str : FlagPreCheck = False
            #
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
            # Load sensors list
            # HandleProbe = open('../projects/'+self.Project+'/'+self.Probe+'/probe.ini','r')
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # HandleProbe.readline()
            # self.Sensors = HandleProbe.readline().split(';')[0].split(',')
            # HandleProbe.close()
            # Load the Time
            self.MobTimeWin = pd.read_pickle('../projects/'+self.Project+'/'+self.Probe+'/SPdata/'+self.Run+'_MobWinTime.pkz',compression='zip')
            # Load Phase
            with open('../projects/'+self.Project+'/'+self.Probe+'/SPdata/'+self.Run+'_Phase.PdList','rb') as f:
                self.dfx = pickle.load(f)
            f.close()
            # Freqs = (self.dfx[0])
            # print(Freqs[self.Sensor].iloc[8])
            # print(Test,type(Test))
            # print(1.0/Test)
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
            # position = self.Sensors.index(self.Sensor) + 1
            # print(self.MobTimeWin.iloc[0].values)
            # print(self.MobTimeWin.iloc[-1].values)
            #
            self.List_dfPhase = []
            for t in range(0,len(self.dfx)):
                df = self.dfx[t]
                self.Sensors = df.columns.to_list()
                position = self.Sensors.index(self.Sensor)
                if (self.MobTimeWin.iloc[t].values >= float(self.From)) and (self.MobTimeWin.iloc[t].values <= float(self.To)):
                    #
                    Phase = df.iloc[int(self.FreqPos),[position]].values[0]
                    # print(t,Phase)
                    if self.Opp == 'up':
                        if Phase < float(self.Threshold):
                            Phase = Phase + 2 * np.pi
                    elif self.Opp == 'dw':
                        if Phase > float(self.Threshold):
                            Phase = Phase - 2 * np.pi
                    #
                    df.iloc[int(self.FreqPos),[position]] = Phase
                    # print(Phase)
                self.List_dfPhase.append(df)
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
            with open('../projects/'+self.Project+'/'+self.Probe+'/SPdata/'+self.Run+'_Phase.PdList','wb') as Handle:
                pickle.dump(self.List_dfPhase,Handle)
            return True
        except:
            return False


if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        opts, args = getopt.getopt(options,'j:p:o:s:f:t:r:q:')
        #
        StringError = 'No Error'
        PC = PhaseCorr(opts, args)
        result = PC.CheckOptions()
        if result:
            result = PC.LoadData()
            if result:
                result = PC.Processing()
                print(result)
                if result:
                    result = PC.SaveData()
                    if result:
                        pass
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