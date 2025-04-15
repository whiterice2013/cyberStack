import pygame
import random

# Initialize pygame
pygame.init()

# Set up the screen
HIEGHT = 500
WIDTH = 500
screen = pygame.display.set_mode((WIDTH, HIEGHT))
pygame.display.set_caption("CyberStack")

# Colors
BASE_COLOR = (0, 255, 0)  # Green base
ENEMY_COLOR = (255, 0, 0)  # Red enemies

# Player base position
base_x, base_y = WIDTH/2-25, HIEGHT/2-25

# Enemy setup
enemies = []

# Create a few enemies
for i in range(5):
    enemy_x = random.randint(50, 450)
    enemy_y = random.randint(50, 150)
    enemies.append([enemy_x, enemy_y])

# Player coins
coins = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen
    screen.fill((200, 200, 200))

    for enemy in enemies:
            # Calculate the direction the enemy should move
            dx = WIDTH/2 - enemy[0] 
            dy = HIEGHT/2 - enemy[1]  

            # Normalize the direction (so enemies move at the same speed no matter the distance)
            distance = (dx**2 + dy**2)**0.5  # Pythagoras theorem to calculate the distance
            dx /= distance
            dy /= distance

            # Move the enemy a little towards the center
            enemy[0] += dx * 0.1  # Move 2 pixels per frame in the x direction
            enemy[1] += dy * 0.1  # Move 2 pixels per frame in the y direction

    # Draw the base
    pygame.draw.rect(screen, BASE_COLOR, (base_x, base_y, 50, 50))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, ENEMY_COLOR, (enemy[0], enemy[1]), 20)

    # Show the number of coins
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
