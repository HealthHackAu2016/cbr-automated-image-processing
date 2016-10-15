#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 13:12:14 2015

@author: chuong nguyen <chuong.v.nguyen@gmail.com>
"""

import sys
import numpy as np
import cv2
from skimage.io import imread
import colorbalance
from skimage.morphology import label

def detectColorCard(Image, Threshold=127, MinArea=10000):
    ''' Find region of image contain a rectangular color card
    '''
    Gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    _, Thresh = cv2.threshold(Gray, Threshold, 255, 1)
    _, Contours, _ = cv2.findContours(Thresh, 1, 2)
    RectContours = []
    for cnt in Contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(approx) >= MinArea:
            RectContours.append(approx)
    return RectContours


def extractColorCard(Image, Contour):
    RectContour = Contour.reshape([4, 2])
    # first find bounding box
    for i in range(0, 4):
        if i == 0:
            xmin = RectContour[0, 0]
            xmax = RectContour[0, 0]
            ymin = RectContour[1, 0]
            ymax = RectContour[1, 0]
        else:
            if xmin > RectContour[i, 0]:
                xmin = RectContour[i, 0]
            if xmax < RectContour[i, 0]:
                xmax = RectContour[i, 0]
            if ymin > RectContour[i, 1]:
                ymin = RectContour[i, 1]
            if ymax < RectContour[i, 1]:
                ymax = RectContour[i, 1]
    BoundBox = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]

    # arrange box in order [TopLeft, TopRight, BottomRight, BottomLeft]
    CardBox = [[], [], [], []]
    for i in range(0, 4):
        V0 = BoundBox[i]
        Distance = []
        for j in range(0, 4):
            V1 = [RectContour[j, 0], RectContour[j, 1]]
            Distance.append(np.sqrt((V0[0] - V1[0])**2 + (V0[1] - V1[1])**2))
        jmin = Distance.index(min(Distance))
        CardBox[i] = [RectContour[jmin, 0], RectContour[jmin, 1]]

    # find mean width and height of the card
    Width = int(0.5*(np.sqrt((CardBox[0][0] - CardBox[1][0])**2 +
                             (CardBox[0][1] - CardBox[1][1])**2) +
                     np.sqrt((CardBox[2][0] - CardBox[3][0])**2 +
                             (CardBox[2][1] - CardBox[3][1])**2)))

    Height = int(0.5*(np.sqrt((CardBox[0][0] - CardBox[3][0])**2 +
                              (CardBox[0][1] - CardBox[3][1])**2) +
                      np.sqrt((CardBox[1][0] - CardBox[2][0])**2 +
                              (CardBox[1][1] - CardBox[2][1])**2)))

    # transform card image region into rectangular of similar size
    SOURCE = np.array(CardBox, dtype=np.float32)
    DEST = np.array([[0, 0], [Width, 0], [Width, Height], [0, Height]],
                    dtype=np.float32)
    TransMat = cv2.getPerspectiveTransform(SOURCE, DEST)
    Card = cv2.warpPerspective(Image, TransMat, (Width, Height))

    # remove outer edge


    return Card


def removeEdge(Card, GridSize=[6, 4], EdgePortion=0.05):
    Height, Width = Card.shape[:2]
    Edge = int(Height*EdgePortion)
    SquareWidth = (Height - 2*Edge)/GridSize[1]
    return Card[Edge:int(Edge + GridSize[1]*SquareWidth),
                Edge:int(Edge + GridSize[0]*SquareWidth)]


def removeContourArea(Image, ColorCardContours, Color=(0, 0, 255)):
    ImageModified = np.copy(Image)
    cv2.drawContours(ImageModified, ColorCardContours, -1, Color, -1)
    return ImageModified


def detectLeaf(Image,
               HSVGreenMin=np.array([25, 60, 80]),
               HSVGreenMax=np.array([80, 255, 255]),
               MinArea=1000):
    '''Find leaf contour given leaf colour range in HSV space
    '''
    HSVImage = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    Thresh = cv2.inRange(HSVImage, HSVGreenMin, HSVGreenMax)
    Contours, _ = cv2.findContours(Thresh, 1, 2)
    LeafContours = []
    for i, cnt in enumerate(Contours):
        approx = cv2.approxPolyDP(cnt, 0.001*cv2.arcLength(cnt, True), True)
        if cv2.contourArea(approx) >= MinArea:
            LeafContours.append(approx)
    return LeafContours


def Contour2Mask(MaskSize, Contours):
    Mask = np.zeros(MaskSize, dtype=np.uint8)
    cv2.drawContours(Mask, Contours, -1, (255, 255, 255), -1)
    return Mask


def processImages(ImageFileNames):
    for ImageFileName in ImageFileNames:
        Image = cv2.imread(ImageFileName)
        ColorCardContours = detectColorCard(Image)
        Card = extractColorCard(Image, ColorCardContours[0])

        # remove the black edge around the card image
        CardTrimmed = removeEdge(Card)

        # correct color, in RGB order
        ImageRGB = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        CardRGB = cv2.cvtColor(Card, cv2.COLOR_BGR2RGB)
        actual_colors = colorbalance.get_colorcard_colors(CardRGB,
                                                          grid_size=[6, 4])
        true_colors = colorbalance.ColorCheckerRGB_CameraTrax
        color_alpha, color_constant, color_gamma = \
            colorbalance.get_color_correction_parameters(true_colors,
                                                         actual_colors)
        ImageRGBCorrected = \
            colorbalance.correct_color(ImageRGB, color_alpha,
                                       color_constant, color_gamma)

        # get back to RBG order for OpenCV
        ImageCorrected = cv2.cvtColor(ImageRGBCorrected, cv2.COLOR_RGB2BGR)

        # extract color card mask and leaf mask and apply to correted image
        ColorCardMask = Contour2Mask(ImageCorrected.shape[:2],
                                     ColorCardContours)
        ImageModified = removeContourArea(ImageCorrected, ColorCardContours)
        LeafContours = detectLeaf(ImageModified)
        LeafMask = Contour2Mask(Image.shape[:2], LeafContours)
        ImageModified = removeContourArea(ImageModified, LeafContours,
                                          Color=(0, 255, 0))

        FileNameBase = ImageFileName[:ImageFileName.rfind('.')]
        PropFileName = FileNameBase + '_Prop.cvs'
        CorrectedFileName = FileNameBase + '_Correct.jpg'
        ProcessedFileName = FileNameBase + '_Processed.jpg'

        cv2.imwrite(CorrectedFileName, ImageCorrected)
        CSVFile = open(PropFileName, 'w')
        CSVFile.write('Area;Perimeter;Solidity;Eccentricity;MeanRed;MeanGreen;MeanBlue\n')

        # get leaf properties
        ProcessedImage = np.copy(ImageCorrected)
        for Contour in LeafContours:
            Moments = cv2.moments(Contour)
            Area = Moments['m00']
            Perimeter = cv2.arcLength(Contour, True)
            ConvexHull = cv2.convexHull(Contour)
            ConvexArea = cv2.contourArea(ConvexHull)
            Solidity = Area/ConvexArea
            Center, Axes, Angle = cv2.fitEllipse(Contour)
            MajorAxis, MinAxis = max(Axes), min(Axes)
            Eccentricity = np.sqrt(1.0 - (MinAxis/MajorAxis)**2)
            BoundingBox = cv2.boundingRect(Contour)
            Centroid = [Moments['m10']/Area, Moments['m01']/Area]

            Mask = np.zeros(Image.shape[0:2]).astype('uint8')
            cv2.drawContours(Mask, [Contour], 0, color=255, thickness=-1)
            Leaf = cv2.bitwise_and(ImageCorrected, ImageCorrected, mask=Mask)

            FilledArea = np.sum(Mask == 255)
            MeanRed = float(np.sum(Leaf[:, :, 2]))/FilledArea
            MeanGreen = float(np.sum(Leaf[:, :, 1]))/FilledArea
            MeanBlue = float(np.sum(Leaf[:, :, 0]))/FilledArea
            MeanRGB = (MeanRed, MeanGreen, MeanBlue)

            cv2.drawContours(ProcessedImage, [Contour], 0, color=MeanRGB[2::-1],
                             thickness=-1)
            cv2.drawContours(ProcessedImage, [ConvexHull], 0, color=(0,0,255),
                             thickness=1)

            CSVFile.write('{};{};{};{};{};{};{}\n'.format(
                Area, Perimeter, Solidity, Eccentricity,
                MeanRed, MeanGreen, MeanBlue))

        CSVFile.close()
        cv2.imwrite(ProcessedFileName, ProcessedImage)

#        cv2.imshow('Image', Image)
#        cv2.imshow('Card', Card)
#        cv2.imshow('Card trimmed', CardTrimmed)
#        cv2.imwrite('card.jpg', Card)
#        cv2.imshow('ImageCorrected', ImageCorrected)
#        cv2.imshow('ColorCardMask', ColorCardMask)
#        cv2.imshow('LeafMask', LeafMask)
#        cv2.imshow('Image with removed contour', ImageModified)
#        cv2.imshow('OutputImage', OutputImage)
#
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        processImages(sys.argv[1:])
    else:
        print('Usage: leafsegmentation <list of images>')