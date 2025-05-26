import pygame, sys
from pygame.locals import *
from colors import *


# Constants
LEFT = 1
RIGHT = 3


# Classes
class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dimensions = (x, y, width, height)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Maze:
    def __init__(self, window, x, y, wall_width, wall_height, rows, columns):
        self.window = window
        self.x = x
        self.y = y
        self.rows = rows
        self.columns = columns
        self.wall_width = wall_width
        self.wall_height = wall_height
        self._init_maze()

    def _init_maze(self):
        self.maze = []
        self.template = []
        for i in range(self.rows):
            self.maze.append([])
            self.template.append([])
            for j in range(self.columns):
                wall = Wall(
                    self.y + (j * self.wall_height),
                    self.x + (i * self.wall_width),
                    self.wall_width,
                    self.wall_height
                )
                self.maze[i].append(wall)
                self.template[i].append(1)

    def draw(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.maze[i][j] is not None:
                    pygame.draw.rect(self.window, BLACK, self.maze[i][j].rect(), self.template[i][j])

    def print(self):
        for i in range(self.rows):
            print(self.template[i])
        print()

    def check_collision(self, point, button):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.maze[i][j].rect().collidepoint(point):
                    if button == LEFT:
                        self.template[i][j] = 0
                    elif button == RIGHT:
                        self.template[i][j] = 1
        return False


def main():
    rows = int(input("Enter the number of rows for the maze: "))
    columns = int(input("Enter the number of columns for the maze: "))

    pygame.init()
    WINDOW = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Maze Maker")
    maze = Maze(WINDOW, 0, 0, 20, 20, rows, columns)
    left_click = False
    right_click = False

    while True:
        WINDOW.fill(WHITE)
        maze.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                left_click = True
            elif event.type == MOUSEBUTTONDOWN and event.button == RIGHT:
                right_click = True
            elif event.type == MOUSEBUTTONUP and event.button == LEFT:
                left_click = False
            elif event.type == MOUSEBUTTONUP and event.button == RIGHT:
                right_click = False
            elif event.type == KEYUP and event.key == K_SPACE:
                maze.print()

            if left_click:
                maze.check_collision(pygame.mouse.get_pos(), LEFT)
            elif right_click:
                maze.check_collision(pygame.mouse.get_pos(), RIGHT)

        pygame.display.update()

main()