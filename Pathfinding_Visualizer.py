"""
@Author: Jaden Chang
Created: 2023-05-04
"""
import pygame, math
from queue import PriorityQueue

#Initializes pygame
pygame.init()

#RGB colour values and assigns them
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (57,255,20)
RED = (255,49,49)
GREY = (169,169,169)
CYAN = (0,100,100)
PURPLE = (160,32,240)
YELLOW = (255,255,0)
BLUE = (100, 149, 237)

#Initializes the pygame screen
TOTAL_WIDTH = 1200
WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode((TOTAL_WIDTH, HEIGHT))
screen.fill(WHITE)
pygame.display.update()
pygame.display.set_caption('Pathfinding Visualizer')

#A class to define each node
class Node:
    #Node class constructor
    def __init__(self,row,col,width,total_rows):
        self.colour = WHITE
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.neighbours = []

    #Sets the state of the node
    def set_start(self):
        self.colour = GREEN
    def set_end(self):
        self.colour = RED
    def set_visted(self):
        self.colour = PURPLE
    def set_open(self):
        self.colour = CYAN
    def set_path(self):
        self.colour = YELLOW
    def set_wall(self):
        self.colour = BLACK
    def set_unvisited(self):
        self.colour = WHITE

    #Checks the state of the node
    def is_start(self):
        return self.colour == GREEN
    def is_end(self):
        return self.colour == RED
    def is_visited(self):
        return self.colour == PURPLE
    def is_open(self):
        return self.colour == CYAN
    def is_path(self):
        return self.colour == YELLOW
    def is_wall(self):
        return self.colour == BLACK
    def is_unvisited(self):
        return self.colour == WHITE
    
    #Draws the node onto the screen
    def draw_node(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.width))

    def neighbours(self):
        pass

#Creates the grid and each node
def add_grid(rows, width):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, width // rows, rows)
            grid[i].append(node)
    return grid

#Draws the grid lines
def draw_grid(screen, width, rows):
    node_width = width // rows
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, node_width * i), (width, node_width * i))
        pygame.draw.line(screen, GREY, (node_width * i, 0), (node_width * i, width))
    pygame.draw.line(screen, GREY, (node_width * (rows), 0), (node_width * (rows), width))

#Draws the instruction panel and buttons
def draw_panel(screen, width, rows):
    pygame.draw.rect(screen, BLUE, [WIDTH, 0, TOTAL_WIDTH - WIDTH, HEIGHT], 1000)
    pygame.draw.rect(screen, BLACK, [WIDTH, 0, TOTAL_WIDTH - WIDTH, HEIGHT], 4)
    font_title = pygame.font.SysFont(None, 48)
    font_instr = pygame.font.SysFont(None, 16)
    font_subtitle = pygame.font.SysFont(None, 24)
    title1 = font_title.render('Pathfinding', True, WHITE)
    title2 = font_title.render('Visualizer', True, WHITE)
    instr_title = font_instr.render('Instructions:', True, WHITE)
    instr_desc1 = font_instr.render('•Place start/end/wall nodes', True, WHITE)
    instr_desc2 = font_instr.render('•Remove start/end/wall nodes (right-click)', True, WHITE)
    instr_desc3 = font_instr.render('•Select search algorithm', True, WHITE)
    instr_desc4 = font_instr.render('•Press the \'START\' button', True, WHITE)
    subtitle1 = font_subtitle.render('Select Algorithm:', True, WHITE)
    screen.blit(title1, (960, 20))
    screen.blit(title2, (970, 55))
    screen.blit(instr_title, (930, 120))
    screen.blit(instr_desc1, (940, 135))
    screen.blit(instr_desc2, (940, 150))
    screen.blit(instr_desc3, (940, 165))
    screen.blit(instr_desc4, (940, 180))
    screen.blit(subtitle1, (980, 220))


#Draws and displays all of the visual components 
def draw_all(screen, width, rows, grid):
    screen.fill(WHITE)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].draw_node(screen)
    draw_panel(screen, width, rows)
    draw_grid(screen, width, rows)
    pygame.display.update()

#Main function that computes user's input
def main(screen, width):
    rows = 36 #Have the user specify later on how many rows (set amount 36, 100, etc)

    grid = add_grid(rows, width)
    start = None
    end = None
    algorithm = None

    running = True
    started = False

    while running:
        draw_all(screen, width, rows, grid)
        #Checks user's event actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if started:
                continue
            #Starts search algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start != None and end != None:
                    started = True
                    #Call upon selected algorithm
            #Checks if user wants to place node blocks or press buttons, then does accordingly
            if pygame.mouse.get_pressed()[0]:
                (point_x, point_y) = pygame.mouse.get_pos()
                (pos_x, pos_y) = ((point_x // (width // rows)), (point_y // (width // rows)))
                if point_x >= width:
                    continue # Checks if user presses button
                elif start == None and end != grid[pos_x][pos_y]:
                    start = grid[pos_x][pos_y]
                    grid[pos_x][pos_y].set_start()
                elif start != None and end == None and start != grid[pos_x][pos_y]:
                    end = grid[pos_x][pos_y]
                    grid[pos_x][pos_y].set_end()
                elif start != grid[pos_x][pos_y] and end != grid[pos_x][pos_y]:
                    grid[pos_x][pos_y].set_wall()
            #Erase node blocks
            if pygame.mouse.get_pressed()[2]:
                (point_x, point_y) = pygame.mouse.get_pos()
                (pos_x, pos_y) = ((point_x // (width // rows)), (point_y // (width // rows)))
                if point_x >= width:
                    continue
                elif start == grid[pos_x][pos_y]:
                    start = None
                elif end == grid[pos_x][pos_y]:
                    end = None
                grid[pos_x][pos_y].set_unvisited()
                
main(screen, WIDTH)