from matplotlib import pyplot as plt
import cv2 as cv
import sys

img = cv.imread(sys.argv[1], 0)

plt.imshow(img)
plt.show()