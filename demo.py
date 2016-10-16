import image_preparer
import rice_stats
import cv2
import argparse
import stats

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,60,255,0)
contours, contours, hierarchy = cv2.findContours(thresh,1,cv2.CHAIN_APPROX_SIMPLE)

img2 = cv2.drawContours(img,contours,0,(0,255,0),2)
image_preparer.image_show("Thresh", thresh)
image_preparer.image_show("Contours", img2)

warray = []
larray = []
for cnt in contours:
    if cv2.contourArea(cnt)<=50000:
        (w,l) = rice_stats.widthAndHeight(rice_stats.imageFromContour(cnt),20)
        print(w)
        print(l)
        warray.append(w)
        larray.append(l)
data = [larray, warray]   

stats.create_hist(data)