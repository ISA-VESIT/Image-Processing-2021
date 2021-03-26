import cv2

cap = cv2.VideoCapture(0)  #This is to specify the cam from which we want to display aur the video which we want to read

while(True):  #this loop ensures that the fram is continuously captured
    ret, frame = cap.read()  #ret returns if frame is available or not and the frame is stored in frame variable
    cv2.imshow('Rakshitha', frame)   #to display the video
    if cv2.waitKey(1) & 0xff == ord('q'):   #gives the delay and 0xFF needed for 64 bit comp and specifies oon pressing q we exit
        break
cap.release()              #very important to reelase adell the frames
cv2.destroyAllWindows()    #destroy all window