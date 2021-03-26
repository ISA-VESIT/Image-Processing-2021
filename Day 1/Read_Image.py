import cv2
import numpy

img = cv2.imread('apple.jpg', 0)#this is to read the image  you can pass values 0=gray, 1=coloured, -1=unchanged
cv2.imshow('Gray Scale', img)  #this displays the image
#print(img)
cv2.waitKey(0)                    #this tells for how much time we need to display the image
cv2.destroyAllWindows()           #this destroys all the windows