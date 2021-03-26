import cv2
import numpy
from matplotlib import pyplot as plt

img = cv2.imread('sudoku.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

thresh_mean_c = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
thresh_gaussian = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)

# 1st param  = source image
#2nd param = max tresh value
#3rd param = thresh mean = average value of all the pixels in the region - constant and gaussian mean = weighted sum - constant
# 4th param = what kind of tresholding
#5th param = block size
#6th param = constant



titles = ['Original Image', 'thresh mean c','thresh gaussian c']
images = [gray, thresh_mean_c, thresh_gaussian]

for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(images[i],'gray' )
    plt.title(titles[i])

plt.show()