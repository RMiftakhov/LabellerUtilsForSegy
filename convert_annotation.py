import os

import numpy as np
import segyio
from image_labelling_tool import labelled_image

if __name__ == "__main__":
    path_to_dataset = r''
    path_to_load = r''

    #This one you need to edit 
    #Select slices to load from annotation files
    slices_to_load = {'inline': [50, 200, 250], 'xline': [50, 300, 600]}
    train_slice = []
    train_segmentation = []

    with segyio.open(path_to_dataset) as segyfile:
        # Memory map file for faster reading (especially if file is big...)
        segyfile.mmap()

        for key in slices_to_load:
            for slice in slices_to_load[key]:

                data = segyfile.iline[segyfile.ilines[slice]] if (key=='inline') else segyfile.xline[segyfile.xlines[slice]]
                labelled_images = labelled_image.LabelledImage.for_directory(path_to_load, image_filename_patterns=[key+'_'+str(slice)+'.png'])[0]
                image_shape = labelled_images.image_source.image_size
                print('image_shape={}'.format(image_shape))
                labels = labelled_images.labels
                segmentation = labels.render_label_classes(label_classes={'F1' : 1, 'F2' : 2, 'F3' : 3}, image_shape=image_shape).T

                train_slice.append(data)
                train_segmentation.append(segmentation)

    print(train_slice)
    print(train_segmentation)