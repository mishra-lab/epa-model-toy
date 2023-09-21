import warnings

def nowarn(fun):
  def decorator(*args,**kwds):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      result = fun(*args,**kwds)
      return result
  return decorator

def Rmap(args=['X']):
  def wrapper(fun):
    def decorator(R,**kwds):
      kwds.update({k:R[k] for k in args})
      return fun(**kwds)
    return decorator
  return wrapper
