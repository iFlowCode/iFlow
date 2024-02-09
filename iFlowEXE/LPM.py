import os,sys
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy
import pandas as pd
import numpy as np
import numpy.matlib
import math



def LocalPolyAnal(Data_Y,Data_U,Data_freq,method_transient,method_dof,method_order,method_step,Data_CY):
    ny = Data_Y.shape[0] #! OK
    F = Data_Y.shape[1] #! OK
    # print(ny,F,method_transient,method_dof)
    #
    try:
        if Data_freq.size == 0:
            Data_freq = np.array([t for t in range(1,F+1)]) # TODO verificare
        else:
            Data_freq = Data_freq.T
            Data_freq = Data_freq / np.min(np.diff(Data_freq)) #! OK
    except:
        Data_freq = np.array([t for t in range(1,F+1)]) # TODO verificare
    # print(Data_freq,Data_freq.shape)
    #
    try: #! OK
        if bool(method_order) == False and bool(method_dof) == False and bool(method_transient) == False and bool(method_step) == False:
            method_order = 2 # TODO verificare
            method_dof = 0 # TODO verificare
    except:
        method_order = 2 # TODO verificare
        method_dof = 0 # TODO verificare
    # print(method_order,method_dof)
    #
    try: #! OK
        if method_order == None:
            method_order = 2
    except:
        method_order = 2 #! OK
    # print(method_order)
    #
    try:
        if method_dof == None:
            method_dof = ny
    except:
        method_dof = ny
    # print(method_dof)
    #
    try:
        if method_transient == None:
            method_transient = 1
    except:
        method_transient = 1
    if method_transient != 1: # if method.transient ~= 1
        method_transient = 0
    # print(method_transient)
    #
    try:
        if method_step == None:
            method_step = 1
    except:
        method_step = 1
    # print(method_step)
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
    # print(SelectFreq,SelectFreq.shape)
    # print(Fselect,nu)
    #
    if nu == 1:
        nu1 = nu + 1 # +1 accounts for the transient parameters
    elif nu == 0:
        nu1 = nu # no transient parameters are estimated
    # print(nu1)
    # half the frequency width in DFT samples of the polynomial method
    nn = math.ceil((method_dof + (R + 1) * nu1 - 1) / 2)
    # print(nn)
    # correlation length nonparametric estimates
    CL = 2 * nn
    # print(CL)
    # number of degrees of freedom in the residuals
    qq = 2 * nn + 1 - (R + 1) * nu1
    # print(qq)
    #  degrees of freedom of the covariance estimate
    dof = qq
    # print(dof)
    # Initizlize output array
    # covariance matrices
    CY_n = np.zeros((ny, ny, Fselect), dtype=complex)
    CY_m = np.zeros((ny, ny, Fselect), dtype=complex)
    CY_m_nt = np.zeros((ny, ny, Fselect), dtype=complex)
    # print(CY_n.shape,CY_m.shape,CY_m_nt.shape)
    # sample mean output
    Y_m = np.zeros((ny, Fselect), dtype=complex)
    Y_m_nt = np.zeros((ny, Fselect))
    # print(Y_m.shape,Y_m_nt.shape)
    # plant and noise transient contribution at output
    TY = np.zeros((ny, Fselect), dtype=complex)
    # print(TY.shape)
    # frequency response matrix
    G = np.zeros((ny, nu, Fselect), dtype=complex)
    # print(G.shape)
    # covariance matrix FRM
    if NoiseCov == 0: # no output noise covariance available
        CvecG = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex)
    else: # output noise covariance available
        CvecG_NL = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex) #TODO
        CvecG_n = np.zeros((ny*nu, ny*nu, Fselect), dtype=complex) #TODO
    # print(CvecG.shape)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #% Calculation of the regressor matrix Kn %
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # regressor matrix
    Kn = np.zeros(((R+1)*nu1, 2*nn+1), dtype=complex)
    # print(Kn.shape)
    # intermediate variable
    Power_r = np.ones((R+1, 2*nn+1), dtype=complex)
    # print(Power_r.shape)

    # loop over all frequencies
    fk = 0 # frequency index of the output parameters 
    for kk in range(1,F+1,Fstep):
        fk += 1
        # range of DFT frequencies around kk
        if kk <= nn:
            r_index = np.array([item for item in range(-kk+1,2*nn-kk+1+1,1)], dtype=int)# [-kk+1:1:2*nn-kk+1]
        if (kk >= nn+1) and (kk <= F-nn): #TODO
            # print('QUI1')
            r_index =  np.array([item for item in range(-nn,nn+1,1)], dtype=int) #[-nn:1:nn]
        if kk >= F-nn+1: #TODO
            # print('QUI2')
            r_index = np.array([item for item in range(-2*nn+F-kk,F-kk+1,1)], dtype=int) #[-2*nn+F-kk:1:F-kk]
        # print(kk,r_index)
        # intermediate variable: powers of r
        r_power = []
        # print(kk,kk+r_index)
        for item in ((kk+r_index-1).tolist()):
            r_power.append(Data_freq[item]-Data_freq[kk-1]) # r_power = Data_freq(kk+r_index)-Data_freq(kk)
        r_power = np.array(r_power)
        
        for ii in range(0,R+1):
            for t in range(0,Power_r.shape[1]):
                Power_r[ii][t] = r_power[t] ** (ii) # Power_r(ii,:) = (r_power).^(ii-1)
        # print(kk,r_power)
        # regressor matrix
        if nu > 0  :
            Ukr = []
            for item in ((kk+r_index-1).tolist()):
                Ukr.append(Data_U[0][item]) #Data_U(:, kk+r_index)
            Ukr = np.array(Ukr, dtype=complex)
            # print(Ukr[7],Ukr.shape)
            # if (1) # Speed improvement by Gerd #TODO ?????????????????
            for jj in range(1,2*nn+1+1):
                Kn[0:(R+1)*nu, jj-1] = np.kron(Power_r[:, jj-1], Ukr[jj-1])
            # print(Kn,Kn.shape)
        else:
            print('Qui')
        #     for jj = 1:(R+1) #TODO
        #         for ii=1:nu #TODO
        #             idx=nu*(ii-1)+jj; #TODO
        #             Kn(idx, :) = Power_r(jj, :).*Ukr(ii, :); #TODO


        if transient:
            Kn[(R+1)*nu:,:] = Power_r
            # print(Kn)
        # normalise the rows of Kn for improving the numerical stability of
        # the calculations
        Scale = np.sum(np.abs(Kn**2), axis=1)**0.5 # 2-norm rows Kn
        # print(Scale)
        Scale = np.where(Scale == 0, 1.0, Scale)
#         # FindZeros = find(Scale == 0) # if the input is exactly zero in the band kk-n:kk+n
#         # Scale(FindZeros) = 1 # then the scaling is set equal to one   2*nn+1
        Kn = Kn / np.matlib.repmat(Scale, 2*nn+1, 1).T
        # print(Kn,Kn.shape)
        # numerical stable LS estimate output (= "sample mean")
        Un, SnTemp, Vn = np.linalg.svd(np.conj(Kn.T), full_matrices=False)# svd(Kn', 0) #! Different result between Numpy and Matlab
        Vn = Vn.T #! PYTHON
        Sn = np.diag(SnTemp)
        # print(Vn[0,5],Vn.shape)
        #
        Yn = []
        Help = (kk+r_index-1).tolist()
        Yn = Data_Y[:,Help[0]:Help[-1]+1]
        Yn = np.matmul(Yn, Un)
        Yn = np.matmul(Yn, np.conj(Un.T))
        # print(Yn[2,6],Yn.shape)
        Index_kk = np.where(r_index == 0)
        if len(Index_kk[0]) != 0:
            for item in Index_kk[0].tolist():
                Y_m[:,fk-1] = Yn[:,item]
        # print(Y_m,Y_m.shape)
        # numerical stable LS estimate of the noise covariance matrix (= "sample covariance matrix")
        # print(kk+r_index)
        Help = (kk+r_index-1).tolist()
        En = Data_Y[:,Help[0]:Help[-1]+1] - Yn # LS residuals En = data.Y(:, kk+r_index)*Pn; with Pn = I2n+1 - Qn
        # print(En,En.shape)
#         # print(np.matmul(En,np.conj(En.T)))
        CY_n[:,:,fk-1] = np.matmul(En,np.conj(En.T)) / complex(qq,0)
        # print(CY_n[:,:,1],CY_n.shape)
        # sample covariance of the sample mean
        if len(Index_kk[0]) != 0:
            Help = Index_kk[0].tolist()
        Qnkk = np.matmul(Un[Help[0], :], np.conj(Un[Help[0], :].T))
        # print(Qnkk)
        CY_m[:,:,fk-1] = complex(Qnkk,0) * CY_n[:,:,fk-1]
        # print(CY_m[:,:,0],CY_m.shape)
        if transient or (nu > 0):
            # LS estimate model parameters (Theta matrix)
            ss = np.diag(Sn)
            ss = ss.astype('complex128')
            # print(ss,ss.shape)
            IndexZeros = np.where(ss == 0)
            # print(IndexZeros)
            if len(IndexZeros[0]) != 0:
                for item in IndexZeros[0].tolist():
                    ss[item] = np.inf
            ss = np.diag(1.0/ss)
            # print(ss.dtype)
            # print(Un.dtype)
            # print(Yn.dtype)
            # print(np.conj(Vn.T).dtype)

            Theta = Yn.dot(Un.dot(ss).dot(np.conj(Vn.T))) #! Different result between Numpy and Matlab
            # print(Theta,Theta.shape)
            
        if transient:
            # LS estimate transient contribution at output
            IndexTrans = nu*(R+1)+1 # position transient parameters in Theta matrix
            TY[:, fk-1] = Theta[:, IndexTrans-1] / Scale[IndexTrans-1] # denormalisation parameters 
            # print(TY,TY.shape)
            Y_m_nt = Y_m - TY # output without transient   
            # print(Y_m_nt,Y_m_nt.shape)
            # covariance matrix Ym-TY
            # qkk = Un * Un[Index_kk, :].T
            # bmm = Un * (diag(ss) .* Vn(IndexTrans, :)') / Scale(IndexTrans);  % denormalisation parameters 
            # difference qkk - bmm
            qkk_bmm = Un.dot(np.conj(Un[Index_kk[0][0], :].T) - np.multiply(np.diag(ss),Vn[IndexTrans-1,:].T) / Scale[IndexTrans-1])
            # print(qkk_bmm,qkk_bmm.shape)
            # CY_m_nt[:,:,fk-1] = (np.linalg.norm(qkk_bmm, 2)**2 * CY_n[:,:,fk-1])
            CY_m_nt[:,:,fk-1] = (np.linalg.norm(qkk_bmm, 2)**2) * (CY_n[:,:,fk-1]) #!
            # print(CY_m_nt[:,:,0],CY_m_nt.shape)

        if nu > 0:
            # estimate FRM
            IndexFRM = [t for t in range(1,nu+1)] # position FRM parameters in Theta matrix
            # print((Theta[:, IndexFRM[0]-1]).shape)
            # print(np.matlib.repmat(Scale[IndexFRM[0]-1], ny, 1).shape)
            
            # print((np.divide(Theta[:, IndexFRM[0]-1], np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1))).shape)
            for i in range(0,(Theta[:, IndexFRM[0]-1]).shape[0]):
                G[i, :, fk-1] = (Theta[:, IndexFRM[0]-1])[i] / np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1)[i]
            # print(G.shape)
            # G[:, :, fk-1] = np.divide(Theta[:, IndexFRM[0]-1].T, np.matlib.repmat(Scale[IndexFRM[0]-1].T, ny, 1))
            # print(G[:,:,fk-1],G.shape)

            # # covariance matrix vec(G)
            dimVn = Vn.shape[1]
            # print(kk,dimVn)
            # print((Vn[IndexFRM[0]-1, :]).shape)
            # print(np.matlib.repmat(Scale[IndexFRM[0]-1], 1, dimVn))
            Temp = []
            for t in range(0,(Vn[IndexFRM[0]-1, :]).shape[0]):
                Temp.append(Vn[IndexFRM[0]-1, t] / np.matlib.repmat(Scale[IndexFRM[0]-1], 1, dimVn)[0,t])
            Temp = np.array(Temp, dtype=complex)
            # print(Temp,Temp.shape)
            VV = Temp.dot(ss) # intermediate variable
            # print(VV,VV.shape)
            if NoiseCov == 0:
                # print((VV.dot(np.conj(VV.T))))
                # print((np.conj(VV.dot(np.conj(VV.T)))))
                # print(CY_n[:,:,fk-1])
                CvecG[:, :, fk-1] = np.kron(np.conj(VV.dot(np.conj(VV.T))), CY_n[:,:,fk-1])
            else:
                CvecG_NL[:, :, fk-1] = np.kron(np.conj(VV * np.conj(VV.T)), CY_n[:,:,fk-1])
                CvecG_n[:, :, fk-1] = np.kron(np.conj(VV * np.conj(VV.T)), data_CY[:,:,fk-1])

            # print(CvecG[:,:,0],CvecG.shape)
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