"""
"""

# Import the libraries
import sys,os
import getopt
import pandas as pd
import numpy as np
import scipy.stats
from scipy import signal
from loguru import logger

class SignalProcessingFFT:
    def __init__(self,opts, args):
        #
        # The above code is defining a class with several attributes and a
        # constructor. The attributes include MobWinLen, FFTWin, dt, MobWin,
        # Detrending, FlagUpdate, RunUpdate, SavePer, Version, OutputFolder, and
        # InputFolder. The constructor takes in command line arguments and assigns
        # them to the corresponding attributes.
        self.MobWinLen = 192.0 # window lenght in hours
        self.FFTWin = "Rectangular" # FFT window
        self.dt = 900.0 # Sample rate in seconds
        self.MobWin = True # Mobile window? True=Yes False=No
        self.Detrending = True # Detrending? True=Yes False=No
        self.FlagUpdate = False # Update? True=Yes False=No
        self.RunUpdate = "-9"# Run to Update
        self.SavePer = [24.0]
        self.Version = False # Flag display version and stop the execution.
        self.OutputFolder = "../temp" # Output folder.
        self.InputFolder = "../temp" # Input folder.
        #
        for opt, arg in opts:
            if opt in ("-f"):
                if arg == "False":
                    self.MobWin = False
                else:
                    self.MobWin = True
            elif opt in ("-s"):
                self.MobWinLen = float(arg)
            elif opt in ("-t"):
                self.FFTWin = arg
            elif opt in ("-d"):
                self.dt = float(arg)
            elif opt in ("-r"):
                if arg == "False":
                    self.Detrending = False
                else:
                    self.Detrending = True
            elif opt in ("-u"):
                if arg == "False":
                    self.FlagUpdate = False
                else:
                    self.FlagUpdate = True
            elif opt in ("-m"):
                self.RunUpdate = arg
            elif opt in ("-a"):
                self.SavePer = []
                for item in arg.split(","):
                    self.SavePer.append(float(item))
            elif opt in("--version"):
                self.Version = True
            elif opt in ("-o"):
                self.OutputFolder = arg
            elif opt in ("-i"):
                self.InputFolder = arg
        return

    def CheckOptions(self):
        """
        """
        # The above code is a function that performs pre-checks on the types of
        # variables used in a class. It checks if the types of variables are
        # correct and returns a boolean value indicating whether the pre-checks
        # passed or not. If any of the variable types are incorrect, the function
        # returns False.
        try:  
            FlagPreCheck = True
            # Check Options type
            if type(self.MobWinLen) != float : FlagPreCheck = False
            if type(self.FFTWin) != str : FlagPreCheck = False
            if type(self.MobWin) != bool : FlagPreCheck = False
            if type(self.dt) != float : FlagPreCheck = False
            if type(self.Detrending) != bool : FlagPreCheck = False
            if type(self.FlagUpdate) != bool : FlagPreCheck = False
            if type(self.RunUpdate) != str : FlagPreCheck = False
            if type(self.OutputFolder) != str : FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
            #
            for item in self.SavePer:
                if type(item) != float : 
                    FlagPreCheck = False
                    break
            #
            if self.Version:
                print("Version 0.1")
                return False
            return FlagPreCheck
        except:
            return False

    def LoadData(self):
        """
        """
        # The above code is a try-except block in Python. It is reading data from
        # a file using the pandas library. It reads the data from a pickle file
        # with compression. It then assigns the column names of the data to the
        # variable `ProcSensors`. It also assigns the first and last time values
        # from the 'Time' column to the variables `StartTime` and `EndTime`
        # respectively.
        try:
            # Read data
            self.df_Sensors = pd.read_pickle(self.InputFolder+"/clean.pkz", compression = "zip")
            self.ProcSensors = (self.df_Sensors.columns.tolist())[1:]
            # Find Starttime and End Tmie
            self.StartTime = self.df_Sensors["Time"].iloc[0]
            self.EndTime = self.df_Sensors["Time"].iloc[self.df_Sensors.shape[0]-1]
            #
            if self.FlagUpdate:
                pass
            else:
                self.MobWinTimeOld = []
            #!
            #!
            return True
        except:
            return False

    def WindowsTime(self):
        """
        """
        # The above code is calculating the number of time steps in the data and
        # calculating the times for the mobile window. It checks if the mobile
        # window is enabled and if so, it calculates the number of time steps in
        # the mobile window and creates a list of times for the mobile window. If
        # the mobile window is not enabled, it sets the number of time steps in
        # the mobile window to be equal to the number of time steps in the data
        # and creates a list with the midpoint time. The code returns True if the
        # calculations are successful and False if there is an error.
        try:
            # nStep in Data
            self.nStepData = self.df_Sensors.shape[0]
            # Calculate the Times
            self.MobWinTime = []
            if self.MobWin:
                self.nStepMWin = (self.MobWinLen * 60.0 * 60.0 / self.dt)
                #
                StartTemp = self.StartTime
                EndTemp = StartTemp + self.dt * (self.nStepMWin)
                while EndTemp < self.EndTime:
                    self.MobWinTime.append((EndTemp - StartTemp) / 2 + StartTemp)
                    StartTemp = StartTemp + self.dt
                    EndTemp = EndTemp + self.dt
                self.MobWinTime.append((EndTemp - StartTemp) / 2 + StartTemp)
            else:
                self.nStepMWin = self.nStepData 
                #
                self.MobWinTime.append((self.EndTime - self.StartTime) / 2)
            return True
        except:
            return False

    def Processing(self):
        """
        """
        # The above code is performing Fast Fourier Transform (FFT) analysis on a
        # time series data. It calculates the amplitude and phase of the frequency
        # components in the data. The code applies different FFT windows
        # (Rectangular, Bartlett, Hamming, Hanning, Triangular, FlatTop) to the
        # data and selects specific frequencies to analyze based on user-defined
        # parameters. It then detrends the data if specified, applies the FFT
        # window, and calculates the FFT. The amplitude and phase values are
        # stored in separate dataframes for each sensor. The code handles cases
        # where there are missing values in the data and returns
        try:
            # Create FFT wnidow
            if(self.FFTWin == "Rectangular"):
                self.Weight = np.asarray([1 for i in range(0,int(self.nStepMWin))])
            elif(self.FFTWin == "Bartlett"):
                self.Weight = np.bartlett(int(self.nStepMWin))
            elif(self.FFTWin == "Hamming"):
                self.Weight = np.hamming(int(self.nStepMWin))
            elif(self.FFTWin == "Hanning"):
                self.Weight = np.hanning(int(self.nStepMWin))
            elif(self.FFTWin == "Triangular"):
                self.Weight = np.asarray([(1 - np.abs(i - 0.5 * (int(self.nStepMWin) - 1)) / (0.5 * (int(self.nStepMWin) + 1))) for i in range(0,int(self.nStepMWin))])
            elif(self.FFTWin == "FlatTop"):
                self.Weight = signal.flattop(int(self.nStepMWin))
            # FFT Frequencies
            Freqs = np.fft.fftfreq(int(self.nStepMWin), self.dt)
            #
            FreqPoss = []
            for FP in self.SavePer:
                FreqPoss.append(np.argmin((Freqs-1/FP/3600.0)**2))
            #
            LimitFreq = -9999 #!#!
            for i,Freq in enumerate(Freqs):
                if Freq <= 1/self.dt and Freq >= 0.0:
                    LimitFreq = i
                else:
                    break
            #
            if LimitFreq != -9999:
                # Initialize Pandas dataframes
                Columns = ["Time","Freq"] + (self.df_Sensors.columns.tolist())[1:]
                self.AmplitudeDB = pd.DataFrame(columns=Columns)
                self.PhaseDB = pd.DataFrame(columns=Columns)
                # For every time
                for t in range (0,len(self.MobWinTime)):
                    if self.MobWinTime[t] in self.MobWinTimeOld:
                        pass
                    else:
                        # Moving window time
                        MVT = t * self.dt
                        # Windows times and nstep
                        StartTemp = self.StartTime + t * self.dt
                        if self.MobWin:
                            EndTemp = StartTemp + self.MobWinLen * 60.0 * 60.0 - self.dt
                            nt = self.MobWinLen * 60 * 60 /self.dt +1
                        else:
                            EndTemp = self.EndTime
                            nt = self.df_Sensors.shape[0]
                        # Extract data window
                        df_temp = self.df_Sensors[(self.df_Sensors["Time"] >= StartTemp) & (self.df_Sensors["Time"] <= EndTemp)]
                        # Store the data time column
                        df_x = df_temp["Time"]
                        # Drop the time column from the work dataframe
                        df_temp = df_temp.drop(["Time"],axis=1)
                        # Initialize Amplitude and Phase dataframe
                        df_Amplitude = pd.DataFrame()
                        df_Phase = pd.DataFrame()
                        # Insert Time into Amplitude and Phase dataframe
                        df_Amplitude["Time"] = [self.MobWinTime[t] for i in range(0,len(FreqPoss))]
                        df_Phase["Time"] = [self.MobWinTime[t] for i in range(0,len(FreqPoss))]
                        # Insert Frequencies into Amplitude and Phase dataframe
                        FreqsOK = []
                        for item in FreqPoss:
                            FreqsOK.append(Freqs[item])
                        df_Amplitude["Freq"] = FreqsOK
                        df_Phase["Freq"] = FreqsOK
                        # For every sensors
                        for Sensor in df_temp.columns:
                            # Check if there is nan into the column
                            if df_temp[Sensor].isnull().values.any():
                                NanList = [np.nan for i in range(0,len(FreqPoss))]
                                df_Amplitude[Sensor] = NanList
                                df_Phase[Sensor] = NanList
                            else:
                                # Detrending if activated
                                if self.Detrending:
                                    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(df_x,df_temp[Sensor])
                                    Detrend = slope * df_x + intercept
                                    df_temp[Sensor] = df_temp[Sensor] - Detrend
                                # Apply FFT window
                                df_temp[Sensor] = df_temp[Sensor].to_numpy() * self.Weight
                                # FFT
                                fft_hat = np.fft.fft(df_temp[Sensor])
                                # Calculate amplitude and phase
                                amplitude = np.zeros(fft_hat.shape)
                                phase = np.zeros(fft_hat.shape)
                                #
                                for i in range(0,LimitFreq):
                                    amplitude[i] = np.abs(fft_hat[i]) / (int(nt) / 2)
                                    phase[i] = np.arctan2(-np.imag(fft_hat[i]),np.real(fft_hat[i]))
                                    # Period in sec
                                    if Freqs[i] == 0.0:
                                        Period = np.inf
                                    else:
                                        Period = 1.0 / Freqs[i]
                                    PhaseCorr = (np.modf(MVT / Period)[0]) * 2 * np.pi
                                    phase[i] = phase[i] + PhaseCorr
                                    #
                                    if phase[i] > np.pi:
                                        phase[i] = phase[i] - 2 * np.pi
                                    elif phase[i] < -np.pi:
                                        phase[i] = phase[i] + 2 * np.pi
                                # Store Amplitude and Phase into the dataframe
                                AmpOK = []
                                PhaseOK = []
                                for item in FreqPoss:
                                    AmpOK.append(amplitude[item])
                                    PhaseOK.append(phase[item])
                                df_Amplitude[Sensor] = AmpOK
                                df_Phase[Sensor] = PhaseOK
                        # Store Amplitude and Phase dataframe into Amplitude and Phase Databases
                        self.AmplitudeDB = self.AmplitudeDB.append(df_Amplitude, ignore_index=True)
                        self.PhaseDB = self.PhaseDB.append(df_Phase, ignore_index=True)
                #
                return True
            else:
                return False
        except:
            return False
            
    def MergeData(self):
        """
        """
        try:
        #!     if self.FlagUpdate:
        #!         AmplitudeDBOld = pd.read_pickle("../projects/"+self.ProjectName+"/"+self.ProbeName+"/SPdata/"+self.Run+"Amplitude.pkz", compression = "zip")
        #!         PhaseDBOld = pd.read_pickle("../projects/"+self.ProjectName+"/"+self.ProbeName+"/SPdata/"+self.Run+"Phase.pkz", compression = "zip")
        #!         self.AmplitudeDB = AmplitudeDBOld.append(self.AmplitudeDB, ignore_index=True)
        #!         self.PhaseDB = PhaseDBOld.append(self.PhaseDB, ignore_index=True)
        #!
            return True
        except:
            return False

    def SaveData(self):
        """
        """
        # The above code is saving dataframes `df_MobWinTime`, `PhaseDB`, and
        # `AmplitudeDB` as pickled files with compression in the specified
        # `OutputFolder`. It returns `True` if the saving is successful and
        # `False` otherwise.
        try:
            df_MobWinTime = pd.DataFrame()
            df_MobWinTime["Time"] = self.MobWinTime
            #
            df_MobWinTime.to_pickle(self.OutputFolder+"/MobWinTime.pkz", compression="zip")
            #
            self.PhaseDB.to_pickle(self.OutputFolder+"/Phase.pkz",compression="zip")
            self.AmplitudeDB.to_pickle(self.OutputFolder+"/Amplitude.pkz",compression="zip")
            #
            return True
        except:
            return False

if __name__ == "__main__":
    options = sys.argv[1:]
    logger.remove()
    logger.add(f"../logs/SignalProcessingFFT.log", rotation="7 days")
    logger.info(f"SignalProcessingFFT started...")
    #
    try:
        opts, args = getopt.getopt(options,"s:t:d:f:r:u:m:a:o:i:l:",["version"])
        #
        StringError = "No Error"
        SP = SignalProcessingFFT(opts, args)
        logger.info(f"\tCheckOptions...")
        result = SP.CheckOptions()
        if result:
            logger.info(f"\tCheckOptions ended...")
            result = SP.LoadData()
            logger.info(f"\tLoadData...")
            if result:
                logger.info(f"LoadData ended...")
                result = SP.WindowsTime()
                logger.info(f"\tWindowsTime...")
                if result:
                    logger.info(f"\tWindowsTime ended...")
                    result = SP.Processing()
                    logger.info(f"\tProcessing...")
                    if result:
                        logger.info(f"\tProcessing ended...")
                        result = SP.MergeData()
                        logger.info(f"\tMergeData...")
                        if result:
                            logger.info(f"\tMergeData ended...")
                            result = SP.SaveData()
                            logger.info(f"\tSaveData...")
                            if result:
                                logger.info(f"\tSaveData ended...")
                                # ImportLog
                                HandleRiassunto = open(SP.OutputFolder+"/XXX.run","w")
                                HandleRiassunto.write("FFT;AnalysisType\n")
                                if SP.MobWin:
                                    HandleRiassunto.write("Yes;MobileWin\n")
                                else:
                                    HandleRiassunto.write("No;MobileWin\n")
                                HandleRiassunto.write(str(SP.MobWinLen)+";MobileWinLenght\n")
                                HandleRiassunto.write(SP.FFTWin+";FFTwin\n")
                                if SP.Detrending:
                                    HandleRiassunto.write("Yes;Detrending\n")
                                else:
                                    HandleRiassunto.write("No;Detrending\n")
                                HandleRiassunto.write(str(SP.dt)+";dt\n")
                                HandleRiassunto.write(",".join([str(item) for item in SP.SavePer])+";Periods\n")
                                HandleRiassunto.write(",".join(SP.ProcSensors)+";ProcSens\n")
                                HandleRiassunto.close()
                            else:
                                StringError = "SaveData Error"
                                logger.error("SaveData")
                        else:
                            StringError = "MergeData Error"
                            logger.error("MergeData")
                    else:
                        StringError = "Processing Error"
                        logger.error("Processing")
                else:
                    StringError = "Windows Time Error"
                    logger.error("WindowsTime")
            else:
                StringError = "LoadData Error"
                logger.error("LoadData")
        else:
            StringError = "CheckOptions Error"
            logger.error("CheckOption")
        #
        HandleLog = open(SP.OutputFolder+"/SignalProcessing.log","w")
        HandleLog.write(StringError)
        HandleLog.close()
        logger.info(f"SignalProcessing finished")
    except getopt.GetoptError:
        HandleLog = open(SP.OutputFolder+"/SignalProcessing.log","w")
        HandleLog.write("Options error")
        HandleLog.close()
        logger.error("Getopt")