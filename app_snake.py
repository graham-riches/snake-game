# -*- coding: utf-8 -*-
"""
Created on Fri Sept 27, 2019

@author: Graham Cracker

Snake class for snake game. It has segments, and it can move.
"""

import numpy as np


class Snake:
    def __init__(self, *args, **kwargs):
        self.segments = 4  # size of the snake to start
        # all segments start at 0
        self.segment_x = np.array([4, 3, 2, 1])
        self.segment_y = np.array([0, 0, 0, 0])
        self.movement_direction = 0

        # game pixel grid for smooth animations.
        self.gridX = np.linspace(0, 39, 40)
        self.gridY = np.linspace(0, 39, 40)

    def move_snake(self):
        # movement direction --> 0 right, 1 up, 2 left, 3 down
        # move trailing limbs up to new positions
        for i in range(1, self.segments):
            self.segment_x[self.segments-i] = self.segment_x[self.segments-i-1]
            self.segment_y[self.segments-i] = self.segment_y[self.segments-i-1]
        # update the head position
        if self.movement_direction == 0:
            self.segment_x[0] = self.segment_x[0]+1
        if self.movement_direction == 1:
            self.segment_y[0] = self.segment_y[0]+1
        if self.movement_direction == 2:
            self.segment_x[0] = self.segment_x[0]-1
        if self.movement_direction == 3:
            self.segment_y[0] = self.segment_y[0]-1
