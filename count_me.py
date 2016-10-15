import cv2
import numpy as np


def count_seeds1(croplocation):
    # setting up
    image = cv2.imread(croplocation, 0)
    h, w = image.shape[:2]
    diff = (3, 3, 3)
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(image, mask, (0,0), (255,255,255), diff, diff)
    image = cv2.Canny(image, 100, 300)

    # scan image and count
    ricecount = 0
    oldlinecount = 0
    for y in range(0, h):
        oldc = 0
        linecount = 0
        start = 0
        for x in range(0, w):
            c = image[y, x] < 128;
            if c == 1 and oldc == 0:
                start = x
            if c == 0 and oldc == 1 and (x - start) > 10:
                linecount += 1
            oldc = c
        if oldlinecount != linecount:
            if linecount < oldlinecount:
                ricecount += oldlinecount - linecount
            oldlinecount = linecount
    return ricecount


def count_seeds3(croplocation):
    image = cv2.imread(croplocation, 0)
    image = cv2.medianBlur(image, 3)
    bw = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    bw = cv2.dilate(cv2.erode(bw, kernel), kernel)
    return np.round_(np.sum(bw == 0) / 3015.0)