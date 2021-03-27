#IMPORTING LIBRARIES
import cv2
import  numpy as np
import math

#CAPTURE THE VIDEO FROM WEBCAM
cap = cv2.VideoCapture(0)

while True: #to run the loop infinitely

    #READ EACH FRAME FROM THE CAPTURED VIDEO
    _, frame = cap.read() # _ is a boolean which indicates if the frame is captured successfully and then store it into a variable frame

    #GET HAND DATA FROM THE RECTANGLE SUB WINDOW
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 1)
    crop_image = frame[100:300, 100:300]
    blur = cv2.blur(crop_image, (11, 11), 0)

    #CHANGE THE COLOR-SPACE FROM BGR TO HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lc = np.array([0, 40, 60])
    hc = np.array([20, 150, 255])

    #CREATE MASK FOR SKIN COLOR
    mask = cv2.inRange(hsv, lc, hc)

    #MORPHOLOGICAL OPERATIONS (CLOSING)
    kernel = np.ones((7, 7), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations= 1)
    erosion = cv2.erode(dilation, kernel, iterations= 1)

    #APPLYING GAUSSIAN BLUR TO REMOVE NOISE
    filtered = cv2.GaussianBlur(erosion, (11, 11), 0)

    #FIND CONTOURS
    cont, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:

        #FIND CONTOURS OF MAX AREA i.e HAND
        max_cont = max(cont, key = lambda x: cv2.contourArea(x))
        #print("max cont:",max_cont)

        #CREATE BOUNDING RECTANGLE AROUND THE CONTOUR
        x, y, w, h = cv2.boundingRect(max_cont)
        cv2.rectangle(crop_image, (x, y), (x + w, y + h), (0, 0, 255), 0)

        #FIND CONVEX HULL
        hull = cv2.convexHull(max_cont)
        #print("asli_hull:", hull)

        #DRAW CONTOURS
        draw = np.zeros(crop_image.shape, np.uint8)
        cv2.drawContours(draw, [max_cont], -1, (0, 255, 0), 0)
        cv2.drawContours(draw, [hull], -1, (0, 255, 0), 0)

        hull = cv2.convexHull(max_cont, returnPoints = False) #to find the indexes of convex hull pts
        #print("sasta_hull:", hull)

        defects = cv2.convexityDefects(max_cont, hull) #we get starting index, ending index, farthest index, approx distance
        #print("defect", defects)

        defectshape = defects.shape[0]
        #print(defectshape)

        # #USE COSINE RULE TO FIND THE ANGLE OF THE FARTHEST PT FROM START PT AND END PT
        count_defects = 0

        for i in range(defectshape):
            s, e, f, d = defects[i][0]
            start = tuple(max_cont[s][0])
            #print(start)
            end = tuple(max_cont[e][0])
            far = tuple(max_cont[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14

            # if angle < 90 draw a circle

            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_image, far, 1, [0, 0, 255], -1)

            cv2.line(crop_image, start, end, [0, 255, 0], 2)

        if count_defects == 0:
            cv2.putText(draw, 'ONE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        elif count_defects == 1:
            cv2.putText(draw, 'TWO', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        elif count_defects == 2:
            cv2.putText(draw, 'THREE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        elif count_defects == 3:
            cv2.putText(draw, 'FOUR', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        elif count_defects == 4:
            cv2.putText(draw, 'FIVE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    except:
        #pass
        draw = np.zeros(crop_image.shape, np.uint8)


    cv2.imshow('frame', frame) #to show the output frame
    cv2.imshow('crop_image', crop_image)
    cv2.imshow('blur', blur)
    cv2.imshow('hsv', hsv)
    cv2.imshow('mask', mask)
    cv2.imshow('dilation', dilation)
    cv2.imshow('erosion', erosion)
    cv2.imshow('filtered', filtered)
    cv2.imshow('draw', draw)
    all_img = np.hstack((draw, crop_image))
    cv2.imshow('control', all_img)

    k = cv2.waitKey(1) #will wait for the key to be pressed for a second and then if not pressed then read the next frame

    if k == 27: #ASCII for escape key
         break #if key pressed is esc then break

cap.release() #release the capture video from webacm
cv2.destroyAllWindows() #destroy all the windows




