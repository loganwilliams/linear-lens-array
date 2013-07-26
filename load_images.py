import math
from scipy.misc import imread
import numpy as np

def load_images_into_memory(image_path, image_name, format, num_images, start_image):
	digits = int(math.ceil(math.log(start_image + num_images+1,10)))

	a = imread(image_path + image_name + str(start_image).zfill(digits) + format)
	(image_height, image_width, image_depth) = a.shape

	print "Allocating " + str(num_images*image_width*image_height*3.0/(1024.0*1024*1024)) + " Gb of RAM"

	# allocate 4-dimensional array for storing all images
	all_images = np.zeros((num_images, image_height, image_width, 3), dtype=np.uint8)

	# load all images into memory
	for i in range(0, num_images):
		# progress display
		print "Loading image " + str(i) + "/" + str(num_images)

		all_images[i, :, :, :] = imread(image_path + image_name + str(i+start_image).zfill(digits) + format)

	return all_images
