import cv2
import numpy as np
import argparse
import image_preparer
from scipy.ndimage import interpolation

def imageFromContour(cnt):
	x,y,w,h = cv2.boundingRect(cnt)
	img = np.zeros([y+h+20,x+w+20,3],dtype=np.uint8)
	img.fill(255)
	img = cv2.drawContours(img,[cnt],0,(0,0,0),-1)
	img = img[y-10:y+h+10, x-10:x+w+10]
	return img

def widthAndHeight(img, precision):
	maxWidth = 0
	finalHeight = 0

	for a in range(0,precision):
		rotated = interpolation.rotate(img,(180/precision)*a)
		gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
		_,thresh2 = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
		contours,contours,hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)
		_,_,w,h = cv2.boundingRect(contours[0])
		if w>maxWidth:
			maxWidth = w
			finalHeight = h

	return (maxWidth,finalHeight)

def maxLength(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
	contours,contours,hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)
	centre,radius = cv2.minEnclosingCircle(contours[0])
	return 2*radius

def area (img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_,thresh = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
	contours,contours,hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)
	return cv2.contourArea(contours[0])

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
contours,contours,hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)

# for cnt in contours:
    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # a, b, c, d = box
    # for p in box:
    # 	print(p)
    # box = np.int0(box)
    # cv2.drawContours(img,[cnt],0,(0,255,0),2)
    # cv2.rectangle(img, (int(x),int(y)), (int(x+w),int(y+h)), (0,255,0),3)

image_preparer.image_show("Title",img)

# h,w,_ = img.shape
# M = cv2.getRotationMatrix2D((w/2,h/2),45,1.0)
# rotated = cv2.warpAffine(img, M, (int(1.42*w),int(1.42*h)))
# -----------------------------------------------
# maxWidth = 0
# finalHeight = 0

# for a in range(0,180):
# 	rotated = interpolation.rotate(img,(180/180)*a)
# 	gray2 = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
# 	_,thresh2 = cv2.threshold(gray2,80,255,cv2.THRESH_BINARY)
# 	contours2,contours2,hierarchy2 = cv2.findContours(thresh2,1,cv2.CHAIN_APPROX_SIMPLE)
# 	x,y,w,h = cv2.boundingRect(contours2[0])
# 	print(w)
# 	if w>maxWidth:
# 		print(w)
# 		maxWidth = w
# 		finalHeight = h
# print(maxWidth)
# print(finalHeight)
# ------------------------------------------------
# # cv2.rectangle(img,(),(),(0,255,0),3)


# # rotated = interpolation.rotate(img1,2*30)
# # gray2 = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
# # _,thresh2 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
# # contours2,contours2,hierarchy2 = cv2.findContours(thresh2,1,cv2.CHAIN_APPROX_SIMPLE)
# # x,y,w,h = cv2.boundingRect(contours2[0])

# # cv2.rectangle(rotated,(x,y),(x+w,y+h),(0,255,0),3)
# # ------------------
# # for cnt in contours:
# # 	cv2.drawContours(img,[cnt],0,(0,255,0),2)

# ------------------------------------------------
# image_preparer.image_show("Title2",rotated)

# print(area(img))
# print(maxLength(img))
# -------------------------------------------------

# for cnt in contours:
# 	image_preparer.image_show("Title3", imageFromContour(cnt))