#SETTING UP WINDOW

import pygame, sys

# General setup
pygame.init() #initiates all the pygame modules and is req before we run any kind of game
clock = pygame.time.Clock()

def quit():
    # Handling input
    for event in pygame.event.get(): #search for all the events i.e it can be movement of mouse, pressing a key,closing window
        if event.type == pygame.QUIT: #check if the user has clicked X on the window
            pygame.quit() #initializes quit to all the modules in pygame [opp of init()]
            sys.exit() #terminate the program

# Setting up the main window
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height)) # display is a module and set_mode is a method that intializes a surface
pygame.display.set_caption('Hand gesture Ping Pong')

while True:

    quit()

    # Updating the window
    pygame.display.update() # update the entire screen
    clock.tick(40) #control the speed of While loop, here 40 times per sec