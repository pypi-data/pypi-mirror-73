import numpy as np
from scipy.stats import norm
from scipy.linalg import eigh
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)
import string

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

def Rotations(I,L):
  #if a label includes a 2 or 4, translate every 2 to 4 and vice versa
  #compare with original labels, if they are the same, store the indices of this pair in a list
  label_list =[]
  ret = I.copy()
  label_copy = L.copy()
  label = L.copy()
  for i in label_copy:
    label_cut = label[int(label.index(i)+1)::]
    if '2' in i or '4' in i:
      translated = i.translate(str.maketrans("24", "42"))
      if translated in label_cut:
        label_list.append([label_copy.index(i), (label_cut.index(translated)+label_copy.index(i)+1)])
  
  #take two channels and find average
  #insert average into one and delete the other (delete labels as well)
  del_label = []
  for c1, c2 in label_list:
    ret[:,:,c1] = (ret[:,:,c1] + ret[:,:,c2])/2
    del_label.append(c2)
  label = np.delete(label,del_label)
  ret = np.delete(ret,del_label,axis=2)
  # if type(label) is not list:
  #   label=label.tolist()
  
  #print(label)
  # print(len(label))
  # print(ret.shape)
  return ret, label

def make_filters(radius=15,n_directions=1,
                 scale_low=2.0, scale_high=3.0,
                 slant=1.7, draw=False):
    '''
    Produce a set of low pass and high pass filters 
    based on the Gaussian kernel, with direction selectivity
    throug the Morlet wavelet.
    
    For the special case of n_directions=1, we do not use the 
    Moret wavelet.
    
    '''
    
    # build a Gaussian filter for low pass
    x = np.arange(-radius,radius+1)
    X = np.stack(np.meshgrid(x,x,indexing='ij'))
    R2 = np.sum(X**2,0)
    h = np.exp(-R2/2.0/scale_low**2)
    h /= np.sum(h) # normalize to 1
    
    # angles for direction selectivity    
    thetas = np.arange(n_directions)/n_directions * np.pi
    
    # build a list of filters at different angles
    gs = []
    for t in thetas:
        # we use a Gaussian filter times a complex exponential
        g0 = np.exp(-((X[0]*np.cos(t) + X[1]*np.sin(t))**2 + (-X[0]*np.sin(t) + X[1]*np.cos(t))**2/(slant)**2)/2.0/(scale_high)**2)
        g0 /= np.sum(g0)
        wave = np.exp(1j*(X[0]*np.cos(t) + X[1]*np.sin(t))/scale_high*slant)

        # we normalize the filter such that it is zero mean and its absolute value sums to 1
        g = g0 * ( wave -  np.sum(g0*wave)/np.sum(g0) ) 
        # the sum is sum(g0*wave) - sum(g0)*sum(g0*wave)/sum(g0) = 0
        g /= np.sum(np.abs(g))

        gs.append(g)
        
    # special case if not using directions
    if n_directions == 1:
        # we use a highpass filter that corresponds to the complement of our original lowpass filter
        gs = [ np.fft.fftshift(np.fft.ifftn(1.0 - np.fft.fftn(np.fft.ifftshift(h)))).real ]
    
    if draw:
        gshow = [h] + gs
        f,ax = plt.subplots(2,n_directions+1,squeeze=False)
        for i,g in enumerate(gshow):
            handle = ax[0,i].imshow(g.real)
            ax[0,i].set_xticks([])
            ax[0,i].set_yticks([])
            #plt.colorbar(handle,ax=ax[0,i])

            handle = ax[1,i].imshow(g.imag)
            ax[1,i].set_xticks([])
            ax[1,i].set_yticks([])
            #plt.colorbar(handle,ax=ax[1,i])

            if i == len(gs)//2:
                ax[0,i].set_title('real part')
                ax[1,i].set_title('imaginary part')

        f.canvas.draw()
    #h: low pass, gs: high pass (last dim)
    return h,np.stack(gs,-1)

def apply_filters(I,filters):
    '''
    Apply filters to a image multi channel image
    Note this only works for square filters (rows = columns)
    This introduces a new dimension to the image, one for each filter
    If there is only one filter, it will introduce a singleton dimension
    If the image is only one channel, it will introduce a singleton dimension
    '''
    # append another dimension if necessary
    if filters.ndim == 2:
        filters = filters[...,None]
    if I.ndim == 2:
        I = I[...,None]
    
    # Fourier transform over first two axes
    Ihat = np.fft.fftn(I,axes=(0,1))
    
    # pad the filters on the right so they are the same size as the image
    topad = np.array(I.shape)[:2] - np.array(filters.shape)[:2]
    topad = [(0,t) for t in topad]
    topad.append((0,0))
    filtersp = np.pad(filters,topad)
    
    # roll them so the center pixel is at the top left corner
    r = (filters.shape[0]-1)//2
    filtersp = np.roll(filtersp,[-r]*2,[0,1]) 
    
    # Fourier transform over first two axes
    filtersphat = np.fft.fftn(filtersp,axes=(0,1))
    
    # filtering is equivalent to multiplying in the Fourier domain
    Ifiltered = np.fft.ifftn(  Ihat[...,None] * filtersphat[...,None,:])
    
    return Ifiltered