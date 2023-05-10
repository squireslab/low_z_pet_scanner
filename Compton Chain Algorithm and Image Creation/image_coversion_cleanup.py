import numpy as np


# source_file = "image_file_name"


# pixels = 440

source_image = np.loadtxt(source_file + ".data")

print(np.shape(source_image))
pixels = int(np.sqrt(np.shape(source_image)[0]))
if (len(np.shape(source_image)) == 1):
    source_image = source_image.reshape((pixels,pixels))
else:
    source_image = source_image.reshape((pixels,pixels,np.shape(source_image)[1]))


print(np.shape(source_image))


np.save(source_file, source_image)
