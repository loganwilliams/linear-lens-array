import numpy as np
from scipy.misc import imread, imsave
import scipy.signal as sig
import math

num_images = 32930 - 32582 + 1;
start_image = 32582
image_width = 1080
image_height = 1920
cols_per_image = 10;
image_path = "/Users/loganw/Desktop/rotation/"
image_name = "IMG_1095 "
output_name = "c_"
format = ".jpg"

digits = int(math.ceil(math.log(num_images+1,10)))
image_width_digits = int(math.ceil(math.log(image_width+1,10)))

print "Allocating " + str(num_images*image_width*image_height*3.0/(1024.0*1024*1024)) + " Gb of RAM"

# allocate 4-dimensional array for storing all images
all_images = np.zeros((num_images, image_height, image_width, 3), dtype=np.uint8)

# load all images into memory
for i in range(0, num_images):
	# progress display
	print "Loading image " + str(i) + "/" + str(num_images)
	
	all_images[i, :, :, :] = imread(image_path + image_name + str(i+start_image).zfill(5) + format)

print "Done loading images. Calculating statistics. This may take a while."

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
column_offsets = np.clip(column_offsets, -10, 10)

# this gives frame by frame row offsets (vertical camera shake). prone to error.
row_offsets = np.argmax(row_correlations,axis=0) - (image_height -n - 1)
row_offsets = np.clip(row_offsets, -10, 10)

np.savetxt(image_path + "column_offsets.txt", column_offsets)
np.savetxt(image_path + "row_offsets.txt", row_offsets)

cols_per_image = int(np.mean(column_offsets))

if (cols_per_image == 0):
	cols_per_image = 5

#print "Using column offset of " + str(cols_per_image) + " pixels"

column_offsets *= 2

for i in range(0, num_images-1):
	if (column_offsets[i] == 0):
		column_offsets[i] = 1

new_image = np.zeros((image_height, np.sum(np.absolute(column_offsets)), 3), dtype=np.uint8)

print "New image width: " + str(np.sum(np.absolute(column_offsets)))

for i in range(0, image_width-np.max(np.absolute(column_offsets))):
	# progress display
	print "Processing column " + str(i) + "/" + str(image_width)
	index = 0

	for j in range(0, num_images-1):
		cols_per_image = column_offsets[j]

		if (cols_per_image > 0):
			new_image[:, index:(index+cols_per_image), :] = all_images[j, :, i:i+cols_per_image, :]
		elif (cols_per_image < 0):
			new_image[:, index:(index+(cols_per_image*-1)), :] = np.fliplr(all_images[j, :, i:i+(-1*cols_per_image), :])

		index += abs(cols_per_image)

	imsave(image_path + output_name + str(i) + format, new_image)
