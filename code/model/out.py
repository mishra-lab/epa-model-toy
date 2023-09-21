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
  X = X_by_r(X.sum(axis=2),r=r)
  X1 = X[:,:,1:].sum(axis=2)
  X2 = X.sum(axis=2)
  return aggratio(X1,X2,aggr)

# TODO: more outputs
