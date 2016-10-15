import cv2
import numpy as np


def image_show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
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


def crop_seeds(img):
    # load the image, clone it for output, and then convert it to grayscale
    output = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect circles in the img
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 100, param1=350, param2=500, minRadius=100)
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
