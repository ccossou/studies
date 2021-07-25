#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Version : 1.0
Date    : 23 août 2011
To run the script, assuming the script is named "test.py" in the current working directory, one might use :
$ gimp -idf --batch-interpreter python-fu-eval -b 'import sys; sys.path=["."]+sys.path;import scantrad;scantrad.run(".")' -b 'pdb.gimp_quit(1)'

From windows, the command is:
E:\GIMP 2\bin\gimp-console-2.10.exe --verbose --batch "(python-fu-gimp-autoclean.py RUN-NONINTERACTIVE)" --batch "(gimp-quit 0)
"E:\GIMP 2\bin\gimp-console-2.10.exe" -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path;import ${1%.py};${1%.py}.run('.')" -b "pdb.gimp_quit(1)"

HOW TO :
    pygimp xcf_to_png.py
    This will search into all the subdirectories of the current working directory for .xcf files and export them as .png in a directory named 'png' in the CWD. In this 'png' folder, a subdirectory will be created for each subdirectory of the CWD

NOTE : pygimp is the name of a bash script that contain:
#!/bin/bash
gimp -idf --batch-interpreter python-fu-eval -b "import sys; sys.path=['.']+sys.path;import ${1%.py};${1%.py}.run('.')" -b "pdb.gimp_quit(1)"
"""
from __future__ import print_function

import os
import glob
import time
from gimpfu import *
import shutil

__author__ = "Autiwa <autiwa@gmail.com>"
__date__ = "23 août 2011"
__version__ = "$Revision: 1.0 $"
__credits__ = """Script that help cleaning a .jpg page. This currently
doesn't work well with a large noisy RAW (but it's ok with smaller
ones I think"""

# Prefix of the subdirectories we want to search into
FOLDER_PREFIX = "Tome"


def process(infile, processed_dir=None):
    """
    Auto clean the file given in parameter, then save it in another folder

    infile: path/lastdir/filename.png
    outfile: path/jpg/lastdir/filename.png

    :param str infile: path to an image
    :param str processed_dir: [optional] Directory that will contains all output file (reproducing the same structure
                              only 1st dir level)
    """

    if processed_dir == None:
        processed_dir = 'processed'

    print("Processing file %s " % infile)

    # Loading the file. We also get the current active layer of the image loaded (in fact, 
    # since it's a .jpg, this must be the right layer)
    image = pdb.gimp_file_load(infile, infile)
    drawable = pdb.gimp_image_get_active_layer(image)

    print("File %s loaded OK" % infile)

    # We want to store outfile in the parent_dir "processed" of the current working directory
    full_path, file = os.path.split(infile)
    base_path, parent_dir = os.path.split(full_path)
    (basename, ext) = os.path.splitext(file)  # We get the filename without the extension

    # We recreate the same structure in another folder in the parent dir of all volumes
    out_folder = os.path.join(base_path, processed_dir, parent_dir)

    # We create a parent_dir in the output directory if it doesn't exist yet.
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    # Only autoclean images that are in grayscale
    if pdb.gimp_drawable_is_gray(drawable):

        pdb.gimp_levels_stretch(drawable)

        # manual correction of levels.
        pdb.gimp_levels(drawable, 0, 20, 220, 1.0, 0, 255)

        # # First we want to select the whites.
        # pdb.gimp_image_set_active_layer(image, drawable)
        # pdb.gimp_selection_none(image)
        #
        # pdb.gimp_by_color_select (drawable, (220, 220, 220), 30,2,False,False,0,False)
        # pdb.gimp_selection_shrink (image,5)
        # pdb.gimp_selection_grow (image,5)
        #
        # pdb.gimp_image_set_active_layer(image, drawable)
        # pdb.gimp_palette_set_foreground ((255, 255, 255))
        # pdb.gimp_bucket_fill(drawable, 0, 0, 100, 10, 0, 0, 0)
        #
        # # We do the same for black
        # pdb.gimp_image_set_active_layer(image, drawable)
        # pdb.gimp_selection_none(image)
        #
        # pdb.gimp_by_color_select (drawable, (10, 10, 10), 15,2,False,False,0,False)
        # pdb.gimp_selection_shrink (image,5)
        # pdb.gimp_selection_grow (image,5)
        #
        # pdb.gimp_image_set_active_layer(image, drawable)
        # pdb.gimp_palette_set_foreground ((0, 0, 0))
        # pdb.gimp_bucket_fill(drawable, 0, 0, 100, 10, 0, 0, 0)
        #
        # pdb.gimp_selection_none(image)

        # pdb.gimp_convert_indexed(image, 0, 0, 16, 0, 0, '')

        # We save in a .jpg file
        outfile_jpg = os.path.join(out_folder, basename + '.jpg')

        # We merge the image before export into bitmap
        drawable = pdb.gimp_image_merge_visible_layers(image,
                                                       EXPAND_AS_NECESSARY)  # EXPAND_AS_NECESSARY, CLIP_TO_IMAGE, CLIP_TO_BOTTOM_LAYER

        print("Saving to %s" % outfile_jpg)
        pdb.file_jpeg_save(image, drawable, outfile_jpg, outfile_jpg, "0.85", 0, 1, 0, "", 0, 1, 0, 0)

        print("Ok")

        pdb.gimp_image_delete(image)
    else:
        outfile = os.path.join(out_folder, file)
        shutil.copyfile(infile, outfile)


def run(directory):
    start = time.time()
    print("Running on directory '%s'" % directory)
    volumes = [d for d in os.listdir(".") if (os.path.isdir(d) and d.count(FOLDER_PREFIX))]
    print(volumes)

    if not (os.path.exists('jpg')):
        os.mkdir('jpg')

    for volume in volumes:
        print("subdirectory : " + volume)
        for infile in glob.glob(os.path.join(directory, volume, '*.jpg')):
            process(infile)
        # ~ print(infile)
    end = time.time()
    print("Finished, total processing time: %.2f seconds" % (end - start))

if __name__ == "__main__":
    # print("Running as __main__ with args: %s" % sys.argv)
    run("G:/Manga/Dragon_Ball_tmp")

