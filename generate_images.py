import numpy as np
from scipy.misc import imread, imsave
import scipy.signal as sig

num_images = 488
image_width = 1920
image_height = 1080
cols_per_image = 10;
image_loc = "/Users/loganw/Desktop/trees/trees "

digits = math.ceil(math.log(num_images+1,10))
image_width_digits = math.ceil(math.log(image_width+1,10))

print "Allocating " + str(num_images*image_width*image_height*3/(1024*1024*1024)) " Gb of RAM"

# allocate 4-dimensional array for storing all images
all_images = np.zeros((num_images, image_height, image_width, 3), dtype=np.uint8)

# load all images into memory
for i in range(0, num_images):
	# progress display
	for j in range(0,digits+1):
		print("\b"),
	print("Loading image " + str(i).zfill(digits)),
	
	all_images[i, :, :, :] = imread("/Users/loganw/Desktop/trees/trees " + str(i+1).zfill(digits) + ".jpg")

# calculate some sums for motion statistics. we don't really do anything with these statistics yet, but we might be able to eventually
row_sums = np.sum(all_images, axis=(2,3))
column_sums = np.sum(all_images, axis=(1,3))

# create a high pass filter, cutoff 0.1 w_n
n = 101
a = sig.firwin(n, cutoff = 0.1, window = "hamming")
a = -a
a[n/2] = a[n/2] + 1

filtered_column_sums = np.zeros((image_width+n-1, num_images))
column_correlations = np.zeros(((image_width-n)*2-1, num_images-1))

filtered_row_sums = np.zeros((image_height+n-1, num_images))
row_correlations = np.zeros(((image_height-n)*2-1, num_images-1))

for i in range(0, num_images):
	filtered_column_sums[:,i] = sig.convolve(column_sums[i,:],a)
	filtered_row_sums[:,i] = sig.convolve(row_sums[i,:],a)

for i in range(0, num_images - 1):
	column_correlations[:,i] = np.correlate(filtered_column_sums[n-1:-n,i], filtered_column_sums[n-1:-n,i+1], mode='full')
	row_correlations[:,i] = np.correlate(filtered_row_sums[n-1:-n,i], filtered_row_sums[n-1:-n,i+1], mode='full')

# this gives frame by frame column offsets (linear speed). prone to error.
column_offsets = np.argmax(column_correlations,axis=0) - (image_width - n - 1)

# this gives frame by frame row offsets (vertical camera shake). prone to error.
row_offsets = np.argmax(row_correlations,axis=0) - (image_height -n - 1)

new_image = np.zeros((image_height, num_images*cols_per_image, 3), dtype=np.uint8)

for i in range(0, image_width):
	# progress display
	for i in range(0, image_width_digits+1):
		print("\b"),
	print("Processing column " + str(i).zfill(image_width_digits)),
	
	for j in range(0, num_images):
		new_image[:, j*cols_per_image:(j+1)*cols_per_image, :] = all_images[j, :, i:i+cols_per_image, :]
	imsave("/Users/loganw/Desktop/trees/c_" + str(i) + ".jpg", new_image)
