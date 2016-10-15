import numpy as np
import cv2
from matplotlib import pyplot as plt


def watershed(img):
    # threshold filter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("thresh 1", thresh)

    # noise removal
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imshow("opening morph", opening)

    # sure background and foreground area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 3)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
    cv2.imshow("sure_bg", sure_bg)
    cv2.imshow("sure_fg", sure_fg)

    # find unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    cv2.imshow("unknown", unknown)

    # marker labelling and add labels
    ret, markers = cv2.connectedComponents(sure_fg)
    markers += 1
    markers[unknown==255] = 0

    # WATERSHED
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [0, 255, 0]
    return img


def watershed_looper(img):
    return watershed(img)
    """x = 0
    while x <= 3:
        result = watershed(result)
        x += 1
    return result"""
