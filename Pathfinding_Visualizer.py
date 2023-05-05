"""
@Author: Jaden Chang
Created: 2023-05-04
"""
import pygame, sys
from queue import PriorityQueue

#Initializes pygame
pygame.init()

#RGB colour values and assigns them
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (57,255,20)
RED = (255,49,49)

#Initializes the pygame screen
(width, height) = (900,900)
screen = pygame.display.set_mode((width,height))
screen.fill(WHITE)
pygame.display.update()

class Node:
    def __init__(self,row,col,width, total_rows):
        self.colour = WHITE
        self.row = row
    def is_start(self):
        self.colour = GREEN
    def is_end(self):
        self.colour = RED
    def is_visited(self):
        pass
    def is_open(self):
        pass
    def is_path(self):
        pass
    def is_wall(self):
        self.colour = BLACK
    def neighbours(self):
        pass


def add_grid():
    pass

def draw_grid():
    pass

def main():
    pass