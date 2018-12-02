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
        self.segments = 4; # size of the snake to start
        # all segments start at 0
        self.segmentX = np.array([4,3,2,1])
        self.segmentY = np.array([0,0,0,0])
        self.movementDirection = 0
        
        # game pixel grid for smooth animations.
        self.gridX = np.linspace(0,39,40)
        self.gridY = np.linspace(0,39,40)
        
    def moveSnake(self):
        # movement direction --> 0 right, 1 up, 2 left, 3 down
        # move trailing limbs up to new positions
        for i in range(1,self.segments):
            self.segmentX[self.segments-i] = self.segmentX[self.segments-i-1]
            self.segmentY[self.segments-i] = self.segmentY[self.segments-i-1]
        # update the head position
        if self.movementDirection == 0:
            self.segmentX[0] = self.segmentX[0]+1
        if self.movementDirection ==1:
            self.segmentY[0] = self.segmentY[0]+1
        if self.movementDirection ==2:
            self.segmentX[0] = self.segmentX[0]-1
        if self.movementDirection ==3:
            self.segmentY[0] = self.segmentY[0]-1



def renderSnakeX(Snake,i):
    # return the snake pixel locations of the current location
    return (Snake.segmentX[i]*20)+10+1
    
    
    
def renderSnakeY(Snake,i):
    # return the snake pixel locations of the current location
    return (Snake.segmentY[i]*20)+100+1
    
    
    
    
    
pygame.init()
screen = pygame.display.set_mode((820, 910))
done = False
is_blue = True
snake= Snake()
food_got = True
food_x = rd.randint(20,480)
food_y = rd.randint(45,480)
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

time.sleep(3)

  
speedControl = 10;
count = 0
  

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        
        
        pastDirection = snake.movementDirection;
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: snake.movementDirection = 3
        if pressed[pygame.K_DOWN]: snake.movementDirection = 1
        if pressed[pygame.K_LEFT]: snake.movementDirection = 2
        if pressed[pygame.K_RIGHT]: snake.movementDirection = 0
        
        # make it so that you can't kill yourself by turning back into yourself
        a = snake.movementDirection # for convenience
        b = pastDirection # also convenient
        if (a == 2 and b == 0): 
            snake.movementDirection = pastDirection
        if (a ==0 and b == 2):
            snake.movementDirection = pastDirection
        if (a == 1 and b == 3):
            snake.movementDirection = pastDirection
        if (a == 3 and b ==1):
            snake.movementDirection = pastDirection
        
        
        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        
        if count == speedControl:
            snake.moveSnake()
            count = 0
        else:
            count = count+1

        
        for i in range(0,snake.segments):

            if snake.movementDirection == 3:
                x_add = 0
                y_add = -2*count
            if snake.movementDirection == 1:
                x_add = 0
                y_add = 2*count
            if snake.movementDirection == 2:
                x_add = -2*count
                y_add = 0
            if snake.movementDirection == 0:
                x_add = 2*count
                y_add = 0
                    
            if i > 0:
                # up
                if snake.segmentX[i] == snake.segmentX[i-1] and snake.segmentY[i] > snake.segmentY[i-1]:
                    x_add = 0
                    y_add = -count*2
                # down
                if snake.segmentX[i] == snake.segmentX[i-1] and snake.segmentY[i] < snake.segmentY[i-1]:
                    x_add = 0
                    y_add = count*2
                # left
                if snake.segmentX[i] > snake.segmentX[i-1] and snake.segmentY[i] == snake.segmentY[i-1]:
                    x_add = -count*2
                    y_add = 0
                #right
                if snake.segmentX[i] < snake.segmentX[i-1] and snake.segmentY[i] == snake.segmentY[i-1]:
                    x_add = count*2
                    y_add = 0
                
            
            pygame.draw.rect(screen, color, pygame.Rect(renderSnakeX(snake,i)+x_add,renderSnakeY(snake,i)+y_add , 18, 18))
            # termination for the snake crashing into itself
            pygame.draw.rect(screen, (255,100,0), pygame.Rect((food_x*20)+11,(food_y*20)+101 , 18, 18))
            pygame.draw.lines(screen,(255,255,255),False,[[10,100],[810,100]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[10,100],[10,900]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[10,900],[810,900]],2)
            pygame.draw.lines(screen,(255,255,255),False,[[810,100],[810,900]],2)
            header_text = my_font.render('I''M A SNAKEY SNAKE',False, (255,255,255))
            screen.blit(header_text,(300,10))
            score_text = my_font.render('Score: ' + str(snake.segments-4),False, (255,255,255))
            screen.blit(score_text,(300,50))
            
            
            if snake.segmentX[0] < 0:
                done = True
            if snake.segmentX[0] > 39:
                done = True
            if snake.segmentY[0] < 0:
                done = True
            if snake.segmentY[0] > 39:
                done = True
            if i > 0:
                curr_x = snake.segmentX[i]
                curr_y = snake.segmentY[i]
                head_x = snake.segmentX[0]
                head_y = snake.segmentY[0]
                if curr_x==head_x and curr_y==head_y:
                    done = True
        
        

        
        
        
        
            
        # ADD FOOD :)
        
        if food_got == True:
            food_x = rd.randint(0,39)
            food_y = rd.randint(0,39)
            food_got = False
        #if snake.movementDirection == 0:
        head_x = snake.segmentX[0]
        head_y = snake.segmentY[0]
        
        if food_x==head_x and food_y==head_y:
            food_got = True
            snake.segmentX = np.append(snake.segmentX,snake.segmentX[snake.segments-1])
            snake.segmentY = np.append(snake.segmentY,snake.segmentY[snake.segments-1])
            snake.segments = snake.segments+1
        
        
        pygame.display.flip()
        clock.tick(120)



pygame.display.flip()
time.sleep(10)
pygame.quit()
