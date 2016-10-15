import cv2
import numpy as np


def get_colorcard_colors(color_card, grid_size):
    grid_cols, grid_rows = grid_size
    colors = np.zeros([3, grid_rows * grid_cols])
    sample_size_row = int(0.25 * color_card.shape[0] / grid_rows)
    sample_size_col = int(0.25 * color_card.shape[1] / grid_cols)
    for row in range(grid_rows):
        for col in range(grid_cols):
            r = int((row + 0.5) * color_card.shape[0] / grid_rows)
            c = int((col + 0.5) * color_card.shape[1] / grid_cols)
            i = row * grid_cols + col
            for j in range(colors.shape[0]):
                channel = color_card[r - sample_size_row:r + sample_size_row,
                                     c - sample_size_col:c + sample_size_col,
                                     j]
                colors[j, i] = np.median(channel.astype(np.float))

    return colors


def get_brightest_rgb(array2d):
    random = [24]
    i = 0
    for row in range(4):
        for col in range(6):
            random[i] = array2d[0][i] + array2d[1][i] + array2d[2][i]
            i += 1
    np.amax(random)
    return

