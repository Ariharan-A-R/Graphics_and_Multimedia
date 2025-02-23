import pygame
import random
import time
from game_enhancements import add_power_ups, play_match_sound, play_level_up_sound, check_power_up, update_game_state

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 750
GRID_SIZE = 8
TILE_SIZE = WIDTH // GRID_SIZE
FPS = 60
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)]
BACKGROUND_COLOR = (30, 30, 30)
SCORE = 0
LEVEL = 1
TIME_LIMIT = 60  # 60 seconds per level
FONT = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jewel Match Puzzle")

def generate_grid():
    while True:
        grid = [[random.choice(COLORS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        if not check_initial_matches(grid):
            return grid

def check_initial_matches(grid):
    return any(check_matches(grid))  # Ensure no initial matches

def swap_tiles(grid, pos1, pos2):
    grid[pos1[1]][pos1[0]], grid[pos2[1]][pos2[0]] = grid[pos2[1]][pos2[0]], grid[pos1[1]][pos1[0]]

def check_matches(grid):
    global SCORE
    matched = set()
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                matched.update([(x, y), (x+1, y), (x+2, y)])
    
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE - 2):
            if grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                matched.update([(x, y), (x, y+1), (x, y+2)])
    
    if matched:
        for x, y in matched:
            SCORE += 10
            grid[y][x] = None
    
    return matched

def collapse_grid(grid):
    for x in range(GRID_SIZE):
        column = [grid[y][x] for y in range(GRID_SIZE) if grid[y][x] is not None]
        column = [None] * (GRID_SIZE - len(column)) + column
        for y in range(GRID_SIZE):
            grid[y][x] = column[y]

def refill_grid(grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] is None:
                grid[y][x] = random.choice(COLORS)

def animate_tile_fall(grid):
    for _ in range(5):  # Number of animation frames
        screen.fill(BACKGROUND_COLOR)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if grid[y][x]:
                    pygame.draw.rect(screen, grid[y][x], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
        pygame.display.flip()
        pygame.time.delay(50)

grid = add_power_ups(generate_grid())
running = True
selected_tile = None
mouse_dragging = False
timer_start = time.time()

def check_time():
    return max(0, TIME_LIMIT - int(time.time() - timer_start))

while running:
    screen.fill(BACKGROUND_COLOR)
    update_game_state(screen, grid, SCORE, LEVEL, check_time(), FONT)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y < WIDTH:
                selected_tile = (x // TILE_SIZE, y // TILE_SIZE)
                mouse_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and mouse_dragging:
            x, y = event.pos
            target_tile = (x // TILE_SIZE, y // TILE_SIZE)
            if selected_tile and abs(selected_tile[0] - target_tile[0]) + abs(selected_tile[1] - target_tile[1]) == 1:
                swap_tiles(grid, selected_tile, target_tile)
                if check_matches(grid) or check_power_up(grid, target_tile[0], target_tile[1]):
                    collapse_grid(grid)
                    animate_tile_fall(grid)
                    refill_grid(grid)
                else:
                    swap_tiles(grid, selected_tile, target_tile)  # Revert if no match
            selected_tile = None
            mouse_dragging = False
    
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
