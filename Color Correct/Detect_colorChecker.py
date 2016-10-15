__author__ = 'Mohammad'

import numpy as np
import argparse
import imutils
import glob
import cv2
import matplotlib.pylab as plt
from scipy import ndimage

# this function searches for color card ('card') in the image ('img').
# The sizes of 'card' and the card in the image are assumed to be almost similar (scale factors in [0.9,1.1] are tested)
# 'orient' is the Oreintation of the image which
# 0<'scale'<=1 is to control the speed (and also accuracy) of detecting the color checker. when it is '1', 'iamge' and the 'card' are
# processed unchanged. Otherwise, they are resized accordingly.

def detect_card(img_orig,card,search_scale):
    '''
    v = np.median(card_orig)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    card = cv2.Canny(card_orig, lower, upper)
    '''
    #plt.imshow(card)
    #plt.show()
    #cv2.waitKey(0)
    img = img_orig
    (H_card, W_card) = card.shape[:2]
    (H_img, W_img) = img.shape[:2]
    (H_orig, W_orig) = img_orig.shape[:2]

    img_cropped = img
    orig_cropped = img_orig
    
    gray = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2GRAY)
    gray = cv2.Canny(gray,40,50)
    #card = cv2.Canny(card,lower,upper)

    plt.imshow(gray)
    plt.show()
    #cv2.waitKey(0)
    found = None
    #[-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3]
    for degree in [-2,-1.5,-1,-0.5,0,0.5,1,1.5,2]:
        #card_rot = ndimage.rotate(card, degree)
        gray_rot = ndimage.rotate(gray, degree)
        for scale2 in search_scale:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(gray_rot, width = int(gray.shape[1] * scale2))
            r = gray_rot.shape[1] / float(resized.shape[1])
            #resized_rot = ndimage.rotate(resized, degree)
            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < H_card or resized.shape[1] < W_card:
                print("!!")
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            # edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(resized, card, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # check to see if the iteration should be visualized
            #if args.get("visualize", False):
                # draw a bounding box around the detected region
            #clone = np.dstack([edged, edged, edged])
            #cv2.rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
            #cv2.imshow("Visualize", clone)
            #cv2.waitKey(0)

            # if we have found a new maximum correlation value, then ipdate
            # the bookkeeping variable
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r, degree, scale2)
                #print(scale2)
    (maxVal, maxLoc, r, deg, SCALE) = found
    print(found)
    #(startX, startY) = (int((((maxLoc[0]) * r) + cropped[2]) / scale), int((maxLoc[1] * r + cropped[0]) / scale))
    #(endX, endY) = (int(((maxLoc[0] + W_card) * r + cropped[2]) / scale), int(((maxLoc[1] + H_card) * r + cropped[0]) / scale))
    (startX, startY) = (int(round(maxLoc[0]*r)), int(round(maxLoc[1]*r)))
    (endX, endY) = (int(round((maxLoc[0] + W_card)*r)), int(round((maxLoc[1] + H_card) * r)))
    #(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
    #(endX, endY) = (int((maxLoc[0] + W_card) * r), int((maxLoc[1] + H_card) * r))

    #img_cropped=ndimage.rotate(img_cropped, deg)
    #output_img = ndimage.rotate(output_img, deg)
#    output_img = img_cropped[startY:endY,startX:endX,:]

    output_img = ndimage.rotate(orig_cropped, deg)
    output_img = output_img[startY:endY,startX:endX,:]
    #output_img = output_img[startY+8:endY-6,startX+8:endX-6,:]

    #if orient == 0:
    #    output_img = ndimage.rotate(output_img, 180)
    # draw a bounding box around the detected result and display the image
    #image = ndimage.rotate(image, 1.5)
    #cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    '''
    plt.imshow(output_img)
    plt.show()
    cv2.waitKey(0)

    plt.imshow(img_cropped)
    plt.show()
    cv2.waitKey(0)
    print(cropped)
    '''
    return(output_img,maxVal,SCALE)





