import numpy as np
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar



source_file = "example_source"

source = np.load(source_file + ".npy")

# print(np.shape(source))

pixels = np.shape(source)[0]
print(pixels)

scalebar = ScaleBar(0.5, "mm")
scalebar2 = ScaleBar(0.5, "mm")

# cross sectional weighted area
# cross_section_area_mm2 = 78.46 # for LYSO 1 sigma binary
# cross_section_area_mm2 = 7.06 # for LYSO 1 sigma binaryt 1 sigma norm long
cross_section_area_mm2 = 5.4 # for LAB 2 gaussian 1mm spatial
# cross_section_area_mm2 = 25.1 # for LAB 2 binary 1mm spatial
# cross_section_area_mm2 = 55.7 # for LAB 2 gaussian 3.2mm spatial
# cross_section_area_mm2 = 0.557 # for LAB 2 gaussian 0.32mm spatial
# cross_section_area_mm2 = 0.054 # for LAB 2 gaussian 0.1mm spatial

if (len(np.shape(source)) > 2):
    image = source[:,:,slice]
else:
    image = source.reshape((pixels,pixels))

fig, pre = plt.subplots()
pre_ = pre.imshow(image / cross_section_area_mm2, cmap='gray')
# pre_ = pre.imshow(np.log(image+1 + second_image), cmap='gray')
pre_bar = plt.colorbar(pre_)
pre.add_artist(scalebar)



plt.show()

