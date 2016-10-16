import image_preparer
import colour_picking
import argparse
import colour_picking
import cv2
import sys
import matplotlib.pyplot as plt
import stats

# Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Read and Show original file
img = cv2.imread(args["image"])
image_preparer.image_show("original", img)

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
image_preparer.image_show("colour", colour_rect)

# Get max white colour on colour card
max_white = colour_picking.get_max_rgb(colour_rect)

# Detect 1px = mm
pixel_mm = image_preparer.length_per_pixel(colour_rect)
print(pixel_mm)

# Brighten based on max_white
# BRIGHTEN

# using CLAHE brightness
brightness = image_preparer.brightness_auto(img)
image_preparer.image_show("brightness filter...", brightness)

# histogram equalisation GREYSCALE: proof of concept
# image_preparer.image_show("hist eq", image_preparer.brightness_hist(brightness))

# Detect circle and crop
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.image_show("Circle crop", crop)
    # Write image
    # image_preparer.image_write("crop.jpg", crop)
else:
    print("No seed circle detected. Exiting...")
    sys.exit(0)

canny = cv2.Canny(crop, 100, 300)
image_preparer.image_show("canny", canny)


warray = []
larray = []
for img in images:
    if (area(img)/(pixel_mm*pixel_mm))<=30:
        (w,l) = rice_stats.widthAndHeight(rice_stats.imageFromContour(cnt),20)
        warray.append(w/pixel_mm)
        larray.append(l/pixel_mm)
data = [larray, warray]    

test = [[1,2,3,4,5,6,7,8,9,5,7,3,4],[8,2,4,6,4,2,1,3,10,3,4,5,2]]

stats.create_hist(test)


