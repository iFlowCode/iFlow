"""
"""

# Import the libraries
import os,sys
import getopt
import pandas as pd
import numpy as np
from scipy import signal
from loguru import logger

class FrequencyAnalysis:
    def __init__(self,opts, args):
        """
        The function initializes various parameters with default values and allows
        them to be modified based on command line arguments.
        
        :param opts: opts is a list of tuples containing the options and their
        corresponding arguments passed to the script when it is executed
        :param args: The `args` parameter in the `__init__` method is typically used
        to accept any additional arguments that are not specified as options in the
        `opts` parameter. In this context, `args` would refer to a list of
        additional arguments that are passed to the class constructor when an
        instance of
        """
        #
        self.FFTWin = "Rectangular" # FFT window
        self.From = 0.0 # From
        self.To = 3109500.0 # To
        self.OutputFolder = "../temp" # Output folder.
        self.Version = False # Flag display version and stop the execution.
        self.InputFolder = "../temp" # Input folder.
        self.dt = 900.0 # Sample frequency
        #
        for opt, arg in opts:
            if opt in ("-w"):
                self.FFTWin = arg
            elif opt in ("-f"):
                self.From = float(arg)
            elif opt in ("-t"):
                self.To = float(arg)
            elif opt in ("-o"):
                self.OutputFolder = arg
            elif opt in ("-i"):
                self.InputFolder = arg
            elif opt in ("-d"):
                self.dt = float(arg)
            elif opt in("--version"):
                self.Version = True

    def CheckOptions(self):
        """
        """
        # This `try-except` block in the `CheckOptions` method of the
        # `FrequencyAnalysis` class is attempting to validate the types of the
        # options provided during initialization. It checks if the specified
        # options (`FFTWin`, `From`, `To`, `OutputFolder`, `InputFolder`, `dt`)
        # are of the expected types (`str` for folders, `float` for numerical
        # values). If any of the options are not of the expected type,
        # `FlagPreCheck` is set to `False`.
        try:
            #  
            FlagPreCheck = True
            # Check Options type
            if type(self.FFTWin) != str : FlagPreCheck = False
            if type(self.From) != float : FlagPreCheck = False
            if type(self.To) != float : FlagPreCheck = False
            if type(self.OutputFolder) != str : FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
            if type(self.dt) != float : FlagPreCheck = False
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
        # This `try-except` block in the `LoadData` method of the
        # `FrequencyAnalysis` class is attempting to load data from a pickle file
        # located at `self.InputFolder+"/clean.pkz"` with zip compression.
        try:
            self.df_Sensors = pd.read_pickle(self.InputFolder+"/clean.pkz", compression = "zip")
            return True
        except:
            return False

    def Processing(self):
        """
        """
        # This block of code is responsible for processing the data by performing
        # Fast Fourier Transform (FFT) analysis on the sensor data. Here's a
        # breakdown of what it does:
        try:
            df_work = self.df_Sensors[(self.df_Sensors["Time"] >= self.From) & (self.df_Sensors["Time"] <= self.To)]
            nStep = df_work.shape[0]
            # Create FFT wnidow
            if(self.FFTWin == "Rectangular"):
                self.Weight = np.asarray([1 for i in range(0,nStep)])
            elif(self.FFTWin == "Bartlett"):
                self.Weight = np.bartlett(nStep)
            elif(self.FFTWin == "Hamming"):
                self.Weight = np.hamming(nStep)
            elif(self.FFTWin == "Hanning"):
                self.Weight = np.hanning(nStep)
            elif(self.FFTWin == "Triangular"):
                self.Weight = np.asarray([(1 - np.abs(i - 0.5 * (nStep - 1)) / (0.5 * (nStep + 1))) for i in range(0,nStep)])
            elif(self.FFTWin == "FlatTop"):
                self.Weight = signal.flattop(nStep)
            # Initialize dataframe
            self.df_Amp = pd.DataFrame()
            self.df_Phi = pd.DataFrame()
            self.df_PSD = pd.DataFrame()
            # FFT Frequencies
            Freqs = np.fft.fftfreq(nStep, self.dt)
            # Insert frequencies calculated as 'Freq' column
            self.df_Amp["Freq"] = Freqs#[1:]
            self.df_Phi["Freq"] = Freqs#[1:]
            self.df_PSD["Freq"] = Freqs#[1:]
            # 
            Columns = df_work.columns
            # For every sensor
            for i in range(1,df_work.shape[1]):
                # Calculate FFT
                fft_hat = np.fft.fft(df_work[Columns[i]]*self.Weight)
                # Initialize vectors
                amplitude = np.zeros(fft_hat.shape)
                phase = np.zeros(fft_hat.shape)
                PSD = np.zeros(fft_hat.shape)
                # Calculate Amplitude, Phase and Power Spectrum Density
                for j,hat in enumerate(fft_hat):
                    amplitude[j] = np.abs(hat) / (int(nStep) / 2)
                    phase[j] = np.arctan2(-np.imag(hat),np.real(hat))
                    PSD[j] = np.real(hat * np.conj(hat))
                # Insert Amplitude, Phase and Power Spectrum Density into the dataframes
                self.df_Amp[Columns[i]] = amplitude
                self.df_Phi[Columns[i]] = phase
                self.df_PSD[Columns[i]] = PSD
            return True
        except:
            return False

    def SaveData(self):
        """
        """
        # This block of code is attempting to save the dataframes `df_Amp`,
        # `df_Phi`, and `df_PSD` to pickle files with specified filenames and
        # compression format in the specified `OutputFolder`.
        try:
            self.df_Amp.to_pickle(self.OutputFolder+"/Amplitude.pkz", compression="zip")
            self.df_Phi.to_pickle(self.OutputFolder+"/Phase.pkz", compression="zip")
            self.df_PSD.to_pickle(self.OutputFolder+"/PSD.pkz", compression="zip")
            return True
        except:
            return False

if __name__ == "__main__":
    options = sys.argv[1:]
    logger.remove()
    logger.add(f"../logs/Frequencies.log", rotation="7 days")
    logger.info(f"FrequencyAnalisis started...")
    #
    try:
        # Get command line options
        opts, args = getopt.getopt(options,"p:j:w:f:t:i:o:d:",["version"])
        # Initialize Error String
        StringError = "No Error"
        # Initialize FrequencyAnalysis class
        FA = FrequencyAnalysis(opts, args)
        # Check the command line options
        logger.info(f"\tCheckOption...")
        result = FA.CheckOptions()
        if result:
            logger.info(f"\tCheckOption ended...")
            # Load the new data
            logger.info(f"\tLoadData...")
            result = FA.LoadData()
            if result:
                logger.info(f"\LoadData ended...")
                # Signal analysis with Fast Fourier Transform
                logger.info(f"\tProcessing...")
                result = FA.Processing()
                if result:
                    logger.info(f"\tProcessing ended...")
                    # Save the data
                    logger.info(f"\tSavedata...")
                    result = FA.SaveData()
                    if result:
                        logger.info(f"SaveData ended...")
                        # FrequnciesLog
                        HandleRiassunto = open(FA.OutputFolder+"/XXX.run","w")
                        HandleRiassunto.write(FA.FFTWin+";FFTwin\n")
                        HandleRiassunto.write(str(FA.From)+";From\n")
                        HandleRiassunto.write(str(FA.To)+";To\n")
                        HandleRiassunto.write(str(FA.dt)+";dt\n")
                        HandleRiassunto.close()
                    else:
                        StringError = "SaveData Error"
                        logger.error("SaveData")
                else:
                    StringError = "Processing Error"
                    logger.error("Analysis")
            else:
                StringError = "LoadData Error"
                logger.error("LoadData")
        else:
            StringError = "CheckOptions Error"
            logger.error("CheckOption")
        #
        HandleLog = open(FA.OutputFolder+"FrequencyAnalysis.log","w")
        HandleLog.write(StringError)
        HandleLog.close()
        logger.info(f"FrequencyAnalisis finished")
    except getopt.GetoptError:
        HandleLog = open(FA.OutputFolder+"/FrequencyAnalysis.log","w")
        HandleLog.write("Options error")
        HandleLog.close()
        logger.error("Getopt")