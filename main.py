from Scene import Scene
from Snake import Snake
import pygame, random
from pygame.locals import *

def GetClick():

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = 'UP'
            elif event.key == K_DOWN:
                my_direction = 'DOWN'
            elif event.key == K_LEFT:
                my_direction = 'LEFT'
            elif event.key == K_RIGHT:
                my_direction = 'RIGHT'
            return my_direction



def Main():
    x_length = 600
    y_length = 600
    clock = pygame.time.Clock()

    while True:
        scene = Scene(x_length,y_length)
        snake = Snake()

        while True:
            clock.tick(10)

            direction = GetClick()
            coord = scene.CalculateDistances(snake)
            #print(coord)
            snake.UpdateDirection(direction)

            scene.CheckCatchApple(snake)

            snake.UpdateSnake()

            ret = scene.CheckColisson(snake)
            if ret == False:
                scene.UpdateScreen(snake)
            else:
                score = scene.GameOver()
                break

Main()