import matplotlib.pyplot as plt

def debug(tvec,outs,ylab=None):
  for k,v in outs.items():
    plt.plot(tvec,v,label=str(k))
  plt.ylabel(ylab)
  plt.xlabel('Year')
  plt.legend()
  plt.show()
