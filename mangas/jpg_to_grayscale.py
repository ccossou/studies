"""
Script to open scans that have 2 pages, and will split them into single pages, using auto detection
of the transition between one page and the other

"""
import imageio
import os
import glob
import numpy as np


def is_grayscale(image):
    """
    If RGB, will test if this can safely be saved into grayscale without loss

    :param ndarray image:
    :return: if the image can be saved as grayscale or not
    :rtype: bool
    """

    if image.ndim == 2:
        return True
    else:
        # All diffs must be 0 for the image to be grayscale
        diff = np.diff(image, axis=2)
        return not np.any(diff)


def save_to_grayscale(filenames, overwrite=True):
    """

    :param filenames: list of filenames
    :type filenames: list(str)
    :param int volume_number:
    :param str output_folder:
    :param bool japan_read: If True, the first page of the double page will be the one on the right
    :param bool overwrite: By default, any existing image will be overwritten
    :return:
    """

    nb_files = len(filenames)
    idx = 0
    for filename in filenames:
        idx += 1
        # print(f"Process {filename}")
        # print(f"\rProcessing page {filename}      ", end="\n")
        im = imageio.imread(filename)

        grayscale = is_grayscale(im)

        # Convert into greyscale (height, width)
        # if grayscale and im.ndim == 3:
        if im.ndim == 3:
            print(f"Conversion of {filename} ({idx}/{nb_files})")
            im = im.mean(axis=2).astype("uint8")
            os.remove(filename)
            imageio.imsave(filename, im)
        else:
            continue

    #     # Force conversion to uint8 because the mean transform it into float
    #     # For an unknown reason, adding dtype into the mean mess things up
    #     im = im.astype("uint8")
    #
    #
    #     out_file = os.path.join(output_folder, f"T{volume_number:02d}_page_{page_number:03d}.png")
    #     # https://imageio.readthedocs.io/en/stable/format_png-pil.html
    #
    #     if os.path.isfile(out_file) and overwrite:
    #         os.remove(out_file)
    #
    #     imageio.imsave(out_file, im)
    #     page_number += 1
    #
    # print(f"\rFinished writting {page_number-1} pages.                       ")

japan_read = False  # If false, first page is the left one, else it's the right one
input_folder = "G:/Manga/Dragon Ball Z"
output_folder = "G:/Manga/Dragon_Ball_tmp"

# for volume_number in range(1, 43):
# print(f"Processing Volume {volume_number:02d}")
files = glob.glob(os.path.join(input_folder, f"**", "*.jpg"))

# Get rid of all first pages
files = [f for f in files if "-000" not in f]

save_to_grayscale(files)

# Double page: (1061, 1292)
# single page: (1063, 650)