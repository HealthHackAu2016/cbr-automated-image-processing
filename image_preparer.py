import cv2
import numpy as np
import imutils
from skimage import io


def show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def write(path, img):
    cv2.imwrite(path, img)
    return


def brightness_hist(img):
    # get gray-scale copy
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    return equ


def brightness_auto(img):
    # convert into lab
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # split into channels
    l, a, b = cv2.split(lab)
    # apply clahe to L
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    # merge L-channel with A and B
    limg = cv2.merge((cl, a, b))
    # return result
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def crop_colours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,60,255,0)
    contours, contours, hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)
    height, width, _ = img.shape

    cropped = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w>150 and h>100 and w<600 and h<400 and x>width/2.5 and y>height/2:
            cropped = img[y:y+h, x:x+w]
    return cropped


def crop_seeds(img):
    # load the image, clone it for output, and then convert it to grayscale
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect circles in the img
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 200, param1=300, param2=500, minRadius=200)
    cropped = None

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output img, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 0, 255), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cropped = img[y-r:y+r, x-r:x+r]

    # write cropped img and show the output img
    return cropped


# returns in mm
def length_per_pixel(rectangle_image):
    # length is given to be 3 inches
    length_of_pixel = (3 * 25.4) / rectangle_image.shape[0]
    return length_of_pixel


def brighten(img, max_rgb):
    # convert original image to BGR HSV
    convert_colour = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_change = 255 - max_rgb[2]
    green_change = 255 - max_rgb[1]
    blue_change = 255 - max_rgb[0]

    difference_in_brightness = 0.2126 * red_change + 0.7152 * green_change + 0.0722 * blue_change

    # change each pixel by value
    convert_colour[2, :, :] += int(difference_in_brightness)
    # reconvert to image
    img = cv2.cvtColor(convert_colour, cv2.COLOR_HSV2BGR)
    return img


def sharpen(img):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)
    return sharpened


def black_white(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bw_image = cv2.threshold(gray_image, 80, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return bw_image


def remove_background(img, bw_image):
    for i in range(0, img.shape[0]):
        for j in range (0, img.shape[1]):
            if np.any(bw_image[i][j] == 255):
                img[i][j] = [255, 255, 255]
    return img
