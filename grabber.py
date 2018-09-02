'''
Sudoku Grabber
Datas are stored in ./data directory as a naive solution
TODO: Modulize the core with SWIG to optimize this
      Optimize the naive algorithm
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
    # max_pt = (-1, -1)
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
# ld, ud <= pi
def inrange(deg, tar, ld=np.pi*10/180, ud=np.pi*10/180):
    if ld < 0 or ud < 0 or ld > np.pi or ud > np.pi:
        raise ValueError('inrange-Boundary Error')
    
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


# Find two points on the line in normal form
def find_two_pts(line, shape):
    h, w = shape
    rho, theta = line
    # pt1, pt2 = (0, 0), (0, 0) # (x, y) format
    if inrange(theta, np.pi * 90 / 180, np.pi * 45 / 180, np.pi * 45 / 180):
        pt1 = (0, rho / np.sin(theta))
        pt2 = (w, rho / np.sin(theta) - w / np.tan(theta))
    else:
        pt1 = (rho / np.cos(theta), 0)
        pt2 = (rho / np.cos(theta) - h * np.tan(theta), h)

    return pt1, pt2


def merge_lines(lines, shape):
    for line in lines:
        rho, theta = line[0] # unwrap
        if (rho, theta) == (0, -100):
            continue

        # Find two points, assume a good position
        pt1, pt2 = find_two_pts((rho, theta), shape)
        
        for cur in lines:
            cur_rho, cur_theta = cur[0]
            if (rho, theta) == (cur_rho, cur_theta):
                continue
            if abs(abs(cur_rho) - abs(rho)) < 20 and inrange(theta, cur_theta):
                # Find two points again
                cur_pt1, cur_pt2 = find_two_pts((cur_rho, cur_theta), shape)

                # Fuse lines
                x1, y1 = cur_pt1
                x2, y2 = cur_pt2
                x3, y3 = pt1
                x4, y4 = pt2
                if (x1-x3)**2 + (y1-y3)**2 < 64**2 and (x2-x4)**2 + (y2-y4)**2 < 64**2:
                    line[0] = [(rho + cur_rho) / 2, (theta + cur_theta) / 2]
                    cur[0] = [0, -100] # destroyed lines

    return lines


def find_intersection(l1, l2, shape):
    pt11, pt12 = find_two_pts(l1, shape)
    pt21, pt22 = find_two_pts(l2, shape)
    A1 = pt12[1] - pt11[1]
    B1 = pt11[0] - pt12[0]
    C1 = A1 * pt11[0] + B1 * pt11[1]
    A2 = pt22[1] - pt21[1]
    B2 = pt21[0] - pt22[0]
    C2 = A2 * pt21[0] + B1 * pt21[1]
    det = A1 * B2 - B1 * A2

    return ((B2 * C1 - B1 * C2) / det, (A1 * C2 - A2 * C1) / det)


# Calculate Euclidean distance between pt1 and pt2
def dist(pt1, pt2):
    return int(np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2))


def undistort(lines, img):
    inf = 1e6
    top_edge, bottem_edge, left_edge, right_edge = (inf, 0), (0, 0), (inf, 0), (0, 0)

    # Find edges
    for line in lines:
        rho, theta = line[0]
        if (rho, theta) == (0, -100):
            continue
        # x_intercept = rho / np.cos(theta)
        # y_intercept = rho / np.sin(theta)
        # Vertical lines
        if  inrange(theta, np.pi * 90 / 180):
            if abs(rho) < abs(top_edge[0]):
                top_edge = (rho, theta)
            if abs(rho) > abs(bottem_edge[0]):
                bottem_edge = (rho, theta)
        # Horizontal lines
        elif inrange(theta, 0) or inrange(theta, np.pi):
            if abs(rho) < abs(left_edge[0]):
                left_edge = (rho, theta)
            if abs(rho) > abs(right_edge[0]):
                right_edge = (rho, theta)
    
    # Find intersections
    shape = img.shape
    tl = find_intersection(top_edge, left_edge, shape)
    tr = find_intersection(top_edge, right_edge, shape)
    bl = find_intersection(bottem_edge, left_edge, shape)
    br = find_intersection(bottem_edge, right_edge, shape)

    # Correct perspective
    max_len = max(dist(tl, tr), dist(tl, bl), dist(br, bl), dist(br, tr))
    src_pts = np.float32([list(tl), list(tr), list(bl), list(br)])
    dst_pts = np.float32([[0, 0], [max_len, 0], [0, max_len], [max_len, max_len]]) # max_len - 1
    M = cv.getPerspectiveTransform(src_pts, dst_pts)
    undistorted = cv.warpPerspective(img, M, (max_len, max_len))

    return undistorted


if __name__ == "__main__":
    # Read the image
    img = cv.imread("./pic/sudoku.jpg", 0) # gray scale mode

    mask_inv = preprocess(img)
    # cv.imwrite("./pic/mask_inv.jpg", mask_inv)

    biggest_blob = detect_blobs(mask_inv)
    # cv.imwrite("./pic/biggest_blob.jpg", biggest_blob)

    lines = merge_lines(detect_lines(biggest_blob), biggest_blob.shape[:2])
    undistorted_img = undistort(lines, img)
    # cv.imwrite("./pic/undistorted_img.jpg", undistorted_img)