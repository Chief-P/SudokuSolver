'''
Sudoku Grabber
Datas are stored in ./data directory as a naive solution
TODO: Modulize the core with SWIG to optimize this
'''


import cv2 as cv
import numpy as np


# Preprocess the image
def preprocess(img):
    img = cv.GaussianBlur(img, (11, 11), 0)
    mask = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 5, 2)
    mask_inv = cv.bitwise_not(mask)
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    mask_inv = cv.dilate(mask_inv, kernel, iterations=1)
    
    return mask_inv


# Detecting blobs manually
# Assume the puzzle is the biggest one
def detect_blobs(mask_inv):
    h, w = mask_inv.shape[:2]
    max_area = -1
    max_pt = (-1, -1)
    ffill_mask = np.zeros((h+2, w+2), np.uint8)

    # Mark blobs with gray
    for i in range(h):
        for j in range(w):
            if mask_inv[i, j] >= 128:
                _, _, _, rect = cv.floodFill(mask_inv, ffill_mask, (j, i), 64) # seed point follows the format of (x, y)
                area = rect[0] * rect[1]
                if area > max_area:
                    max_pt = (j, i)
                    max_area = area
                    # print(area)
                    # print(max_pt)

    # FloodFill the biggest blob with white
    cv.floodFill(mask_inv, ffill_mask, max_pt, 255)

    # FloodFill other blobs with black
    for i in range(h):
        for j in range(w):
            if mask_inv[i, j] == 64 and (j, i) != max_pt:
                cv.floodFill(mask_inv, ffill_mask, (j, i), 0)

    # Offset dilation
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    mask_inv = cv.erode(mask_inv, kernel, iterations=1)

    return mask_inv


if __name__ == "__main__":
    # Read the image
    img = cv.imread("./pic/sudoku.jpg", 0) # gray scale mode
    # mask = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)

    mask_inv = preprocess(img)
    # cv.imwrite("./pic/mask_inv.jpg", mask_inv)

    mask_inv = detect_blobs(mask_inv)
    cv.imwrite("./pic/biggest_blob.jpg", mask_inv)