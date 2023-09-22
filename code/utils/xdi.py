_ = None

def xdi(X,di):
  # slice X using {dim:index, ...} or x.sum(axis=d) if index=None
  # e.g. xdi(np.ones(5,4,3,2),{0:None,1:(1,2),2:0}).shape = (1,2,1,2)
  for d,i in di.items():
    if d==0:
      X = X.sum(axis=0,keepdims=True) if i is None \
        else X[i,_] if isinstance(i,int) \
        else X[i]
    elif d==1:
      X = X.sum(axis=1,keepdims=True) if i is None \
        else X[:,i,_] if isinstance(i,int) \
        else X[:,i]
    elif d==2:
      X = X.sum(axis=2,keepdims=True) if i is None \
        else X[:,:,i,_] if isinstance(i,int) \
        else X[:,:,i]
    elif d==3:
      X = X.sum(axis=3,keepdims=True) if i is None \
        else X[:,:,:,i,_] if isinstance(i,int) \
        else X[:,:,:,i]
    elif d==4:
      X = X.sum(axis=4,keepdims=True) if i is None \
        else X[:,:,:,:,i,_] if isinstance(i,int) \
        else X[:,:,:,:,i]
    elif d==5:
      X = X.sum(axis=5,keepdims=True) if i is None \
        else X[:,:,:,:,:,i,_] if isinstance(i,int) \
        else X[:,:,:,:,:,i]
  return X
