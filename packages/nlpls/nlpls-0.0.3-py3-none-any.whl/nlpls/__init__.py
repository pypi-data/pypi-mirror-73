# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 07:06:26 2020

@author: User
"""



import numpy as np
from scipy.optimize import minimize



def fct_min_gamma(params,X,cw,w,x):

  # Calculate the resulting score
  t = X@(cw*w**(params[0]/(1-params[0]))).T
  t= t[:,0]

  # Calculate the monotonic NL relation
  paramsm = params[1:]
  g = np.array([t]).T*np.abs(np.array([paramsm[:int(len(paramsm)/2)]])) + \
    np.array([paramsm[int(len(paramsm)/2):]])
  g = 1/(1+np.exp(-g))
  ypred = np.sum(g,axis=1)
  return -np.corrcoef(x,ypred)[0,1]



def fct_min(params,X,cw,w,x):

  # Calculate the monotonic NL relation
  g = np.array([t]).T*np.abs(np.array([params[:int(len(params)/2)]])) + \
    np.array([params[int(len(params)/2):]])
  g = 1/(1+np.exp(-g))
  ypred = np.sum(g,axis=1)
  return -np.corrcoef(x,ypred)[0,1]



class regression:


  def __init__(self):
    self.all_w = []
    self.all_b = []
    self.all_std = []
    self.all_gamma = []
    self.all_paramsm = []
    self.preprocess = True
    self.Xmean = None
    self.Xstd = None


  def predict(self,X,comp=np.inf):
    X = X.copy()
      
    if(self.preprocess):
      for i in range(len(X)):
        spectrum = X[i]
        spectrum = (spectrum-np.mean(spectrum))/np.std(spectrum)
        spectrum = np.gradient(spectrum)
        X[i] = spectrum
    X = (X-self.Xmean)/self.Xstd

    y = np.zeros([len(X),1])
    for nb_comp in range(int(np.min([len(self.all_w),comp]))):
      t = X@self.all_w[nb_comp].T
      t = t[:,0]
      paramsm = self.all_paramsm[nb_comp]
      g = np.array([t]).T*np.abs(np.array([paramsm[:int(len(paramsm)/2)]])) + \
          np.array([paramsm[int(len(paramsm)/2):]])
      g = 1/(1+np.exp(-g))
      ypred = np.array([np.sum(g,axis=1)]).T
      ypred1 = np.append(ypred,ypred*0+1,axis=1)
      y = y + ypred1@self.all_b[nb_comp]

    return y[:,0]


  def get_weights(self,comp=np.inf):
    w = np.zeros(len(self.all_w[0][0]))
    for i in range(int(np.min([len(self.all_w),comp]))):
        w += np.abs(self.all_w[i][0])*self.all_std[i]**2
    w = w/np.max(w)
    return w

  def fit(self,X,y,nb_comp=1,preprocess=True):

    bounds = []
    for i in range(31):
      if(i==0):
        bounds.append((.5,1-1e-10))
      else:
        bounds.append((None,None))
    bounds = tuple(bounds)

    y_ori = y.copy()

    
    X = X.copy()

    # Preprocess
    self.preprocess = preprocess
    if(self.preprocess):
      for i in range(len(X)):
        spectrum = X[i]
        spectrum = (spectrum-np.mean(spectrum))/np.std(spectrum)
        spectrum = np.gradient(spectrum)
        X[i] = spectrum
    self.Xmean = np.array(np.mean(X,axis=0))
    self.Xstd = np.array(np.std(X,axis=0))
    X = (X-self.Xmean)/self.Xstd


    for nb_comp in range(nb_comp):

      # First linear process
      w = np.corrcoef(X.T,y.T)
      w = np.array([w[-1,:-1]])
      cw = w/np.abs(w)
      w = np.abs(w)
      w = w-np.min(w)
      w = w/np.max(w)
      w[np.isnan(w)] = 0

      # First linear pass
      allcorr = []
      gammas = np.arange(0,1,.005)
      for gamma in gammas:
        ww = cw*w**(gamma/(1-gamma))
        t = X@ww.T
        allcorr.append(np.corrcoef(t.T,y.T)[0,1])
      gamma = gammas[np.argmax(allcorr)]
      t = X@(cw*w**(gamma/(1-gamma))).T

      # Linear regression
      t1 = np.append(t,t*0+1,axis=1)
      b = np.linalg.inv(t1.T@t1)@t1.T@y


      # NL+gamma iteration
      x = y[:,0]
      bounds = []
      for i in range(31):
        if(i==0):
          bounds.append((0,1-1e-10))
        else:
          bounds.append((None,None))
      bounds = tuple(bounds)
      x0 = np.append(np.array([gamma]),np.random.randn(30))
      res = minimize(fct_min_gamma,x0,bounds=bounds,args=(X,cw,w,x))
      gamma = res.x[0]
      params = res.x


      for iter in range(10):

        print("Comp {:.0f} : Iter {:.0f}/10".format(nb_comp+1,iter+1))

        # Linear coeff calculation
        t = X@(cw*w**(params[0]/(1-params[0]))).T
        t = t[:,0]
        paramsm = params[1:]
        g = np.array([t]).T*np.abs(np.array([paramsm[:int(len(paramsm)/2)]])) + \
          np.array([paramsm[int(len(paramsm)/2):]])
        g = 1/(1+np.exp(-g))
        ypred = np.array([np.sum(g,axis=1)]).T
        ypred1 = np.append(ypred,ypred*0+1,axis=1)
        b = np.linalg.inv(ypred1.T@ypred1)@ypred1.T@y

        # NL-reverse
        t = np.linspace(np.min(t),np.max(t),10000)
        g = np.array([t]).T*np.abs(np.array([paramsm[:int(len(paramsm)/2)]])) + \
          np.array([paramsm[int(len(paramsm)/2):]])
        g = 1/(1+np.exp(-g))
        ypred = np.array([np.sum(g,axis=1)]).T
        ypred = np.append(ypred,ypred*0+1,axis=1)
        ypred = ypred@b
        e2 = (y-ypred.T)**2
        e2minpos = np.argmin(e2,axis=1)
        ylin = np.array([t[e2minpos]])

        # w update
        w = np.corrcoef(X.T,ylin)
        w = np.array([w[-1,:-1]])
        cw = w/np.abs(w)
        w = np.abs(w)
        w = w-np.min(w)
        w = w/np.max(w)
        w[np.isnan(w)] = 0

        # NL+gamma iteration
        x = y[:,0]
        x0 = np.append(np.array([gamma]),np.random.randn(30))
        res = minimize(fct_min_gamma,x0,bounds=bounds,args=(X,cw,w,x))
        gamma = res.x[0]
        params = res.x


      # Linear coeff calculation
      w_final = cw*w**(params[0]/(1-params[0]))
      t = X@(cw*w**(params[0]/(1-params[0]))).T
      t = t[:,0]
      paramsm = params[1:]
      g = np.array([t]).T*np.abs(np.array([paramsm[:int(len(paramsm)/2)]])) + \
        np.array([paramsm[int(len(paramsm)/2):]])
      g = 1/(1+np.exp(-g))
      ypred = np.array([np.sum(g,axis=1)]).T
      ypred1 = np.append(ypred,ypred*0+1,axis=1)
      b = np.linalg.inv(ypred1.T@ypred1)@ypred1.T@y
      ypred = ypred1@b

      # Save data
      self.all_w.append(w_final.copy())
      self.all_b.append(b.copy())
      self.all_std.append(np.std(ypred))
      self.all_gamma.append(params[0])
      self.all_paramsm.append(paramsm.copy())

      # Deflate
      y = y - ypred




# # Data
# X = np.random.randn(100,5)
# y = X[:,2:3]*.5 - X[:,3:4]*.25
# y = y-np.min(y)
# y = y**2



# regression = regression()
# regression.fit(X,y,3,preprocess=False)
# ypred = regression.predict(X)


# import matplotlib.pyplot as plt

# plt.figure()
# plt.plot(y,ypred,'.')

# plt.figure()
# plt.stem(regression.get_weights())