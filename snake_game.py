"""
Created on Fri Sep 27 21:08:34 2019

@author: Graham Riches
@brief snake game engine

"""
import sys
sys.path.append('C:\ProgramData\Anaconda3\Lib\site-packages')

import random as rd
import numpy as np
import pygame
import json
from snake_objs import Snake
from game_score import GameScore
from datetime import datetime


class SnakeGame:
    def __init__(self, grid_size=20, scaling_factor=39):
        """
        Generates a custom snake game with a variable resolution and a variable
        grid size for scale. 
        Note:
            scaling_factor is the number of pixels per grid square
        """
        self.display_x = grid_size*scaling_factor
        self.display_y = grid_size*scaling_factor
        self.score_size = 24  # pixels for the score area
        self.grid = grid_size  # number of grid locations
        self.unit_size = scaling_factor  # size of a single unit
        # handle the game grid with lists might not need these
        self.grid_x = list(range(0, grid_size))
        self.grid_y = list(range(0, grid_size))
        self.game_colors = dict(orange=(255, 100, 0), blue=(0, 128, 255),
                                black=(0, 0, 0), white=(255, 255, 255))
        self.directions = {'up': 3, 'down': 1, 'left': 2, 'right': 0}
        self.snake = Snake()
        self.score = GameScore()
        self.score.simple_score_with_highscore('snake_game')
        self.got_last_food = False  # user for animating the eating of the food
        self.len_at_last_food = self.snake.segments
        self.food_x = -1
        self.food_y = -1
        self.last_food_x = -1
        self.last_food_y = -1
        self.count_to_end = 0

    def load_highscore(self):
        path = self.score.get_path('snake_game')
        try:
            with open(path) as json_file:
                old_score = json.load(json_file)
            self.high_score = old_score['high_score']
        except:
            self.high_score = 0

    def save_score(self):
        path = self.score.get_path('snake_game')
        with open(path, 'w') as json_file:
            _score = {'high_score': self.score.get_score('snake_game')}
            json.dump(_score, json_file)

    def render_x(self, i):
        # return the snake pixel locations of the current location
        return (self.snake.segment_x[i]*20)+10+1

    def render_y(self, i):
        # return the snake pixel locations of the current location
        return (self.snake.segment_y[i]*20)+100+1

    def generate_food(self):
        self.last_food_x = self.food_x
        self.last_food_y = self.food_y
        self.food_x = rd.randint(1, self.grid-2)
        self.food_y = rd.randint(1, self.grid-2)

    def init_game(self, speed_modifier):
        """
        Setup pygame
            speed_modifier - units per second
        """
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.display_x,
                                               self.display_y + self.score_size))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf',
                                     round(self.score_size/1.25))
        self.speed_modifier = speed_modifier
        pygame.time.set_timer(pygame.USEREVENT, 10)
        self.load_highscore()

    def register_keypress(self, pressed_key):
        """
        Register a keypress to change directions but don't allow
        the snake to turn back on itself 180 degrees resulting in death
        """
        if pressed_key == pygame.K_UP and self.snake.movement_direction != self.directions['down']:
            self.snake.movement_direction = self.directions['up']
        elif pressed_key == pygame.K_DOWN and self.snake.movement_direction != self.directions['up']:
            self.snake.movement_direction = self.directions['down']
        elif pressed_key == pygame.K_LEFT and self.snake.movement_direction != self.directions['right']:
            self.snake.movement_direction = self.directions['left']
        elif pressed_key == pygame.K_RIGHT and self.snake.movement_direction != self.directions['left']:
            self.snake.movement_direction = self.directions['right']

    def check_inbounds(self):
        """
        check that the snake is in the game region
        """
        valid = True
        if self.snake.segment_x[0] < 0:
            valid = False
        if self.snake.segment_x[0] == self.grid - 1:
            valid = False
        if self.snake.segment_y[0] < 0:
            valid = False
        if self.snake.segment_y[0] == self.grid - 1:
            valid = False
        for i in range(1, self.snake.segments):
            if self.snake.segment_x[0] == self.snake.segment_x[i] and self.snake.segment_y[0] == self.snake.segment_y[i]:
                valid = False
        return valid

    def render_segment(self, loc_x, loc_y, segment_direction, interval,
                       is_head, is_food):
        """
        blit a single snake segment with pygame.
        pygame rectangle object uses top and left coordinates.
        interval is a pixel interpolation value for smoothing video
            every frame needs to continue in the direction it was moving
            prior to the update
        if is_head is for rendering the snakes head
        is_food is for rendering the food the snake just ate
        """
        offset = 1
        eye_offset = 7
        eye_radius = 6
        if is_head or is_food:
            head_modifier = 6*offset
        else:
            head_modifier = offset
        # location is the baseline location
        # add a pixel modifier for movement direction for smooth animation
        unit_width = self.unit_size-2*offset
        radius = int(unit_width/2 + head_modifier)
        if segment_direction == self.directions['up']:
            location = (loc_x*self.unit_size + offset,
                        loc_y*self.unit_size + offset - interval)
            circ_cent = (int(location[0] + 0.5*unit_width),
                         int(location[1] + 0.5*unit_width))
            eye_1_loc = (circ_cent[0] - eye_offset, circ_cent[1] - eye_offset)
            eye_2_loc = (circ_cent[0] + eye_offset, circ_cent[1] - eye_offset)

        elif segment_direction == self.directions['down']:
            location = (loc_x*self.unit_size + offset,
                        loc_y*self.unit_size + offset + interval)
            circ_cent = (int(location[0] + 0.5*unit_width),
                         int(location[1] + 0.5*unit_width))
            eye_1_loc = (circ_cent[0] - eye_offset, circ_cent[1] + eye_offset)
            eye_2_loc = (circ_cent[0] + eye_offset, circ_cent[1] + eye_offset)

        elif segment_direction == self.directions['left']:
            location = (loc_x*self.unit_size + offset - interval,
                        loc_y*self.unit_size + offset)
            circ_cent = (int(location[0] + 0.5*unit_width),
                         int(location[1] + 0.5*unit_width))
            eye_1_loc = (circ_cent[0] - eye_offset, circ_cent[1] + eye_offset)
            eye_2_loc = (circ_cent[0] - eye_offset, circ_cent[1] - eye_offset)

        elif segment_direction == self.directions['right']:
            location = (loc_x*self.unit_size + offset + interval,
                        loc_y*self.unit_size + offset)
            circ_cent = (int(location[0] + 0.5*unit_width),
                         int(location[1] + 0.5*unit_width))
            eye_1_loc = (circ_cent[0] + eye_offset, circ_cent[1] - eye_offset)
            eye_2_loc = (circ_cent[0] + eye_offset, circ_cent[1] + eye_offset)

        pygame.draw.circle(self.screen, self.game_colors['blue'],
                           circ_cent, radius)
        # if it's the head, draw the eyes
        if is_head:
            pygame.draw.circle(self.screen, self.game_colors['white'],
                               eye_1_loc, eye_radius)
            pygame.draw.circle(self.screen, self.game_colors['white'],
                               eye_2_loc, eye_radius)
            pygame.draw.circle(self.screen, self.game_colors['black'],
                               eye_1_loc, int(eye_radius/2 + 1))
            pygame.draw.circle(self.screen, self.game_colors['black'],
                               eye_2_loc, int(eye_radius/2 + 1))

    def render_bounds(self):
        """
        draw the game bounds
        """
        pygame.draw.rect(self.screen, self.game_colors['white'],
                         (0, 0, self.display_x, self.display_y), 1)

    def wait_ticks(self):
        self.clock.tick(self.speed_modifier)

    def update_snake_movement(self):
        """
        update the snakes position
        """
        for i in range(1, self.snake.segments):
            self.snake.segment_y[-i] = self.snake.segment_y[-i-1]
            self.snake.segment_x[-i] = self.snake.segment_x[-i-1]

        if self.snake.movement_direction == self.directions['up']:
            self.snake.segment_y[0] -= 1
        elif self.snake.movement_direction == self.directions['down']:
            self.snake.segment_y[0] += 1
        elif self.snake.movement_direction == self.directions['left']:
            self.snake.segment_x[0] -= 1
        elif self.snake.movement_direction == self.directions['right']:
            self.snake.segment_x[0] += 1

    def render_frame(self):
        """
        Everything for a single frame
        """
        for j in range(self.unit_size):
            self.screen.fill(self.game_colors['black'])  # background
            self.render_bounds()  # boundary
            self.render_food()
            for i in range(self.snake.segments):
                if i == 0:
                    segment_direction = self.snake.movement_direction
                    is_head = True
                    is_food = False
                else:
                    # get previous segment location and move in that direction
                    prev_loc = [self.snake.segment_x[i-1], self.snake.segment_y[i-1]]
                    curr_loc = [self.snake.segment_x[i], self.snake.segment_y[i]]
                    if curr_loc[0] == self.last_food_x and curr_loc[1] == self.last_food_y:
                        if self.count_to_end < self.len_at_last_food*self.unit_size:
                            self.count_to_end += 1
                            is_food = True
                            is_head = False
                        else:
                            is_food = False
                            is_head = False
                            self.got_last_food = False
                    else:
                        is_food = False
                        is_head = False
                    if prev_loc[0] == curr_loc[0] and prev_loc[1] < curr_loc[1]:
                        segment_direction = self.directions['up']
                    elif prev_loc[0] == curr_loc[0] and prev_loc[1] > curr_loc[1]:
                        segment_direction = self.directions['down']
                    elif prev_loc[0] < curr_loc[0] and prev_loc[1] == curr_loc[1]:
                        segment_direction = self.directions['left']
                    elif prev_loc[0] > curr_loc[0] and prev_loc[1] == curr_loc[1]:
                        segment_direction = self.directions['right']
                self.render_segment(self.snake.segment_x[i],
                                    self.snake.segment_y[i],
                                    segment_direction, j, is_head, is_food)
            self.render_score()
            pygame.display.flip()
            pygame.time.delay(self.speed_modifier)

    def render_food(self):
        """
        render the food to a random location in the game window
        """
        offset = 1
        location = (self.food_x*self.unit_size + offset,
                    self.food_y*self.unit_size + offset,
                    self.unit_size-2*offset,
                    self.unit_size-2*offset)
        pygame.draw.rect(self.screen, self.game_colors['orange'], location)

    def render_score(self):
        """ show the score at the bottom """
        location = (0, self.display_y, self.display_x, self.score_size)
        pygame.draw.rect(self.screen, self.game_colors['black'], location)
        score_text = self.font.render('Score: {}    High Score: {}'.format(self.score.get_score('snake_game'), self.high_score),
                                      True, self.game_colors['white'])
        rect = score_text.get_rect()
        rect.center = (self.display_x / 2, self.display_y + self.score_size/2)
        self.screen.blit(score_text, rect)

    def check_got_food(self):
        if self.snake.segment_x[0] == self.food_x and self.snake.segment_y[0] == self.food_y:
            self.snake.segments += 1
            self.snake.segment_x.append(self.snake.segment_x[-1])
            self.snake.segment_y.append(self.snake.segment_y[-1])
            self.generate_food()
            self.score.add(1, 'snake_game')
            self.got_last_food = True
            self.len_at_last_food = self.snake.segments - 1
            self.count_to_end = 0

    def start_splash_screen(self):
        """
        splash screen for startup/keypress
        """
        self.screen.fill(self.game_colors['black'])  # background
        self.render_bounds()  # boundary
        text_loc = (0, self.display_y, self.display_x, self.score_size)
        pygame.draw.rect(self.screen, self.game_colors['black'], text_loc)
        start_text = self.font.render('Press any key to start', True,
                                      self.game_colors['white'])
        rect = start_text.get_rect()
        rect.center = (self.display_x / 2, self.display_y/2)
        self.screen.blit(start_text, rect)
        pygame.display.flip()

    def game_over_screen(self):
        """
        show the game over and high score screen
        """
        self.screen.fill(self.game_colors['black'])  # background
        self.render_bounds()  # boundary
        text_loc = (self.display_y/2, self.display_y,
                    self.display_x, self.score_size)
        pygame.draw.rect(self.screen, self.game_colors['black'], text_loc)
        game_over_text = self.font.render('GAME OVER... SCORE: {}'.format(self.score.get_score('snake_game')), True,
                                      self.game_colors['white'])
        rect = game_over_text.get_rect()
        rect.center = (self.display_x / 2, self.display_y/2)
        self.screen.blit(game_over_text, rect)
        pygame.display.flip()

    def snake_runner(self):
        """
        main game loop
        """
        start_up = True
        alive = True
        quit_event = False
        while start_up:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    start_up = False
                if event.type == pygame.QUIT:
                    alive = False
                    quit_event = True
                    start_up = False
                    game_over = False
                    break
            self.start_splash_screen()
        self.generate_food()
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alive = False  # handle game end
                    quit_event = True
                if event.type == pygame.KEYDOWN:
                    self.register_keypress(event.key)
            self.render_frame()
            self.update_snake_movement()
            alive = self.check_inbounds()
            self.check_got_food()
        if self.score.get_score('snake_game') > self.high_score:
            self.save_score()
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    alive = False  # handle game end
                    quit_event = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    game_over = False
                self.game_over_screen()
        return quit_event


if __name__ == '__main__':
    game_running = True
    while game_running:
        snake_game = SnakeGame(scaling_factor=30, grid_size=20)
        snake_game.init_game(3)
        should_quit = snake_game.snake_runner()
        game_running = not should_quit
    pygame.quit()
    sys.exit()
