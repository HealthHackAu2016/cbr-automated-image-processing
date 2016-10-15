import image_preparer
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

"""
Proposed Method:
    1. Detect colour card and return crop
    2. Brighten image based on colour card white square
    3. Scale image based on size of colour card
    4. Detect seeds and crop
    5. Apply segmentation and count for seeds
    6. Profit?
"""

# using CLAHE brightness
brightness = image_preparer.brightness_auto(img)
image_preparer.image_show("brightness filter...", brightness)

# histogram equalisation
image_preparer.image_show("hist eq", image_preparer.brightness_hist(brightness))

# Cropping for circle
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.image_show("Circle crop", crop)
else:
    print("No seed circle detected")

image_preparer.image_write("crop.jpg", crop)

canny = cv2.Canny(crop, 100, 300)
image_preparer.image_write("canny.jpg", canny)
image_preparer.image_show("canny", canny)