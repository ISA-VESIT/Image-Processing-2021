#MOVING THE OBJECTS

import pygame, sys
import random
import cv2
import  numpy as np
import math

# General setup
pygame.init() #initiates all the pygame modules and is req before we run any kind of game
clock = pygame.time.Clock()

def quit():
    # Handling input
    for event in pygame.event.get(): #search for all the events i.e it can be movement of mouse, pressing a key,closing window
        if event.type == pygame.QUIT: #check if the user has clicked X on the window
            pygame.quit() #initializes quit to all the modules in pygame [opp of init()]
            sys.exit() #terminate the program

def quit1():
    global lives
    if lives == 0: #if life is 0 then quit
        pygame.quit()
        sys.exit()

def ball_restart():
    global  ball_speed_x, ball_speed_y
    ball.center = (screen_width/2, screen_height/2) #restart the ball at the og pos
    ball_speed_y *= random.choice((1,-1)) #ball will start from any direction
    ball_speed_x *= random.choice((1,-1))

def player_anim():

    if player.top <= 0:  # if the player paddle top hits the top of the screen
        player.top = 0
    if player.bottom >= screen_height:  # if the player paddle top hits the bottom of the screen
        player.bottom = screen_height


def opponent_anim():

    if opponent.top < ball.y: #if the top of the opponent is below y cord of ball move the opponent by 10
        opponent.top += 10
    if opponent.top > ball.y: #if the top of the opponent is above y cord of ball move the opponent by 10
        opponent.top -= 10

    if opponent.top <= 0:  # if the player paddle top hits the top of the screen
        opponent.top = 0
    if opponent.bottom >= screen_height:  # if the player paddle top hits the bottom of the screen
        opponent.bottom = screen_height

def paddle_restart():
    global  player, opponent
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 80, 10, 160)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 160)

def ball_anim():
    global ball_speed_x, ball_speed_y, lives

    # Movement of the ball
    ball.x = ball_speed_x + ball.x
    ball.y = ball_speed_y + ball.y

    # Collisions
    if ball.top <= 0 or ball.bottom >= screen_height:  # ball is colliding with top and bottom of the screen
        ball_speed_y *= -1

    if ball.left <= 0:
        ball_restart()
        paddle_restart()

    if ball.right >= screen_width:
        lives -= 1
        ball_restart()
        paddle_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):  # ball is colliding on both the paddles
        ball_speed_x *= -1

# Setting up the main window
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) # display is a module and set_mode is a method that intializes a surface
pygame.display.set_caption('Hand gesture Ping Pong')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0, 255)


# Objects

#BRO MUZE BHI BATA YAHAPE PE -12 KYU LIKHA HAI -_-
ball = pygame.Rect(screen_width / 2 - 12, screen_height / 2 - 12 , 24, 24)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 80, 10, 160)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 160)

# speeds
ball_speed_x = 6 * random.choice((1,-1))
ball_speed_y = 6 * random.choice((1,-1))

# lives
lives = 5
game_font = pygame.font.Font('freesansbold.ttf', 32) #font for lives text

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
            player.y = player.y - 10
        elif count_defects == 2:
            cv2.putText(draw, 'THREE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            player.y = player.y + 10
        elif count_defects == 3:
            cv2.putText(draw, 'FOUR', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
        elif count_defects == 4:
            cv2.putText(draw, 'FIVE', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
    except:
        #pass
        draw = np.zeros(crop_image.shape, np.uint8)


    ball_anim()
    player_anim()
    opponent_anim()

    quit1()
    quit()
    # Drawing the objects
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLUE, opponent)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (screen_width / 2, 0), (screen_width / 2, screen_height))

    lives_text = game_font.render("lives:" + str(lives), True, WHITE)  # forms a surface/template to display the text for lives
    screen.blit(lives_text, (50, 10))  # blitting the pixels of lives_text onto the screen


    # Updating the window
    pygame.display.update() # update the entire screen
    clock.tick(40) #control the speed of While loop, here 40 times per sec

    cv2.imshow('frame', frame)  # to show the output frame
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

    k = cv2.waitKey(1)  # will wait for the key to be pressed for a second and then if not pressed then read the next frame

    if k == 27:  # ASCII for escape key
        break  # if key pressed is esc then break

cap.release()  # release the capture video from webacm
cv2.destroyAllWindows()  # destroy all the windows