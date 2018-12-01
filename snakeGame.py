# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 14:20:41 2018

@author: Graham Cracker

Python game of snake :)
"""

import numpy as np
import random as rd
import pygame
import time

        
class Snake:
    def __init__(self,*args,**kwargs):
        self.segments = 8; # size of the snake to start
        # all segments start at 0
        self.segmentX = np.array([40,35,30,25,20,15,10,5])
        self.segmentY = np.array([0,0,0,0,0,0,0,0])
        self.movementDirection = 0
        
    def moveSnake(self):
        # movement direction --> 0 right, 1 up, 2 left, 3 down
        # move trailing limbs up to new positions
        for i in range(1,self.segments):
            self.segmentX[self.segments-i] = self.segmentX[self.segments-i-1]
            self.segmentY[self.segments-i] = self.segmentY[self.segments-i-1]
        # update the head position
        if self.movementDirection == 0:
            self.segmentX[0] = self.segmentX[0]+5
        if self.movementDirection ==1:
            self.segmentY[0] = self.segmentY[0]+5
        if self.movementDirection ==2:
            self.segmentX[0] = self.segmentX[0]-5
        if self.movementDirection ==3:
            self.segmentY[0] = self.segmentY[0]-5



        
pygame.init()
screen = pygame.display.set_mode((500, 500))
done = False
is_blue = True
snake= Snake()
food_got = True
food_x = rd.randint(20,480)
food_y = rd.randint(45,480)
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

time.sleep(10)

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: snake.movementDirection = 3
        if pressed[pygame.K_DOWN]: snake.movementDirection = 1
        if pressed[pygame.K_LEFT]: snake.movementDirection = 2
        if pressed[pygame.K_RIGHT]: snake.movementDirection = 0
        snake.moveSnake()
        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        
        
        # edge detection
        if snake.segmentX[0]+250 < 15:
            done = True
        if snake.segmentX[0]+250 > 470:
            done = True
        if snake.segmentY[0]+250 < 40:
            done = True
        if snake.segmentY[0]+250 > 470:
            done = True
        
        for i in range(0,snake.segments):
            pygame.draw.rect(screen, color, pygame.Rect(snake.segmentX[i]+250,snake.segmentY[i]+250 , 20, 20))
            # termination for the snake crashing into itself
            pygame.draw.rect(screen, (255,100,0), pygame.Rect(food_x-10,food_y-10 , 20, 20))
            pygame.draw.lines(screen,(255,255,255),False,[[10,35],[490,35]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[10,35],[10,490]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[10,490],[490,490]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[490,35],[490,490]],2)
            score_text = my_font.render('Score: ' + str(snake.segments-8),False, (255,255,255))
            screen.blit(score_text,(200,10))
            
            if i > 0:
                curr_x = snake.segmentX[i]+250
                curr_y = snake.segmentY[i]+250
                head_x = snake.segmentX[0]+250
                head_y = snake.segmentY[0]+250
                crashTolerance = 5
                if (abs(curr_x-head_x) < crashTolerance) and (abs(curr_y-head_y) < crashTolerance):
                    done = True
            
        
        # ADD FOOD :)
        
        if food_got == True:
            food_x = rd.randint(20,480)
            food_y = rd.randint(45,480)
            food_got = False
        #if snake.movementDirection == 0:
        head_x = snake.segmentX[0]+250
        head_y = snake.segmentY[0]+250
        """#if snake.movementDirection == 1:
            head_x = snake.segmentX[0]+260
            head_y = snake.segmentY[0]+250
        #if snake.movementDirection == 2:
            head_x = snake.segmentX[0]+250
            head_y = snake.segmentY[0]+260
        #if snake.movementDirection == 3:
            head_x = snake.segmentX[0]+260
            head_y = snake.segmentY[0]+250
        """
        foodTolerance = 20
        if (abs(food_x-head_x) < foodTolerance) and (abs(food_y-head_y) < foodTolerance):
            food_got = True
            snake.segmentX = np.append(snake.segmentX,snake.segmentX[snake.segments-1])
            snake.segmentY = np.append(snake.segmentY,snake.segmentY[snake.segments-1])
            snake.segments = snake.segments+1
        
        
        pygame.display.flip()
        clock.tick(30)        




pygame.display.flip()
time.sleep(10)
pygame.quit()
