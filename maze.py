import pygame, sys
from pygame.locals import *
from colors import *
from templates import *


# Global Constants
IDLE    = "idle"
LEFT    = "left"
RIGHT   = "right"
UP      = "up"
DOWN    = "down"
TILE_WIDTH = 16
TILE_HEIGHT = 16
PLAYER_WIDTH = 8
PLAYER_SPEED = 5


# Classes
class Wall:
    def __init__(self, x, y, width, height, solid=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.solid = False

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Maze:
    def __init__(self, window, x, y, wall_width, wall_height, template):
        self.window = window
        self.x = x
        self.y = y
        self.rows = len(template["maze"])
        self.columns = len(template["maze"][0])
        self.wall_width = wall_width
        self.wall_height = wall_height
        self.template = template["maze"]
        self.tiles_map = template["tiles"]
        self._init_maze()

    def _init_maze(self):
        self.maze = []
        self.tiles = []
        for i in range(self.rows):
            self.maze.append([])
            for j in range(self.columns):
                wall = Wall(
                    self.y + (j * self.wall_height),
                    self.x + (i * self.wall_width),
                    self.wall_width,
                    self.wall_height
                )
                if self.template[i][j] > 0:
                    wall.solid = True
                self.maze[i].append(wall)
        tile_earth = self.get_tile(1, 0)
        tile_stone = self.get_tile(1, 8)
        self.tiles.append(tile_earth)
        self.tiles.append(tile_stone)

    def draw(self):
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.maze[i][j].solid:
                        pygame.draw.rect(self.window, BLACK, self.maze[i][j].rect(), 1)
                    self.window.blit(self.tiles[self.template[i][j]], self.maze[i][j].rect().topleft)

    def check_collision(self, rect):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.maze[i][j] is None:
                    continue
                if self.maze[i][j].rect().colliderect(rect) and self.maze[i][j].solid:
                    return True
        return False

    def get_tile(self, x, y):
        tile_set = pygame.image.load(self.tiles_map).convert_alpha()
        rect = pygame.Rect(x * TILE_WIDTH, y * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        tile = tile_set.subsurface(rect).copy()
        return tile



class Player:
    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.speed = PLAYER_SPEED
        self.moving = False

    def move(self, direction, maze):
        dx, dy = 0, 0

        if direction == LEFT:
            dx = -self.speed
        elif direction == RIGHT:
            dx = self.speed
        elif direction == UP:
            dy = -self.speed
        elif direction == DOWN:
            dy = self.speed

        future_rect = pygame.Rect(self.x + dx, self.y + dy, self.width, self.width)

        if not maze.check_collision(future_rect):
            self.x += dx
            self.y += dy

        self.moving = direction if dx != 0 or dy != 0 else IDLE

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.width)

    def draw(self):
        pygame.draw.rect(self.window, BLUE, self.rect())


# Main Function
def main():
    pygame.init()
    FPS = 30
    GAME_CLOCK = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Maze Runner")
    maze = Maze(WINDOW, 0, 0, TILE_WIDTH, TILE_HEIGHT, MAZE_TEMPLATE_00)
    player = Player(WINDOW, 176, 0)
    player_directions = []

    while True:
        WINDOW.fill(BLACK)
        maze.draw()
        player.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_r:
                player.x = 25
                player.y = 0
                player.moving = IDLE
            elif event.type == KEYDOWN and event.key == K_a and LEFT not in player_directions:
                player_directions.append(LEFT)
            elif event.type == KEYDOWN and event.key == K_d and RIGHT not in player_directions:
                    player_directions.append(RIGHT)
            elif event.type == KEYDOWN and event.key == K_w and UP not in player_directions:
                player_directions.append(UP)
            elif event.type == KEYDOWN and event.key == K_s and DOWN not in player_directions:
                    player_directions.append(DOWN)
            elif event.type == KEYUP and event.key == K_a and LEFT in player_directions:
                player_directions.remove(LEFT)
            elif event.type == KEYUP and event.key == K_d and RIGHT in player_directions:
                    player_directions.remove(RIGHT)
            elif event.type == KEYUP and event.key == K_w and UP in player_directions:
                player_directions.remove(UP)
            elif event.type == KEYUP and event.key == K_s and DOWN in player_directions:
                    player_directions.remove(DOWN)

        if not player_directions:
            player.move(IDLE, maze)
        else:
            if player_directions[-1] == LEFT:
                player.move(LEFT, maze)
            elif player_directions[-1] == RIGHT:
                player.move(RIGHT, maze)
            elif player_directions[-1] == UP:
                player.move(UP, maze)
            elif player_directions[-1] == DOWN:
                player.move(DOWN, maze)

        pygame.display.update()
        GAME_CLOCK.tick(FPS)


main()
