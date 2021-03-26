import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('j.png', cv2.IMREAD_GRAYSCALE)
th_val, th_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

img1 = cv2.imread('j_open.jpg', cv2.IMREAD_GRAYSCALE)
th_val1, j1_th_img = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)

img2 = cv2.imread('j_close.jpg', cv2.IMREAD_GRAYSCALE)
th_val2, j2_th_img = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)

print(th_val)

kernel = np.ones((5,5), np.uint8)

dilation = cv2.dilate(th_img, kernel, iterations=2)
erosion = cv2.erode(th_img, kernel, iterations=1)
opening = cv2.morphologyEx(j1_th_img, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(j2_th_img, cv2.MORPH_CLOSE, kernel)

titles = ['image', 'th_img', 'dilation', 'erosion', 'Outside dots j', 'opening', 'Inside Dots j' , 'closing']
images = [img, th_img, dilation, erosion, j1_th_img, opening, j2_th_img, closing]

for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()