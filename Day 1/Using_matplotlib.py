import cv2
import numpy
from matplotlib import pyplot as plt

img = cv2.imread('apple.jpg')   #reads the image to be displayed
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    #converts the img from  bgr to rgb as matplolib reads image in rgb form
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)    # converts the image to gray


Titles = ['Coloured apple', 'Gray apple']    #to plot the title
images  = [image , gray ]                # to plot images

for i in range(2):     #to plot multiple images here range 2 because we display 2 images
    plt.subplot(1, 2,i+1)  # 1 row 2 columns
    plt.xticks([]), plt.yticks([]) # removes coordinate
    plt.imshow(images[i], 'gray')  #displays the image read from cv2
    plt.title(Titles[i])  # plots the titles passed



plt.show()   #displays the images in matpliotlib window