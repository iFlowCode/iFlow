"""
"""

import os, sys
import getopt
import pandas as pd
import numpy as np
import numpy.matlib
import math
import pickle
from loguru import logger
from scipy import linalg

# np.savetxt('../temp/SNRFinalPython.csv', SRN, delimiter=',')


def LocalPolyAnal(Data_Y, Data_U, Data_freq, method):
    """LocalPolyAnal

                Estimates the frequency response function (FRF) and the output noise covariance matrix from
        arbitrary input/output data via a local polynomial least squares approximation of the
        plant transfer function and the plant and noise transient terms. The input signal may be
        exactly zero in (parts of) the frequency band of interest.

        For nonlinear systems the FRF is the best linear approximation and the output covariance
        is the sum of the noise covariance and the covariance of the stochastic nonlinear distortions.

        If no input data is provided, then the algorithm simplifies to nonparametric
        time series analysis (noise power spectrum estimation).

        Warning: the estimated frequency response matrix is meaningless in those
        frequency bands were the input is exactly zero.

    Args:
        Data_Y ([type]): output signal, size ny x F
        Data_U ([type]): input signal, size nu x F
        Data_freq ([type]): requency vector in Hz or in DFT numbers, size 1 x F (optional)
            default: [1:1:F]
        Data_CY ([type]): optional parameter (default empty) for nonlinear systems, size ny x ny x F #! To add
            noise covariance matrix data.Y => the total covariance on the frequency response #! To add
            matrix can be split in noise and nonlinear contributions #! To add
        method ([type]): structure containing the parameters of the method used (optional)
            order = order of the polynomial approximation (optional; default 2)
            dof = determines the degrees of freedom noise covariance estimate CY^-1
                (optional; default ny)
            transient = determines the estimation of the transient term (optional; default 1)
                1: transient term is estimated
                0: no transient term is estimated
            step = determines at which entries of data.freq the output parameters are calculated:
                (optional; default 1)
                data.freq(1:step:end)

    Rik Pintelon, July 2008
    version March 2, 2010

    Local Polynomial Method is based on Copyright (c) 2012 Rik Pintelon:
    [3] Pintelon, R., Schoukens, J., Vandersteen, G., and Barbe, K., 2010.
        Estimation of nonparametric noise and FRF models for multivariable systems-Part I: Theory,
        Mechanical Systems and Signal Processing, 24(3), 573-595.
    """
    # Initialisation variables
    ny = Data_Y.shape[0]  # number of outputs ny
    F = Data_Y.shape[1]  # number of frequencies F
    #
    try:
        if Data_freq.size == 0:
            Data_freq = np.array([t for t in range(1, F + 1)])  # TODO
        else:
            Data_freq = Data_freq  #! Transpose removed to keep the shape
            Data_freq = Data_freq / np.min(np.diff(Data_freq))  # normalisation for improving the numerical conditioning
    except:
        Data_freq = np.array([t for t in range(1, F + 1)])  # TODO
    #
    try:
        if len(method) == 0:
            method["order"] = 2  # TODO
            method["dof"] = 0  # TODO
    except:
        method["order"] = 2  # TODO
        method["dof"] = 0  # TODO
    #
    if "order" in method:
        if method["order"] == "":
            method["order"] = 2  # TODO
    else:
        method["order"] = 2  # TODO
    #
    if "dof" in method:
        if method["dof"] == "":
            method["dof"] = ny  # TODO
    else:
        method["dof"] = ny  # TODO
    #
    if "transient" in method:
        if method["transient"] == "":
            method["transient"] = 1  # TODO
    else:
        method["transient"] = 1  # TODO
    #
    if method["transient"] != 1:
        method["transient"] = 0  # TODO
    #
    if "step" in method:
        if method["step"] == "":
            method["step"] = 1  # TODO
    else:
        method["step"] = 1
    #
    try:
        if Data_U.size == 0:
            Data_U = np.array([], dtype=complex)  # TODO
    except:
        Data_U = np.array([], dtype=complex)  # TODO
    #
    try:
        if Data_CY.size == 0:
            Data_CY = np.array([], dtype=complex)  # TODO
            NoiseCov = 0  # no noise covariance matrix available #TODO
        else:
            NoiseCov = 1  # noise covariance available #TODO
    except:
        Data_CY = np.array([], dtype=complex)
        NoiseCov = 0
    #
    R = method["order"]  # order polynomial method
    transient = method["transient"]  # if 1 then transient is estimated (default); otherwise 0
    Fstep = method["step"]  # frequency step
    SelectFreq = np.array([[i + 1] for i in range(0, F, Fstep)])  # entries of data.freq at which the output parameters are calculated
    Fselect = SelectFreq.shape[0]  # number of frequencies at which the output parameters are calculated
    nu = Data_U.shape[0]  # number of inputs nu
    #
    if transient == 1:
        nu1 = nu + 1  # +1 accounts for the transient parameters
    elif transient == 0:
        nu1 = nu  # no transient parameters are estimated #TODO
    # half the frequency width in DFT samples of the polynomial method
    nn = math.ceil((method["dof"] + (R + 1) * nu1 - 1) / 2)
    # correlation length nonparametric estimates
    CL = 2 * nn
    # number of degrees of freedom in the residuals
    qq = 2 * nn + 1 - (R + 1) * nu1
    #  degrees of freedom of the covariance estimate
    dof = qq
    # Initizlize output array
    # covariance matrices
    CY_n = np.zeros((ny, ny, Fselect), dtype=complex)
    CY_m = np.zeros((ny, ny, Fselect), dtype=complex)
    CY_m_nt = np.zeros((ny, ny, Fselect), dtype=complex)
    # sample mean output
    Y_m = np.zeros((ny, Fselect), dtype=complex)
    Y_m_nt = np.zeros((ny, Fselect), dtype=complex)
    # plant and noise transient contribution at output
    TY = np.zeros((ny, Fselect), dtype=complex)
    # frequency response matrix
    G = np.zeros((ny, nu, Fselect), dtype=complex)
    # covariance matrix FRM
    if NoiseCov == 0:  # no output noise covariance available
        CvecG = np.zeros((ny * nu, ny * nu, Fselect), dtype=complex)
    else:  # output noise covariance available
        CvecG_NL = np.zeros((ny * nu, ny * nu, Fselect), dtype=complex)  # TODO
        CvecG_n = np.zeros((ny * nu, ny * nu, Fselect), dtype=complex)  # TODO
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Calculation of the regressor matrix Kn %
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # regressor matrix
    Kn = np.zeros(((R + 1) * nu1, 2 * nn + 1), dtype=complex)
    # intermediate variable
    Power_r = np.ones((R + 1, 2 * nn + 1), dtype=complex)
    # loop over all frequencies
    fk = 0  # frequency index of the output parameters
    for kk in range(1, F + 1, Fstep):
        fk += 1
        # range of DFT frequencies around kk
        if kk <= nn:
            r_index = np.array([[item for item in range(-kk + 1, 2 * nn - kk + 1 + 1, 1)]], dtype=int)
        if (kk >= nn + 1) and (kk <= F - nn):
            r_index = np.array([[item for item in range(-nn, nn + 1, 1)]], dtype=int)  # TODO
        if kk >= F - nn + 1:
            r_index = np.array([[item for item in range(-2 * nn + F - kk, F - kk + 1, 1)]], dtype=int)  # TODO
        # intermediate variable: powers of r
        r_power = np.zeros((r_index.shape))
        for i, item in enumerate(r_index[0]):
            r_power[0, i] = Data_freq[0, kk + item - 1] - Data_freq[0, kk - 1]
        #
        for ii in range(2, R + 1 + 1):
            Power_r[ii - 1, :] = np.power(r_power, ii - 1)
        # regressor matrix
        if nu > 0:
            Ukr = np.zeros((r_index.shape), dtype=complex)
            for i, item in enumerate(r_index[0]):
                Ukr[0, i] = Data_U[:, kk + item - 1]
            if 1:  # Speed improvement by Gerd
                for jj in range(1, 2 * nn + 1 + 1):
                    Kn[0 : (R + 1) * nu, jj - 1] = np.kron(Power_r[:, jj - 1], Ukr[:, jj - 1])
            else:
                logger.critical("Qui non entrera mai")  # TODO
                # for jj = 1:(R+1)
                #     for ii=1:nu
                #         idx=nu*(ii-1)+jj;
                #         Kn(idx, :) = Power_r(jj, :).*Ukr(ii, :);
        #
        if transient:
            Kn[(R + 1) * nu :, :] = Power_r
        # normalise the rows of Kn for improving the numerical stability of
        # the calculations
        Scale = np.power(np.sum(np.abs(np.power(Kn, 2)), axis=1), 0.5)  # 2-norm rows Kn
        Scale = (np.where(Scale == 0.0, 1.0, Scale)).reshape(Scale.shape[0], 1)  # if the input is exactly zero in the band kk-n:kk+n then the scaling is set equal to one   2*nn+1
        #
        Kn = np.divide(Kn, np.matlib.repmat(Scale, 1, 2 * nn + 1))
        # numerical stable LS estimate output (= "sample mean")
        Un, SnTemp, VnTemp = linalg.svd(np.conj(Kn.T), compute_uv=True, full_matrices=False, lapack_driver="gesvd")
        # Un, SnTemp, VnTemp = np.linalg.svd(np.conj(Kn.T), full_matrices=False)
        Vn = np.conj(VnTemp).T  #! PYTHON
        Sn = np.diag(SnTemp)  #! PYTHON
        #
        Yn = ((Data_Y[:, kk + r_index[0] - 1]).dot(Un)).dot(np.conj(Un.T))
        Index_kk = np.where(r_index == 0.0)[1]
        if Index_kk.size != 0:
            Y_m[:, [fk - 1]] = Yn[:, Index_kk]
        # numerical stable LS estimate of the noise covariance matrix (= "sample covariance matrix")
        En = np.subtract(Data_Y[:, kk + r_index[0] - 1], Yn)
        CY_n[:, :, fk - 1] = (En.dot(np.conj(En.T))) / qq
        # sample covariance of the sample mean
        Qnkk = (Un[Index_kk[0], :]).dot(np.conj((Un[Index_kk[0], :]).T))
        CY_m[:, :, fk - 1] = np.real(Qnkk) * (CY_n[:, :, fk - 1])
        #
        if transient or (nu > 0):
            # LS estimate model parameters (Theta matrix)
            # ss = np.diag(Sn)
            ss = np.array([Sn[i, i] for i in range(0, Sn.shape[0])])  #! PYTHON
            #
            IndexZeros = np.where(ss == 0)[0]
            if IndexZeros.shape[0] != 0:
                for item in IndexZeros:  # TODO
                    ss[item] = np.inf
            ss = np.diag(np.divide(1.0, ss))
            Theta = Yn.dot(Un.dot(ss.dot(np.conj(Vn.T))))
        #
        if transient:
            # LS estimate transient contribution at output
            IndexTrans = (nu * (R + 1) + 1)  # position transient parameters in Theta matrix
            TY[:, fk - 1] = (Theta[:, IndexTrans - 1] / Scale[IndexTrans - 1])  # denormalisation parameters
            Y_m_nt = Y_m - TY  # output without transient
            # covariance matrix Ym-TY
            # qkk = Un * Un[Index_kk, :].T
            # bmm = Un * (diag(ss) .* Vn(IndexTrans, :)') / Scale(IndexTrans);  % denormalisation parameters
            # difference qkk - bmm
            if Index_kk.shape[0] > 1:
                logger.critical("Problema")  # TODO
            qkk_bmm = Un.dot(np.conj(Un[Index_kk[0], :].T)- np.conj((np.multiply(np.diag(ss), Vn[IndexTrans - 1, :])).T)/ Scale[IndexTrans - 1])
            # CY_m_nt[:,:,fk-1] = (np.linalg.norm(qkk_bmm, 2)**2 * CY_n[:,:,fk-1])
            CY_m_nt[:, :, fk - 1] = (np.linalg.norm(qkk_bmm, 2) ** 2) * (CY_n[:, :, fk - 1])
        #
        if nu > 0:
            # estimate FRM
            IndexFRM = [t for t in range(1, nu + 1)]  # position FRM parameters in Theta matrix
            for i in range(0, (Theta[:, IndexFRM[0] - 1]).shape[0]):
                G[i, :, fk - 1] = (Theta[:, IndexFRM[0] - 1])[i] / np.matlib.repmat(Scale[IndexFRM[0] - 1].T, ny, 1)[i]
            # G[:, :, fk-1] = np.divide(Theta[:, IndexFRM[0]-1].T, np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1))
            # covariance matrix vec(G)
            dimVn = Vn.shape[1]
            Temp = []
            for t in range(0, (Vn[IndexFRM[0] - 1, :]).shape[0]):
                Temp.append(Vn[IndexFRM[0] - 1, t]/ np.matlib.repmat(Scale[IndexFRM[0] - 1], 1, dimVn)[0, t])
            Temp = np.array(Temp, dtype=complex)
            VV = Temp.dot(ss)  # intermediate variable
            if NoiseCov == 0:
                CvecG[:, :, fk - 1] = np.kron(np.conj(VV.dot(np.conj(VV.T))), CY_n[:, :, fk - 1])
            else:
                CvecG_NL[:, :, fk - 1] = np.kron(np.conj(VV * np.conj(VV.T)), CY_n[:, :, fk - 1])  # TODO
                CvecG_n[:, :, fk - 1] = np.kron( np.conj(VV * np.conj(VV.T)), data_CY[:, :, fk - 1])  # TODO
    #
    return CY_n, CY_m, CY_m_nt, Y_m, Y_m_nt, TY, G, CvecG, dof, CL

class SignalProcessingLPM:
    def __init__(self, opts, args):
        #
        self.MobWin = True  # False#
        self.MobWinLen = 96.0
        self.SensorRef = "T0"  # None
        self.dt = 900.0  # np.nan
        self.FlagUpdate = False
        self.RunUpdate = "-9"
        self.dof = 8
        self.order = 2
        self.OutputFolder = "../temp"  # Output folder.
        self.Version = False  # Flag display version and stop the execution.
        self.InputFolder = "../temp"  # Input folder.
        # 
        for opt, arg in opts:
            if opt in ("-f"):
                if arg == "False":
                    self.MobWin = False
                else:
                    self.MobWin = True
            elif opt in ("-s"):
                self.MobWinLen = float(arg)
            elif opt in ("-q"):
                self.SensorRef = arg
            elif opt in ("-d"):
                self.dt = float(arg)
            elif opt in ("-u"):
                if arg == "False":
                    self.FlagUpdate = False
                else:
                    self.FlagUpdate = True
            elif opt in ("-r"):
                self.RunUpdate = arg
            elif opt in ("-o"):
                self.dof = int(arg)
            elif opt in ("-m"):
                self.order = int(arg)
            elif opt in ("-c"):
                self.OutputFolder = arg
            elif opt in ("-i"):
                self.InputFolder = arg
            elif opt in ("--version"):
                self.Version = True
        return

    def CheckOptions(self):
        try:
            #
            FlagPreCheck = True
            # Check Options type
            if type(self.MobWin) != bool:
                FlagPreCheck = False
            if type(self.MobWinLen) != float:
                FlagPreCheck = False
            if type(self.SensorRef) != str:
                FlagPreCheck = False
            if type(self.dt) != float:
                FlagPreCheck = False
            if type(self.FlagUpdate) != bool:
                FlagPreCheck = False
            if type(self.RunUpdate) != str:
                FlagPreCheck = False
            if type(self.dof) != int:
                FlagPreCheck = False
            if type(self.order) != int:
                FlagPreCheck = False
            if type(self.OutputFolder) != str:
                FlagPreCheck = False
            if type(self.InputFolder) != str:
                FlagPreCheck = False
            #
            if self.Version:
                print("Version 0.1")
                return False
            return FlagPreCheck
        except:
            return False

    def LoadData(self):
        try:
            # Load the dataset
            self.df_Sensors = pd.read_pickle(self.InputFolder + "/clean.pkz", compression="zip")
            self.ProcSensors = (self.df_Sensors.columns.tolist())[1:]
            # Load or create old processing
            if self.FlagUpdate:
                pass
                # self.MobWinTimeOld = (pd.read_pickle('../projects/'+self.ProjectName+'/'+self.ProbeName+'/SPdata/'+self.RunUpdate+'_MobWinTime.pkz', compression='zip'))['Time'].tolist()
            else:
                self.MobWinTimeOld = []
            # Time limits
            self.StartTime = self.df_Sensors["Time"].iloc[0]
            self.EndTime = self.df_Sensors["Time"].iloc[self.df_Sensors.shape[0] - 1]
            return True
        except:
            return False

    def WindowsTime(self):
        try:
            self.nStepData = self.df_Sensors.shape[0]
            #
            self.MobWinTime = []
            if self.MobWin:
                self.nStepMWin = self.MobWinLen * 60.0 * 60.0 / self.dt
                #
                StartTemp = self.StartTime
                EndTemp = StartTemp + self.dt * self.nStepMWin
                while EndTemp <= self.EndTime:
                    self.MobWinTime.append((EndTemp - StartTemp) / 2 + StartTemp)
                    StartTemp = StartTemp + self.dt
                    EndTemp = EndTemp + self.dt
                #
                del StartTemp
                del EndTemp
            else:
                self.nStepMWin = self.nStepData
                #
                self.MobWinTime.append((self.EndTime - self.StartTime) / 2)
            #
            return True
        except:
            return False

    def Processing(self):
        try:
            # Lists initialization
            self.List_SRN = []
            self.List_Y = []
            self.List_CY_m_nt = []
            # Flag first window calculation
            Flag = True
            # Windows loop
            for t in range(0, len(self.MobWinTime)):
                # for t in range (0,100):
                if self.MobWinTime[t] in self.MobWinTimeOld:
                    # Window already processed
                    pass
                else:
                    # Window start and end time calculation
                    StartTemp = self.StartTime + t * self.dt  # slider
                    if self.MobWin:
                        EndTemp = StartTemp + self.MobWinLen * 60.0 * 60.0
                        df_temp = self.df_Sensors[
                            (self.df_Sensors["Time"] >= StartTemp)
                            & (self.df_Sensors["Time"] < EndTemp)
                        ]
                    else:
                        EndTemp = self.EndTime
                        df_temp = self.df_Sensors
                    # Check nan
                    if df_temp.isnull().sum().sum() == 0:
                        df_DataRef_temp = (df_temp[self.SensorRef]).tolist()
                        #
                        df_DataRef = np.zeros((1, len(df_DataRef_temp)))
                        for i in range(0, len(df_DataRef_temp)):
                            df_DataRef[0, i] = df_DataRef_temp[i]
                        #
                        df_Data = df_temp.drop(["Time"], axis=1)
                        Columns = (df_Data.columns).tolist()
                        # for i in range(0,len(Columns)):
                        #     if Columns[i] == self.SensorUP:
                        #         break
                        #     else:
                        #         df_Data = df_Data.drop([Columns[i]], axis=1)
                        # #
                        # for i in range(len(Columns),0,-1):
                        #     if Columns[i-1] == self.SensorDOWN:
                        #         break
                        #     else:
                        #         df_Data = df_Data.drop([Columns[i-1]], axis=1)
                        self.Columns_OK = (df_Data.columns).tolist()
                        #
                        df_Data.columns = [""] * len(df_Data.columns)
                        #
                        df_Data = df_Data.to_numpy()
                        #
                        nt = df_Data.shape[0]
                        Fmax = math.floor(nt / 10)
                        #
                        freq = np.fft.fftfreq(int(nt), self.dt)
                        freq = freq[1:Fmax]
                        #
                        freq = freq.reshape(1, freq.shape[0])
                        #
                        U = np.ones(df_Data.shape, dtype=complex)
                        U[:] = np.nan
                        for i in range(0, df_Data.shape[1]):
                            U[:, i] = np.fft.fft(df_Data[:, i]) / nt
                        if df_DataRef.size != 0:
                            Uref = np.ones((df_DataRef.shape[1], 1), dtype=complex)
                            Uref[:, 0] = np.fft.fft(df_DataRef[0, :]) / nt
                            Uin = Uref[1:Fmax, :].T
                            Yin = U[1:Fmax, 0:].T
                        else:
                            Uin = U[0, 1:Fmax]
                            Yin = U[1:Fmax, 0:].T
                        #
                        method = {"transient": 1, "dof": self.dof, "order": self.order}
                        #
                        (CY_n,CY_m,CY_m_nt,Y_m,Y_m_nt,TY,G,CvecG,dof,CL) = LocalPolyAnal(Yin, Uin, freq, method)
                        #
                        Y = Y_m_nt.T
                        #
                        VarF = []
                        for ii in range(0, (freq.shape[1])):
                            VarF.append(np.real(np.diag(CY_m_nt[:, :, ii])))
                        VarF = np.array(VarF, dtype=float)
                        #
                        rows = Y.shape[0]
                        cols = Y.shape[1]
                        SRN = np.zeros((rows, cols), dtype=complex)
                        SRN = 20 * np.log10(abs(Y) / np.sqrt(VarF))
                        #
                        df_Amplitude = pd.DataFrame()
                        df_Phase = pd.DataFrame()
                        #
                        df_Amplitude["Time"] = [self.MobWinTime[t] for i in range(0, len(freq[0, :]))]
                        df_Phase["Time"] = [self.MobWinTime[t] for i in range(0, len(freq[0, :]))]
                        #
                        df_Amplitude["Freq"] = freq[0, :]
                        df_Phase["Freq"] = freq[0, :]
                        #
                        for j in range(0, Y.shape[1]):
                            Amptemp = []
                            Phasetemp = []
                            for i in range(0, Y.shape[0]):
                                Amptemp.append(np.abs(Y[i, j]) / (1.0 / 2.0))
                                Phasetemp.append(np.arctan2(-np.imag(Y[i, j]), np.real(Y[i, j])))
                            df_Amplitude[self.Columns_OK[j]] = Amptemp
                            df_Phase[self.Columns_OK[j]] = Phasetemp
                        #
                        if Flag:
                            self.AmplitudeDB = pd.DataFrame()
                            self.PhaseDB = pd.DataFrame()
                            #
                            self.AmplitudeDB = self.AmplitudeDB.append(df_Amplitude, ignore_index=True)
                            self.PhaseDB = self.PhaseDB.append(df_Phase, ignore_index=True)
                            Flag = False
                        else:
                            self.AmplitudeDB = self.AmplitudeDB.append(df_Amplitude, ignore_index=True)
                            self.PhaseDB = self.PhaseDB.append(df_Phase, ignore_index=True)
                        #
                        self.List_SRN.append(SRN)
                        self.List_Y.append(Y)
                        #
                        CY_m_nt.tofile(self.OutputFolder+ "/"+ str(self.MobWinTime[t])+ ".CY_m_nt")
                    else:
                        if Flag:
                            logger.critical("BIG ERROR")
                        else:
                            df_Amplitude.iloc[:, 2 : df_Amplitude.shape[1]] = np.nan
                            self.AmplitudeDB = self.AmplitudeDB.append(df_Amplitude, ignore_index=True)
                            df_Phase.iloc[:, 2 : df_Phase.shape[1]] = np.nan
                            self.PhaseDB = self.PhaseDB.append(df_Phase, ignore_index=True)
                            SRN[:] = np.nan
                            self.List_SRN.append(SRN)
                            Y[:] = complex(np.nan, np.nan)
                            self.List_Y.append(Y)
                            CY_m_nt[:, :, :] = complex(np.nan, np.nan)
                            CY_m_nt.tofile(self.OutputFolder+ "/"+ str(self.MobWinTime[t])+ ".CY_m_nt")
            #
            return True
        except:
            return False

    def PostPhase(self):
        try:
            #             # StartTime = self.PhaseDB['Time'].min()
            #             # # print(self.PhaseDB)
            #             # for i in range(0,self.PhaseDB.shape[0]):
            #             #     print(i,self.PhaseDB.shape[0])
            #             #     List = self.PhaseDB.iloc[i].to_list()
            #             #     deltaT = List[0] - StartTime
            #             #     Period = 1.0/List[1]
            #             #     # print(List)
            #             #     # print(deltaT,Period)
            #             #     while deltaT > Period:
            #             #         deltaT = deltaT - Period
            #             #     PhiCor = 2.0*np.pi*deltaT/Period
            #             #     # print(deltaT,Period,PhiCor)
            #             #     for j in range(2,len(List)):
            #             #         NewPhase = List[j]+PhiCor
            #             #         if NewPhase > np.pi:
            #             #             NewPhase = NewPhase - 2 * np.pi
            #             #         elif NewPhase < -np.pi:
            #             #             NewPhase = NewPhase + 2 * np.pi
            #             #         self.PhaseDB.iloc[i,j] = NewPhase
            #             # deltaT = self.PhaseDB['Time']-StartTime
            #             # print(deltaT)
            return True
        except:
            return False

    def SaveData(self):
        try:
            df_MobWinTime = pd.DataFrame()
            df_MobWinTime["Time"] = self.MobWinTime
            #
            df_MobWinTime.to_pickle(self.OutputFolder + "/MobWinTime.pkz", compression="zip")
            #
            self.AmplitudeDB.to_pickle(self.OutputFolder + "/Amplitude.pkz", compression="zip")
            #
            self.PhaseDB.to_pickle(self.OutputFolder + "/Phase.pkz", compression="zip")
            #
            with open(self.OutputFolder + "/SRN.PdList", "wb") as Handle:
                pickle.dump(self.List_SRN, Handle)
            #
            with open(self.OutputFolder + "/Y.PdList", "wb") as Handle:
                pickle.dump(self.List_Y, Handle)
            #
            return True
        except:
            return False


if __name__ == "__main__":
    options = sys.argv[1:]
    logger.remove()
    logger.add(f"../logs/SignalProcessingLP.log", rotation="7 days")
    logger.info(f"SignalProcessingLP started...")
    #
    try:
        opts, args = getopt.getopt(options, "f:s:q:w:e:d:u:r:o:m:c:i:l:", ["version"])
        #
        StringError = "No Error"
        LPM = SignalProcessingLPM(opts, args)
        logger.info(f"CheckOptions...")
        result = LPM.CheckOptions()
        if result:
            logger.info(f"\tCheckOptions ended...")
            logger.info(f"\tLoadData...")
            result = LPM.LoadData()
            if result:
                logger.info(f"\tLoadData ended...")
                logger.info(f"\tWindowsTime...")
                result = LPM.WindowsTime()
                if result:
                    logger.info(f"\tWindowsTime ended...")
                    logger.info(f"\tProcessing...")
                    result = LPM.Processing()
                    if result:
                        logger.info(f"\tProcessing ended...")
                        logger.info(f"\tPostPhase...")
                        result = LPM.PostPhase()
                        if result:
                            logger.info(f"\tPostPhase ended...")
                            logger.info(f"\tSaveData...")
                            result = LPM.SaveData()
                            if result:
                                logger.info(f"\tSaveData ended...")
                                # ImportLog
                                HandleRiassunto = open(LPM.OutputFolder + "/XXX.run", "w")
                                HandleRiassunto.write("LPM;AnalysisType\n")
                                if LPM.MobWin:
                                    HandleRiassunto.write("Yes;MobWin\n")
                                else:
                                    HandleRiassunto.write("No;MobWin\n")
                                HandleRiassunto.write(str(LPM.MobWinLen) + ";MobWinLen\n")
                                HandleRiassunto.write(LPM.SensorRef + ";SensorRef\n")
                                HandleRiassunto.write(str(LPM.dt) + ";dt\n")
                                HandleRiassunto.write(str(LPM.dof) + ";dof\n")
                                HandleRiassunto.write(str(LPM.order) + ";order\n")
                                HandleRiassunto.write(",".join(LPM.ProcSensors) + ";ProcSens\n")
                                HandleRiassunto.close()
                            else:
                                StringError = "SaveData Error"
                                logger.error("SaveData")
                        else:
                            StringError = "PostPhase Error"
                            logger.error("PostPhase")
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
            logger.error("CheckOptions")
        #
        HandleLog = open(LPM.OutputFolder + "/SignalProcessing.log", "w")
        HandleLog.write(StringError)
        HandleLog.close()
        logger.info(f"SignalProcessingLP finished")
    except getopt.GetoptError:
        HandleLog = open(LPM.OutputFolder + "/SignalProcessing.log", "w")
        HandleLog.write("Options error")
        HandleLog.close()
        logger.error("Getopt")