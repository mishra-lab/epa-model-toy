import numpy as np
from utils import _

# population strata:
# - s = seroconcordance (1+3) none/chance, main, casu, once
# - r = risk (3) low, medium, high
# - h = health (3) susceptible, asymptomatic, symptomatic
# plus p = partnership types (3) main, casu, once

def get_all():
  # create a dict of all model [P]arameters
  P = {}
  # independent
  P['N0']    = 100
  P['PX0_s'] = np.array([1,0,0,0]) # seroc (s:4)
  P['PX0_r'] = np.array([.75,.20,.5]) # risk (r:3)
  P['PX0_h'] = np.array([.99,.01,.00]) # health (h:3)
  P['K_pr']  = np.array([[1,1,1],[0,2,2],[0,2,100]]) # num partners
  P['aK_ps'] = np.array([[0,1,0,0],[0,0,1,0],[0,0,0,1]]) # seroc adjust
  P['beta']  = .0004 # prob transm per sex
  P['Rbeta_h'] = np.array([0,1,5]) # relative prob: health
  P['Rbeta_p'] = np.array([1,.5,.5]) # relative prob: partner
  P['freq_p']  = np.array([100,30,10]) # sex freq per partner
  P['dur_p']   = np.array([10,1,.1]) # partner duration
  P['dur_h']   = np.array([7]) # health durations
  P['birth'] = .02 # birth rate
  P['death'] = .01 # death rate
  # dependent
  P['X0']    = P['N0'] * P['PX0_s'][:,_,_] * P['PX0_r'][_,:,_] * P['PX0_h'][_,_,:] # (s:4,r:3,h:3)
  P['K_psr'] = np.maximum(0,P['K_pr'][:,_,:] - P['aK_ps'][:,:,_])
  P['beta_ph'] = P['beta'] * P['Rbeta_p'][:,_] * P['Rbeta_h'][_,:] # (p:3,h:3)
  return(P)
