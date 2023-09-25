import numpy as np
from model import param,system,out,plot

tvec = system.get_tvec()
P = param.get_all()
R = system.run(P,tvec)

plot.debug(tvec,ylab='Population Proportion',
  outs={'r = {}'.format(r):out.PX(R,r=r) for r in (None,0,1,2)})
plot.debug(tvec,ylab='Prevalence',
  outs={'r = {}'.format(r):out.prevalence(R,r=r) for r in (None,0,1,2)})
plot.debug(tvec,ylab='Incidence',
  outs={'r = {}'.format(r):out.incidence(R,r=r) for r in (None,0,1,2)})
plot.debug(tvec,ylab='Transmission-driven Seroconcordance',
  outs={'p = {}'.format(p):out.tdsc(R,p=p) for p in (None,0,1,2)})