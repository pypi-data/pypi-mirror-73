import numpy as np 
import matplotlib.pyplot as plt
from .helpers import reshape_array,pca,Rotations,make_filters,apply_filters
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning)
import string

# method 1: downsample by mean and standard deviation
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

# method 2: downsample with 3 direction
def down2withDirection(I,L,F=2):
  #initialize labels
    if type(L) is not list:
        L=L.tolist()
    if not L:
        L = ["r","g","b"]

  #copy the original image
    n = np.array(I.shape)
    nd = np.copy(n)
    nd[:2] = nd[:2]//2
    I_1 = np.zeros(nd)
    I_2= np.zeros(nd)
    I_3 = np.zeros(nd)
    I_4= np.zeros(nd)
    a=nd[0]*2
    b=nd[1]*2

  #apply averaging (mean)
    for i in range(2):
        for j in range(2):
            I_1 += I[i:a:2, j:b:2,:] / 4.0 
    rmv = [L.index(x) for x in L if (x.count("1") + x.count("2") + x.count("3") + x.count("4"))>(F-1)]
    Im = np.delete(I, rmv, axis=2)

  #adding directions
  #derivative in the (1,0) direction (x direction), label: 2
    I_2 = abs(Im[0:a:2,0:b:2,:]*0.25 - Im[1:a:2,0:b:2,:]*0.25 + Im[0:a:2,1:b:2,:]*0.25 - Im[1:a:2,1:b:2,:]*0.25)
  #derivative in the (1,1) direction, label: 3
    I_3 = abs(Im[0:a:2,0:b:2,:]*0.25 + Im[1:a:2,0:b:2,:]*0.25 - Im[0:a:2,1:b:2,:]*0.25 - Im[1:a:2,1:b:2,:]*0.25)
  #derivative in the (0,1) direction (y direction), label: 4
    I_4 = abs(Im[0:a:2,0:b:2,:]*0.25 - Im[1:a:2,0:b:2,:]*0.25 - Im[0:a:2,1:b:2,:]*0.25 + Im[1:a:2,1:b:2,:]*0.25)

  #concatenate channels
    ret = np.concatenate((I_1, I_2, I_3, I_4), axis=2)
  #update labels
    label = [x+"0" for x in L] +[x+"2" for x in L if (x.count("1") + x.count("2") + x.count("3") + x.count("4"))<F]+[x+"3" for x in L if (x.count("1") + x.count("2") + x.count("3") + x.count("4"))<F]+[x+"4" for x in L if (x.count("1") + x.count("2") + x.count("3") + x.count("4"))<F]

  #if a label includes a 2 or 4, translate every 2 to 4 and vice versa
  #compare with original labels, if they are the same, store the indices of this pair in a list
    label_list =[]
    label_copy = label.copy()
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

  # print(label)
  # print(len(label))
  # print(ret.shape)
    return ret, label

# method 3: gaussian filter downsampling
def gaussianDownsampling(I,L,F=2,directions=2):
  #convert labels to list
  if type(L) is not list:
    L=L.tolist()
  label = L
  I_cp = I.copy()

  #remove labels with F characters that are not 0
  rmv = [L.index(x) for x in L if (len(x)-x.count("0"))>F]
  I_cp = np.delete(I_cp, rmv, axis=2)

  # make filters
  lp,hp = make_filters(n_directions=directions)    

  #apply high pass filters, take absolute value
  Ifiltered = np.abs(apply_filters(I_cp,hp))
  Ifiltered = Ifiltered.reshape(Ifiltered.shape[0],Ifiltered.shape[1],Ifiltered.shape[2]*directions)
 
  #concatenate with original
  Ifiltered = np.concatenate((I, Ifiltered), axis=-1)

  #apply low pass filter, take absolute value
  Ifiltered = np.abs(apply_filters(Ifiltered,lp))
  Ifiltered = Ifiltered.reshape(Ifiltered.shape[0],Ifiltered.shape[1],Ifiltered.shape[2])

  # #downsample with slicing
  Ifiltered = Ifiltered[::2,::2,:]

  #update labels
  for i in range(int(hp.shape[2])+1):
    if i == 0:
      label =[x+"0" for x in L]
    else: 
      label += [x + str(i) for x in L if (len(x)-x.count("0"))<(F+1)]

  # print(label)
  # print(len(label))
  # print(Ifiltered.shape)
  return Ifiltered, label

def ScatterDown(I,ndown2,filtered_std=2,method=1):
    I = plt.imread(I)
    I = I.astype(float)
    I /= 255.0
    Id = np.copy(I)
    L = ["r","g","b"]

#     if method ==1:
#         for n in range(ndown2):
#             Id,L = down2withSD(Id,L,filtered_std)
#     elif method ==2:
#         for n in range(ndown2):
#             Id,L = down2withDirection(Id,L)
#     elif method == 3
#         for n in range(ndown2):
#             Id,L = gaussianDownsampling(Id,L)
    if method == 1:
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

