import image_preparer
import argparse
import cv2
from sklearn import random_projection


image_preparer.crop_seeds
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

origin = args["image"]
image_preparer.crop_seeds(origin)

crop = cv2.imread("crop.jpg")
image_preparer.show_img("poo", crop)
