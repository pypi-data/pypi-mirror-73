# Downsampling high resolution images using the scattering transform
Atlasing high resolution data

Scattering transform

visualization of imges

downsampling with multiple methods

# Usage
## ScatterDown(img,ndown2,filtered_std=2):
Input:

    - img: input image
    - ndown2: how many times to downsample by a factor of 2
    - filtered_std: how many standard deviations maximum should not get filtered out (default 2)

Output: 

    - high dimensional image
    - labels for each channel
    - an example visualization that you save as a png file

# Tests
installed by: `python -m unittest tests/testcase.py`

- a small (256,256,3) image to test for the shape of output image and labels

