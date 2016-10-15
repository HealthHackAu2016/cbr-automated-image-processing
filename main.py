import image_preparer
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])


# using CLAHE
brightness = image_preparer.brightness_auto(img)
image_preparer.image_show("brightness filter...", brightness)

# histogram equalisation
image_preparer.image_show("hist eq", image_preparer.brightness_hist(brightness))


# Cropping for circle
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.image_show("Circle crop", crop)

canny = cv2.Canny(crop, 200, 600)
image_preparer.image_show("canny", canny)
