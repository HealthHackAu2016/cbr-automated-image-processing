import image_preparer
import colour_picking
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

'''
# using CLAHE
brightness = image_preparer.brightness_auto(img)
image_preparer.image_show("brightness filter...", brightness)

# histogram equalisation
image_preparer.image_show("hist eq", image_preparer.brightness_hist(brightness))


# Cropping for circle
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.image_show("Circle crop", crop)

canny = cv2.Canny(crop, 100, 300)
image_preparer.image_show("canny", canny)
'''

print(colour_picking.get_max_rgb(img))

numrows = len(img)
numcols = len(img[0])

for i in range(numcols):
    for j in range(numcols):
        print(img[i][j])


image_preparer.image_show("reduced", img)



