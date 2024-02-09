###############################################################################
#
# 
# 
# Options:
# Probe name [STRING] -p
# Project name [STRING] -j
# FileIn [STRING] -f
# TimeSerie [STRING] -s
# TimeType [STRING] -t
# SampleRate [FLOAT] -r
# Interpolate missing data  [BOOLEAN] -i
# Rebuild time serie [BOOLEAN] -e
# Sensors to import [LIST of string] -n
# Sensors heights [LIST of float] -h
# From [STRING] -a
# To [STRING] -b
# Update [BOOLEAN] -u
# FlagTimeSeries [BOOLEAN] -g
# FlagHeader [BOOLEAN] -l
# OutputFolder [STRING] -o
###############################################################################

# Import the libraries
import os,sys
import getopt
import pandas as pd
import numpy as np
import datetime 
#%%
class DataImport:
    '''
    Class DataImport:
    '''
    def __init__(self,opts, args):
        #
        self.FileName = 'D:/Lavoro/PhD/iFlow/temp2/Test0Update.csv'#'' # Data file path.
        self.TimeSerie = 'Time'#'' # Name of the TimeSerie column.
        self.TimeType = 'Time'#'' # Type of the TimeSerie column.
        self.dt = 900.0#np.nan # Sampling interval of the data [s].
        self.FlagIMD = False # Interpolate missing data? [True=Yes False=No] 
        self.FlagRTS = False # Rebuild TimeSerie? [True=Yes False=No] 
        self.Sensors = ['T0','T1','T2','T3','T4','T5','T6']#[] # Sensors to import.
        self.Heights = [0.0,-0.15,-0.3,-0.45,-0.6,-0.75,-0.9]#[] # Sensors' elevation.
        self.From = '2419200'#'' # Import from timestamp.
        self.To = '4838400'#'' # Import to timestamp.
        self.FlagUpdate = True#False # Flag update data. [True - update an existing probe]
        self.FlagHeader = True#True # True - The data file to import has columns name.
        self.FlagTimeSeries = True#True # True - The data file to import has a TimeSerie column.
        self.OutputFolder = '../temp' # Output folder.
        self.Version = False # Flag display version and stop the execution.
        #
        for opt, arg in opts:
            if opt in ('-f'):
                self.FileName = arg
            elif opt in ('-s'):
                self.TimeSerie = arg
            elif opt in ('-t'):
                self.TimeType = arg
            elif opt in ('-r'):
                self.dt = float(arg)
            elif opt in ('-i'):
                if arg == 'False':
                    self.FlagIMD = False
                else:
                    self.FlagIMD = True
            elif opt in ('-e'):
                if arg == 'False':
                    self.FlagRTS = False
                else:
                    self.FlagRTS = True
            elif opt in ('-n'):
                self.Sensors = arg.split(',')
            elif opt in ('-h'):
                self.Heights = [float(item) for item in arg.split(',')]
            elif opt in ('-a'):
                self.From = arg
            elif opt in ('-b'):
                self.To = arg
            elif opt in ('-u'):
                self.FlagUpdate = True
            elif opt in ('-g'):
                if arg == 'False':
                    self.FlagTimeSeries = False
                else:
                    self.FlagTimeSeries = True
            elif opt in ('-l'):
                if arg == 'False':
                    self.FlagHeader = False
                else:
                    self.FlagHeader = True
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in('--version'):
                self.Version = True
        #
        self.df_DataNew = pd.DataFrame()
        self.df_DataMiss = pd.DataFrame()

    def Interpolate(self,ind,PreInd,PostInd,PreValue,PostValue):
        '''Interpolate [summary]

        [extended_summary]

        Args:
            ind ([type]): [description]
            PreInd ([type]): [description]
            PostInd ([type]): [description]
            PreValue ([type]): [description]
            PostValue ([type]): [description]

        Returns:
            [type]: [description]
        '''
        return PreValue + (ind - PreInd) / (PostInd - PreInd) * (PostValue - PreValue)

    def CheckOptions(self):
        '''CheckOptions 
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('CheckOptions...')
        try:
            FlagPreCheck = True
            # Check Options type
            # if type(self.ProbeName) != str: FlagPreCheck = False
            # if type(self.ProjectName) != str: FlagPreCheck = False
            if type(self.FileName) != str: FlagPreCheck = False
            if type(self.TimeSerie) != str: FlagPreCheck = False
            if type(self.TimeType) != str: FlagPreCheck = False
            if type(self.dt) != float: FlagPreCheck = False
            if type(self.FlagIMD) != bool: FlagPreCheck = False
            if type(self.FlagRTS) != bool: FlagPreCheck = False
            if type(self.Sensors) != list: FlagPreCheck = False
            if type(self.Heights) != list: FlagPreCheck = False
            if type(self.From) != str: FlagPreCheck = False
            if type(self.To) != str: FlagPreCheck = False
            if type(self.FlagUpdate) != bool: FlagPreCheck = False
            if type(self.FlagTimeSeries) != bool: FlagPreCheck = False
            if type(self.OutputFolder) != str: FlagPreCheck = False
            # Check if old data 
            # File = './projects/'+self.ProjectName+'/'+self.ProbeName+'/Data/clean.pkz'
            # if os.path.isfile(File) is True and self.FlagUpdate is False:
            #     FlagPreCheck = False
            # Check Sensors items type
            for item in self.Sensors:
                if type(item) != str: FlagPreCheck = False
            # Check Height items type
            for item in self.Heights:
                if type(item) != float: FlagPreCheck = False
            #
            if self.Version:
                print('Version 0.1')
                return False
            return FlagPreCheck
        except:
            return False

    def LoadNewData(self):
        '''LoadNewData
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('LoadNewData...')
        try:
            if self.FlagTimeSeries:
                # File has a TimeSerie column
                if self.FlagHeader:
                    # File has column name
                    self.df_newData = pd.read_csv(self.FileName)
                else:
                    # File hasn't column name
                    self.df_newData = pd.read_csv(self.FileName, header = None)
                    # Automatic create the columns name
                    SensorsTemp = []
                    for i in range(0,self.df_newData.shape[1]):
                        SensorsTemp.append('Sensor'+str(i))
                    # Add the column names create to the dataframe
                    self.df_newData.columns = SensorsTemp
                # If the TimeSerie type is Datetime convert the TimeSerie to timestamp
                if self.TimeType == 'yyyy-mm-dd h24:min:sec':
                    self.df_newData[self.TimeSerie] = (pd.to_datetime(self.df_newData[self.TimeSerie]) - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')
            else:
                # File hasn't a TimeSerie column
                if self.FlagHeader:
                    # File has column name
                    self.df_newData = pd.read_csv(self.FileName)
                else:
                    # File hasn't column name
                    self.df_newData = pd.read_csv(self.FileName, header=None)
                    # Automatic create the columns name
                    SensorsTemp = []
                    for i in range(0,self.df_newData.shape[1]):
                        SensorsTemp.append('Sensor'+str(i))
                    # Add the column names create to the dataframe
                    self.df_newData.columns = SensorsTemp
            return True
        except:
            return False

    def CreateTimeSerie(self):
        '''CreateTimeSerie
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('CreateTimeSerie...')
        try:
            if self.FlagRTS:
                # Rebuild TimeSerie with a costant dt was chosen.
                # Set the number of timestep to the dimension of the datafile
                nTimeStep = self.df_newData.shape[0]
                # Set the starting time 
                self.From = int(self.From)
            else:
                if self.TimeType == 'yyyy-mm-dd h24:min:sec':
                    # TimeSerie type is Datetime
                    self.From = (pd.Timestamp(self.From) - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')
                    self.To = (pd.Timestamp(self.To) - pd.Timestamp('1970-01-01')) // pd.Timedelta('1s')
                elif self.TimeType == 'Time':
                    # TimeSerie type is Time
                    self.From = int(self.From)
                    self.To = int(self.To)
                # Calculate the number of timestep to import
                nTimeStep = int((self.To-self.From)/self.dt) + 1
            # Insert the column Time in the format of timestamp into the DataFrame
            self.df_DataNew['Time'] = [(t * self.dt + self.From) for t in range(0,nTimeStep)]
            self.df_DataMiss['Time'] = [(t * self.dt + self.From) for t in range(0,nTimeStep)]
            return True
        except:
            return False

    def FillDataNew(self):
        '''FillDataNew
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('FillDataNew...')
        try:
            if self.FlagRTS:
                # User choose to rebuild the time serie
                for Sensor in self.Sensors:
                    # Initialize Data Vector
                    DataArrayTemp = np.empty(self.df_DataNew.shape[0])
                    DataArrayTemp[:] = np.nan
                    MissArrayTemp = np.empty(self.df_DataNew.shape[0])
                    MissArrayTemp[:] = np.nan
                    # First run fill
                    for t in range(0,DataArrayTemp.shape[0]):
                        # DataArrayTemp[t] = self.df_newData[Sensor].iloc[t]
                        if pd.isnull(self.df_newData[Sensor].iloc[t]):
                            MissArrayTemp[t] = -9999
                        else:
                            DataArrayTemp[t] = self.df_newData[Sensor].iloc[t]
                    # Fill missing data
                    if self.FlagIMD:
                        NanPos = np.argwhere(np.isnan(DataArrayTemp))
                        # If there are any NaN
                        if NanPos.shape[0] > 0:
                            # For every NaN position
                            for ind in NanPos:
                                BackIndex = ind[0]
                                ForwardIndex = ind[0]
                                try:
                                    # Find backward
                                    while pd.isnull(self.df_newData[Sensor].iloc[BackIndex]):
                                        BackIndex -= 1
                                    BackValue = self.df_newData[Sensor].iloc[BackIndex]
                                    if BackIndex < 0:
                                        MissArrayTemp[ind[0]] = -9999
                                    else:
                                        # Find forward
                                        while pd.isnull(self.df_newData[Sensor].iloc[ForwardIndex]):
                                            ForwardIndex += 1
                                        ForwardValue = self.df_newData[Sensor].iloc[ForwardIndex]
                                        # Interpolate
                                        InterpolateValue = self.Interpolate(ind[0],BackIndex,ForwardIndex,BackValue,ForwardValue)
                                        DataArrayTemp[ind[0]] = InterpolateValue
                                        MissArrayTemp[ind[0]] = InterpolateValue
                                except:
                                    MissArrayTemp[ind[0]] = -9999
                    #
                    self.df_DataNew[Sensor] = DataArrayTemp
                    self.df_DataMiss[Sensor] = MissArrayTemp
            else:
                # For every sensor to import
                for Sensor in self.Sensors:
                    # Initialize Data Vector
                    DataArrayTemp = np.empty(self.df_DataNew.shape[0])
                    DataArrayTemp[:] = np.nan
                    MissArrayTemp = np.empty(self.df_DataNew.shape[0])
                    MissArrayTemp[:] = np.nan
                    # First run fill only the coincident datetime
                    for i,time in enumerate(self.df_DataNew['Time']):
                        try:
                            t = self.df_newData[self.TimeSerie].loc[self.df_newData[self.TimeSerie] == time].index[0]
                            if pd.isnull(self.df_newData[Sensor].iloc[t]):
                                MissArrayTemp[i] = -9999
                            else:
                                DataArrayTemp[i] = self.df_newData[Sensor].iloc[t]
                        except:
                            MissArrayTemp[i] = -9999
                    # Fill missing data
                    if self.FlagIMD:
                        # Find NaN positions
                        NanPos = np.argwhere(np.isnan(DataArrayTemp))
                        # If there are any NaN
                        if NanPos.shape[0] > 0:
                            # For every NaN position
                            for ind in NanPos:
                                try:
                                    # Find backward
                                    BackIndex = self.df_newData[self.TimeSerie][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] < int(self.df_DataNew['Time'].iloc[ind]))].iloc[-1]
                                    BackValue = self.df_newData[Sensor][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] < int(self.df_DataNew['Time'].iloc[ind]))].iloc[-1]
                                    # Find forward
                                    ForwardIndex = self.df_newData[self.TimeSerie][ (pd.notnull(self.df_newData[Sensor]))  & (self.df_newData[self.TimeSerie] > int(self.df_DataNew['Time'].iloc[ind]))].iloc[0]
                                    ForwardValue = self.df_newData[Sensor][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] > int(self.df_DataNew['Time'].iloc[ind]))].iloc[0]
                                    # Interpolate
                                    InterpolateValue = self.Interpolate(self.df_DataNew['Time'].iloc[ind[0]],BackIndex,ForwardIndex,BackValue,ForwardValue)
                                    DataArrayTemp[ind[0]] = InterpolateValue
                                    MissArrayTemp[ind[0]] = InterpolateValue
                                except:
                                    MissArrayTemp[ind[0]] = -9999
                    #
                    self.df_DataNew[Sensor] = DataArrayTemp
                    self.df_DataMiss[Sensor] = MissArrayTemp
            return True
        except:
            return False

    def MergeData(self):
        '''MergeData
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('MergeData...')
        try:
            if self.FlagUpdate:
                self.df_DataOld = pd.read_pickle('../temp/clean_old.pkz', compression='zip')
                self.df_MissOld = pd.read_pickle('../temp/miss_old.pkz', compression='zip')
                print(self.df_DataOld.columns)
                print(self.df_DataOld['Time'].iloc[0],self.df_DataOld['Time'].iloc[self.df_DataOld.shape[0]-1])
                print(self.df_DataNew.columns)
                print(self.df_DataNew['Time'].iloc[0],self.df_DataNew['Time'].iloc[self.df_DataNew.shape[0]-1])
                print(self.df_DataNew['Time'].iloc[0]-self.df_DataOld['Time'].iloc[self.df_DataOld.shape[0]-1])
                nStepInter = int((self.df_DataNew['Time'].iloc[0]-self.df_DataOld['Time'].iloc[self.df_DataOld.shape[0]-1])/self.dt - 1)
                print(nStepInter)
                # nTimeStep = int((self.df_DataNew['Time'].loc[self.df_DataNew.shape[0]-1] - self.df_DataOld['Time'].iloc[0])/self.dt) + 1
                self.df_Merge = pd.DataFrame()
                #
                TimeTemp = self.df_DataOld['Time'].tolist()
                print(len(TimeTemp))
                for t in range (0,nStepInter):
                    TimeTemp.append(self.df_DataOld['Time'].iloc[self.df_DataOld.shape[0]-1]+self.dt*t)
                print(len(TimeTemp))
                TimeTemp.append(self.df_DataNew['Time'].tolist())
                print(len(TimeTemp))

                # self.df_Merge['Time'] = [(t * self.dt + self.df_DataOld['Time'].iloc[0]) for t in range(0,nTimeStep)]
                # self.df_MergeTemp = self.df_Merge
                # #
                # self.df_Merge = pd.merge_ordered(self.df_Merge, self.df_DataOld, on='Time' )
                # self.df_MergeTemp = pd.merge_ordered(self.df_MergeTemp, self.df_DataNew, on='Time' )
                # for Sensor in self.df_Merge.columns:
                #     List = self.df_Merge[self.df_Merge[Sensor].isnull()].index.tolist()
                #     for pos in List:
                #         self.df_Merge[Sensor].iloc[pos] = self.df_MergeTemp[Sensor].iloc[pos]
                # # MissingData
                # self.df_MissOld = pd.read_pickle('../projects/'+self.ProjectName+'/'+self.ProbeName+'/data/miss.pkz', compression='zip')
                # nTimeStep = int((self.df_DataMiss['Time'].loc[self.df_DataMiss.shape[0]-1] - self.df_MissOld['Time'].iloc[0])/self.dt) + 1
                # self.df_MergeMiss = pd.DataFrame()
                # self.df_MergeMiss['Time'] = [(t * self.dt + self.df_MissOld['Time'].iloc[0]) for t in range(0,nTimeStep)]
                # self.df_MergeMissTemp = self.df_MergeMiss
                # #
                # self.df_MergeMiss = pd.merge_ordered(self.df_MergeMiss, self.df_MissOld, on='Time' )
                # self.df_MergeMissTemp = pd.merge_ordered(self.df_MergeMissTemp, self.df_DataMiss, on='Time' )
                # for Sensor in self.df_Merge.columns:
                #     List = self.df_MergeMiss[self.df_MergeMiss[Sensor].isnull()].index.tolist()
                #     for pos in List:
                #         self.df_MergeMiss[Sensor].iloc[pos] = self.df_MergeMissTemp[Sensor].iloc[pos]
            return True
        except:
            return False
#%%
    def SaveData(self):
        '''SaveData
        [extended_summary]
        Returns:
            [BOOLEAN]: [description]
        '''
        print('SaveData...')
        try:
            if self.FlagUpdate:
                pass
                # self.df_DataOld.to_pickle(self.OutputFolder+'/clean_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+'.pkz', compression='zip')
                # self.df_Merge.to_pickle(self.OutputFolder+'/clean.pkz', compression='zip')
                # self.df_DataMiss.to_pickle(self.OutputFolder+'/miss.pkz', compression='zip')
            else:
                self.df_DataNew.to_pickle(self.OutputFolder+'/clean.pkz', compression='zip')
                self.df_DataMiss.to_pickle(self.OutputFolder+'/miss.pkz', compression='zip')
            return True
        except:
            return False

if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        # Get command line options
        opts, args = getopt.getopt(options,'p:j:f:s:t:r:i:e:n:h:a:b:u:g:l:o:',['version'])
        # Initialize Error String
        StringError = 'No Error'
        # Initialize DataImport class
        DI = DataImport(opts, args)
        # Check the command line options
        result = DI.CheckOptions()
        if result:
            # Load the new data
            result = DI.LoadNewData()
            if result:
                # Create the storing time serie
                result = DI.CreateTimeSerie()
                if result:
                    # Check the data imported
                    result = DI.FillDataNew()
                    if result:
                        # Update the data stored
                        result = DI.MergeData()
                        if result:
                            # Save the data
                            result = DI.SaveData()
                            if result:
                                # ImportLog
                                HandleRiassunto = open(DI.OutputFolder+'/probe.ini','w')
                                HandleRiassunto.write(DI.FileName+';LastDatafile\n')
                                HandleRiassunto.write(DI.TimeSerie+';TimeSerieName\n')
                                HandleRiassunto.write(DI.TimeType+';TimeType\n')
                                HandleRiassunto.write(str(DI.dt)+';SampleRate\n')
                                HandleRiassunto.write(str(DI.FlagIMD)+';IMD\n')
                                HandleRiassunto.write(str(DI.FlagRTS)+';RTS\n')
                                HandleRiassunto.write(','.join(DI.Sensors)+';SensorsName\n')
                                HandleRiassunto.write(','.join([str(item) for item in DI.Heights])+';SensorsHeight\n')
                                HandleRiassunto.write(str(DI.From)+';From\n')
                                HandleRiassunto.write(str(DI.To)+';To\n')
                                HandleRiassunto.write(str(DI.FlagUpdate)+';FlagUpdate\n')
                                HandleRiassunto.write(str(DI.FlagTimeSeries)+';FlagTimeSerie\n')
                                HandleRiassunto.write(str(DI.FlagHeader)+';FlagHeader\n')
                                HandleRiassunto.close()
                            else:
                                StringError = 'SaveData Error'
                        else:
                            StringError = 'MergeData Error'
                    else:
                        StringError = 'FillDataNew Error'
                else:
                    StringError = 'CreateTimeSerie Error'
            else:
                StringError = 'LoadNewData Error'
        else:
            StringError = 'CheckOptions Error'
        #
        # print((DataImport.OutputFolder)
        HandleLog = open(DI.OutputFolder+'/DataImport.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open(DI.OutputFolder+'/DataImport.log','w')
        HandleLog.write('Options error')
        HandleLog.close()