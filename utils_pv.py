"""
Collection of small utils to create figures with PyVista:
    - Step nice default parameters.
    - Trim the output PNG files.
"""

__author__ = "Thomas Guillod"
__copyright__ = "Thomas Guillod - Dartmouth College"
__license__ = "Mozilla Public License Version 2.0"

import pyvista as pv
import PIL.Image as img


def set_global():
    """
    Set the global PyVista options.
    """

    pv.global_theme.transparent_background = True
    pv.global_theme.show_scalar_bar = False


def get_crop(filename, margin=0):
    # open the image
    input_img = img.open(filename)

    # get the bounding box and crop
    bbox = input_img.getbbox()
    image = input_img.crop(bbox)

    # get the new size
    (width, height) = image.size

    # create the new image
    output_img = img.new("RGBA", (width + 2 * margin, height + 2 * margin), (0, 0, 0, 0))

    # add the cropped image with the margin as offset
    output_img.paste(image, (margin, margin))

    # overwrite the original image
    output_img.save(filename)
