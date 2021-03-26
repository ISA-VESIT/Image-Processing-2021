import cv2 as cv

img = cv.imread('kaleen.jpg', -1);

img_gray = cv.imread('kaleen.jpg', 0);

haar_cascade = cv.CascadeClassifier('haarcascade_frontalface.xml')

faces_rect = haar_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=3)
print(faces_rect)

print(f'Number of faces detected : {len(faces_rect)}')

for (x,y,w,h) in faces_rect:
    cv.rectangle(img,(x,y), (x+w,y+w), (0,255,0), thickness=2)


cv.imshow('Detected faces', img)

cv.waitKey(0)
