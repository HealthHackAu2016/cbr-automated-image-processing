__author__ = 'Mohammad'

import numpy as np
import os
import argparse
import imutils
import cv2
import matplotlib.pylab as plt
from scipy import ndimage
from Detect_colorChecker import detect_card
import glob
from leafsegmentation import detectColorCard, extractColorCard
import colorbalance
from docopt import (docopt, DocoptExit)
from Color_correction import Color_correct_and_write




OPTS = """
USAGE:
    run_color_correction -i INPUT -o OUTPUT -c CARD
    run_color_correction -i INPUT -o OUTPUT -c CARD -v
    run_color_correction -i INPUT -o OUTPUT -c CARD -s  LOWER UPPER NUM
    run_color_correction -i INPUT -o OUTPUT -c CARD -s  LOWER UPPER NUM -v
    run_color_correction -h | --help
OPTIONS:
    -h --help   Show this screen
    -i INPUT    Path to input folder
    -o OUTPUT   Path to output folder
    -c CARD     Path to colorcard
    -s          if present, optional scaling of card template is done, for example with "-s 0.95 1.05 11", eleven different scales in the mentioned range are tested and best scale is selected. Without "-s", no scaling is performed.
    -v          if present, this means colorcard is placed vertically (i.e. colorcard is portrait and image is landscape or vice versa)
"""

def path_exists(x):
    """Validator for path field."""
    x = x.replace('\\', '/')
    if os.path.exists(x):
        return os.path.join(x, '', '')
    raise ValueError("path '%s' doesn't exist" % x)
	
def file_exists(x):
    """Validator for path field."""
    x = x.replace('\\', '/')
    if os.path.isfile(x):
        return x
    else:
        raise ValueError("file '%s' doesn't exist" % x)
        # return (False,x)
        
  
def main(input_dir,output_dir,card_path,vertical,lower,upper,num):
    try:
        input_dir = path_exists(input_dir)
        output_dir = path_exists(output_dir)
        card_path = file_exists(card_path)
        card = cv2.imread(card_path,0)
        Default_card_h = 100
        height_card = np.size(card,0)
        width_card = np.size(card,1)
        print(height_card, width_card)
        if height_card > width_card:
            card = np.rot90(card)
            height_card, width_card = width_card, height_card
        scale = Default_card_h/float(height_card)
     
        card = cv2.resize(card,(0,0), fx=scale, fy=scale)
        card = cv2.Canny(card, 40, 50)
        
        plt.imshow(card)
        plt.show()
        cv2.waitKey(0)
        
        for dirpath, dirnames, filenames in os.walk(input_dir):
            for f in filenames:
                full_output_name = os.path.join(dirpath.replace(input_dir,output_dir),f)
                print(os.path.join(dirpath.replace(input_dir,output_dir),f))
                if 'jpg' in f.lower():
                    fp = os.path.join(dirpath, f)
                    image_orig = cv2.imread(fp)
                    image_resized = cv2.resize(image_orig,(0,0), fx=scale, fy=scale)
                    height_image = np.size(image_resized,0)
                    width_image = np.size(image_resized,1)
                    if (height_image > width_image) & (vertical is False):
                        image_resized = np.rot90(image_resized)
                        image_orig = np.rot90(image_orig)
                    if (height_image < width_image) & (vertical is True):
                        image_resized = np.rot90(image_resized)
                        image_orig = np.rot90(image_orig)
                    Detected_card, Acc, SCALE = detect_card(image_resized,card,np.linspace(lower,upper,num))
                    Color_correct_and_write(Detected_card,image_orig,full_output_name, Acc)
                    plt.imshow(Detected_card)
                    plt.show()
                    # cv2.waitKey(0)
                #fp = os.path.join(dirpath, f)
    except ValueError as e:
        print ("Error on entry", e)
    

        
if __name__ == '__main__':
    opts = docopt(OPTS)
    print(opts)
    if opts["-v"]:
        vertical = True
    else:
        vertical = False
    if opts["-s"]:
        lower = float(opts["LOWER"])
        upper = float(opts["UPPER"])
        num = float(opts["NUM"])
    else:
        lower = 1
        upper = 1
        num = 1
    print
    main(str(opts["-i"]),opts["-o"],opts["-c"],vertical,lower,upper,num)
