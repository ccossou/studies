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


def split_volume_pages(filenames, volume_number, output_folder=None, japan_read=False, overwrite=True):
    """

    :param filenames: list of filenames
    :type filenames: list(str)
    :param int volume_number:
    :param str output_folder:
    :param bool japan_read: If True, the first page of the double page will be the one on the right
    :param bool overwrite: By default, any existing image will be overwritten
    :return:
    """

    if output_folder is None:
        output_folder = "."

    # Create output folder if it doesn't exist
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    cover_page = True  # Flag to prevent first page to be split
    page_number = 1
    for filename in filenames:
        print(f"\rProcessing page {filename}      ", end="")
        im = imageio.imread(filename)

        grayscale = is_grayscale(im)

        if im.ndim == 2:
            (height, width) = im.shape
        elif im.ndim == 3:
            (height, width, dummy) = im.shape
        else:
            ValueError(f"Unexpected file format for {filename} (ndim = {im.ndim})")

        # Convert into greyscale (height, width)
        if grayscale and im.ndim == 3:
            im = im.mean(axis=2)

        # Force conversion to uint8 because the mean transform it into float
        # For an unknown reason, adding dtype into the mean mess things up
        im = im.astype("uint8")

        double_page = False
        # Cover page is never a double page, even if larger
        # We don't split color images because double page in color are generally one big image.
        if not cover_page and width > height and grayscale:
            double_page = True

        pages = []
        if not double_page:
            pages.append(im)
        else:
            # new value come from JapFlap scantrad ratio ; old: 0.6857142857142857
            new_width = int(height * 0.68518518518)

            left_page = im[:, :new_width]
            right_page = im[:, width - new_width:]

            if japan_read:
                pages.append(right_page)
                pages.append(left_page)
            else:
                pages.append(left_page)
                pages.append(right_page)

        for page in pages:
            out_file = os.path.join(output_folder, f"T{volume_number:02d}_page_{page_number:03d}.png")
            # https://imageio.readthedocs.io/en/stable/format_png-pil.html

            if os.path.isfile(out_file) and overwrite:
                os.remove(out_file)

            imageio.imsave(out_file, page)
            page_number += 1

        # After the first loop, all other pages are not a cover page
        cover_page = False
    print(f"\rFinished writting {page_number-1} pages.                       ")

japan_read = False  # If false, first page is the left one, else it's the right one
input_folder = "G:/Manga/Dragon Ball"
output_folder = "G:/Manga/Dragon_Ball_tmp"

for volume_number in range(1, 43):
    print(f"Processing Volume {volume_number:02d}")
    files = glob.glob(os.path.join(input_folder, f"T{volume_number}", "*.png"))
    files.sort()

    split_volume_pages(files, volume_number, output_folder=os.path.join(output_folder, f"T{volume_number:02d}"))

# Double page: (1061, 1292)
# single page: (1063, 650)