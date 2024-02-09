# from black import T
import numpy as np
from numpy.linalg import inv
# import cmath
from scipy.linalg import sqrtm
#
def ac2qk(PBest, CovP, c_x_rho, cw_x_rhow):
    '''
    Conversion parameters [a,c] towards the physical parameters v and k,
    together with the covariance matrix.
    
    Copyright (c) 2015 Uwe Schneidewind, Matthijs van Berkel, Gerd Vandersteen, 
    All rights reserved.
    Software can be used freely for non-commercial applications only. 
    If used in publications please reference
    [1] van Berkel, M., Vandersteen, G., Geerardyn, E., Pintelon, R., Zwart,
        H.J. and de Baar, M. R., 2014. Frequency domain sample maximum likelihood
        estimation for spatially dependent parameter estimation in PDEs,
        Automatica 50(8): 2113 - 2119. DOI: 10.1016/j.automatica.2014.05.027
    [2] Schneidewind, U., van Berkel, M., Anibas, C., Vandersteen, G.,
        Schmidt, C., Joris, I., Seuntjens, P., Batelaan, O., and Zwart, H.J.,
        2016. LPMLE3 - A Novel Method to Quantify Vertical Water Fluxes in
        Streambeds Using Heat as a Tracer, Water Resources Research, 
        DOI:10.1002/2015WR017453'''
    #
    a = PBest[0]
    c = PBest[2]
    qk = [-c_x_rho/cw_x_rhow*2*a/c, c_x_rho/c] # transform parameters
    J = np.array([[-2*c_x_rho/cw_x_rhow/c,c_x_rho/cw_x_rhow*2*a/c**2],
        [0,-c_x_rho/c**2]]) # Calculate Jacobian
    #
    CovPrid = CovP[1:3,1:3] #! ??????????????????????????????????????????????????????????
    Cvk = np.dot(J,np.dot(CovPrid,J.T)) # transform covariance matrix
    #
    return qk, Cvk
#
def G_and_J_G_analytic_slab_abcd(P,x,omega):
    # Calculating G1, G2 and Gp from analytic expressions in slab geometry
    # Theta(xc) = G1 Theta(x1) +  G2 Theta(x1) + Gp Theta_p
    # Model
    a=P[0]
    b=P[1]
    c=P[2]
    d=P[3]
    # mu and position
    x1 = x[0][0] # Measurement positions --x1
    xc = x[0][1] # Measurement positions ---xc---
    x2 = x[0][2] # Measurement positions x2--
    mu = np.sqrt(np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))) # mu (lambda =-a/+mu)
    # Denominator Transfer function (noemer)
    Denom = np.exp(np.dot(2,np.dot(x1,mu)))-np.exp(np.dot(2,np.dot(x2,mu))) #COR
    # Transfer functions
    G1 = np.multiply(np.exp(-np.dot(xc,(a+mu))),((np.exp(np.dot((a+mu),x1)+np.dot(2,np.dot(xc,mu)))-np.exp(np.dot((a+mu),x1)+np.dot(2,np.dot(x2,mu))))))/Denom
    G2 = np.multiply(np.exp(np.dot(-xc,(a+mu))),((np.exp(np.dot((a+mu),x2)+np.dot(2,np.dot(x1,mu)))-np.exp(np.dot((a+mu),x2)+np.dot(2,np.dot(xc,mu))))))/Denom
    Gp = np.multiply(d,np.multiply((1.0/(np.power(a,2)-np.power(mu,2))),(G1+G2-np.ones(omega.shape))))
    # Jacobian
    # Derivatives of mu
    dmuda = np.multiply(a,np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2)))
    dmudb = np.multiply((1/2),np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2)))
    dmudc = np.multiply((complex(0,1)*(1/2)),np.multiply(omega,np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2))))
    # Derivatives of G1
    # The derivatives contain a number of common terms
    ProdG1 = np.exp(np.dot((x1-xc),(a+mu)))/np.power(Denom,2)
    CommonTermG1 = np.dot((np.exp(np.multiply(2,np.dot(mu,(xc+x1))))-np.exp(np.multiply(4,np.multiply(mu,x2)))),(xc-x1))+np.dot((-np.exp(np.dot(2,np.dot(mu,(xc+x2))))+np.exp(np.multiply(2,np.multiply(mu,(x1+x2))))),(xc+x1-np.dot(2,x2)))
    dG1dbc = np.multiply(ProdG1,CommonTermG1)
    dG1da = np.multiply(ProdG1,(np.multiply((np.exp(np.multiply(2,np.multiply(xc,mu)))-np.exp(np.multiply(2,np.multiply(x2,mu)))),np.dot((np.exp(np.multiply(2,np.multiply(x2,mu)))-np.exp(np.multiply(2,np.multiply(x1,mu)))),(xc-x1)))+np.multiply(dmuda,CommonTermG1)))
    dG1db = np.multiply(dmudb,dG1dbc)
    dG1dc = np.multiply(dmudc,dG1dbc)
    dG1dd = np.zeros((dG1dc.shape)) # G1 does not contain d
    # Derivatives of G2
    ProdG2 = np.exp(np.dot((x2-xc),(a+mu)))/np.power(Denom,2)
    CommonTermG2 = np.dot((np.exp(np.multiply(2,np.multiply(mu,(xc+x2))))-np.exp(np.multiply(4,np.multiply(mu,x1)))),(xc-x2))+np.dot((np.exp(np.multiply(2,np.multiply(mu,(x1+x2))))-np.exp(np.multiply(2,np.multiply(mu,(xc+x1))))),(xc+x2-np.dot(2,x1)))
    dG2dbc = np.multiply(ProdG2,CommonTermG2)
    dG2da = np.multiply(ProdG2,(np.multiply((np.exp(np.multiply(2,np.multiply(xc,mu)))-np.exp(np.multiply(2,np.multiply(x1,mu)))),np.dot((np.exp(np.multiply(2,np.multiply(x1,mu)))-np.exp(np.multiply(2,np.multiply(x2,mu)))),(xc-x2)))+np.multiply(dmuda,CommonTermG2)))
    dG2db = np.multiply(dmudb,dG2dbc)
    dG2dc = np.multiply(dmudc,dG2dbc)
    dG2dd = np.zeros((dG2dc.shape)) # G2 does not contain d
    # Derivatives of Gp
    dGpda = np.multiply(d,np.multiply((1/(np.power(a,2)-np.power(mu,2))),(dG1da+dG2da)))
    dGpdb = np.multiply(d,np.multiply((1/(np.power(a,2)-np.power(mu,2))),(dG1db+dG2db)))+np.multiply(d,np.multiply((1/np.power((np.power(a,2)-np.power(mu,2)),2)),(G1+G2-np.ones((omega.shape)))))
    dGpdc = np.multiply(d,np.multiply((1/(np.power(a,2)-np.power(mu,2))),(dG1dc+dG2dc)))+np.multiply(d,np.multiply((np.multiply(complex(0,1),omega)/np.power((np.power(a,2)-np.power(mu,2)),2)),(G1+G2-np.ones((omega.shape)))))
    dGpdd = np.multiply((1/(np.power(a,2)-np.power(mu,2))),(G1+G2-np.ones((omega.shape))))
    # Restructuring the derivatives
    dG1 = np.hstack((dG1da,dG1db,dG1dc,dG1dd))
    dG2 = np.hstack((dG2da,dG2db,dG2dc,dG2dd))
    dGp = np.hstack((dGpda,dGpdb,dGpdc,dGpdd))
    #
    return dGp,dG1,dG2,Gp,G1,G2
#
def G_and_J_G_analytic_slab_abcd_n(P,x,omega):
    # This file extends the constant parameter slab-gemometry to multiple
    # channels.
    if x.shape[1] == 1:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Only one spatial point available, impossible. Check input spatial x vector\n')
        Handle.close()
        return        
    elif x.shape[1] == 2: # semi-infinite solution
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Warning_Not sufficient spatial points switch to semi-infinite domain solution (note this is entirely different solution)\n')
        Handle.close()
        if P(3) != 0:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_This (semi-infinite) analytic solution does not exist for non-zero power (length of x is only two)\n')
            Handle.close()
            return 
        # Note the change in order of [dGp,dG1,dG2,Gp,G1,G2]  ~= [G1,G2,Gp,dG1,dG2,Gp] 
        # Calculate semi-infinite domain
        dGpn,dG1n,dG2n,Gpn,G1n,G2n = G_and_J_G_analytic_slab_abcd_inf(P,x,omega)
        #! G1(0,0,:) = G1n.T # convert to multidimensional format
        #! G2(0,0,:) = G2n.T # convert to multidimensional format
        #! Gp(0,0,:) = Gpn.T # convert to multidimensional format
        #! dG1(0,:,:) = dG1n.T
        #! dG2(0,:,:) = dG2n.T
        #! dGp(0,:,:) = dGpn.T 
    elif x.shape[1] == 3: # standard case for original algorithm
        dGpn,dG1n,dG2n,Gpn,G1n,G2n = G_and_J_G_analytic_slab_abcd(P,x,omega)
        G1  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        G2  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        Gp  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        dG1  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dG2  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dGp  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        G1[0,0,:] = G1n.T # convert to multidimensional format
        G2[0,0,:] = G2n.T # convert to multidimensional format
        Gp[0,0,:] = Gpn.T # convert to multidimensional format
        dG1[0,:,:] = dG1n.T
        dG2[0,:,:] = dG2n.T
        dGp[0,:,:] = dGpn.T       
    else:
        G1  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        G2  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        Gp  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        dG1  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dG2  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dGp  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        for ii in range(x.shape[1]-2,0,-1): # loop over multiple sensors
            ListTemp = x[0].tolist()
            NewList = [np.array([ListTemp[0],ListTemp[ii],ListTemp[-1]])]
            dGpout,dG1out,dG2out,Gpout,G1out,G2out = G_and_J_G_analytic_slab_abcd(P,NewList,omega) # Generates the Transfer function and the Jacobian
            G1[ii-1,0,:] = G1out.T # save in the correct format
            G2[ii-1,0,:] = G2out.T # save in the correct format
            Gp[ii-1,0,:] = Gpout.T # save in the correct format
            dG1[ii-1,:,:] = dG1out.T
            dG2[ii-1,:,:] = dG2out.T
            dGp[ii-1,:,:] = dGpout.T
    #
    return G1,G2,Gp,dG1,dG2,dGp
#
def dabcd_dDVKP(Pdvkp):
    # This function calculates Jacobian from abcd format to DVKP
    D = Pdvkp[0]
    V = Pdvkp[1]
    K = Pdvkp[2]
    P = Pdvkp[3]
    # Calculate partial derivatives
    dadD = -0.5*V/D**2
    dadV = 0.5/D
    dadK = 0
    dadP = 0
    #
    dbdD = -K/D**2
    dbdV = 0
    dbdK = 1/D
    dbdP = 0
    #
    dcdD = -1/D**2
    dcdV = 0
    dcdK = 0
    dcdP = 0
    #
    dddD = -P/D**2
    dddV = 0
    dddK = 0
    dddP = 1/D
    ## d(a,b,c,d)/d(D,V,K,P)
    dabcd__dDVKP = np.zeros((4,4))
    dabcd__dDVKP[0,0] = dadD
    dabcd__dDVKP[0,1] = dadV
    dabcd__dDVKP[0,2] = dadK
    dabcd__dDVKP[0,3] = dadP
    dabcd__dDVKP[1,0] = dbdD
    dabcd__dDVKP[1,1] = dbdV
    dabcd__dDVKP[1,2] = dbdK
    dabcd__dDVKP[1,3] = dbdP
    dabcd__dDVKP[2,0] = dcdD
    dabcd__dDVKP[2,1] = dcdV
    dabcd__dDVKP[2,2] = dcdK
    dabcd__dDVKP[2,3] = dcdP
    dabcd__dDVKP[3,0] = dddD
    dabcd__dDVKP[3,1] = dddV
    dabcd__dDVKP[3,2] = dddK
    dabcd__dDVKP[3,3] = dddP
    #
    return dabcd__dDVKP
#
def idxFreeDVKP(options):
    # Defines idxFree in terms of DVKP
    idxFree=[]
    if 'D' in options['parameters']: # c
        idxFree.append(1)
    #
    if 'V' in options['parameters']: # a
        idxFree.append(2)
    #
    if 'K' in options['parameters']: # b
        idxFree.append(3)
    #
    if 'P' in options['parameters']: # d
        idxFree.append(4)
    #
    if not idxFree:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_no or wrong parameter to be estimated defined\n')
        Handle.close()
        return
    #
    return np.array(idxFree)
#
def P2DVKP(PBest,CovP):
    # Calulate back to real variables
    V_est= 2 * PBest[0] / PBest[2]
    tau_inv_est = PBest[1] / PBest[2]
    Chi_est = 1 / PBest[2]
    P_est = PBest[3] / PBest[2] 
    Help1 = np.vstack((Chi_est,V_est))
    Help2 = np.vstack((Help1,tau_inv_est))
    DVKP = np.vstack((Help2,P_est))

    Mat = np.zeros((4,4))
    Mat[0,2] = -1.0
    Mat[1,0] = 2.0*PBest[2]
    Mat[1,2] = -2.0*PBest[0]
    Mat[2,1] = PBest[2]
    Mat[2,2] = -PBest[1]
    Mat[3,2] = -PBest[3]
    Mat[3,3] = PBest[2]
    Jac = np.dot((1.0/np.power(PBest[2],2)),Mat)
    CovR = np.dot(Jac,np.dot(CovP,np.conj(Jac.T)))
    #
    return DVKP,CovR
#
def dVardtheta_lpmen(G1,G2,Gp,dG1dt,dG2dt,dGpdt,Cov_m,ntheta,options):
    # Calculates the derivative of the variance
    #   [dVardtheta] = dVardtheta_Full(G1,G2,Gp,dG1dt,dG2dt,dGpdt,CY,options)
    nw = G1.shape[2] # number of frequencies
    ny = G1.shape[0] # number of outputs
    Iy = np.identity(ny,dtype=complex) # I matrix number of outputs
    dIy = np.zeros((ny,ny),dtype=complex) # dI/dt = 0 matrix number of outputs
    # based on derivative of definition in Pintelon et al 2012 p 471 eq 12-17
    dVardtheta = np.zeros((ny,ny,nw), dtype=complex)
    for j in range(nw-1,-1,-1):
        Term0 = np.hstack((-dG1dt[:,ntheta-1,j].reshape(dG1dt.shape[0],1),dIy,-dG2dt[:,ntheta-1,j].reshape(dG2dt.shape[0],1),-dGpdt[:,ntheta-1,j].reshape(dGpdt.shape[0],1)))
        Term1 = np.hstack((-G1[:,:,j].reshape(G1.shape[0],1), Iy,-G2[:,:,j].reshape(G2.shape[0],1),-Gp[:,:,j].reshape(Gp.shape[0],1)))
        #
        TermA = np.dot(Term0,(np.dot(Cov_m[:,:,j],(np.conj(Term1.T)))))
        TermB = np.dot(Term1,(np.dot(Cov_m[:,:,j],(np.conj(Term0.T)))))
        #
        dVardtheta[:,:,j] = TermA + TermB
    #
    return dVardtheta
#
def Cost_Func_MLE(G1,G2,Gp,dG1,dG2,dGp,U,Cov_m,options):
    # This code loops over frequency for cost-function and over space for
    # Jacobian consider modifying as over space will be faster
    # multiplication per freq. [-G1y1 1 0  -G2y1 -Gpy1]*[U1, Y1, Y2, U2, Up].'
    #                          [-G1y2 0 1  -G2y2 -Gpy2]
    # as e1 = Y1 - G1y1*U1 - G2y1*U2 - Gpy1*Up
    # as e2 = Y2 - G1y2*U1 - G2y2*U2 - Gpy2*Up
    ## MLE multiple signals
    # Calculate Cost function and its derivatives
    nw = G1.shape[2] # number of frequency points
    ny = G1.shape[0] # number of outputs
    Iy = np.identity(ny, dtype=complex) # I matrix number of outputs
    e = np.zeros((ny,nw), dtype=complex)
    C_e = np.zeros((ny,ny,nw), dtype=complex)
    invC_e = np.zeros((ny,ny,nw), dtype=complex)    #TODO
    sqrtInvC_e = np.zeros((ny,ny,nw), dtype=complex)    #TODO
    Eps_wx = np.zeros((ny,nw), dtype=complex)
    for i in range(nw-1,-1,-1):
        # Calculate numerator of the sqrt cost function
        e[:,i] = np.dot((np.hstack((-G1[:,:,i],Iy,-G2[:,:,i],-Gp[:,:,i]))),U[i,:].T)
        # Calculate variance (based on def. in Pintelon et al 2012 p 471 eq 12-15)
        C_e[:,:,i] = np.dot(np.hstack((-G1[:,:,i],Iy,-G2[:,:,i],-Gp[:,:,i])),(np.dot(Cov_m[:,:,i],np.conj(np.hstack((-G1[:,:,i],Iy,-G2[:,:,i],-Gp[:,:,i])).T))))
        #
        # C_e = np.real(C_e) # suppress numerical errors #!Removed in last version by Ricky
        # Calculate inverse of C_e
        # invC_e[:,:,i] = inv(np.real(C_e[:,:,i]))
        invC_e[:,:,i] = inv(C_e[:,:,i])
        # Calculate square root of matrix
        sqrtInvC_e[:,:,i] = sqrtm(invC_e[:,:,i])
        # Calculate eps based on (12-28)
        Eps_wx[:,i] = np.dot(sqrtInvC_e[:,:,i],(e[:,i]))
    # Calculate Jacobian
    dimU = U.shape
    dimUr = dimU[1] - 1
    # Can be implemented more efficiently
    dUda = np.zeros((dimU[0],dimU[1]-3), dtype=complex)
    dUdb = np.zeros((dimU[0],dimU[1]-3), dtype=complex)
    dUdc = np.zeros((dimU[0],dimU[1]-3), dtype=complex)
    dUdp = np.zeros((dimU[0],dimU[1]-3))
    for j in range(dimU[1]-3,0,-1): 
        dUda[:,j-1] = np.multiply(np.squeeze(dG1[j-1,0,:]),U[:,0]) + np.multiply(np.squeeze(dG2[j-1,0,:]),U[:,dimUr-1]) + np.multiply(np.squeeze(dGp[j-1,0,:]),U[:,dimU[1]-1])
        dUdb[:,j-1] = np.multiply(np.squeeze(dG1[j-1,1,:]),U[:,0]) + np.multiply(np.squeeze(dG2[j-1,1,:]),U[:,dimUr-1]) + np.multiply(np.squeeze(dGp[j-1,1,:]),U[:,dimU[1]-1])
        dUdc[:,j-1] = np.multiply(np.squeeze(dG1[j-1,2,:]),U[:,0]) + np.multiply(np.squeeze(dG2[j-1,2,:]),U[:,dimUr-1]) + np.multiply(np.squeeze(dGp[j-1,2,:]),U[:,dimU[1]-1])
        dUdp[:,j-1] = np.real(np.multiply(np.squeeze(dG1[j-1,3,:]),U[:,0]) + np.multiply(np.squeeze(dG2[j-1,3,:]),U[:,dimUr-1]) + np.multiply(np.squeeze(dGp[j-1,3,:]),U[:,dimU[1]-1]))
    # Derivatives Variance uncertainty
    dC_a = dVardtheta_lpmen(G1,G2,Gp,dG1,dG2,dGp,Cov_m,1,options)
    dC_b = dVardtheta_lpmen(G1,G2,Gp,dG1,dG2,dGp,Cov_m,2,options)
    dC_c = dVardtheta_lpmen(G1,G2,Gp,dG1,dG2,dGp,Cov_m,3,options)
    dC_p = dVardtheta_lpmen(G1,G2,Gp,dG1,dG2,dGp,Cov_m,4,options)
    #
    dEpsda_wx = np.zeros((dimU[1]-3,dimU[0]), dtype=complex)
    dEpsdb_wx = np.zeros((dimU[1]-3,dimU[0]), dtype=complex)
    dEpsdc_wx = np.zeros((dimU[1]-3,dimU[0]), dtype=complex)
    dEpsdp_wx = np.zeros((dimU[1]-3,dimU[0]), dtype=complex)
    for j in range(nw-1,-1,-1):
        # Calculate numerator of the sqrt cost function (note -sign in dUda due
        # to de/dtheta = -dUdt
        # dEpsda_wx[:,j] = np.dot(np.sqrt(invC_e[:,:,j].astype(complex)),-dUda[j,:].T-0.5*np.dot(dC_a[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        # dEpsdb_wx[:,j] = np.dot(np.sqrt(invC_e[:,:,j].astype(complex)),-dUdb[j,:].T-0.5*np.dot(dC_b[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        # dEpsdc_wx[:,j] = np.dot(np.sqrt(invC_e[:,:,j].astype(complex)),-dUdc[j,:].T-0.5*np.dot(dC_c[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        # dEpsdp_wx[:,j] = np.dot(np.sqrt(invC_e[:,:,j].astype(complex)),-dUdp[j,:].T-0.5*np.dot(dC_p[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        dEpsda_wx[:,j] = np.dot(sqrtInvC_e[:,:,j],-dUda[j,:].T-0.5*np.dot(dC_a[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        dEpsdb_wx[:,j] = np.dot(sqrtInvC_e[:,:,j],-dUdb[j,:].T-0.5*np.dot(dC_b[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        dEpsdc_wx[:,j] = np.dot(sqrtInvC_e[:,:,j],-dUdc[j,:].T-0.5*np.dot(dC_c[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
        dEpsdp_wx[:,j] = np.dot(sqrtInvC_e[:,:,j],-dUdp[j,:].T-0.5*np.dot(dC_p[:,:,j],(np.dot(invC_e[:,:,j].astype(complex),e[:,j]))))
    # Sum over spatial outputs to construct final cost-function
    # Vectorize
    Eps = np.zeros((Eps_wx.shape[0]*Eps_wx.shape[1]), dtype=complex)
    dEpsda = np.zeros((dEpsda_wx.shape[0]*dEpsda_wx.shape[1]), dtype=complex)
    dEpsdb = np.zeros((dEpsdb_wx.shape[0]*dEpsdb_wx.shape[1]), dtype=complex)
    dEpsdc = np.zeros((dEpsdc_wx.shape[0]*dEpsdc_wx.shape[1]), dtype=complex)
    dEpsdp = np.zeros((dEpsdp_wx.shape[0]*dEpsdp_wx.shape[1]), dtype=complex)
    cont = 0
    for i in range(0,Eps_wx.shape[1]):
        for j in range(0,Eps_wx.shape[0]):
            Eps[cont] = Eps_wx[j,i]
            dEpsda[cont] = dEpsda_wx[j,i]
            dEpsdb[cont] = dEpsdb_wx[j,i]
            dEpsdc[cont] = dEpsdc_wx[j,i]
            dEpsdp[cont] = dEpsdp_wx[j,i]
            cont += 1
    # Eps = np.reshape(Eps_wx,(Eps_wx.shape[0]*Eps_wx.shape[1],1))
    # Sum over space and enforce real values
    # dEpsda = dEpsda_wx.sum(axis=0)
    # dEpsdb = dEpsdb_wx.sum(axis=0)
    # dEpsdc = dEpsdc_wx.sum(axis=0)
    # dEpsdp = dEpsdp_wx.sum(axis=0)
    #
    return Eps,dEpsda,dEpsdb,dEpsdc,dEpsdp
#
def G_and_J_G_analytic_slab_abcd_inf(P,x,omega):
    # Model
    a = P[0]
    b = P[1]
    c = P[2] # return to original parameter set
    # mu and position
    x1 = x[0]
    x2 = x[1]
    dx = np.abs(x2-x1) # Measurement positions --x1--x2-- #! add abs for distance
    mu = np.zeros((omega.shape), dtype=complex)
    H = np.zeros((omega.shape), dtype=complex)
    dmuda = np.zeros((omega.shape), dtype=complex)
    dmudb = np.zeros((omega.shape), dtype=complex)
    dmudc = np.zeros((omega.shape), dtype=complex)
    dHda = np.zeros((omega.shape), dtype=complex)
    dHdb = np.zeros((omega.shape), dtype=complex)
    dHdc = np.zeros((omega.shape), dtype=complex)
    mu = np.sqrt(np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega)))
    H = np.exp(np.dot((-a-mu),dx))
    # H = H(:) #! ?????????????????????????????????????????
    # Jacobian
    # Derivatives of mu
    dmuda = np.multiply(a,np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2)))
    dmudb = np.multiply((1/2),np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2)))
    dmudc = np.multiply((complex(0,1)*(1/2)),np.multiply(omega,np.power((np.power(a,2)+b+np.multiply(complex(0,1),np.multiply(c,omega))),(-1/2))))
    # Derivatives of H
    dHda = np.multiply((-1-dmuda),np.multiply(dx,H))
    dHdb = np.multiply(-dmudb,np.multiply(dx,H))
    dHdc = np.multiply(-dmudc,np.multiply(dx,H))
    dHdd = np.zeros((dHda.shape))
    # Output generation
    G1 = np.copy(H) # semi-infinite domain hence Y = G1 U(left) + G2 (U(right) = 0) 
    G0 = np.zeros(H.shape, dtype = complex)
    G2 = np.copy(G0)
    Gp = np.copy(G0) # are all zero;
    # Jacobian
    dG1 = np.hstack((dHda,dHdb,dHdc,dHdd))
    dG2 = np.zeros(dG1.shape, dtype = complex)
    dGp = np.zeros(dG1.shape, dtype = complex)
    #
    return dGp,dG1,dG2,Gp,G1,G2
#
def G_and_J_G_analytic_slab_inf_n(P,x,omega):
    # This file extends the constant parameter slab-gemometry to multiple
    # channels.
    if x.shape[1] == 1 or x.shape[1] == 2:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Only one spatial point available, impossible. Check input spatial x vector\n')
        Handle.close()
        return
    elif x.shape[1] == 3: # semi-infinite solution
        if P[3] != 0: # should not be called upon
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_This (semi-infinite) analytic solution does not exist for non-zero power\n')
            Handle.close()
            return
        # Note the change in order of [dGp,dG1,dG2,Gp,G1,G2]  ~= [G1,G2,Gp,dG1,dG2,Gp] 
        # Calculate semi-infinite domain
        G1  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        G2  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        Gp  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        dG1  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dG2  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dGp  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dGpn,dG1n,dG2n,Gpn,G1n,G2n = G_and_J_G_analytic_slab_abcd_inf(P,[x[0,0],x[0,1],x[0,2]],omega)
        G1[0,0,:] = G1n.T
        G2[0,0,:] = G2n.T
        Gp[0,0,:] = Gpn.T # convert to multidimensional format
        dG1[0,:,:] = dG1n.T
        dG2[0,:,:] = dG2n.T
        dGp[0,:,:] = dGpn.T
    else:
        G1  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        G2  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        Gp  = np.zeros((x.shape[1]-2,1,omega.shape[0]), dtype = complex)
        dG1  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dG2  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        dGp  = np.zeros((x.shape[1]-2,4,omega.shape[0]), dtype = complex)
        for i in range(x.shape[1]-2,0,-1): # loop over multiple sensors
            dGpout,dG1out,dG2out,Gpout,G1out,G2out = G_and_J_G_analytic_slab_abcd_inf(P,[x[0,0],x[0,i]],omega) # Generates the Transfer function and the Jacobian
            G1[i-1,0,:] = G1out.T # save in the correct format
            G2[i-1,0,:] = G2out.T # save in the correct format
            Gp[i-1,0,:] = Gpout.T # save in the correct format
            dG1[i-1,:,:] = dG1out.T
            dG2[i-1,:,:] = dG2out.T
            dGp[i-1,:,:] = dGpout.T
    #               
    return G1,G2,Gp,dG1,dG2,dGp
#
def MLEn_select_geometry(P,x,omega,options):
    # Select which geometry to be used, what kind of method, solution used:
    # semi-infinite solutions
    #        
    if options['method'] == 'infinite': # semi-infinite case
        if options['geometry'] == 'slab': # Analytic solutions check which geometry
            G1,G2,Gp,dG1,dG2,dGp = G_and_J_G_analytic_slab_inf_n(P,x,omega)
        elif options['geometry'] == 'cyl':
            print('Ciccio')
            pass
#!            [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_cyl_inf_n(P,x,omega)
    # source-less solutions
    #        
    elif options['method'] == 'boundaries': # source-less domains
        if options['solution'] == 'numeric': # Numeric solutions geometry is encompased in the state-space matrices
            print('Ciccio')
            pass
#!                [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_num_bothgeom_abcd(P,omega,options) # Generates the Transfer function and the Jacobian
        elif options['solution'] == 'analytic': # Select geometry        
            if options['geometry'] == 'slab': # Analytic solutions check which geometry
                G1,G2,Gp,dG1,dG2,dGp = G_and_J_G_analytic_slab_abcd_n(P,x,omega)
            elif options['geometry'] == 'cyl':
                print('Ciccio')
                pass
#!                [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_cyl_abcd_n(P,x,omega)
            # Special case for cylindrical coordinates (should only be called by users knowing what they are doing)
        elif options['solution'] == 'analyticJY': # suffers often from numerical errors
            print('Ciccio')
            pass
#!            [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_cyl_abcdJY(P,x,omega)
    # including source solutions
    #        
    elif options['method'] == 'source': # source-less domains            
        if options['solution'] == 'numeric': # Numeric solutions geometry is encompased in the state-space matrices
            print('Ciccio')
            pass
#!            [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_num_bothgeom_abcd(P,omega,options);# Generates the Transfer function and the Jacobian
        elif options['solution'] == 'analytic':
            # Select geometry        
            if options['geometry'] == 'slab': # Analytic solutions check which geometry
                print('Ciccio')
                pass
#!                [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_slab_abcd_n(P,x,omega)
            if options['geometry'] == 'cyl':
                print('Ciccio')
                pass
#!                [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_cyl_abcd_n(P,x,omega)
            # Special case for cylindrical coordinates (should only be called by users knowing what they are doing)
        elif options['solution'] == 'analyticJY': # suffers often from numerical errors
            print('Ciccio')
            pass
#!            [G1,G2,Gp,dG1,dG2,dGp] = G_and_J_G_analytic_cyl_abcdJY(P,x,omega)
    #
    return G1,G2,Gp,dG1,dG2,dGp
#
def MLEn_cost(P,x,omega,U,Cov_m,options):
    ''' Computation of the ML cost function for following model
            P is vector of coefficients P = [a,b,c] (real-valued)
            x positions of the measurement [m]
            omega is the frequency vector [rad/s]
            U real measurements temperature (frequency dependent)
            Cov_m is the covariance matrix
            options
        Copyright (c) 2020 Matthijs van Berkel
        All rights reserved.
        Software can be used freely for non-commercial applications only. 
        If used in publications please reference 
        [1] van Berkel, M., Vandersteen, G., Geerardyn, E., Pintelon, R., Zwart, H.J. and de Baar, M. R., 2014. Frequency domain sample maximum likelihood estimation for spatially dependent parameter estimation in PDEs, Automatica 50(8): 2113 ï¿½ 2119. DOI: 10.1016/j.automatica.2014.05.027
    '''
    # Call the transfer functions for the different geometries
    # Select what kind of mapping is used
    if options['mapping'] == 'abcd':
        G1,G2,Gp,dG1,dG2,dGp = MLEn_select_geometry(P,x,omega,options)
    elif options['mapping'] == 'DVKP':
        # transform to DVKP (note that P can be propagated in DVKP format)
        Pabcd = DVKP2abcd(P)
        G1,G2,Gp,dG1,dG2,dGp = MLEn_select_geometry(Pabcd,x,omega,options)
    # Construction of cost function optimization (uses always same structure)  
    #       
    # Choose Least Square Estimator or Maximum Likelihood Estimator
    if options['estimation'] == 'LSE':
        print('Ciccio')
        pass
#!        Eps,dEpsda,dEpsdb,dEpsdc,dEpsdp = Cost_Func_LSE(G1,G2,Gp,dG1,dG2,dGp,U) # Generates cost and Jacobian of cost for LSE
    elif options['estimation'] == 'WLSE':
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_The options.estimation = WLSE has not been implemented\n')
        Handle.close()
    elif options['estimation'] == 'MLE':
        Eps,dEpsda,dEpsdb,dEpsdc,dEpsdp = Cost_Func_MLE(G1,G2,Gp,dG1,dG2,dGp,U,Cov_m,options)  # Generates cost and Jacobian of cost for MLE
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Warning_No type of estimator chosen options.estimation = LSE or WLSE or MLE default choice MLE\n')
        Handle.close()
    # Output cost-function
    e = Eps[:] # Cost function
    # Output Jacobian
    J = np.zeros((dEpsdp.shape[0],4), dtype = complex)
    J[:,3] = dEpsdp[:] # Calculate Jacobian for d
    J[:,2] = dEpsdc[:] # Calculate Jacobian for c
    J[:,1] = dEpsdb[:] # Calculate Jacobian for b
    J[:,0] = dEpsda[:] # Calculate Jacobian for a
    
    # Transform Jacobian if in DVKP form
    if options['mapping'] == 'DVKP':
        dabcd__dDVKP = dabcd_dDVKP(P) # calculate derivative matrix
        J = np.dot(J,dabcd__dDVKP) # Transform matrix
    #
    return e,J,G1,G2,Gp
#
def MLEn_optimization(PBest,x,omega,U,Cov_m,idxFree,options):

    '''Copyright (c) 2015 Matthijs van Berkel, Gerd Vandersteen
    All rights reserved.
    Software can be used freely for non-commercial applications only. 
    If used in publications please reference 
    [1] van Berkel, M., Vandersteen, G., Geerardyn, E., Pintelon, R., Zwart, H.J. and de Baar, M. R., 2014. Frequency domain sample maximum likelihood estimation for spatially dependent parameter estimation in PDEs, Automatica 50(8): 2113 ??? 2119. DOI: 10.1016/j.automatica.2014.05.027
    '''
    # Compute the MLE error vector and the Jacobian matrix
    # if (nargin < 7) #?
    #     idxFree=[]; #?
    # end #?
    # if isempty(idxFree)#?
    #     idxFree = 1:length(PBest);#?
    # end#?
    e,J,G1,G2,Gp = MLEn_cost(PBest,x,omega,U,Cov_m,options)
    #
    CostBest = np.real(np.dot(np.conj(e.T),e))
    lambda0 = np.linalg.norm(J)
    counter = 0
    Xlambda = 0 #Ex lambda... name forbiden in Python
    # PList = PBest;# New line added to track list of P

    Phist = []
    Phist.append(PBest) # Track P #!
    infeasibleStep = False #!

    idxFree = np.array(idxFree) - 1
    while ((counter < options['maxNbfOfSteps']) and (Xlambda < 1e10*lambda0)) and (infeasibleStep == False):
        # While the cost in decreasing, perform a Newton-Gauss
        # optimization step.
        counter = counter + 1
        # Compute the necessary step.
        if (Xlambda != 0):
            # Levenberg-Marquart
            Help0 = np.dot(Xlambda,np.identity(len(idxFree)))
            Help5 = np.zeros((len(idxFree),1), dtype=complex)
            Help1 = np.vstack((np.real(J[:,idxFree]),np.imag(J[:,idxFree])))
            Help2 = np.vstack((Help1,Help0))
            Help3 = np.vstack((np.real(e[:,None]),np.imag(e[:,None])))
            Help4 = np.vstack((Help3,Help5))
            dP = - np.linalg.pinv(Help2).dot(Help4)
        else:
            # Gauss-Newton.
            Help1 = np.vstack((np.real(J[:,idxFree]),np.imag(J[:,idxFree])))
            Help2 = np.vstack((np.real(e[:,None]),np.imag(e[:,None])))
            dP = - np.linalg.pinv(Help1).dot(Help2)
        #!
        if (np.any(np.isinf(dP))) or (np.any(np.isnan(dP))):
            infeasibleStep = True
            # warning(['The next optimization step is infeasible. '...             'Try again with a different initial point or parameter mapping. '])
        else:
            PNew = np.copy(PBest)
            cont = 0
            for i in idxFree:
                PNew[i] = PBest[i] + dP[cont][0]
                cont +=1

            if options['hist']: # Track P
                Phist.append(PNew)
            # Evaluate the new optimized point.
            eNew,JNew,G1,G2,Gp = MLEn_cost(PNew,x,omega,U,Cov_m,options)
            # NewCost = real(NewJ(:,end)'*NewJ(:,end));
            CostNew = np.real(np.conj(eNew.T).dot(eNew))    
            # If the step is succesful: take the step and decrease lambda
            if (CostNew < CostBest):
                J = JNew
                e = eNew
                PBest = PNew
                CostBest = CostNew
                Xlambda = Xlambda / 3
                G1Best = G1
                G2Best = G2
                GpBest = Gp
            else:
                # If the step is not succesful: use lamdba to controle the stepsize
                if (Xlambda == 0):
                    Xlambda0 = np.linalg.norm(JNew)
                    Xlambda = Xlambda0
                else:
                    Xlambda = Xlambda * 10
    Help1 = np.real(J[:,idxFree])
    Help2 = np.imag(J[:,idxFree])
    J_RI = np.vstack((Help1,Help2)) # select only varied parameters
    CovP = np.zeros((len(PBest),len(PBest)))
    Help = 0.5*inv(np.conj(J_RI.T).dot(J_RI))
    for i in range(0,len(idxFree)):
        for j in range(0,len(idxFree)):
            CovP[idxFree[i],idxFree[j]] = Help[i,j]
    #
    if not options['hist']: # only initial and final value of P if not tracked
        Phist.append(PBest)

    # determine exitflag
    if infeasibleStep:
        exitflag = -1
    elif counter >= options['maxNbfOfSteps']:
        exitflag = 0
    elif Xlambda >= 1e10*lambda0:
        exitflag = 1
    else:
        exitflag = 99

    return PBest, CostBest, CovP,G1Best,G2Best,GpBest,exitflag,Phist
#
def MLEn_check_geometry(P0,x,omega,U,Cov_m,idxFree,options):
    # [CostBest,PBest,CovP] = MLEn_check_geometry(P0,x,omega,U,VarCovar,idxFree,options)
    #   SET GEOMETRY AND PREDEFINE STRUCTURES
    # slab
    if options['geometry'] == 'slab':
        # choose calculation method
        if options['solution'] == 'analytic':
            pass
        elif options['solution'] == 'numeric':
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_not implemented options in FDSL slab, choose either numeric or analytic\n')
            Handle.close()
            return
# #!            # [~,~,~,~,options] = FDSL_diriclet(1,1,1,1,x,options); # generate static state-space matrices 
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_no calculation method selected in slab choose either numeric or analytic\n')
            Handle.close()
            return
    # cylindrical
    elif options['geometry']  == 'cyl':
        # analytic solutions cannot deal with non-zero convective V contributions
        if (P0[0] != 0.0 and options['solution'] !='numeric' and options['mapping'] == 'abcd') or (P0[1] != 0.0 and options['solution'] !='numeric' and options['mapping'] == 'DVKP'):
            options['solution'] = 'numeric'
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_V is non-zero in cylindrical domain (convection) switch to numerical solution\n')
            Handle.close()
        # choose calculation method
        if options['solution'] == 'analyticJY': # see lower level 
            pass
        elif options['solution'] == 'analytic': # see lower level
            pass
        elif options['solution'] == 'numeric':
            print('Ciccio')
            pass
#!            #[~,~,~,~,options] = FDCL_diriclet(1,1,1,1,x,options); # generate static state-space matrices (1,1,1,1) 
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_no calculation method selected in cyl, choose either numeric,analytic,  or analyticJY\n')
            Handle.close()
            return
    # no geometry
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_no geometry selected or incorrect geometry selected choose either slab or cyl\n')
        Handle.close()
        return
    # start optimization
    PBest,CostBest,CovP,G1,G2,Gp,exitflag,Phist = MLEn_optimization(P0,x,omega,U,Cov_m,idxFree,options) # Estimates parameters for each sub-domain
    return CostBest,PBest,CovP,G1,G2,Gp,exitflag,Phist
#
def DVKP2abcd(DVKP0_):
    #
    P3 = 1.0 / DVKP0_[0]
    abcd = [P3 * 0.5 * DVKP0_[1],P3 * DVKP0_[2],P3,P3 * DVKP0_[3]]
    #
    return np.array(abcd)
#
def idxFreeDVKP2abcd(options):
    # Defines idxFree in terms of DVKP
    idxFree=[]
    if 'V' in options['parameters']: # a
        idxFree.append(1)
    if 'K' in options['parameters']: # b
        idxFree.append(2)
    if 'D' in options['parameters']: # c
        idxFree.append(3)
    if 'P' in options['parameters']: # d
        idxFree.append(4)
    if not idxFree:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_no or wrong parameter to be estimated defined\n')
        Handle.close()
        return
    #
    return np.array(idxFree)
#
def MLEn_check_partially_fixed_divisions(DVKP0_,options):
    '''[options] = MLE3P_check_fixed_devisions(DVKP0,estimate,options)
    In case a parameter set is optimized where some parameters are fixed to non-zero
    values (V, K, P) and where the diffusion coefficient (D) is free to be estimated 
    the 'abcd' parameter-set results in errors. The reason is that all parameters 
    are divided by the diffusion coefficient and start to move
    Hence, the estimation is better performed in 'DVKP' which does not 
    suffer from this problem. This function checks if
    this is the case and if yes switches the optimization procedure from
    'abcd' to 'DVKP'
    '''
    if ('D' in options['parameters'] and options['mapping'] == 'abcd') and (('V' not in options['parameters'] and DVKP0_[1] != 0.0 ) or ('K' not in options['parameters'] and DVKP0_[2] != 0.0) or ('P' not in options['parameters'] and DVKP0_[3] != 0.0)):
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Warning_switched to optimization in terms of DVKP parameter set instead of abcd in options.parametersetoptimize to avoid errors due to constants in estimates\n')
        Handle.close()
        options['mapping'] = 'DVKP' # set DVKP
    return options
#%%
def MLEn_check_input(DVKP0,x,w,U,Cov_m,options):
    # This file checks input format of information and transforms it to a
    # standard output format
    # Check input dimensions)
    # Frequencies and spatial coordinates
    nw = w.shape[1] # number of frequencies
    nx = x.shape[1] # number of spatial measurements
    # Fourier coefficients 
    nu1 = U.shape[0] # number of input frequencies
    nu2 = U.shape[1] # number of inputs
    # Covariance matrix
    ncov1 = Cov_m.shape[0] # number of inputs
    ncov2 = Cov_m.shape[1] # number of inputs
    ncov3 = Cov_m.shape[2] # number of input frequencies
    npt = len(DVKP0) # number of parameters
    # Checks the different input formats
    # Check if proper input is generated
    if options['method'] == 'infinite' or options['method'] == 'boundaries':
        if options['parameters'] == 'P':
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_options.method = contains P, P cannot be estimated for options.method = infinite or options.method = boundaries\n')
            Handle.close()
            return
    elif options['method'] == 'source':
        if options['parameters'] == 'P' and DVKP0[3] == 0.0: # P is being estimated
            pass
        elif options['parameters'] == 'P' and DVKP0[3] != 0.0: # P is being estimated and is non-zero
            pass
        elif options['parameters'] != 'P' and DVKP0[3] != 0.0: # P is not being estimated but is non-zero
            pass
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_source is set to zero and is not varied, defacto this is the options.method = boundaries case\n')
            Handle.close()
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_incorrect or undefined options.method: choose from infinite, boundaries, source\n')
        Handle.close()
        return
    # Check that there are not too many dimensions
    if len(U.shape) > 2:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: too many input dimensions U = [number of frequencies x number of inputs]\n')
        Handle.close()
        return
    elif len(Cov_m.shape) > 3: # should not exist
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: too many input dimensions Cov_m =  [number of inputs x number of inputs x number of frequencies]\n')
        Handle.close()
        return
    # Verify if frequency dimensions match
    if nw != nu1:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: number of frequencies (omega) does not match input dimensions U = [number of frequencies x number of inputs]\n')
        Handle.close()
        return
    elif nw != ncov3  and options['estimation'] == 'MLE':
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: number of frequencies (omega) does not match input dimensions Cov_m =  [number of inputs x number of inputs x number of frequencies]\n')
        Handle.close()
        return
    elif nu1 != ncov3 and options['estimation'] == 'MLE':
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: number of frequencies input dimensions U = [number of frequencies x number of inputs] does not match input dimensions Cov_m =  [number of inputs x number of inputs x number of frequencies]\n')
        Handle.close()
        return
    #  Verify if initial guess is correct length
    if npt == 1:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Warning_Only initial guess for ''D'' is given the rest will be set to zero DVKP0 = [D,0,0,(0)]\n')
        Handle.close()
    elif npt == 2:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Warning_Only initial guess for [D,V] is given the rest will be set to zero DVKP0 = [D,V,0,(0)]\n')
        Handle.close()
    elif npt == 3:
        if options['method'] == 'infinite' or options['method'] == 'boundaries': # correct choice
            pass
        else: 
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_Only initial guess for ''[D,V,K]'' is given the rest will be set to zero inclusive P, DVKP0 = [D,V,K,(0)]\n')
            Handle.close()
    elif npt == 4: # Correct choice
        if options['method'] == 'infinite' and DVKP0[3] != 0.0:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Source P initial guess is non-zero (impossible) set DVKP0(4) to zero or switch to different method\n') 
            Handle.close()
            return
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_DVKP0 = [D,V,K,P] is too long reduce to at least 4\n')
        Handle.close()
        return
    # Verify if spatial points match input dimensions
    # two cases possible nx + 1 or nx matches dimensions
    if ncov1 != ncov2:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Input error: first two input dimensions are not square Cov_m =  [number of inputs x number of inputs x number of frequencies]\n')
            Handle.close()
            return
    elif nu2 != ncov1 and options['estimation'] == 'MLE':
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Input error: number of inputs in U = [number of frequencies x number of inputs] does not match input dimensions Cov_m =  [number of inputs x number of inputs x number of frequencies]\n')
            Handle.close()
            return
    elif nx == nu2 or (nx + 1) == nu2: # do nothing
        pass
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_Input error: number of spatial points (x) does not match input dimensions U = [number of frequencies x number of inputs ( + 1)]\n')
        Handle.close()
        return
    # Check if the method chosen matches input data
    # Case one U = [T1,T2]
    if nx == 2 and nu2 == 2:
        if  options['method'] == 'infinite': # correct choice
            pass
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Combination method choice options.method and input dimension U and/or x is incorrect, probably should be  options.method = infinite\n')
            Handle.close()
            return
    # Case two U = [T1,T2,T3] and x = [x1,x2,x3];
    elif nx == 3 and nu2 == 3:
        if options['method'] == 'infinite': # ok choice
            #warning('Consider using ''options.method = boundaries'' for more reliable results (U(:,1) used as boundary, U(:,2:3) used for estimation)\n')
            pass
        elif options['method'] == 'boundaries': # best choice
            pass
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Combination method choice options.method and input dimension U is incorrect, probably should be  options.method = boundaries\n')
            Handle.close()
            return
    # Case three U = [T1,T2,T3,P] and x = [x1,x2,x3];
    elif nx == 3 and nu2 == 4:
        if options['method'] == 'source': # ok choice
            pass
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_Fourth dimension U ignored consider using options.method = source\n')
            Handle.close()
    # Case four LPMn for semi-infinite and case five LPMn for 3-point;
    elif nx == nu2:
        if options['method'] == 'infinite': # ok choice
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_Consider using options.method = boundaries for more reliable results (U(:,1) used as boundary, U(:,2:'+str(nx)+') used for estimation)\n')
            Handle.close() 
        elif options['method'] == 'boundaries': # best choice
            pass
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_Combination method choice options.method = source and input dimension U is incorrect (should be one longer than x with one), probably should be options.method = boundaries\n')
            Handle.close()
            return
    # Case six LPMn for 3-point + source;
    elif nx + 1 == nu2:
        if options['method'] == 'source': # correct choice
            pass
        elif options['method'] == 'infinite':
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_'+str(nu2)+'-dimension of input U is ignored (U(:,1) used as boundary, U(:,2:'+str(nx)+') used for estimation) consider using options.method = source\n')
            Handle.close()
        elif options['method'] == 'boundaries': 
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Warning_Dimension'+str(nu2)+' of input U is ignored options.method = boundaries is used, consider using options.method = source\n')
            Handle.close()
        else:
            Handle = open('../temp/MLEn2.log','a')
            Handle.write('Error_huh, how did you end up here :(\n')
            Handle.close()
            return
    # Transform input data to standard format
    # Transform in correct dimension (forgiving form)
    w_ = w.T # assure omega is a vector
    x_ = x # assure is a row

    # Set empty covariance matrix for 'LSE' and 'WLSE'
    if options['estimation'] != 'MLE':
        Cov_m = np.zeros[nu2,nu2,nu1]     #TODO

    # Transform input to correct format
    if nx == nu2 and options['method'] =='infinite':
        # add an extra zero x
        Temp = np.zeros((1,1))
        Temp[0,0] = np.inf
        x_ = np.concatenate((x_,Temp),axis=1)
        # Define correct input size nw,(nx+2)
        U_ = np.zeros((nw,nx+2),dtype=complex)
        Cov_m_ = np.zeros((nx+2,nx+2,nw),dtype=complex)
        # Fill up
        U_[:,:-2] = U
        Cov_m_[:-2,:-2,:] = Cov_m
    elif nx+1 == nu2 and options['method'] == 'infinite':
        # add an extra zero x
        Temp = np.zeros((1,1))
        Temp[0,0] = np.inf
        x_ = np.concatenate((x_,Temp),axis=1)
        # Define correct input size
        U_ = np.zeros((nw,nx+2),dtype=complex)
        Cov_m_ = np.zeros((nx+2,nx+2,nw),dtype=complex) 
        # Fill up
        #! U_(1:nw,[1:nx,end]) = U(1:nw,[1:nx,end]); # note that P cannot exist for semi-infinite domains hence set to zero #!
        #! Cov_m_([1:nx,end],[1:nx,end],:) = Cov_m;
    elif nx == nu2 and options['method'] == 'boundaries': # Extend U and Cov_m  
        # Define correct input size 
        U_ = np.zeros((nw,nx+1),dtype=complex)
        Cov_m_ = np.zeros((nx+1,nx+1,nw),dtype=complex) 
        # Fill up
        U_[0:nw,0:nx] = U
        Cov_m_[0:nx,0:nx,:] = Cov_m
    elif nx + 1 == nu2: # correct length
        U_ = U  
        Cov_m_ = Cov_m
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_U and x are not matching up (you should not be seeing this error)\n')
        Handle.close()
        return
    # Transform U to one-dimensional format sum([G11, G12; G21, G22]*[U1;U2])
    # --> [G11*U1 + G21*U2; G12*U1 + G22*U2] --> [G11*U1, G12*U1, G21*U2,
    # G22*U2] --> [G11, G12, G21, G22]*[U1;U1;U2;U2];
    # n_outputs = length(x_)-2;
    # U_full = [repmat(U_(:,1),1,n_outputs),U_(:,2:n_outputs+1),repmat(U_(:,n_outputs+2),1,n_outputs),repmat(U_(:,n_outputs+3),1,n_outputs)];
    #  
    # options.Uout = U_full;
    # keyboard
    # Transform parameter set to full format 
    DVKP0_ = [0.0,0.0,0.0,0.0]
#     # DVKP0 = DVKP0(:);
#     DVKP0
    if npt == 1:
        DVKP0_[0] = DVKP0
    elif npt == 2: 
        DVKP0_[0:1] = DVKP0
    elif npt == 3: 
        DVKP0_[0:2] = DVKP0
    elif npt == 4: 
        DVKP0_= DVKP0
    else:
        Handle = open('../temp/MLEn2.log','a')
        Handle.write('Error_DVKP0 = [D,V,K,P] is too long reduce to at least 4\n')
        Handle.close()
        return
    #
    return DVKP0_,x_,w_,U_,Cov_m_,options