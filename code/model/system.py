import numpy as np
from utils import _,deco

tol = 1e-9

def get_tvec(t0=1985,tf=2025,dt=.1):
  return np.arange(t0,tf+dt,dt)

def init_X(X0,tvec):
  X = np.nan * np.ndarray([tvec.size,*X0.shape])
  X[0] = X0
  return X

def run(P,tvec):
  # solve the model & collect outputs in [R]esults dict
  X   = init_X(P['X0'],tvec) # (s:4,r:3,h:3)
  foi = init_X(np.zeros((3,3,3,3)),tvec) # (p:3,r:3,r':3,h':3)
  for i in range(1,tvec.size):
    Ri = get_dX(X[i-1],tvec[i-1],tvec[i],P)
    X[i] = X[i-1] + (tvec[i] - tvec[i-1]) * Ri['dX']
    foi[i] = Ri['foi']
    if np.any(X[i].sum(axis=1) < 0) or np.any(foi[i] < 0): # abort / fail
      raise Exception('model.run() failed at t = {}'.format(tvec[i]))
  return {
    'P': P,
    'X': X,
    'foi': foi,
    'tvec': tvec,
  }

def get_mix(M_pr,P):
  # define population-level [M]ixing matrix from M_pr
  M0_prr = M_pr[:,:,_] * M_pr[:,_,:] / M_pr.sum(axis=1)[:,_,_] + tol # random
  # TODO: mixing
  return M0_prr # (p:3,r:3,r':3)

def get_foi(X,t,P):
  # (p:3,r:3,r':3,h':3)
  # M = total partnerships 'offered'
  M_prh = (X[_,:,:,:] * P['K_psr'][:,:,:,_]).sum(axis=1) # (p:3,r:3,h:3)
  M_prh[M_prh<0] = 0
  M_pr = M_prh.sum(axis=2)
  # Ph_pr = distribution of health states for each partnership type & risk group
  Ph_pr = M_prh / (M_pr[:,:,_] + tol)
  M_prr = get_mix(M_pr,P) # (p:3,r:3,r':3)
  Fbeta = P['beta_ph'] * P['freq_p'][:,_] # transmission rate per partnership
  return Fbeta[:,_,_,:] * M_prr[:,:,:,_] * Ph_pr[:,:,0,_,_] * Ph_pr[:,_,:,:] # (p:3,r:3,r':3,h':3)

@deco.rk4
def get_dX(X,t,P):
  dX = 0*X
  # force of infection (EPA)
  foi = get_foi(X,t,P) # (p:3,r:3,r':3,h':3)
  dXi = foi.sum(axis=(2,3)) # acquisition (p:3,r:3)
  dX[0 ,:,0] -= dXi.sum(axis=0) # remove newly infected from s'=0,h=0
  dX[1:,:,1] += dXi # add newly infected to s'=p,h=1
  dXi = foi.sum(axis=(1)) # transmission (p:3,r':3,h':3)
  dX[0 ,:,:] -= dXi.sum(axis=0) # remove newly transmitted from s'=0,h
  dX[1:,:,:] += dXi # add newly transmitted to s'=p,h
  dXi = X[1:,:,:] / P['dur_p'][:,_,_] # partnership change (s:3,r:3,h:3)
  dX[1:,:,:] -= dXi # remove partner changers from s'=p,h
  dX[0 ,:,:] += dXi.sum(axis=0) # add partners changers to s'=0,h
  # entry & exit
  dX[0,:,0] += X.sum() * P['entry'] * P['PXe_r'] # all susceptible & s'=0
  dX -= X * P['exit'] # everybody
  # turnover
  dXi = X[:,:,_,:] * P['turn_rr'][_,:,:,_]
  dX -= dXi.sum(axis=2)
  dX += dXi.sum(axis=1)
  # health transitions
  dXi = X[:,:,1] / P['dur_h']
  dX[:,:,1] -= dXi
  dX[:,:,2] += dXi
  return {
    'dX': dX,
    'foi': foi,
  }
