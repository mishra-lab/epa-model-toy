import warnings
import numpy as np

def nowarn(fun):
  # suppress warnings while running fun
  def decorator(*args,**kwds):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      result = fun(*args,**kwds)
      return result
  return decorator

def nanzero(fun):
  # replace nans with 0 in the return of fun
  def decorator(*args,**kwds):
    result = nowarn(fun)(*args,**kwds)
    result[np.isnan(result)] = 0
    return result
  return decorator

def Rmap(args=['X']):
  # extract named values from R and pass as args to fun
  def wrapper(fun):
    def decorator(R,**kwds):
      kwds.update({k:R[k] for k in args})
      return fun(**kwds)
    return decorator
  return wrapper

def rk4(dXfun):
  def decorator(Xi,ti,tf,*args,**kwds):
    dt = tf - ti
    R1 = dXfun(Xi,              ti,     *args,**kwds)
    R2 = dXfun(Xi+dt*R1['dX']/2,ti+dt/2,*args,**kwds)
    R3 = dXfun(Xi+dt*R2['dX']/2,ti+dt/2,*args,**kwds)
    R4 = dXfun(Xi+dt*R3['dX'],  ti+dt,  *args,**kwds)
    return {k:(R1[k]+2*R2[k]+2*R3[k]+R4[k])/6 for k in R1.keys()}
  return decorator
