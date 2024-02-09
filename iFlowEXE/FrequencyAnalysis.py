################################# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#
#     Probe name  [STRING] -p
#     Project name  [STRING] -j
#     FFT window [STRING] -w
#     From [FLOAT] -f
#     To [BOOLEAN] -t
# 
# 
############################### 

# Import the libraries
import os,sys
import getopt
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import numpy as np
from scipy import signal
#%%
class FrequencyAnalysis:
    def __init__(self,opts, args):
        #
        # self.ProbeName = '' # Probe Name
        # self.ProjectName = '' # Project Name
        self.FFTWin = 'Rectangular' # FFT window
        self.From = np.nan # From
        self.To = np.nan # To
        self.OutputFolder = '../temp' # Output folder.
        self.Version = False # Flag display version and stop the execution.
        self.InputFolder = '../temp' # Input folder.
        self.dt = np.nan # Sample frequency
        #
        for opt, arg in opts:
            # if opt in ('-p'):
            #     self.ProbeName = arg
            # elif opt in ('-j'):
            #     self.ProjectName = arg
            # el
            if opt in ('-w'):
                self.FFTWin = arg
            elif opt in ('-f'):
                self.From = float(arg)
            elif opt in ('-t'):
                self.To = float(arg)
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in ('-i'):
                self.InputFolder = arg
            elif opt in ('-d'):
                self.dt = float(arg)
            elif opt in('--version'):
                self.Version = True

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
            # if type(self.ProbeName) != str : FlagPreCheck = False
            # if type(self.ProjectName) != str : FlagPreCheck = False
            if type(self.FFTWin) != str : FlagPreCheck = False
            if type(self.From) != float : FlagPreCheck = False
            if type(self.To) != float : FlagPreCheck = False
            if type(self.OutputFolder) != str : FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
            if type(self.dt) != float : FlagPreCheck = False
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
            # self.df_Sensors = pd.read_pickle('../projects/'+self.ProjectName+'/'+self.ProbeName+'/data/clean.pkz', compression = 'zip')
            self.df_Sensors = pd.read_pickle(self.InputFolder+'/clean.pkz', compression = 'zip')
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
            df_work = self.df_Sensors[(self.df_Sensors['Time'] >= self.From) & (self.df_Sensors['Time'] <= self.To)]
            nStep = df_work.shape[0]
            # dt = (self.To-self.From)/(nStep-1)
            # Create FFT wnidow
            if(self.FFTWin == 'Rectangular'):
                self.Weight = np.asarray([1 for i in range(0,nStep)])
            elif(self.FFTWin == 'Bartlett'):
                self.Weight = np.bartlett(nStep)
            elif(self.FFTWin == 'Hamming'):
                self.Weight = np.hamming(nStep)
            elif(self.FFTWin == 'Hanning'):
                self.Weight = np.hanning(nStep)
            elif(self.FFTWin == 'Triangular'):
                self.Weight = np.asarray([(1 - np.abs(i - 0.5 * (nStep - 1)) / (0.5 * (nStep + 1))) for i in range(0,nStep)])
            elif(self.FFTWin == 'FlatTop'):
                self.Weight = signal.flattop(nStep)
            # Initialize dataframe
            self.df_Amp = pd.DataFrame()
            self.df_Phi = pd.DataFrame()
            self.df_PSD = pd.DataFrame()
            # FFT Frequencies
            Freqs = np.fft.fftfreq(nStep, self.dt)
            # Insert frequencies calculated as 'Freq' column
            self.df_Amp['Freq'] = Freqs#[1:]
            self.df_Phi['Freq'] = Freqs#[1:]
            self.df_PSD['Freq'] = Freqs#[1:]
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
        '''SaveData [summary]

        [extended_summary]

        Returns:
            [type]: [description]
        '''
        print('SaveData...')
        try:
            self.df_Amp.to_pickle(self.OutputFolder+'/Amplitude.pkz', compression='zip')
            self.df_Phi.to_pickle(self.OutputFolder+'/Phase.pkz', compression='zip')
            self.df_PSD.to_pickle(self.OutputFolder+'/PSD.pkz', compression='zip')
            return True
        except:
            return False

if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        # Get command line options
        opts, args = getopt.getopt(options,'p:j:w:f:t:i:o:d:',['version'])
        # Initialize Error String
        StringError = 'No Error'
        # Initialize FrequencyAnalysis class
        FA = FrequencyAnalysis(opts, args)
        # Check the command line options
        result = FA.CheckOptions()
        if result:
            # Load the new data
            result = FA.LoadData()
            if result:
                # Signal analysis with Fast Fourier Transform
                result = FA.Processing()
                if result:
                    # Save the data
                    result = FA.SaveData()
                    if result:
                        # ImportLog
                        HandleRiassunto = open(FA.OutputFolder+'/XXX.run','w')
                        HandleRiassunto.write(FA.FFTWin+';FFTwin\n')
                        HandleRiassunto.write(str(FA.From)+';From\n')
                        HandleRiassunto.write(str(FA.To)+';To\n')
                        HandleRiassunto.write(str(FA.dt)+';dt\n')
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
        HandleLog = open('../temp/FrequencyAnalysis.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open('../temp/FrequencyAnalysis.log','w')
        HandleLog.write('Options error')
        HandleLog.close()