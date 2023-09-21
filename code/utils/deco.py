import warnings

def nowarn(fun):
  # suppress warnings while running fun
  def decorator(*args,**kwds):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore')
      result = fun(*args,**kwds)
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
