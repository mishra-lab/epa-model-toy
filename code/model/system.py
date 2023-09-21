import numpy as np
from scipy.integrate import solve_ivp
from utils import _

tol = 1e-9

def get_tvec(t0=1985,tf=2025,dt=1):
  return np.arange(t0,tf+dt,dt)

def run(P,tvec):
  # solve the model & collect outputs in [R]esults dict
  S = solve_ivp(get_dX,tvec[[0,-1]],P['X0'].flatten(),t_eval=tvec,args=(P,))
  X = S['y'].T.reshape((len(tvec),*P['X0'].shape)) # reshape so t-dimension is first
  return {
    'P': P,
    'X': X,
    't': tvec,
  }

def get_mix(M_pr,P):
  # define population-level mixing matrix from M_pr
  M0_prr = M_pr[:,:,_] * M_pr[:,_,:] / M_pr.sum(axis=1)[:,_,_] + tol # random
  # TODO: mixing
  return M0_prr # (p:3,r:3,r':3)

def get_foi(t,X,P):
  # (p:3,r:3,r':3,h':3)
  # M = total partnerships 'offered'
  M_prh = (X[_,:,:,:] * P['K_prs'][:,:,:,_]).sum(axis=2) # (p:3,r:3,h:3)
  M_prh[M_prh<0] = 0
  M_pr = M_prh.sum(axis=2)
  # Ph_pr = distribution of health states for each partnership type & risk group
  Ph_pr = M_prh / (M_pr[:,:,_] + tol)
  M_prr = get_mix(M_pr,P) # (p:3,r:3,r':3)
  Fbeta = P['beta_ph'] * P['freq_p'][:,_] # transmission rate per partnership
  return Fbeta[:,_,_,:] * M_prr[:,:,:,_] * Ph_pr[:,:,0,_,_] * Ph_pr[:,_,:,:] # (p:3,r:3,r':3,h':3)

def get_dX(t,X,P):
  X = X.reshape(P['X0'].shape) # (r:3,s:4,h:3)
  dX = 0*X
  # force of infection (EPA)
  foi = get_foi(t,X,P) # (p:3,r:3,r':3,h':3)
  dXi = foi.sum(axis=(2,3)) # acquisition (p:3,r:3)
  dX[:,0 ,0] -= dXi.sum(axis=0) # remove newly infected from s'=0
  dX[:,1:,1] += np.moveaxis(dXi,0,1) # add newly infected to s'=p
  dXi = foi.sum(axis=(1)) # transmission (p:3,r':3,h':3)
  dX[:,0 ,:] -= dXi.sum(axis=0) # remove newly transmitted from s'=0
  dX[:,1:,:] += np.moveaxis(dXi,0,1) # add newly transmitted to s'=p
  dXi = X[:,1:,:] / P['dur_p'][_,:,_] # partnership change (r:3,s:3,h:3)
  dX[:,1:,:] -= dXi # remove partner changers from s'=p
  dX[:,0 ,:] += dXi.sum(axis=1) # add partners changers to s'=0
  # births & deaths
  dX[:,0,0] += X.sum() * P['birth'] * P['PX0_r'] # all susceptible & s'=0
  dX -= X * P['death'] # everybody
  # health transitions
  dXi = X[:,:,1] / P['dur_h']
  dX[:,:,1] -= dXi
  dX[:,:,2] += dXi
  # TODO: turnover
  return dX.flatten()
