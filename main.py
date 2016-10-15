import image_preparer
import image_segment
import numpy as np
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
image_preparer.write("results/1-original.jpg", img)

"""
Proposed Method:
    1. Detect colour card and return crop
    2. Brighten image based on colour card white square
    3. Scale image based on size of colour card
    4. Detect seeds and crop
    5. Apply segmentation
    6. Cut each segment invidually
    7. Measure statistics
    8. ??? Profit ???
"""

# Cropping the colour card rectangle
colour_rect = image_preparer.crop_colours(img)
image_preparer.show("colour", colour_rect)
image_preparer.write("results/2-cropped-colour-card.jpg", colour_rect)

# Get max white colour on colour card
max_white = colour_picking.get_max_rgb(colour_rect)
print("Maximum White on Colour Card: ")
print(max_white)

# Detect 1px = mm
pixel_mm = image_preparer.length_per_pixel(colour_rect)
print("1px = "+str(pixel_mm)+"mm")

# Brighten based on max_white
brightness = image_preparer.brighten(img, max_white)
image_preparer.show("brighten by allen", brightness)
image_preparer.write("results/3-subtle-brightness.jpg", brightness)

# using CLAHE brightness
brightness = image_preparer.brightness_auto(brightness)
image_preparer.show("CLAHE brightness filter...", brightness)
image_preparer.write("results/4-clahe-brightness.jpg", brightness)

# Detect circle and crop
crop = image_preparer.crop_seeds(brightness)
if crop is not None:
    image_preparer.show("Circle crop", crop)
    image_preparer.write("results/5-seed-circle.jpg", crop)
else:
    print("No seed circle detected. Exiting...")
    sys.exit(0)

# Create copy of crop, apply Otsu and Remove background
crop_copy = crop.copy()
bw = image_preparer.black_white(crop_copy)
image_preparer.show("bw", bw)
image_preparer.write("results/6-threshold-filter.jpg", bw)

back_removed = image_preparer.remove_background(crop_copy, bw)
image_preparer.show("back removed", back_removed)
image_preparer.write("results/7-background-removed.jpg", back_removed)

outlined = image_preparer.outline(back_removed)
image_preparer.show("outlined", outlined)
image_preparer.write("results/8-outline-image.jpg", outlined)

"""
# Do stuff
removed_edge = image_preparer.remove_edge(back_removed)
image_preparer.show("asd", removed_edge)


width = removed_edge.shape[0]
height = removed_edge.shape[1]
count = 0

for i in range(2, width-2):
    for j in range(2, height-2):
        if (np.any(removed_edge[i][j]) != 255):
            new_array = image_preparer.initialise_white_array(5000)
            image_preparer.get_segment_image(removed_edge, new_array, i, j, 0, 250)
            image_preparer.show("seed crop", new_array)
            # FIXME save the 2d array into an image or array, using count
            count += 1


# Sharpen
# sharpen = image_preparer.sharpen(crop)
# image_preparer.show("sharpen", sharpen)
watershed = image_segment.watershed_looper(outlined)
watershed = image_preparer.show("watershed", watershed)

array = [[]]
for cnt in contours:
    row = rice_stats.widthAndHeight(rice_stats.imageFromContour(cnt),20)
    array.append(row)
table = pd.DataFrame(array,columns=["Length","Width"])
"""