import numpy as np
from utils import _,deco

def by_name(name):
  return globals()[name]

def aggratio(X1,X2,aggr,axis=None):
  if axis is None: axis = 1
  if aggr:
    return X1.sum(axis=axis) / X2.sum(axis=axis)
  else:
    return X1 / X2

def X_by_r(X,r=None):
  return X.sum(axis=1,keepdims=True) if r is None \
    else X[:,_,r] if isinstance(r,int) \
    else X[:,r]

@deco.Rmap(args=['X'])
def prevalence(X,r=None,aggr=True):
  # X: (t:*,r:3,s:4,h:3)
  X = X_by_r(X.sum(axis=2),r=r)
  X1 = X[:,:,1:].sum(axis=2)
  X2 = X.sum(axis=2)
  return aggratio(X1,X2,aggr)

@deco.Rmap(args=['X','foi'])
def incidence(X,foi,r=None,aggr=True):
  # foi: (t:*,p:3,r:3,r':3,h':3)
  foi = foi.sum(axis=(1,3,4))
  X1 = X_by_r(foi,r=r)
  X2 = X_by_r(X[:,:,0,0],r=r)
  return aggratio(X1,X2,aggr)

# TODO: more outputs
