import image_preparer
import colour_picking
import argparse
import cv2
import sys

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

# Detect scale for image from colour card rectanger
# rescaled_img = image_preparer.rescale(crop)

# Get white colour on colour card
#maxWhite = colour_picking.get_max_rgb(colour_rect)
#print(maxWhite)

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


