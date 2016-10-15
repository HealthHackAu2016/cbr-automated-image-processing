import image_preparer
import image_segment
import colour_picking
import argparse
import colour_picking
import cv2
import sys

# Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Read and Show original file
img = cv2.imread(args["image"])
image_preparer.show("original", img)

"""
Proposed Method:
    1. Detect colour card and return crop
    2. Brighten image based on colour card white square
    3. Scale image based on size of colour card
    4. Detect seeds and crop
    5. Apply segmentation and count for seeds
    6. Profit?
"""

# Cropping the colour card rectangle
colour_rect = image_preparer.crop_colours(img)
image_preparer.show("colour", colour_rect)

# Get max white colour on colour card
max_white = colour_picking.get_max_rgb(colour_rect)

# Detect 1px = mm
pixel_mm = image_preparer.length_per_pixel(colour_rect)
print(pixel_mm)

# Brighten based on max_white
brightness = image_preparer.brighten(img, max_white)
image_preparer.show("brighten by allen", brightness)

# using CLAHE brightness
brightness = image_preparer.brightness_auto(brightness)
image_preparer.show("CLAHE brightness filter...", brightness)

# Detect circle and crop
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.show("Circle crop", crop)
else:
    print("No seed circle detected. Exiting...")
    sys.exit(0)

# Create copy of crop, apply Otsu and Remove background
crop_copy = crop.copy()
bw = image_preparer.black_white(crop_copy)
image_preparer.show("bw", bw)
back_removed = image_preparer.remove_background(crop_copy, bw)
image_preparer.show("back removed", back_removed)

outlined = image_preparer.outline(back_removed)
image_preparer.show("outlined", outlined)

# Sharpen
# sharpen = image_preparer.sharpen(crop)
# image_preparer.show("sharpen", sharpen)

watershed = image_segment.watershed_looper(outlined)
watershed = image_preparer.show("watershed", watershed)
