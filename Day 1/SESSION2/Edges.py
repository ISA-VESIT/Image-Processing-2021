import cv2 as cv
from matplotlib import pyplot as plt

# gaussImg = cv.imread("gauss.jpg")
# blur = cv.GaussianBlur(gaussImg,(5,5),0)
# cv.imshow("gaussian", blur)



img = cv.imread('itachi.jpg')
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# sobelx = cv.Sobel(gray, cv.CV_64F, 1, 0)
# sobely = cv.Sobel(gray, cv.CV_64F, 0, 1)
# combined_sobel = cv.bitwise_or(sobelx, sobely)
#
# cv.imshow('Sobel X', sobelx)
# cv.imshow('Sobel Y', sobely)
# cv.imshow('Combined Sobel', combined_sobel)

canny = cv.Canny(gray, 40, 120)

titles = ['itachi', 'itachi_gray', 'itachi_edges']
images = [img, gray, canny]
for i in range(3):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
cv.waitKey(0)