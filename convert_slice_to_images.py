import os
import segyio
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageEnhance

def normalize(slice_data):
    slice_data /= max(np.abs(slice_data.min()), np.abs(slice_data.max()))
    slice_data = slice_data / 2 + 0.5
    return slice_data

def save_image(slice_data):
        image = color_map(data)[:,:,:3]
        image = Image.fromarray(np.uint8(image *255))
        image = ImageEnhance.Contrast(image).enhance(1.2)
        image.save(os.path.join(path_to_save, key+'_'+str(slice)+'.png'))

if __name__ == "__main__":
    path_to_dataset = r''
    path_to_save = r''
    if not os.path.isdir(path_to_save):
        os.makedirs(path_to_save)

    # Define the colormap for the saved images
    color_map = plt.cm.seismic
    #This one you need to edit 
    #Select slices to convert
    slices_to_save = {'inline': [50, 200, 250], 'xline': [50, 300, 600]}

    with segyio.open(path_to_dataset) as segyfile:
        # Memory map file for faster reading (especially if file is big...)
        segyfile.mmap()

        for key in slices_to_save:
            for slice in slices_to_save[key]:
                data = segyfile.iline[segyfile.ilines[slice]] if (key=='inline') else segyfile.xline[segyfile.xlines[slice]]
                data = normalize(data.T)
                save_image(data)
