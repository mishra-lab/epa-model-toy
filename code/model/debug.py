import numpy as np
from model import param,system,out,plot

tvec = system.get_tvec()
P = param.get_all()
R = system.run(P,tvec)

plot.debug(tvec,ylab='Prevalence',
  outs={'r = '+str(r):out.prevalence(R,r=r) for r in (None,0,1,2)})
plot.debug(tvec,ylab='Incidence',
  outs={'r = '+str(r):out.incidence(R,r=r) for r in (None,0,1,2)})
