import pygame
pygame.init()


## Phần cài đặt của game
white = (255, 255, 255) 
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
HEIGHT = 10
WIDTH = 15
FIELD_SIZE = HEIGHT * WIDTH
HEAD = 0

FOOD = 0
UNDEFINED = (HEIGHT + 1) * (WIDTH + 1)
SNAKE = 2 * UNDEFINED

LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH 

ERR = -2333
MOV = [LEFT, RIGHT, UP, DOWN]

SNAKE_BLOCK = 30
SNAKE_SPEED = 30

FONT_STYLE = pygame.font.SysFont("arial", 12)
SCORE_FONT = pygame.font.SysFont("arial", 20)