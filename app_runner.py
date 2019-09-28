# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 21:08:34 2019

@author: Graham Cracker
    snake game class. Handles the food and whatnot.
"""

import random as rd
import numpy as np
import pygame
import time
from app_snake import Snake


class SnakeGame:
    def __init__(self, _grid_size=20, _display_x=800, _display_y=600):
        """
        Generates a custom snake game with a variable resolution and a variable
        grid size for scale
        """
        self.display_x = _display_x
        self.display_y = _display_y
        self.grid = _grid_size
        self.snake = Snake()

    def render_x(self, i):
        # return the snake pixel locations of the current location
        return (self.snake.segment_x[i]*20)+10+1

    def render_y(self, i):
        # return the snake pixel locations of the current location
        return (self.snake.segment_y[i]*20)+100+1

    def generate_food(self):
        food_x = rd.randint(0, self.grid)
        food_y = rd.randint(0, self.grid)
        return (food_x, food_y)

    def init_game(self, _speed_modifier):
        """
        Setup pygame
        """
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.display_x, self.display_y))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS',
                                        round(self.display_y/40))
        self.speed_modifier = _speed_modifier

    def register_keypress(self):
        pressed_key = pygame.key.get_pressed()
        directions = {'up': 3, 'down': 1, 'left': 2, 'right': 0}
        # might need to switch these to ifs depending on timing
        if pressed_key[pygame.K_UP]:
            self.snake.movement_direction = directions['up']
        elif pressed_key[pygame.K_DOWN]:
            self.snake.movement_direction = direction['down']
        elif pressed_key[pygame.K_LEFT]:
            self.snake.movement_direction = direction['left']
        elif pressed_key[pygame.K_RIGHT]:
            self.snake.movement_direction = direction['right']

        # make sure you don't kill yourself by moving backwards accidentally
        

    def snake_runner(self):
        














  

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        is_blue = not is_blue
        
        # make it so that you can't kill yourself by turning back into yourself
        a = snake.movement_direction # for convenience
        b = pastDirection # also convenient
        if (a == 2 and b == 0): 
            snake.movement_direction = pastDirection
        if (a ==0 and b == 2):
            snake.movement_direction = pastDirection
        if (a == 1 and b == 3):
            snake.movement_direction = pastDirection
        if (a == 3 and b ==1):
            snake.movement_direction = pastDirection
        
        
        screen.fill((0, 0, 0))
        if is_blue: color = (0, 128, 255)
        else: color = (255, 100, 0)
        
        if count == speedControl:
            snake.move_snake()
            count = 0
        else:
            count = count+1

        
        for i in range(0,snake.segments):

            if snake.movement_direction == 3:
                x_add = 0
                y_add = -2*count
            if snake.movement_direction == 1:
                x_add = 0
                y_add = 2*count
            if snake.movement_direction == 2:
                x_add = -2*count
                y_add = 0
            if snake.movement_direction == 0:
                x_add = 2*count
                y_add = 0
                    
            if i > 0:
                # up
                if snake.segment_x[i] == snake.segment_x[i-1] and snake.segment_y[i] > snake.segment_y[i-1]:
                    x_add = 0
                    y_add = -count*2
                # down
                if snake.segment_x[i] == snake.segment_x[i-1] and snake.segment_y[i] < snake.segment_y[i-1]:
                    x_add = 0
                    y_add = count*2
                # left
                if snake.segment_x[i] > snake.segment_x[i-1] and snake.segment_y[i] == snake.segment_y[i-1]:
                    x_add = -count*2
                    y_add = 0
                #right
                if snake.segment_x[i] < snake.segment_x[i-1] and snake.segment_y[i] == snake.segment_y[i-1]:
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
            
            
            if snake.segment_x[0] < 0:
                done = True
            if snake.segment_x[0] > 39:
                done = True
            if snake.segment_y[0] < 0:
                done = True
            if snake.segment_y[0] > 39:
                done = True
            if i > 0:
                curr_x = snake.segment_x[i]
                curr_y = snake.segment_y[i]
                head_x = snake.segment_x[0]
                head_y = snake.segment_y[0]
                if curr_x==head_x and curr_y==head_y:
                    done = True
        
          
        # ADD FOOD :)
        
        if food_got == True:
            food_x = rd.randint(0,39)
            food_y = rd.randint(0,39)
            food_got = False
        #if snake.movement_direction == 0:
        head_x = snake.segment_x[0]
        head_y = snake.segment_y[0]
        
        if food_x==head_x and food_y==head_y:
            food_got = True
            snake.segment_x = np.append(snake.segment_x,snake.segment_x[snake.segments-1])
            snake.segment_y = np.append(snake.segment_y,snake.segment_y[snake.segments-1])
            snake.segments = snake.segments+1
        
        
        pygame.display.flip()
        clock.tick(120)



pygame.display.flip()
time.sleep(10)
pygame.quit()