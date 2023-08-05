import math
import numpy as np
def down2mean_std(I_I,label,std): #1 input
  # the size of the image
  n = np.array(I_I.shape)
  # the size of the downsampled image, use integer division
  nd = np.copy(n)
  nd[:2] = nd[:2]//2
  # print(nd)
  # Initialize a downsampled image
  J = np.zeros(nd)
  H = np.zeros(nd)
  I2 = I_I**2
    
  # average and standard deviation over a 2x2 neighborhood via slicing
  # we get every other pixel, and add up four times
  for i in range(2):
    for j in range(2):
      J += I_I[i:nd[0]*2:2, j:nd[1]*2:2,:] / 4.0
      # print(I_I)
      # I2 = I_I**2
      H += I2[i:nd[0]*2:2, j:nd[1]*2:2,:] / 4.0  #E(x^2)
      # print("H",H.shape)
      # print(H)
  # return this image
  K = np.sqrt(abs(H-J**2)) # or absolute value
  Output = np.concatenate((J,K),2) 

  # num_ch = n[2]
  # print(num_ch)
  # for c in label:
  #   ch = label.index(c)
  #   if c.count('1') == 2:
  #     Output = np.delete(Output,ch+num_ch,2)
  # account for the deletion of paths containing more than 2 '1's  
  # label = [x+'0' for x in label] + [x+'1' for x in label]
  label = [x+'0' for x in label] + [x+'1' for x in label if x.count('1') >= std]
  return Output,label # 1 output with 2x channels



def ScatterDown(img,ndown2,filtered_std=2):
  # downsampling with numbers of mean and filtered std specified
  label = ['r','g','b']
  for i in range(ndown2):
    img,label = down2mean_std(img,label,filtered_std)
  
  # save png file
  # f,ax = plt.subplots()
  # ax.imshow(Ip[...,3:6],cmap='gray')
  # ax.set_title('three to six channels')
  # .save(visual)
  return img,label #,visual

def check():
  test_img = np.full((256,256,3),0.5)
  label = []
  test_img,label = ScatterDown(test_img,5)
  return test_img,label

if __name__ == "__main__": 
	test_image, label = check()
	print(test_image,label)