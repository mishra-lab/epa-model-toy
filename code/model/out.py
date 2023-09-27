import numpy as np
from utils import _,xdi,deco

def by_name(name):
  return globals()[name]

def aggratio(X1,X2,aggr,axis):
  if aggr:
    return X1.sum(axis=axis) / X2.sum(axis=axis)
  else:
    return X1 / X2

@deco.Rmap(args=['X'])
def PX(X,r=None,h=None,aggr=True):
  X2 = X.sum(axis=1)
  X1 = xdi(X2,{1:r,2:h})
  return aggratio(X1,X2,aggr,axis=(1,2))

@deco.Rmap(args=['X'])
def prevalence(X,r=None,aggr=True):
  # X: (t:*,s:4,r:3,h:3)
  X = xdi(X.sum(axis=1),{1:r})
  X1 = X[:,:,1:].sum(axis=2) # infected
  X2 = X.sum(axis=2) # total
  return aggratio(X1,X2,aggr,axis=1)

@deco.Rmap(args=['X','foi'])
def incidence(X,foi,p=None,r=None,aggr=True):
  # foi: (t:*,p:3,r:3,r':3,h':3)
  foi = foi.sum(axis=(3,4))
  X1 = xdi(foi,{1:p,2:r}) # new infections
  X2 = xdi(X[:,_,0,:,0],{2:r}) # susceptible
  return aggratio(X1,X2,aggr,axis=(1,2))

@deco.nanzero
@deco.Rmap(args=['X','P'])
def tdsc(X,P,p=None,r=None,aggr=True):
  # transmission-driven seroconcordance proportion
  X = X.sum(axis=3)
  X1 = xdi(X[:,1:,:],{1:p,2:r}) # seroconcordant partnerships
  X2 = xdi(X.sum(axis=1,keepdims=1) * P['K_pr'][_,:,:],{1:p,2:r}) # total partnerships
  return aggratio(X1,X2,aggr,axis=(1,2))

# TODO: more outputs
