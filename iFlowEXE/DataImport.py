"""
"""

# Import the libraries
import sys
import getopt
import pandas as pd
import numpy as np
from loguru import logger

class DataImport:
    """
    """
    def __init__(self,opts, args):
        """
        The function initializes various parameters and settings based on the input
        arguments provided.
        
        :param opts: The `opts` parameter is a list of tuples where each tuple
        contains an option and its corresponding argument. The code snippet you
        provided is an `__init__` method of a class where these options and
        arguments are used to initialize various attributes of the class instance
        :param args: The `args` parameter in the `__init__` method is used to pass
        command-line arguments to the script or program. These arguments are
        typically provided by the user when running the script from the command
        line. In this context, `args` would contain the command-line arguments
        passed to the script
        """
        #
        self.FileName = "" # Data file path.
        self.TimeSerie = "" # Name of the TimeSerie column.
        self.TimeType = "Time" # Type of the TimeSerie column.
        self.dt = np.nan # Sampling interval of the data [s].
        self.FlagIMD = False # Interpolate missing data? [True=Yes False=No] 
        self.FlagRTS = False # Rebuild TimeSerie? [True=Yes False=No] 
        self.Sensors = [] # Sensors to import.
        self.Heights = [] # Sensors' elevation.
        self.From = "" # Import from timestamp.
        self.To = "" # Import to timestamp.
        self.FlagUpdate = False # Flag update data. [True - update an existing probe]
        self.FlagHeader = True # True - The data file to import has columns name.
        self.FlagTimeSeries = True # True - The data file to import has a TimeSerie column.
        self.OutputFolder = "../temp" # Output folder.
        self.Version = False # Flag display version and stop the execution.
        #
        for opt, arg in opts:
            if opt in ("-f"):
                self.FileName = arg
            elif opt in ("-s"):
                self.TimeSerie = arg
            elif opt in ("-t"):
                self.TimeType = arg
            elif opt in ("-r"):
                self.dt = float(arg)
            elif opt in ("-i"):
                if arg == "False":
                    self.FlagIMD = False
                else:
                    self.FlagIMD = True
            elif opt in ("-e"):
                if arg == "False":
                    self.FlagRTS = False
                else:
                    self.FlagRTS = True
            elif opt in ("-n"):
                self.Sensors = arg.split(",")
            elif opt in ("-h"):
                self.Heights = [float(item) for item in arg.split(",")]
            elif opt in ("-a"):
                self.From = arg
            elif opt in ("-b"):
                self.To = arg
            elif opt in ("-u"):
                self.FlagUpdate = True
            elif opt in ("-g"):
                if arg == "False":
                    self.FlagTimeSeries = False
                else:
                    self.FlagTimeSeries = True
            elif opt in ("-l"):
                if arg == "False":
                    self.FlagHeader = False
                else:
                    self.FlagHeader = True
            elif opt in ("-o"):
                self.OutputFolder = arg
            elif opt in("--version"):
                self.Version = True
        #
        self.df_DataNew = pd.DataFrame()
        self.df_DataMiss = pd.DataFrame()

    def Interpolate(self,ind,PreInd,PostInd,PreValue,PostValue):
        """
        """
        # The code snippet is calculating a linear interpolation between two
        # points based on the given input values. It takes the previous value
        # (`PreValue`), the current index (`ind`), the previous index (`PreInd`),
        # the next index (`PostInd`), the next value (`PostValue`), and uses them
        # to interpolate a value between `PreValue` and `PostValue` based on the
        # position of `ind` between `PreInd` and `PostInd`.
        return PreValue + (ind - PreInd) / (PostInd - PreInd) * (PostValue - PreValue)

    def CheckOptions(self):
        """
        """
        # This Python code snippet is performing a series of type checks on
        # various attributes of an object. It checks if the types of the
        # attributes match the expected types and sets a flag (`FlagPreCheck`)
        # accordingly. If any type check fails, the flag is set to `False`.
        try:
            FlagPreCheck = True
            # Check Options type
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
        # This code snippet is defining a method `SaveData` within the
        # `FrequencyAnalysis` class.
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
                print("Version 0.1")
                return False
            return FlagPreCheck
        except:
            return False

    def LoadNewData(self):
        """
        """
        # This Python code is a method that reads a CSV file into a pandas
        # DataFrame. Here is a breakdown of what the code is doing:
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
                        SensorsTemp.append("Sensor"+str(i))
                    # Add the column names create to the dataframe
                    self.df_newData.columns = SensorsTemp
                # If the TimeSerie type is Datetime convert the TimeSerie to timestamp
                if self.TimeType == "yyyy-mm-dd h24:min:sec":
                    self.df_newData[self.TimeSerie] = (pd.to_datetime(self.df_newData[self.TimeSerie]) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
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
                        SensorsTemp.append("Sensor"+str(i))
                    # Add the column names create to the dataframe
                    self.df_newData.columns = SensorsTemp
            return True
        except:
            return False

    def CreateTimeSerie(self):
        """
        """
        # The above code is a Python script that seems to be handling time series
        # data. Here is a breakdown of what the code is doing:
        try:
            if self.FlagRTS:
                # Rebuild TimeSerie with a costant dt was chosen.
                # Set the number of timestep to the dimension of the datafile
                nTimeStep = self.df_newData.shape[0]
                # Set the starting time 
                self.From = int(self.From)
            else:
                if self.TimeType == "yyyy-mm-dd h24:min:sec":
                    # TimeSerie type is Datetime
                    self.From = (pd.Timestamp(self.From) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
                    self.To = (pd.Timestamp(self.To) - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
                elif self.TimeType == "Time":
                    # TimeSerie type is Time
                    self.From = int(self.From)
                    self.To = int(self.To)
                # Calculate the number of timestep to import
                nTimeStep = int((self.To-self.From)/self.dt) + 1
            # Insert the column Time in the format of timestamp into the DataFrame
            self.df_DataNew["Time"] = [(t * self.dt + self.From) for t in range(0,nTimeStep)]
            self.df_DataMiss["Time"] = [(t * self.dt + self.From) for t in range(0,nTimeStep)]
            return True
        except:
            return False

    def FillDataNew(self):
        """
        """
        # This Python code snippet is a part of a larger program that appears to
        # be handling time series data processing. Here is a breakdown of what the
        # code is doing:
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
                    for i,time in enumerate(self.df_DataNew["Time"]):
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
                                    BackIndex = self.df_newData[self.TimeSerie][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] < int(self.df_DataNew["Time"].iloc[ind]))].iloc[-1]
                                    BackValue = self.df_newData[Sensor][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] < int(self.df_DataNew["Time"].iloc[ind]))].iloc[-1]
                                    # Find forward
                                    ForwardIndex = self.df_newData[self.TimeSerie][ (pd.notnull(self.df_newData[Sensor]))  & (self.df_newData[self.TimeSerie] > int(self.df_DataNew["Time"].iloc[ind]))].iloc[0]
                                    ForwardValue = self.df_newData[Sensor][(pd.notnull(self.df_newData[Sensor])) & (self.df_newData[self.TimeSerie] > int(self.df_DataNew["Time"].iloc[ind]))].iloc[0]
                                    # Interpolate
                                    InterpolateValue = self.Interpolate(self.df_DataNew["Time"].iloc[ind[0]],BackIndex,ForwardIndex,BackValue,ForwardValue)
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
        """
        """
        # The code snippet is attempting to execute a block of code within a
        # try-except block. If the `FlagUpdate` attribute of the `self` object is
        # true, it is supposed to perform some action (commented as "Rebuild" in
        # the code). Regardless of whether the action is performed or not, the
        # function will return `True`. If an exception occurs during the execution
        # of the code block, the function will return `False`.
        try:
            if self.FlagUpdate:
                #! Rebuild
                pass
            return True
        except:
            return False

    def SaveData(self):
        """
        """
        # The code snippet is a Python try-except block. It first checks if the
        # `FlagUpdate` attribute is True. If it is True, it performs some action
        # (which is not specified in the code snippet). If `FlagUpdate` is False,
        # it saves two DataFrames (`df_DataNew` and `df_DataMiss`) to pickle files
        # with zip compression in the specified output folder. Finally, the
        # function returns True if successful and False if an exception occurs
        # during the process.
        try:
            if self.FlagUpdate:
                #! Rebuild
                pass
            else:
                self.df_DataNew.to_pickle(self.OutputFolder+"/clean.pkz", compression="zip")
                self.df_DataMiss.to_pickle(self.OutputFolder+"/miss.pkz", compression="zip")
            return True
        except:
            return False

if __name__ == "__main__":
    options = sys.argv[1:]
    logger.remove()
    logger.add(f"../logs/DataImport.log", rotation="7 days")
    logger.level("DEBUG")
    logger.info(f"Dataimport started...")
    #
    try:
        # Get command line options
        opts, args = getopt.getopt(options,"p:j:f:s:t:r:i:e:n:h:a:b:u:g:l:o:",["version"])
        # Initialize Error String
        StringError = "No Error"
        # Initialize DataImport class
        DI = DataImport(opts, args)
        # Check the command line options
        logger.info(f"\tCheckOption...")
        result = DI.CheckOptions()
        if result:
            logger.info(f"\tCheckOption ended...")
            # Load the new data
            logger.info(f"\tLoadData...")
            result = DI.LoadNewData()
            if result:
                logger.info(f"\tLoadData ended...")
                # Create the storing time serie
                logger.info(f"\tCreateTimeSeries...")
                result = DI.CreateTimeSerie()
                if result:
                    logger.info(f"\tCreateTimeSeries ended...")
                    # Check the data imported
                    logger.info(f"\tFillData...")
                    result = DI.FillDataNew()
                    if result:
                        logger.info(f"\tCFillDataEnded...")
                        # Update the data stored
                        logger.info(f"\tMergeData...")
                        result = DI.MergeData()
                        if result:
                            logger.info(f"\tMergeData ended...")
                            # Save the data
                            logger.info(f"\tSaveData...")
                            result = DI.SaveData()
                            if result:
                                logger.info(f"\tSaveData ended...")
                                # ImportLog
                                HandleRiassunto = open(DI.OutputFolder+"/probe.ini","w")
                                HandleRiassunto.write(DI.FileName+";LastDatafile\n")
                                HandleRiassunto.write(DI.TimeSerie+";TimeSerieName\n")
                                HandleRiassunto.write(DI.TimeType+";TimeType\n")
                                HandleRiassunto.write(str(DI.dt)+";SampleRate\n")
                                HandleRiassunto.write(str(DI.FlagIMD)+";IMD\n")
                                HandleRiassunto.write(str(DI.FlagRTS)+";RTS\n")
                                HandleRiassunto.write(",".join(DI.Sensors)+";SensorsName\n")
                                HandleRiassunto.write(",".join([str(item) for item in DI.Heights])+";SensorsHeight\n")
                                HandleRiassunto.write(str(DI.From)+";From\n")
                                HandleRiassunto.write(str(DI.To)+";To\n")
                                HandleRiassunto.write(str(DI.FlagUpdate)+";FlagUpdate\n")
                                HandleRiassunto.write(str(DI.FlagTimeSeries)+";FlagTimeSerie\n")
                                HandleRiassunto.write(str(DI.FlagHeader)+";FlagHeader\n")
                                HandleRiassunto.close()
                            else:
                                StringError = "SaveData Error"
                                logger.error("SaveData")
                        else:
                            StringError = "MergeData Error"
                            logger.error("MergeData")
                    else:
                        StringError = "FillDataNew Error"
                        logger.error("FillData")
                else:
                    StringError = "CreateTimeSerie Error"
                    logger.error("CreateTimeSerie")
            else:
                StringError = "LoadNewData Error"
                logger.error("LoadData")
        else:
            StringError = "CheckOptions Error"
            logger.error("CheckOption")
        #
        HandleLog = open(DI.OutputFolder+"/DataImport.log","w")
        HandleLog.write(StringError)
        HandleLog.close()
        logger.info(f"DataImport finished")
    except getopt.GetoptError:
        HandleLog = open(DI.OutputFolder+"/DataImport.log","w")
        HandleLog.write("Options error")
        HandleLog.close()
        logger.error("Getopt")