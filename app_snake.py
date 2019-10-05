# -*- coding: utf-8 -*-
"""
Created on Fri Sept 27, 2019

@author: Graham Riches

Snake class for snake game. It has segments, and it can move.
This is extendable to snake AI functionality.
"""


class Snake:
    def __init__(self):
        self.segments = 3
        self.segment_x = [3, 2, 1]
        self.segment_y = [0, 0, 0]
        self.movement_direction = 0
        self.directions = {'right':0, 'up':1, 'left':2, 'down':3}

    def move_snake(self):
        """
        Update snake segment locations
        """
        for i in range(1, self.segments):
            self.segment_x[self.segments-i] = self.segment_x[self.segments-i-1]
            self.segment_y[self.segments-i] = self.segment_y[self.segments-i-1]
        # update the head position
        if self.movement_direction == self.directions['right']:
            self.segment_x[0] = self.segment_x[0]+1
        if self.movement_direction == self.directions['up']:
            self.segment_y[0] = self.segment_y[0]+1
        if self.movement_direction == self.directions['left']:
            self.segment_x[0] = self.segment_x[0]-1
        if self.movement_direction == self.directions['down']:
            self.segment_y[0] = self.segment_y[0]-1
