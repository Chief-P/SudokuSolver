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
# Assume the puzzle is the biggest one in the picture
def detect_blobs(mask_inv):
    h, w = mask_inv.shape[:2]
    max_area = -1
    max_pt = (-1, -1)
    ffill_mask = np.zeros((h+2, w+2), np.uint8)

    # Mark blobs with gray
    for i in range(h):
        for j in range(w):
            if mask_inv[i, j] >= 128:
                area, _, _, _ = cv.floodFill(mask_inv, ffill_mask, (j, i), 64) # seed point follows format (x, y)
                if area > max_area:
                    max_pt = (j, i)
                    max_area = area

    # FloodFill the biggest blob with white
    ffill_mask[:] = 0 # reset mask
    cv.floodFill(mask_inv, ffill_mask, max_pt, 255, 20, 20)

    # FloodFill other blobs with black
    for i in range(h):
        for j in range(w):
            if mask_inv[i, j] == 64 and (j, i) != max_pt:
                ffill_mask[:] = 0
                cv.floodFill(mask_inv, ffill_mask, (j, i), 0)

    # Offset dilation
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    mask_inv = cv.erode(mask_inv, kernel, iterations=1)

    return mask_inv


# For debug
def plot_lines(lines, blob):
    for line in lines:
        for rho, theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))
            cv.line(blob, (x1, y1), (x2, y2), 128, 1) # polluted blob
    cv.imwrite("./pic/lines.jpg", blob)


def detect_lines(blob):
    lines = cv.HoughLines(blob, 1, np.pi/180, 200)

    # plot_lines(lines, blob)

    # Normalize lines
    # Abandoned because of the discontinuity of polar c.s. in a certain interval
    # for line in lines:
    #     for rho, theta in line:
    #         if rho < 0:
    #             rho, theta = -rho, theta + np.pi
    #         while theta > np.pi * 2:
    #             theta -= np.pi * 2
    #         while theta < 0:
    #             theta += np.pi * 2

    return lines


# Detect if deg is in the range regradless of the period
def inrange(deg, tar, ld=10, ud=10):
    if  tar - deg > 0:
        while deg > tar + ud:
            deg -= np.pi * 2
    else:
        while deg < tar - ld:
            deg += np.pi * 2

    if tar - ld <= deg <= tar + ld:
        return True
    else:
        return False


def merge_lines(lines, shape):
    h, w = shape
    for line in lines:
        rho, theta = line[0] # unwrap
        if (rho, theta) == (0, -100):
            continue

        # Find two points, assume a good position
        pt1, pt2 = (0, 0), (0, 0) # (x, y) format
        if inrange(theta, np.pi * 90 / 180, 45, 45):
            pt1 = (0, rho / np.sin(theta))
            pt2 = (w, rho / np.sin(theta) - w / np.tan(theta))
        else:
            pt1 = (rho / np.cos(theta), 0)
            pt2 = (rho / np.cos(theta) - h * np.tan(theta), h)
        
        for cur in lines:
            cur_rho, cur_theta = cur[0]
            if (rho, theta) == (cur_rho, cur_theta):
                continue
            if abs(abs(cur_rho) - abs(rho)) < 20 and inrange(theta, cur_theta):
                # Find two points again
                cur_pt1, cur_pt2 = (0, 0), (0, 0)
                if inrange(cur_theta, np.pi * 90 / 180, 45, 45):
                    cur_pt1 = (0, cur_rho / np.sin(cur_theta))
                    cur_pt2 = (w, cur_rho / np.sin(cur_theta) - w / np.tan(cur_theta))
                else:
                    cur_pt1 = (cur_rho / np.cos(cur_theta), 0)
                    cur_pt2 = (cur_rho / np.cos(cur_theta) - h * np.tan(cur_theta), h)
                
                # Fuse lines
                x1, y1 = cur_pt1
                x2, y2 = cur_pt2
                x3, y3 = pt1
                x4, y4 = pt2
                if (x1-x3)**2 + (y1-y3)**2 < 64**2 and (x2-x4)**2 + (y2-y4)**2 < 64**2:
                    line[0] = [(rho + cur_rho) / 2, (theta + cur_theta) / 2]
                    cur[0] = [0, -100] # destroyed lines

    return lines


def find_intersections(l1, l2):
    pass


def find_edges(lines):
    inf = 100000
    top_edge, bottem_edge, left_edge, right_edge = (inf, 0), (-inf, 0), (inf, 0), (-inf, 0)

    # Find edges
    for line in lines:
        rho, theta = line[0]
        if (rho, theta) == (0, -100):
            continue
        # x_intercept = rho / np.cos(theta)
        # y_intercept = rho / np.sin(theta)
        # Vertical lines
        if  inrange(theta, np.pi * 90 / 180):
            if rho < top_edge[0]:
                top_edge = (rho, theta)
            elif rho > bottem_edge[0]:
                bottem_edge = (rho, theta)
        # Horizontal lines
        elif inrange(theta, 0) or inrange(theta, np.pi):
            if rho < left_edge[0]:
                left_edge = (rho, theta)
            elif rho > right_edge[0]:
                right_edge = (rho, theta)
    
    # Find intersections
    tl = find_intersections(top_edge, left_edge)
    tr = find_intersections(top_edge, right_edge)
    bl = find_intersections(bottem_edge, left_edge)
    br = find_intersections(bottem_edge, right_edge)



if __name__ == "__main__":
    # Read the image
    img = cv.imread("./pic/sudoku.jpg", 0) # gray scale mode
    # mask = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX, cv.CV_8UC1)

    mask_inv = preprocess(img)
    # cv.imwrite("./pic/mask_inv.jpg", mask_inv)

    biggest_blob = detect_blobs(mask_inv)
    # cv.imwrite("./pic/biggest_blob.jpg", biggest_blob)

    lines = merge_lines(detect_lines(biggest_blob), biggest_blob.shape[:2])
    edges = find_edges(lines)