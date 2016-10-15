__author__ = 'Mohammad'

import numpy as np
import cv2
import matplotlib.pylab as plt
from scipy import ndimage
import colorbalance
import os

def Write_ColorCard(info,card,study_file_name):
    dest_folder = info['destination']+info['expt']+'-'+info['location']+'-'+'CorrectedColorCards/'
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    cv2.imwrite(dest_folder+study_file_name.replace('~fullres-orig','-CorrectedCard'),card)   

def Color_correct_and_write(card,image,study_file_name, Acc):
    CardRGB = cv2.cvtColor(card, cv2.COLOR_BGR2RGB)
    ImageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    actual_colors = colorbalance.get_colorcard_colors(CardRGB,grid_size=[6, 4])
    cnt_color = 0
    #print(actual_colors)
    if np.sum(actual_colors[:, 8])> np.sum(actual_colors[:, -9]):
        cnt_color = cnt_color + 1
    if np.sum(actual_colors[:, 5])> np.sum(actual_colors[:, -6]):
        cnt_color = cnt_color + 1
    if np.sum(actual_colors[:, 0])< np.sum(actual_colors[:, -1]):
        cnt_color = cnt_color + 1
    if cnt_color >= 2:
        actual_colors = actual_colors[:, ::-1]
    true_colors = colorbalance.ColorCheckerRGB_CameraTrax
    Check = True
    actual_colors2 = actual_colors
    iter = 0
    while Check:
        iter = iter + 1
        color_alpha, color_constant, color_gamma = colorbalance.get_color_correction_parameters(true_colors,actual_colors2,'gamma_correction')
        corrected_colors = colorbalance._gamma_correction_model(actual_colors2, color_alpha, color_constant, color_gamma)
        diff_colors = true_colors - corrected_colors
        errors = np.sqrt(np.sum(diff_colors * diff_colors, axis=0)).tolist()
        if Acc > 0.4 and np.mean(errors) > 30 and iter < 6:
            actual_colors2 = actual_colors + np.random.rand(3,24)
            print('again....!')
        else:
            Check = False
            
    print(np.mean(errors),np.median(errors))
    # CardRGBCorrected = colorbalance.correct_color(CardRGB, color_alpha,color_constant, color_gamma)
    # CardCorrected = cv2.cvtColor(CardRGBCorrected, cv2.COLOR_RGB2BGR)
    
    # Write_ColorCard(info,CardCorrected,study_file_name)
    if np.mean(errors) > 35:
        cv2.imwrite(study_file_name,image)
    else:
        ImageRGBCorrected = colorbalance.correct_color(ImageRGB, color_alpha,color_constant, color_gamma)
        # get back to RBG order for OpenCV
        ImageCorrected = cv2.cvtColor(ImageRGBCorrected, cv2.COLOR_RGB2BGR)
        cv2.imwrite(study_file_name,ImageCorrected)   