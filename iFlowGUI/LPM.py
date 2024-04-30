import os,sys
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import pandas as pd
import numpy as np
import numpy.matlib
import math
from loguru import logger


def LocalPolyAnal(Data_Y,Data_U,Data_freq,method_transient,method_dof,method_order,method_step,Data_CY):
    ny = Data_Y.shape[0] #! OK
    F = Data_Y.shape[1] #! OK
    #
    try:
        if Data_freq.size == 0:
            Data_freq = np.array([t for t in range(1,F+1)]) # TODO verificare
        else:
            Data_freq = Data_freq.T
            Data_freq = Data_freq / np.min(np.diff(Data_freq)) #! OK
    except:
        Data_freq = np.array([t for t in range(1,F+1)]) # TODO verificare
    #
    try: #! OK
        if bool(method_order) == False and bool(method_dof) == False and bool(method_transient) == False and bool(method_step) == False:
            method_order = 2 # TODO verificare
            method_dof = 0 # TODO verificare
    except:
        method_order = 2 # TODO verificare
        method_dof = 0 # TODO verificare
    #
    try: #! OK
        if method_order == None:
            method_order = 2
    except:
        method_order = 2 #! OK
    #
    try:
        if method_dof == None:
            method_dof = ny
    except:
        method_dof = ny
    #
    try:
        if method_transient == None:
            method_transient = 1
    except:
        method_transient = 1
    if method_transient != 1: # if method.transient ~= 1
        method_transient = 0
    #
    try:
        if method_step == None:
            method_step = 1
    except:
        method_step = 1
    #
    try:
        if Data_U.size == 0:
            Data_U = np.array([], dtype=complex)
    except:
        Data_U = np.array([], dtype=complex)
    #
    try:
        if Data_CY.size == 0:
            Data_CY = np.array([], dtype=complex)
            NoiseCov = 0
        else:
            NoiseCov = 1
    except:
        Data_CY = np.array([], dtype=complex)
        NoiseCov = 0
    #
    R = method_order # order polynomial method
    transient = method_transient # if 1 then transient is estimated (default); otherwise 0
    Fstep = method_step # frequency step
    SelectFreq = np.array([[i+1] for i in range(0,F,Fstep)]) # entries of data.freq at which the output parameters are calculated 
    Fselect = SelectFreq.shape[0] # number of frequencies at which the output parameters are calculated
    nu = Data_U.shape[0] # number of inputs nu
    #
    if nu == 1:
        nu1 = nu + 1 # +1 accounts for the transient parameters
    elif nu == 0:
        nu1 = nu # no transient parameters are estimated
    # half the frequency width in DFT samples of the polynomial method
    nn = math.ceil((method_dof + (R + 1) * nu1 - 1) / 2)
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
    Y_m_nt = np.zeros((ny, Fselect))
    # plant and noise transient contribution at output
    TY = np.zeros((ny, Fselect), dtype=complex)
    # frequency response matrix
    G = np.zeros((ny, nu, Fselect), dtype=complex)
    # covariance matrix FRM
    if NoiseCov == 0: # no output noise covariance available
        CvecG = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex)
    else: # output noise covariance available
        CvecG_NL = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex) #TODO
        CvecG_n = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex) #TODO
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #% Calculation of the regressor matrix Kn %
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # regressor matrix
    Kn = np.zeros(((R+1)*nu1, 2*nn+1), dtype=complex)
    # intermediate variable
    Power_r = np.ones((R+1, 2*nn+1), dtype=complex)
    # loop over all frequencies
    fk = 0 # frequency index of the output parameters 
    for kk in range(1,F+1,Fstep):
        fk += 1
        # range of DFT frequencies around kk
        if kk <= nn:
            r_index = np.array([item for item in range(-kk+1,2*nn-kk+1+1,1)], dtype=int)# [-kk+1:1:2*nn-kk+1]
        if (kk >= nn+1) and (kk <= F-nn): #TODO
            r_index =  np.array([item for item in range(-nn,nn+1,1)], dtype=int) #[-nn:1:nn]
        if kk >= F-nn+1: #TODO
            r_index = np.array([item for item in range(-2*nn+F-kk,F-kk+1,1)], dtype=int) #[-2*nn+F-kk:1:F-kk]
        # intermediate variable: powers of r
        r_power = []
        for item in ((kk+r_index-1).tolist()):
            r_power.append(Data_freq[item]-Data_freq[kk-1]) # r_power = Data_freq(kk+r_index)-Data_freq(kk)
        r_power = np.array(r_power)
        
        for ii in range(0,R+1):
            for t in range(0,Power_r.shape[1]):
                Power_r[ii][t] = r_power[t] ** (ii) # Power_r(ii,:) = (r_power).^(ii-1)
        # regressor matrix
        if nu > 0  :
            Ukr = []
            for item in ((kk+r_index-1).tolist()):
                Ukr.append(Data_U[0][item]) #Data_U(:, kk+r_index)
            Ukr = np.array(Ukr, dtype=complex)
            # if (1) # Speed improvement by Gerd #TODO ?????????????????
            for jj in range(1,2*nn+1+1):
                Kn[0:(R+1)*nu, jj-1] = np.kron(Power_r[:, jj-1], Ukr[jj-1])
        else:
            logger.critical('Qui')
        #     for jj = 1:(R+1) #TODO
        #         for ii=1:nu #TODO
        #             idx=nu*(ii-1)+jj; #TODO
        #             Kn(idx, :) = Power_r(jj, :).*Ukr(ii, :); #TODO


        if transient:
            Kn[(R+1)*nu:,:] = Power_r
        # normalise the rows of Kn for improving the numerical stability of
        # the calculations
        Scale = np.sum(np.abs(Kn**2), axis=1)**0.5 # 2-norm rows Kn
        Scale = np.where(Scale == 0, 1.0, Scale)
#         # FindZeros = find(Scale == 0) # if the input is exactly zero in the band kk-n:kk+n
#         # Scale(FindZeros) = 1 # then the scaling is set equal to one   2*nn+1
        Kn = Kn / np.matlib.repmat(Scale, 2*nn+1, 1).T
        # numerical stable LS estimate output (= "sample mean")
        Un, SnTemp, Vn = np.linalg.svd(np.conj(Kn.T), full_matrices=False)# svd(Kn', 0) #! Different result between Numpy and Matlab
        Vn = Vn.T #! PYTHON
        Sn = np.diag(SnTemp)
        #
        Yn = []
        Help = (kk+r_index-1).tolist()
        Yn = Data_Y[:,Help[0]:Help[-1]+1]
        Yn = np.matmul(Yn, Un)
        Yn = np.matmul(Yn, np.conj(Un.T))
        Index_kk = np.where(r_index == 0)
        if len(Index_kk[0]) != 0:
            for item in Index_kk[0].tolist():
                Y_m[:,fk-1] = Yn[:,item]
        # numerical stable LS estimate of the noise covariance matrix (= "sample covariance matrix")
        Help = (kk+r_index-1).tolist()
        En = Data_Y[:,Help[0]:Help[-1]+1] - Yn # LS residuals En = data.Y(:, kk+r_index)*Pn; with Pn = I2n+1 - Qn
        CY_n[:,:,fk-1] = np.matmul(En,np.conj(En.T)) / complex(qq,0)
        # sample covariance of the sample mean
        if len(Index_kk[0]) != 0:
            Help = Index_kk[0].tolist()
        Qnkk = np.matmul(Un[Help[0], :], np.conj(Un[Help[0], :].T))
        CY_m[:,:,fk-1] = complex(Qnkk,0) * CY_n[:,:,fk-1]
        if transient or (nu > 0):
            # LS estimate model parameters (Theta matrix)
            ss = np.diag(Sn)
            ss = ss.astype('complex128')
            IndexZeros = np.where(ss == 0)
            if len(IndexZeros[0]) != 0:
                for item in IndexZeros[0].tolist():
                    ss[item] = np.inf
            ss = np.diag(1.0/ss)
            Theta = Yn.dot(Un.dot(ss).dot(np.conj(Vn.T))) #! Different result between Numpy and Matlab
        if transient:
            # LS estimate transient contribution at output
            IndexTrans = nu*(R+1)+1 # position transient parameters in Theta matrix
            TY[:, fk-1] = Theta[:, IndexTrans-1] / Scale[IndexTrans-1] # denormalisation parameters
            Y_m_nt = Y_m - TY # output without transient
            # covariance matrix Ym-TY
            # qkk = Un * Un[Index_kk, :].T
            # bmm = Un * (diag(ss) .* Vn(IndexTrans, :)') / Scale(IndexTrans);  % denormalisation parameters 
            # difference qkk - bmm
            qkk_bmm = Un.dot(np.conj(Un[Index_kk[0][0], :].T) - np.multiply(np.diag(ss),Vn[IndexTrans-1,:].T) / Scale[IndexTrans-1])
            # CY_m_nt[:,:,fk-1] = (np.linalg.norm(qkk_bmm, 2)**2 * CY_n[:,:,fk-1])
            CY_m_nt[:,:,fk-1] = (np.linalg.norm(qkk_bmm, 2)**2) * (CY_n[:,:,fk-1]) #!

        if nu > 0:
            # estimate FRM
            IndexFRM = [t for t in range(1,nu+1)] # position FRM parameters in Theta matrix
            for i in range(0,(Theta[:, IndexFRM[0]-1]).shape[0]):
                G[i, :, fk-1] = (Theta[:, IndexFRM[0]-1])[i] / np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1)[i]
            # G[:, :, fk-1] = np.divide(Theta[:, IndexFRM[0]-1].T, np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1))
            # # covariance matrix vec(G)
            dimVn = Vn.shape[1]
            Temp = []
            for t in range(0,(Vn[IndexFRM[0]-1, :]).shape[0]):
                Temp.append(Vn[IndexFRM[0]-1, t] / np.matlib.repmat(Scale[IndexFRM[0]-1], 1, dimVn)[0,t])
            Temp = np.array(Temp, dtype=complex)
            VV = Temp.dot(ss) # intermediate variable
            if NoiseCov == 0:
                CvecG[:, :, fk-1] = np.kron(np.conj(VV.dot(np.conj(VV.T))), CY_n[:,:,fk-1])
            else:
                CvecG_NL[:, :, fk-1] = np.kron(np.conj(VV * np.conj(VV.T)), CY_n[:,:,fk-1])
                CvecG_n[:, :, fk-1] = np.kron(np.conj(VV * np.conj(VV.T)), data_CY[:,:,fk-1])
#
    return CY_n,CY_m,CY_m_nt,Y_m,Y_m_nt,TY,G,CvecG,dof,CL

# Parameters
dt = 360.0

# Read Data
df_Time = pd.read_csv('Tnoise1_0.csv', header=None).to_numpy()
df_Data = pd.read_csv('Tnoise2_0.csv', header=None).to_numpy()
df_DataRef = pd.read_csv('Tnoise3_0.csv', header=None).to_numpy()
print(df_DataRef.shape)


nt = df_Data.shape[0] #! OK
# print(nt)
Fmax = math.floor(nt / 10) #! OK
# print(Fmax)
freq = np.fft.fftfreq(int(nt), dt)
freq =freq[1:Fmax] #! OK
# print(freq[178],freq.shape)
U = np.ones(df_Data.shape, dtype=complex)
U[:] = np.nan
for i in range(0,df_Data.shape[1]):
    U[:,i] = np.fft.fft(df_Data[:,i]) / nt #! Leggere differenze e-15
# print(U[714,3],U.shape)
if df_DataRef.size != 0:
    Uref = (np.fft.fft(df_DataRef) / nt)
    print(Uref.shape)
    Uin = Uref[:,1:Fmax] #! Leggere differenze e-15
    Yin = U[1:Fmax,0:].T #! Leggere differenze e-15
else:
    Uin = U[0,1:Fmax] # TODO
    Yin = U[1:Fmax,0:].T # TODO
# print(Yin[2,217],Yin.shape)
dofLPM = 6

CY_n,CY_m,CY_m_nt,Y_m,Y_m_nt,TY,G,CvecG,dof,CL = LocalPolyAnal(Yin,Uin,freq,1,dofLPM,None,None,np.array([]))

Y = Y_m_nt.T

print(len(freq))
VarF = []
for ii in range(len(freq)-1,-1,-1):
    # print(ii,freq[ii])
    # print(CY_m_nt.shape)
    # print(np.diag(CY_m_nt[:,:,ii]))
    VarF.append(np.diag(CY_m_nt[:,:,ii]))
VarF = np.array(VarF, dtype=float)
# print(VarF)
# print(Y.shape)
# print(np.abs(Y).shape)
# print(np.sqrt(VarF).shape)
rows = Y.shape[0]
cols = Y.shape[1]
SRN = np.zeros((rows,cols), dtype=float)
# print(SRN.shape)
for i in range(0,rows):
    for j in range(0,cols):
        SRN[i,j] = np.abs(Y[i,j]) / np.sqrt(VarF[i,j])
# print(SRN)