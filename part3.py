#MOVING THE OBJECTS

import pygame, sys
import random

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

while True:
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