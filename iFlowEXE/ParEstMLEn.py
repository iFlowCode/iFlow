###############################################################################
#
# 
# 
# Options:
# Probe name  [STRING] -p
# Project name  [STRING] -j
# Sensors [LIST] -s
# Heights [LIST] -h
# FreqType [INTEGER] -f
# Run [STRING] -r
# MethodDV [STRING] -t
# D [FLOAT] - d
# V [FLOAT] - v
# Method [STRING] -m
# SRNLimit [FLOAT] -n
# FreqLimit [FLOAT] -l
# MinMaxSRN [INTEGER] -a
# cw_x_rhow [FLOAT] -x
# c_x_rho [FLOAT] -z
# Init [INTEGER] -i
# OutputFolder [STRING] -o
###############################################################################

# Import the libraries
# from _typeshed import Self
import cmath
import os,sys
import getopt
# import numpy.random.common
# import numpy.random.bounded_integers
# import numpy.random.entropy
import pandas as pd
import numpy as np
import pickle
from numpy.linalg import pinv
from scipy import special

import MLEnLib as Lib

# np.savetxt('../temp/DVKPBestPython.csv', DVKPBest, delimiter=',')

def MLEn(DVKP0,xTemp,w,U,Cov_m,options):
    x = np.zeros((1,len(xTemp)))
    for i,item in enumerate(xTemp):
        # x[0,i] = float(xTemp[0]) - float(item)
        x[0,i] = -float(item)
    # Check of set has been selected for estimation if not
    if options['parameters'] == '':
        if options['method'] == 'infinite': # semi-infinite case
            options['parameters'] = 'DVK'
        elif options['method'] == 'boundaries': # source-less domains
            options['parameters'] = 'DVK'
        elif options['method'] == 'source': # source-less domains
            options['parameters'] = 'DVKP'
    # Check and modify inputs where necessary
    DVKP0,x,w,U,Cov_m,options = Lib.MLEn_check_input(DVKP0,x,w,U,Cov_m,options)
    ## Check if a switch to 'DVKP' is necessary
    # Check if the parameter set in which to optimize has been defined
    # if not set options.parametersetoptimize set to 'abcd'
    if 'mapping' in options:
        pass
    else:
        options['mapping'] = 'abcd'
    if 'maxNbfOfSteps' in options:
        pass
    else:
        options['maxNbfOfSteps'] = 100
    # Check for a special case in which the estimation goes wrong for a,b,c,d
    options = Lib.MLEn_check_partially_fixed_divisions(DVKP0,options)
    # Check if the optimization will be performed directly in DVKP or the more
    # reliable abcd parameter set (preferred)

    if options['mapping'] == 'abcd':
        # Translate 'DVKP' in terms of idxFree for abcd
        idxFree = Lib.idxFreeDVKP2abcd(options)
        # Transform to 'DVKP' into 'abcd'
        abcd0 = Lib.DVKP2abcd(DVKP0)
        # Optimize parameters in terms of abcd (larger region of attraction)
        CostBest,abcdBest,Cov_abcd,G1,G2,Gp,exitflag,Phist = Lib.MLEn_check_geometry(abcd0,x,w,U,Cov_m,idxFree,options)
        # Converting the parameters from abcd back to DVKP 
        DVKPBest, Cov_DVKP = Lib.P2DVKP(abcdBest, Cov_abcd)
    elif options['mapping'] == 'DVKP': 
        # Define 'DVKP' in terms of idxFree
        idxFree = Lib.idxFreeDVKP(options) 
        # optimization in terms of DVKP (internally evaluated in [G1,G2,Gp,dG1,dG2,dGp] = MLEn_select_geometry(P,x,omega,options))
        CostBest,DVKPBest,Cov_DVKP,G1,G2,Gp,exitflag,Phist = Lib.MLEn_check_geometry(DVKP0,x,w,U,Cov_m,idxFree,options)
        # Converting the parameters from abcd back to DVKP 
        abcdBest = Lib.DVKP2abcd(DVKPBest)
        abcd0 = Lib.DVKP2abcd(DVKP0)
        #
        dabcd__dDVKP = Lib.dabcd_dDVKP(DVKPBest)
        dDVKP__dabcd = pinv(dabcd__dDVKP) # Safer to program directly like in dabcd_dDVKP (too lazy)
        #
        Cov_abcd = np.dot(dDVKP__dabcd,(np.dot(Cov_DVKP,np.conj(dDVKP__dabcd.T)))) #Cov_abcd = J^-1*Cov_DVKP*J^-H
    #
    return CostBest,DVKPBest,Cov_DVKP,abcdBest,Cov_abcd,abcd0,G1,G2,Gp,exitflag,Phist

def LAS_DV(Y,Freq,Heights):
    #
    Omega = 2 * np.pi * Freq
    #
    amplitude = np.zeros(Y.shape)
    phase = np.zeros(Y.shape)
    #
    for i in range(0,Y.shape[0]):
        amplitude[i] = np.abs(Y[i])
        phase[i] = np.arctan2(-np.imag(Y[i]),np.real(Y[i]))
    #
    for i in range(0,phase.shape[0]-1):
        if phase[i] > phase[i+1]:
            for j in range(i+1,phase.shape[0]):
                phase[j] = phase[j] + 2 * np.pi
    #
    amp_w = amplitude[0]
    phi_w = phase[0]
    for i in range(phase.shape[0]-1,0,-1):
        if phase[i]-phi_w > 2 * np.pi:
            pass
        else:
            amp_s = amplitude[i]
            phi_s = phase[i]
            dx = float(Heights[0]) - float(Heights[i])
            break
    #
    dPhi = phi_s - phi_w
    LAR = -np.log(amp_s/amp_w)
    eta = LAR / dPhi
    #
    k_e = Omega * dx ** 2 / dPhi ** 2 * eta / (1 + eta ** 2)# 4e-6#
    v_t = -Omega * dx / dPhi * (1 - eta ** 2) /(1 + eta ** 2)#-1e-5#
    #
    return k_e,v_t

def LAS_D(Y,Freq,Heights):
#
    Omega = 2 * np.pi * Freq
    #
    amplitude = np.zeros(Y.shape)
    phase = np.zeros(Y.shape)
    #
    for i in range(0,Y.shape[0]):
        amplitude[i] = np.abs(Y[i])
        phase[i] = np.arctan2(-np.imag(Y[i]),np.real(Y[i]))
    #
    for i in range(0,phase.shape[0]-1):
        if phase[i] > phase[i+1]:
            for j in range(i+1,phase.shape[0]):
                phase[j] = phase[j] + 2 * np.pi
    #
    amp_w = amplitude[0]
    phi_w = phase[0]
    for i in range(phase.shape[0]-1,0,-1):
        if phase[i]-phi_w > 2 * np.pi:
            pass
        else:
            amp_s = amplitude[i]
            phi_s = phase[i]
            dx = float(Heights[0]) - float(Heights[i])
            break
    #
    dPhi = phi_s - phi_w
    LAR = -np.log(amp_s/amp_w)
    eta = LAR / dPhi
    #
    k_e = Omega * dx ** 2 / dPhi ** 2 * eta / (1 + eta ** 2)
    v_t = -9999
    #
    return k_e,v_t

def LAS_V(Y,Freq,Heights):
#
    Omega = 2 * np.pi * Freq
    #
    amplitude = np.zeros(Y.shape)
    phase = np.zeros(Y.shape)
    #
    for i in range(0,Y.shape[0]):
        amplitude[i] = np.abs(Y[i])
        phase[i] = np.arctan2(-np.imag(Y[i]),np.real(Y[i]))
    #
    for i in range(0,phase.shape[0]-1):
        if phase[i] > phase[i+1]:
            for j in range(i+1,phase.shape[0]):
                phase[j] = phase[j] + 2 * np.pi
    #
    amp_w = amplitude[0]
    phi_w = phase[0]
    for i in range(phase.shape[0]-1,0,-1):
        if phase[i]-phi_w > 2 * np.pi:
            pass
        else:
            amp_s = amplitude[i]
            phi_s = phase[i]
            dx = float(Heights[0]) - float(Heights[i])
            break
    #
    dPhi = phi_s - phi_w
    LAR = -np.log(amp_s/amp_w)
    eta = LAR / dPhi
    #
    k_e = -9999
    v_t = -Omega * dx / dPhi * (1 - eta ** 2) /(1 + eta ** 2)
    #
    return k_e,v_t

class ParEstMLEn:
    def __init__(self,opts, args):
        #
        self.Sensors = []
        self.Heights =[]
        self.FreqOK = 2#0
        self.RunSP = '-9'
        self.MethodDV = 'DV'
        self.D = 5e-07
        self.V = 6e-06
        self.Method = 'boundaries' # infinite,boundaries
        self.SRNLimit = 0.0
        self.FreqLimit = 5.0
        self.MinMaxSRN = 1  # 0>Max, 1>Min
        self.cw_x_rhow = 4.18e6
        self.c_x_rho = 4.18e6
        self.IniFlag = 1
        self.OutputFolder = '../temp' # Output folder.
        self.InputFolder = '../temp' # Input folder.
        self.Version = False # Flag display version and stop the execution.
#         self.Slider = 1
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
            elif opt in ('-f'):
                self.FreqOK = int(arg)
            elif opt in ('-r'):
                self.RunSP = arg
            elif opt in ('-t'):
                self.MethodDV = arg
            elif opt in ('-d'):
                self.D = float(arg)
            elif opt in ('-v'):
                self.V = float(arg)
            elif opt in ('-m'):
                self.Method = arg
            elif opt in ('-n'):
                self.SRNLimit = float(arg)
            elif opt in ('-l'):
                self.FreqLimit = float(arg)
            elif opt in ('-a'):
                self.MinMaxSRN = int(arg)
            elif opt in ('-x'):
                self.cw_x_rhow = float(arg)
            elif opt in ('-z'):
                self.c_x_rho = float(arg)
            elif opt in ('-i'):
                self.IniFlag = int(arg)
            elif opt in ('-o'):
                self.OutputFolder = arg
            elif opt in ('-b'):
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
#             elif opt in ('-c'):
#                 self.Slider = int(arg)
        return

    def CheckOptions(self):
        print('CheckOptions...')
        try:
            #  
            FlagPreCheck = True
            # Check Options type
            if type(self.RunSP) != str : FlagPreCheck = False
            if type(self.FreqOK) != int : FlagPreCheck = False
            if type(self.MethodDV) != str : FlagPreCheck = False
            if type(self.D) != float : FlagPreCheck = False
            if type(self.V) != float : FlagPreCheck = False
            if type(self.Method) != str : FlagPreCheck = False
            if type(self.SRNLimit) != float : FlagPreCheck = False
            if type(self.FreqLimit) != float : FlagPreCheck = False
            if type(self.MinMaxSRN) != int : FlagPreCheck = False
            if type(self.cw_x_rhow) != float : FlagPreCheck = False
            if type(self.c_x_rho) != float : FlagPreCheck = False
            if type(self.IniFlag) != int : FlagPreCheck = False
            if type(self.OutputFolder) != str: FlagPreCheck = False
            if type(self.InputFolder) != str : FlagPreCheck = False
            if type(self.FlagUpdate) != bool : FlagPreCheck = False
            if type(self.RunUpdate) != str: FlagPreCheck = False
#             if type(self.Slider) != int : FlagPreCheck = False
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
            if self.FreqLimit == 0.0:
                pass
            else:
                self.FreqLimit = self.FreqLimit/24.0/3600.0
            #
            if self.Version:
                print('Version 0.1')
                return False
            #
            return FlagPreCheck
        except:
            return False

    def LoadData(self):
        print('LoadData...')
        try:
            # Load the Time
            self.MobWinTime = (pd.read_pickle(self.InputFolder+'/MobWinTime.pkz',compression='zip'))['Time'].to_numpy()
            # Load the SRN
            with open(self.InputFolder+'/SRN.PdList','rb') as f:
                self.SRNList = pickle.load(f)
            f.close()
            # Load Y
            with open(self.InputFolder+'/Y.PdList','rb') as f:
                self.YList = pickle.load(f)
            f.close()
            # Load Freq
            dfx = pd.read_pickle(self.InputFolder+'/Amplitude.pkz',compression='zip')
            self.Freq = dfx['Freq'].drop_duplicates().to_numpy()
            self.Columns = (dfx.columns.tolist())[2:]
            #
            if self.FlagUpdate:
                pass
            else:
                self.MobWinTimeOld = []
            #
            return True
        except:
            return False

    def Processing(self):
        print('Processing...')
        try:
            Handle = open(self.OutputFolder + '/MLEn2.log','w')
            Handle.close()
            #
            self.Diffusivity = []
            self.Velocity = []
            self.DiffusivityInc = []
            self.VelocityInc = []
            self.Pearson = []
            self.DiffusivityL = []
            self.VelocityL = []
            self.q = []
            self.k = []
            self.qInc = []
            self.kInc = []
            self.PearsonQK = []
            self.Cost = []
            self.Soil = []
            # PreCleaning
            Flags = []
            for item in self.Columns:
                if item in self.Sensors:
                    Flags.append(1)
                else:
                    Flags.append(0)
            # SNRList
            for t in range(0,len(self.SRNList)):
                for i in range(len(Flags)-1,-1,-1):
                    if Flags[i] == 0:
                        self.SRNList[t] = np.delete(self.SRNList[t],i,1)
            # YList
            for t in range(0,len(self.YList)):
                for i in range(len(Flags)-1,-1,-1):
                    if Flags[i] == 0:
                        self.YList[t] = np.delete(self.YList[t],i,1)
            #
            if self.FreqOK == 2:
                if self.FreqLimit == 0.0:
                    PosFreqLim = len(self.Freq)
                else:
                    PosFreqLim = len(self.Freq)
                    for i,item in enumerate(self.Freq):
                        if item > self.FreqLimit:
                            PosFreqLim = i
                            break
            #
            Dini = -9999
            Vini = -9999
            # zSoil = self.Zuser
            # Layers = [float(item) for item in self.Heights]
            #
            for t in range(0,self.MobWinTime.shape[0]):
                print(t,self.MobWinTime.shape[0])
                if self.MobWinTime[t] in self.MobWinTimeOld:
                    pass
                else:
                    item3 = self.MobWinTime[t]
                    Handle = open(self.OutputFolder + '/MLEn.log','a')
                    Handle.write('Time:'+str(item3)+'\n')
                    Handle.close()
                    #
                    Cov_Temp = (np.fromfile(self.OutputFolder+'/'+str(self.MobWinTime[t])+'.CY_m_nt', dtype=complex)).reshape((len(self.Columns),len(self.Columns),self.Freq.shape[0]))
                    #
                    # np.savetxt('Test.csv',Cov_Temp[:,:,0],delimiter=',')
                    for i in range(Cov_Temp.shape[0]-1,-1,-1):
                        if Flags[i] == 0:
                            Cov_Temp = np.delete(Cov_Temp,i,1)
                            Cov_Temp = np.delete(Cov_Temp,i,0)
                    # np.savetxt('Test2.csv',Cov_Temp[:,:,0],delimiter=',')
                    #
                    if np.isnan(Cov_Temp).any():
                        self.Diffusivity.append(np.nan)
                        self.Velocity.append(np.nan)
                        self.DiffusivityInc.append(np.nan)
                        self.VelocityInc.append(np.nan)
                        self.Pearson.append(np.nan)
                        self.q.append(np.nan)
                        self.k.append(np.nan)
                        self.qInc.append(np.nan)
                        self.kInc.append(np.nan)
                        self.PearsonQK.append(np.nan)
                        self.DiffusivityL.append(np.nan)
                        self.VelocityL.append(np.nan)
                        self.Cost.append(np.nan)
                        self.Soil.append(np.nan)
                    else:
                        SNR2 = self.SRNList[t]
                        MaxSNR2Temp = []
                        for item in SNR2:
                            Temp = np.abs(item)
                            if self.MinMaxSRN == 0:
                                pos = np.argmax(Temp)
                                MaxSNR2Temp.append(item[pos])
                            elif  self.MinMaxSRN == 1:
                                pos = np.argmin(Temp)
                                MaxSNR2Temp.append(item[pos])
                        MaxSNR2 = np.array(MaxSNR2Temp)
                        # if self.MinMaxSRN == 0:
                        #     MaxSNR2 = np.max(SNR2, axis=1)
                        # elif  self.MinMaxSRN == 1:
                        #     MaxSNR2 = np.min(SNR2, axis=1)
                        #
                        if self.FreqOK == 0:
                            Y_sel = np.empty((1,len(self.Sensors)), dtype=complex)
                            w_sel = np.empty((1,1), dtype=float)
                            Cov_m_sel = np.empty((len(self.Sensors),len(self.Sensors),1), dtype=complex)
                            #
                            MaxPos = np.argmax(MaxSNR2)
                            Highest = MaxPos
                            w_sel[0,0] = 2*np.pi*self.Freq[MaxPos]
                            Y_sel[0,:] = (self.YList[t])[MaxPos]
                            Cov_m_sel[:,:,0] = Cov_Temp[:,:,MaxPos]
                        elif self.FreqOK == 1:
                            Y_sel = np.empty((5,len(self.Sensors)), dtype=complex)
                            w_sel = np.empty((1,5), dtype=float)
                            Cov_m_sel = np.empty((len(self.Sensors),len(self.Sensors),5), dtype=complex)
                            for i in range(0,5):
                                MaxPos = np.argmax(MaxSNR2)
                                if i == 0:
                                    Highest = MaxPos
                                w_sel[0,i] = 2*np.pi*self.Freq[MaxPos]
                                Y_sel[i,:] = (self.YList[t])[MaxPos]
                                Cov_m_sel[:,:,i] = Cov_Temp[:,:,MaxPos]
                                #
                                MaxSNR2[MaxPos] = np.max(MaxSNR2) - 9999
                        elif self.FreqOK == 2:
                            #
                            occ = MaxSNR2 > self.SRNLimit
                            #
                            occ = occ[0:PosFreqLim]
                            #
                            n = occ.sum()
                            #
                            Y_sel = np.empty((n,len(self.Sensors)), dtype=complex)
                            w_sel = np.empty((1,n), dtype=float)
                            Cov_m_sel = np.empty((len(self.Sensors),len(self.Sensors),n), dtype=complex)
                            #
                            Highest = np.argmax(MaxSNR2)
                            #
                            cont = 0
                            for i,item2 in enumerate(occ):
                                if item2:
                                    w_sel[0,cont] = 2*np.pi*self.Freq[i]
                                    Y_sel[cont,:] = (self.YList[t])[i]
                                    Cov_m_sel[:,:,cont] = Cov_Temp[:,:,i]
                                    cont += 1
                        #
                        pos = np.argmin((self.Freq-(1/24.0/3600.))**2)
                        #
                        if self.IniFlag == 0:
                            if self.MethodDV == 'DV':
                                D,V = LAS_DV((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                # D,V = LAS_DV((self.YList[t])[pos],self.Freq[pos],self.Heights)
                            elif self.MethodDV == 'D':
                                D,V = LAS_D((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                # D,V = LAS_D((self.YList[t])[pos],self.Freq[pos],self.Heights)
                                V = self.V
                            elif self.MethodDV == 'V':
                                D,V = LAS_V((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                # D,V = LAS_V((self.YList[t])[pos],self.Freq[pos],self.Heights)
                                D = self.D
                            self.DiffusivityL.append(D)
                            self.VelocityL.append(V)
                        elif self.IniFlag == 1:
                            if Dini == -9999 or Vini == -9999:
                                if self.MethodDV == 'DV':
                                    # D,V = LAS_DV((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                    D,V = LAS_DV((self.YList[t])[pos],self.Freq[pos],self.Heights)
                                elif self.MethodDV == 'D':
                                    # D,V = LAS_D((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                    D,V = LAS_D((self.YList[t])[pos],self.Freq[pos],self.Heights)
                                    V = self.V
                                elif self.MethodDV == 'V':
                                    # D,V = LAS_V((self.YList[t])[Highest],self.Freq[Highest],self.Heights)
                                    D,V = LAS_V((self.YList[t])[pos],self.Freq[pos],self.Heights)
                                    D = self.D
                                self.DiffusivityL.append(D)
                                self.VelocityL.append(V)
                            else:
                                D = Dini
                                V = Vini
                                self.DiffusivityL.append(np.nan)
                                self.VelocityL.append(np.nan)
                        # Call MLEn
                        DVKP0 = [D,V,0.0,0.0]
                        try:
                            options = {'geometry': 'slab', 'solution': 'analytic', 'estimation': 'MLE', 'parameters': self.MethodDV, 'method': self.Method, 'hist': False}
                            CostBest,DVKPBest,Cov_DVKP,abcdBest,Cov_abcd,abcd0,G1,G2,Gp,exitflag,Phist = MLEn(DVKP0,self.Heights,w_sel,Y_sel,Cov_m_sel,options)
                            #
                            qk, Cvk = Lib.ac2qk(abcdBest, Cov_abcd, self.c_x_rho, self.cw_x_rhow)
                            pearson_qk = Cvk[0,1]/((Cvk[0,0]**0.5)*(Cvk[1,1]**0.5))
                            self.q.append(qk[0])
                            self.k.append(qk[1])
                            self.PearsonQK.append(pearson_qk)
                            #
                            if self.MethodDV == 'DV':
                                self.Diffusivity.append(DVKPBest[0][0])
                                self.Velocity.append(DVKPBest[1][0])
                                Dini = DVKPBest[0][0]
                                Vini = DVKPBest[1][0]
                            else:
                                self.Diffusivity.append(DVKPBest[0])
                                self.Velocity.append(DVKPBest[1])
                                Dini = DVKPBest[0]
                                Vini = DVKPBest[1]
                            #
                            try:
                                pearson = Cov_DVKP[0,1]/(np.dot(np.sqrt(Cov_DVKP[0,0]),np.sqrt(Cov_DVKP[1,1])))
                            except:
                                pearson = -9999
                            BND = 0.95
                            cstd = special.erfinv(BND)*np.sqrt(2)
                            DUnc = cstd*np.sqrt(Cov_DVKP[0,0])
                            VUnc = cstd*np.sqrt(Cov_DVKP[1,1])
                            QUnc = cstd*np.sqrt(Cvk[0,0])
                            KUnc = cstd*np.sqrt(Cvk[1,1])
                            #
                            self.DiffusivityInc.append(DUnc)
                            self.VelocityInc.append(VUnc)
                            self.Pearson.append(pearson)
                            self.qInc.append(QUnc)
                            self.kInc.append(KUnc)
                            self.Cost.append(CostBest)
                        except:
                            self.Diffusivity.append(np.nan)
                            self.Velocity.append(np.nan)
                            self.DiffusivityInc.append(np.nan)
                            self.VelocityInc.append(np.nan)
                            self.Pearson.append(np.nan)
                            self.q.append(np.nan)
                            self.k.append(np.nan)
                            self.qInc.append(np.nan)
                            self.kInc.append(np.nan)
                            self.PearsonQK.append(np.nan)
                            self.Cost.append(np.nan)
            #
            return True
        except:
            return False
            
    def SaveData(self):
        print('SaveData...')
        try:
            #
            df_Diffusivity = pd.DataFrame()
            df_Diffusivity['Time'] = (self.MobWinTime.tolist())
            df_Diffusivity['DifL'] = self.DiffusivityL
            df_Diffusivity['Dif'] = self.Diffusivity
            df_Diffusivity['DifI'] = self.DiffusivityInc
            #
            df_Velocity = pd.DataFrame()
            df_Velocity['Time'] = self.MobWinTime.tolist()
            df_Velocity['VelL'] = self.VelocityL
            df_Velocity['Vel'] = self.Velocity
            df_Velocity['VelI'] = self.VelocityInc
            #
            df_Pearson = pd.DataFrame()
            df_Pearson['Time'] = self.MobWinTime.tolist()
            df_Pearson['Pearson'] = self.Pearson
            #
            df_Q = pd.DataFrame()
            df_Q['Time'] = self.MobWinTime.tolist()
            df_Q['Vel'] = self.q
            df_Q['VelI'] = self.qInc
            #
            df_K = pd.DataFrame()
            df_K['Time'] = self.MobWinTime.tolist()
            df_K['K'] = self.k
            df_K['KI'] = self.kInc
            #
            df_PearsonQ = pd.DataFrame()
            df_PearsonQ['Time'] = self.MobWinTime.tolist()
            df_PearsonQ['Pearson'] = self.PearsonQK
            #
            df_CostBest = pd.DataFrame()
            df_CostBest['Time'] = self.MobWinTime.tolist()
            df_CostBest['Cost'] = self.Cost
            #
            df_Diffusivity.to_pickle(self.OutputFolder + '/Diffusivity.pkz', compression='zip')
            df_Velocity.to_pickle(self.OutputFolder + '/Velocity.pkz', compression='zip')
            df_Pearson.to_pickle(self.OutputFolder + '/Pearson.pkz', compression='zip')
            df_Q.to_pickle(self.OutputFolder + '/Q.pkz', compression='zip')
            df_K.to_pickle(self.OutputFolder + '/K.pkz', compression='zip')
            df_PearsonQ.to_pickle(self.OutputFolder + '/PearsonQ.pkz', compression='zip')
            df_CostBest.to_pickle(self.OutputFolder + '/CostBest.pkz', compression='zip')
            #
            return True
        except:
            return False

if __name__ == '__main__':
    options = sys.argv[1:]
    #
    try:
        opts, args = getopt.getopt(options,'s:h:f:r:t:d:v:m:n:l:z:x:a:i:o:b:c:',['version'])
        #
        StringError = 'No Error'
        MLE = ParEstMLEn(opts, args)
        result = MLE.CheckOptions()
        if result:
            result = MLE.LoadData()
            if result:
                result = MLE.Processing()
                if result:
                    result = MLE.SaveData()
                    if result:
                        # ImportLog
                        HandleRiassunto = open(MLE.OutputFolder+'/XXX.run','w')
                        HandleRiassunto.write('MLEn;Analysis\n')
                        HandleRiassunto.write(str(MLE.RunSP)+';LPMRun\n')
                        HandleRiassunto.write(','.join(MLE.Sensors)+';Sensors\n')
                        HandleRiassunto.write(','.join(MLE.Heights)+';Heights\n')
                        HandleRiassunto.write(str(MLE.FreqOK)+';FreqOK\n')
                        HandleRiassunto.write(str(MLE.MethodDV)+';MethodDV\n')
                        HandleRiassunto.write(str(MLE.D)+';D\n')
                        HandleRiassunto.write(str(MLE.V)+';V\n')
                        HandleRiassunto.write(str(MLE.Method)+';Method\n')
                        HandleRiassunto.write(str(MLE.SRNLimit)+';SRNLimit\n')
                        HandleRiassunto.write(str(MLE.FreqLimit)+';FreqLimit\n')
                        HandleRiassunto.write(str(MLE.MinMaxSRN)+';MinMaxSRN\n')
                        HandleRiassunto.write(str(MLE.cw_x_rhow)+';cw_x_rhow\n')
                        HandleRiassunto.write(str(MLE.c_x_rho)+';c_x_rho\n')
                        HandleRiassunto.write(str(MLE.IniFlag)+';IniFlag\n')
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
        HandleLog = open(MLE.OutputFolder + '/MLEn.log','w')
        HandleLog.write(StringError)
        HandleLog.close()
    except getopt.GetoptError:
        HandleLog = open(MLE.OutputFolder + '/MLEn.log','w')
        HandleLog.write('Options error')
        HandleLog.close()