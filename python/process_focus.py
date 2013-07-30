import numpy as np
from scipy.misc import imread, imsave
import scipy.signal as sig
import math
from load_images import *
import scipy.ndimage.interpolation

num_images =  488;
start_image = 1
image_width = 1920
image_height = 1080
cols_per_image = 10;
image_path = "/Users/loganw/Desktop/trees/"
image_name = "trees "
output_name = "f_"
format = ".jpg"

all_images = load_images_into_memory(image_path, image_name, format, num_images, start_image)

print "Done loading images. Calculating statistics. This may take a while."
'''
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
'''

image_sized_ones = np.ones((image_height, image_width, 3), dtype=np.dtype('uint8'))
output_image = np.zeros((image_height, image_width, 3), dtype=np.dtype('uint8'))

for i in np.arange(0.5, 19.5, 1):
	print "Saving image " + str(i) + "/20" 

	new_image = np.zeros((image_height, image_width+i*(num_images-1), 3), dtype=np.dtype('uint32'))
	scale_factor = np.zeros((image_height, image_width+i*(num_images-1), 3), dtype=np.dtype('uint16'))

	for j in range(0,num_images):
		new_image[:,j*i:j*i+image_width,:] = new_image[:,j*i:j*i+image_width,:] + all_images[j,:,:,:]
		scale_factor[:,j*i:j*i+image_width,:] = scale_factor[:,j*i:j*i+image_width,:] + image_sized_ones
	
	new_image = np.divide(new_image,scale_factor)

	scipy.ndimage.interpolation.zoom(new_image, (1.0, (float(image_width)/float(image_width+i*(num_images-1))), 1.0), output=output_image)
	imsave(image_path + output_name + str(i) + format, output_image)

