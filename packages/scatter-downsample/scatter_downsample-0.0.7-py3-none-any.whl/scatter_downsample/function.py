import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.linalg import eigh
import argparse

#reshape the 3D array into 4D with dimensions (h/2,w/2,c,4)
def reshape_array(I):
  h,w,c = I.shape
  new_arr=np.zeros(shape=(int(h/2),int(w/2),int(c),4))
  k = 0
  for i in range(2):
    for j in range(2):
      new_arr[:,:,:,k] = I[i:len(new_arr)*2:2,j:len(new_arr[0])*2:2,:]
      k += 1
  return new_arr

def down2withSD(I,L,filter=2):

  #initialize labels
  if not L:
    L = ["r","g","b"]

  #copy the original image
  n = np.array(I.shape)
  nd = np.copy(n)
  nd[:2] = nd[:2]//2
  J = np.zeros(nd)
  K = np.zeros(nd)
  #apply averaging
  for i in range(2):
    for j in range(2):
      J += I[i:nd[0]*2:2, j:nd[1]*2:2,:] / 4.0

  #filtering out the channels with 2 1's
  rmv = [L.index(x) for x in L if x.count("1")>(filter-1)]
  Im = np.delete(I, rmv, axis=2)

  #calculate standard deviations
  Im = reshape_array(Im)
  K = np.std(Im,axis=3)

  #concatenate mean and standard deviation arrays
  ret = np.concatenate((J,K), axis=2)

  #each iteration, append to labels
  label = [x+"0" for x in L] + [x+"1" for x in L if x.count("1")<filter]

  return ret, label

def pca(Iout,normalize=None,mask=None):
    if mask is None:
        mask = np.ones_like(Iout[...,0])
    if normalize is None:
        normalize = 'dn'
    X = np.reshape(Iout,(-1,Iout.shape[-1]))
    mask = mask.ravel()[...,None]
    Xbar = np.sum(X*mask,0)/np.sum(mask)
    X0 = X - Xbar
    Sigma = X0.transpose() @ (X0*mask) / np.sum(mask)
    d2,V = eigh(Sigma)
    d = np.sqrt(d2)
    XV = X0 @ V
    if 'd0' in normalize:
        XVd = XV / d[-1]
    elif 'd1' in normalize:
        XVd = XV / d[-2]
    elif 'd2' in normalize:
        XVd = XV / d[-3]
    elif 'd3' in normalize:
        XVd = XV / d[-4]
    elif 'd4' in normalize:
        XVd = XV / d[-5]
    elif 'd' in normalize:
        XVd = XV / d
    else:
        XVd = XV
    if 'n' in normalize:
        XVdn = norm.cdf(XVd)
    else:
        XVdn = XVd
    out = np.reshape(XVdn,Iout.shape)
    out = out[:,:,::-1] # change it from ascending to descending   
    return out 

def ScatterDown(I,ndown2,filtered_std=2):
  I = plt.imread(I)
  I = I.astype(float)
  I /= 255.0

  Id = np.copy(I)
  L = ["r","g","b"]
  for n in range(ndown2):
    Id,L = down2withSD(Id,L,filtered_std)
  
  Ip = pca(Id)
  f,ax = plt.subplots()
  ax.imshow(Ip[...,0:3])
  ax.set_title('First three channels')
  f.savefig('output.jpg')

  # f,ax = plt.subplots()
  # ax.imshow(Ip[...,3:6])
  # ax.set_title('Second three channels')

  # f,ax = plt.subplots()
  # ax.imshow(Ip[...,6:9])
  # ax.set_title('Third three channels')

  # f,ax = plt.subplots()
  # ax.imshow(Ip[...,9:12])
  # ax.set_title('Last three channels')

  return Id,L,f

