# from .function import reshape_array,down2withSD,pca,ScatterDown
import scatter_downsample as sd
import argparse
import textwrap

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Multiple scattering downsample methods for images',formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument('-i', '--image', required=True, dest='image_file',
                        help='File containing an image to downsample')
  parser.add_argument('-n', '--num_downsample', required=True, dest='ndown',
                        help='number of times the image needs to be downsampled')
  parser.add_argument('-s', '--std', required=False, dest='filtered_std',
                        help='number of times the standard deviation is filtered (default 2)')
  parser.add_argument('-d', '--direction', required=False, dest='dirt',
                        help='number of direction for gaussian downsampling (default 2)')
  parser.add_argument('-m', '--method', required=False, dest='down_method',
                        help=textwrap.dedent('''\
                          The method that is used to scatter downsample the image, it has to be the following:
                             1) 2 x 2 mean and standard deviation
                             2) 2 x 2 mean and standard deviation with 3 direction
                             3) Gaussian Filtering
                             4) TBD ... '''))
  args = parser.parse_args()
  I = args.image_file
  ndown2 = int(args.ndown)

  filtered_std = 2 if args.filtered_std is None else int(args.filtered_std)
  method = 1 if args.down_method is None else int(args.down_method)
  dirt = 2 if args.dirt is None else int(args.dirt)
  sd.ScatterDown(I,ndown2,filtered_std,method,dirt)