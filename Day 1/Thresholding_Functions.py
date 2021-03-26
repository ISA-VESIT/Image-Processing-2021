import cv2
import numpy
from matplotlib import pyplot as plt

img = cv2.imread('gradient.png') #read the image
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def thresh_binary(T1, image1): # we make our own function
    copy1 = numpy.array(image1)  # we create the copy of our image
    length = copy1.shape[0]    #this gives the no of rows
    width = copy1.shape[1]     #this gives the no of columns
    for y in range(0,length):   # for the yth row in all the rows
        for x in range(0, width ): # for the xth row in all the columns
            if copy1[y,x] >=T1:     # copy[y,x] = one pixel this basically compares all the pixel values with threshold
                copy1[y, x] = 255    # if pixel value greater than thresh  than make  it white
            else:
                copy1[y,x] = 0   # less than tresh make it dark
    return copy1

def thresh_binary_inverse(T1, image1):
    copy1 = numpy.array(image1)
    length = copy1.shape[0]
    width = copy1.shape[1]
    for y in range(0,length):
        for x in range(0, width ):
            if copy1[y,x] >=T1:     # copy[y,x] = one pixel this basically compares all the pixel values with threshold
                copy1[y, x] = 0    # if pixel value greater than thresh  than make  it dark
            else:
                copy1[y,x] = 255  # less than tresh make it light
    return copy1

def thresh_trunc(T2, image2):
    copy2 = numpy.array(image2)
    length = copy2.shape[0]
    width = copy2.shape[1]
    for y in range(0, length):
        for x in range(0, width):
            if copy2[y,x] >=T2:
                copy2[y,x] = T2 # make the pixel value same as tresh
            else:
                copy2[y,x] =copy2[y,x]  # let the pixel value remain the same
    return copy2



tresh_binary = thresh_binary(127,gray)
tresh_binary_inverse = thresh_binary_inverse(127, gray)
thresh_trunc = thresh_trunc(127,gray)
titles =['original image','tresh_binary','thresh_binary_inverse', 'tresh_trunc']
images =[gray,tresh_binary, tresh_binary_inverse,thresh_trunc]

for i in range(4):
    plt.subplot(2,2, i+1)
    plt.xticks([]), plt.yticks([])
    plt.imshow(images[i], 'gray')
    plt.title(titles[i])

plt.show()