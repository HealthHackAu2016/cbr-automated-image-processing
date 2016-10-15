import cv2
import numpy as np
import imutils
import shapedetector
from skimage import io


def image_show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def image_write(path, img):
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
    ret,thresh = cv2.threshold(gray,60,255,0)
    contours,contours,hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)

    height, width, _ = img.shape

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w>150 and h>100 and w<600 and h<400 and x>width/2.5 and y>height/2:
            cropped = img[y:y+h, x:x+w]
            cv2.imwrite("123.jpg", cropped)

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


def find_brightest_spot(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_show("evaev", gray)
    (minVal, maxVal, minLoc, maxloc) = cv2.minMaxLoc(gray)
    print(minLoc)
    print(minVal)


def rescale(img, fixed_size):
    width, height, channels = img.shape

    # gets image and size of current image
    rectangle = crop_colours(img)
    widthr, heightr, channelsr = rectangle.shape

    # can be changed, fixes size of small rectangle
    r = fixed_size / widthr
    dim = (fixed_size, int(height * r))

    # perform the actual resizing of the image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def brighten(img, value):
    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # change each pixel by value
    hsv[:, :, 2] += value
    # reconvert to image
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img
