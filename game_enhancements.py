import pygame
import random

# Initialize Pygame mixer for sounds
pygame.mixer.init()

# Load sounds
try:
    match_sound = pygame.mixer.Sound("match.wav")
    level_up_sound = pygame.mixer.Sound("level_up.wav")
    power_up_sound = pygame.mixer.Sound("power_up.wav")
except pygame.error:
    print("Error: Sound files not found. Ensure match.wav, level_up.wav, and power_up.wav exist.")

def play_match_sound():
    """Plays a sound when a match is made."""
    match_sound.play()

def play_level_up_sound():
    """Plays a sound when leveling up."""
    level_up_sound.play()

def play_power_up_sound():
    """Plays a sound when a power-up is activated."""
    power_up_sound.play()

def add_power_ups(grid):
    """Randomly assigns power-ups in the grid."""
    for _ in range(3):  # Add 3 power-ups randomly
        x, y = random.randint(0, 7), random.randint(0, 7)
        grid[y][x] = (255, 255, 255)  # White color represents power-up
    return grid

def check_power_up(grid, x, y):
    """Check if the tile is a power-up and trigger effect."""
    if grid[y][x] == (255, 255, 255):  # If it's a power-up
        for row in range(len(grid)):
            grid[row][x] = None  # Clears entire column
        play_power_up_sound()
        return True
    return False

def update_game_state(screen, grid, score, level, remaining_time, font):
    """Updates UI and animations."""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    timer_text = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
    screen.blit(score_text, (20, 620))
    screen.blit(level_text, (250, 620))
    screen.blit(timer_text, (450, 620))
