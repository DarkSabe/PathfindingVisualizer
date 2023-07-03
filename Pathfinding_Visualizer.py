"""
@Author: Jaden Chang
Created: 2023-05-04
"""
import pygame, math
from queue import PriorityQueue
from collections import deque

#Initializes pygame
pygame.init()

#RGB colour values and assigns them
BLACK = (0,0,0)
WHITE = (255,255,255)
NEON_GREEN = (57,255,20)
GREEN = (34,177,76)
NEON_RED = (255,49,49)
RED = (220,20,60)
GREY = (169,169,169)
CYAN = (127,255,212)
PURPLE = (147,112,219)
LIGHT_PURPLE = (204, 153, 255)
YELLOW = (255,255,102)
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
    def __init__(self, row, col, width, total_rows):
        self.colour = WHITE
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows

    #Sets the state of the node
    def set_start(self):
        self.colour = NEON_GREEN
    def set_end(self):
        self.colour = NEON_RED
    def set_visited(self):
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
        return self.colour == NEON_GREEN
    def is_end(self):
        return self.colour == NEON_RED
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
        return [(self.row - 1, self.col), (self.row, self.col - 1), (self.row + 1, self.col), (self.row, self.col + 1)]

def bfs(screen, rows, grid, start, end):
    rows = len(grid)
    cols = len(grid[0])

    queue = deque()
    queue.append(start)
    parents = {start: None}

    while queue:
        node = queue.popleft()

        if node.is_end():
            break
        elif node.is_wall() or node.is_visited():
            continue
        else:
            if node.is_open():
                node.set_visited()
                node.draw_node(screen)
                pygame.display.update()
            neighbours = node.neighbours()
            for neighbour in neighbours:
                pos_x, pos_y = neighbour
                if 0 <= pos_x < rows and 0 <= pos_y < cols:
                    neighbour_node = grid[pos_x][pos_y]
                    if neighbour_node.is_wall() or neighbour_node.is_visited() or neighbour_node.is_start():
                        continue
                    if neighbour_node.is_unvisited():
                        neighbour_node.set_open()
                    neighbour_node.draw_node(screen)
                    queue.append(grid[pos_x][pos_y])
                    pygame.display.update()
                    if neighbour_node.is_end():
                        parents[end] = node
                        break
                    parents[neighbour_node] = node

    if end not in parents:
        return None
    
    path = []
    current_node = end
    while current_node:
        path.append(current_node)
        current_node = parents[current_node]

    path = path[::-1]

    for path_node in path:
        if path_node.is_start() or path_node.is_end():
            continue
        path_node.set_path()
        path_node.draw_node(screen)
    pygame.display.update()

    return len(path)

def draw_alg_buttons(screen):
    font1 = pygame.font.SysFont(None, 48)
    font2 = pygame.font.SysFont(None, 24)

    #Draws the A* button
    pygame.draw.rect(screen, WHITE, [990, 260, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [990, 260, 115, 75], 5, border_radius= 15)
    astar_title = font1.render("A*", True, BLACK)
    screen.blit(astar_title, (1030, 283))
    
    #Draws the BFS button
    pygame.draw.rect(screen, WHITE, [920, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 360, 115, 75], 5, border_radius= 15)
    bfs_title = font1.render("BFS", True, BLACK)
    screen.blit(bfs_title, (943, 383))

    #Draws the Dijkstra's button
    pygame.draw.rect(screen, WHITE, [1060, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [1060, 360, 115, 75], 5, border_radius= 15)
    dijkstras_title = font2.render("Dijkstra's", True, BLACK)
    screen.blit(dijkstras_title, (1082, 390))
    
    #Draws the START button
    pygame.draw.rect(screen, BLACK, [920, 460, 255, 75], border_radius= 15)

    #Draws the stats board
    pygame.draw.rect(screen, BLACK, [920, 560, 255, 200])
    stats_title = font2.render("Stats:", True, WHITE)
    screen.blit(stats_title, (1020, 573))

    #Draws the RESET button
    pygame.draw.rect(screen, GREY, [920, 792, 255, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 792, 255, 75], 5, border_radius= 15)
    reset_title = font1.render("Reset", True, BLACK)
    screen.blit(reset_title, (1000, 815))
    
def draw_start_button(screen):
    font = pygame.font.SysFont(None, 48)
    
    #Draws the START button
    pygame.draw.rect(screen, GREEN, [920, 460, 255, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 460, 255, 75], 5, border_radius= 15)
    start_title = font.render("Start", True, BLACK)
    screen.blit(start_title, (1007, 482))

def draw_astar_button(screen):
    font1 = pygame.font.SysFont(None, 48)
    font2 = pygame.font.SysFont(None, 24)
    #Draws the highlighted A* button
    pygame.draw.rect(screen, LIGHT_PURPLE, [990, 260, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [990, 260, 115, 75], 5, border_radius= 15)
    astar_title = font1.render("A*", True, BLACK)
    screen.blit(astar_title, (1030, 283))

    #Clears the highlighted BFS button
    pygame.draw.rect(screen, WHITE, [920, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 360, 115, 75], 5, border_radius= 15)
    bfs_title = font1.render("BFS", True, BLACK)
    screen.blit(bfs_title, (943, 383))

    #Clears the highlighted Dijkstra's button
    pygame.draw.rect(screen, WHITE, [1060, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [1060, 360, 115, 75], 5, border_radius= 15)
    dijkstras_title = font2.render("Dijkstra's", True, BLACK)
    screen.blit(dijkstras_title, (1082, 390))

def draw_bfs_button(screen):
    font1 = pygame.font.SysFont(None, 48)
    font2 = pygame.font.SysFont(None, 24)

    #Draws the highlighted BFS button
    pygame.draw.rect(screen, LIGHT_PURPLE, [920, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 360, 115, 75], 5, border_radius= 15)
    bfs_title = font1.render("BFS", True, BLACK)
    screen.blit(bfs_title, (943, 383))

    #Clears the highlighted A* button
    pygame.draw.rect(screen, WHITE, [990, 260, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [990, 260, 115, 75], 5, border_radius= 15)
    astar_title = font1.render("A*", True, BLACK)
    screen.blit(astar_title, (1030, 283))

    #Clears the highlighted Dijkstra's button
    pygame.draw.rect(screen, WHITE, [1060, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [1060, 360, 115, 75], 5, border_radius= 15)
    dijkstras_title = font2.render("Dijkstra's", True, BLACK)
    screen.blit(dijkstras_title, (1082, 390))

def draw_dijkstras_button(screen):
    font1 = pygame.font.SysFont(None, 48)
    font2 = pygame.font.SysFont(None, 24)

    #Draws the highlighted Dijkstra's button
    pygame.draw.rect(screen, LIGHT_PURPLE, [1060, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [1060, 360, 115, 75], 5, border_radius= 15)
    dijkstras_title = font2.render("Dijkstra's", True, BLACK)
    screen.blit(dijkstras_title, (1082, 390))

    #Clears the highlighted A* button
    pygame.draw.rect(screen, WHITE, [990, 260, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [990, 260, 115, 75], 5, border_radius= 15)
    astar_title = font1.render("A*", True, BLACK)
    screen.blit(astar_title, (1030, 283))

    #Clears the highlighted BFS button
    pygame.draw.rect(screen, WHITE, [920, 360, 115, 75], border_radius= 15)
    pygame.draw.rect(screen, BLACK, [920, 360, 115, 75], 5, border_radius= 15)
    bfs_title = font1.render("BFS", True, BLACK)
    screen.blit(bfs_title, (943, 383))

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
def draw_all(screen, width, rows, grid, algorithm):
    screen.fill(WHITE)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].draw_node(screen)
    draw_panel(screen, width, rows)
    draw_grid(screen, width, rows)
    draw_alg_buttons(screen)

    if algorithm == 1:
        draw_astar_button(screen)
        draw_start_button(screen)
    elif algorithm == 2:
        draw_bfs_button(screen)
        draw_start_button(screen)
    elif algorithm == 3:
        draw_dijkstras_button(screen)
        draw_start_button(screen)
    #draw_start_button(screen) # remove and place into algorithm button functions
    pygame.display.update()

#Main function that computes user's input
def main(screen, width):
    rows = 36 #Have the user specify later on how many rows (set amount 36, 100, etc)

    grid = add_grid(rows, width)
    start = None
    end = None
    algorithm = None

    running = True
    #started = False

    while running:
        draw_all(screen, width, rows, grid, algorithm)
        #Checks user's event actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            #if started:
            #    continue
           
                    #Call upon selected algorithm
            #Checks if user wants to place node blocks or press buttons, then does accordingly
            if pygame.mouse.get_pressed()[0]:
                (point_x, point_y) = pygame.mouse.get_pos()
                (pos_x, pos_y) = ((point_x // (width // rows)), (point_y // (width // rows)))
                #Starts search algorithm
                if ((920 <= point_x <= 1175) and (460 <= point_y <= 535)) and (start != None) and (end != None) and (algorithm != None):
                    if algorithm == 1:
                        pass #call upon A* 
                    elif algorithm == 2:
                        bfs(screen, rows, grid, start, end) #call upon BFS
                    elif algorithm == 3:
                        pass #call upon Dijkstra's
                    algorithm = None 
                    continue
                elif ((990 <= point_x <= 1105) and (260 <= point_y <= 335)):
                    algorithm = 1   #indicates that A* algorithm has been chosen
                elif ((920 <= point_x <= 1035) and (360 <= point_y <= 435)):
                    algorithm = 2   #indicates that BFS algorithm has been chosen
                elif ((1060 <= point_x <= 1175) and (360 <= point_y <= 435)):
                    algorithm = 3   #indicates that Dijkstra's algorithm has been chosen
                elif ((920 <= point_x <= 1175) and (792 <= point_y <= 867)): #checks if "reset" button was pressed, then resets the board
                    for i in range(rows):
                        for j in range(rows):
                            grid[i][j].set_unvisited()
                    start = None
                    end = None
                    algorithm = None
                elif point_x >= width:
                    continue
                elif start == None and end != grid[pos_x][pos_y]: #Checks if start block has been placed
                    start = grid[pos_x][pos_y]
                    grid[pos_x][pos_y].set_start()
                elif start != None and end == None and start != grid[pos_x][pos_y]: #Checks if end block has been placed
                    end = grid[pos_x][pos_y]
                    grid[pos_x][pos_y].set_end()
                elif start != grid[pos_x][pos_y] and end != grid[pos_x][pos_y]: #then places a wall if both end and start blocks have been placed
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