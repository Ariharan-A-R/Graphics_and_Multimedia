import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

# Initialize pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL Space Shooter")

# Load sounds
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.mp3")
explosion_sound = pygame.mixer.Sound("explosion.mp3")
bg_music = "bgm.mp3"
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)  # Loop background music

# Game Variables
ship_x = 0
ship_speed = 0.1
score = 0
font = pygame.font.Font(None, 36)

# Asteroids
asteroids = [[random.uniform(-1, 1), random.uniform(0.5, 1)] for _ in range(5)]

# Bullets
bullets = []

# Load spaceship texture
def load_texture(filename):
    texture = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture, "RGBA", 1)
    width, height = texture.get_size()
    
    texID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texID)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    
    return texID

ship_texture = load_texture("spaceship.png")
asteroid_texture = load_texture("asteroid.png")

# Draw spaceship
def draw_ship(x):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ship_texture)
    glBegin(GL_QUADS)
    
    glTexCoord2f(0, 0); glVertex2f(x - 0.1, -0.8)
    glTexCoord2f(1, 0); glVertex2f(x + 0.1, -0.8)
    glTexCoord2f(1, 1); glVertex2f(x + 0.1, -0.6)
    glTexCoord2f(0, 1); glVertex2f(x - 0.1, -0.6)
    
    glEnd()
    glDisable(GL_TEXTURE_2D)

# Draw asteroid
def draw_asteroid(x, y):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, asteroid_texture)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 0); glVertex2f(x - 0.05, y)
    glTexCoord2f(1, 0); glVertex2f(x + 0.05, y)
    glTexCoord2f(1, 1); glVertex2f(x + 0.05, y + 0.1)
    glTexCoord2f(0, 1); glVertex2f(x - 0.05, y + 0.1)

    glEnd()
    glDisable(GL_TEXTURE_2D)

# Draw bullet
def draw_bullet(x, y):
    glColor3f(1, 1, 1)  # White bullet (Removed red shooting effect)
    glBegin(GL_QUADS)
    glVertex2f(x - 0.01, y)
    glVertex2f(x + 0.01, y)
    glVertex2f(x + 0.01, y + 0.05)
    glVertex2f(x - 0.01, y + 0.05)
    glEnd()

# Display text
def draw_text(text, x, y):
    """ Render text using Pygame fonts and blit it as a texture """
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glWindowPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


# Show countdown before game starts
def countdown():
    for i in range(3, 0, -1):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_text(f"Game starts in: {i}", WIDTH // 2 - 50, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(1)

# Show controls before game starts
def show_controls():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_text("Controls:", WIDTH // 2 - 50, HEIGHT // 2 + 40)
    draw_text("Left Arrow: Move Left", WIDTH // 2 - 70, HEIGHT // 2)
    draw_text("Right Arrow: Move Right", WIDTH // 2 - 90, HEIGHT // 2 - 20)
    draw_text("Spacebar: Shoot", WIDTH // 2 - 50, HEIGHT // 2 - 40)
    draw_text("Press ENTER to start", WIDTH // 2 - 60, HEIGHT // 2 - 80)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                waiting = False

# Start game sequence
show_controls()
countdown()

# Main loop
running = True
while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                ship_x -= ship_speed
            if event.key == K_RIGHT:
                ship_x += ship_speed
            if event.key == K_SPACE:
                bullets.append([ship_x, -0.55])
                shoot_sound.play()

    # Draw spaceship
    draw_ship(ship_x)

    # Update and draw asteroids
    for asteroid in asteroids:
        asteroid[1] -= 0.01
        draw_asteroid(asteroid[0], asteroid[1])

        if asteroid[1] < -1:  # Reset asteroid position
            asteroid[0] = random.uniform(-1, 1)
            asteroid[1] = random.uniform(0.5, 1)

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet[1] += 0.05
        draw_bullet(bullet[0], bullet[1])

        # Collision detection
        for asteroid in asteroids:
            if asteroid[0] - 0.05 < bullet[0] < asteroid[0] + 0.05 and asteroid[1] < bullet[1] < asteroid[1] + 0.1:
                explosion_sound.play()
                bullets.remove(bullet)
                asteroid[0] = random.uniform(-1, 1)
                asteroid[1] = random.uniform(0.5, 1)
                score += 10  # Increase score

        if bullet[1] > 1:
            bullets.remove(bullet)

    # Display score
    draw_text(f"Score: {score}", 10, HEIGHT - 30)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
