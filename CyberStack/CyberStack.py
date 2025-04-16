import pygame
import random
import math

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
base_x, base_y = WIDTH / 2 - 25, HIEGHT / 2 - 25

# Enemy setup
enemies = []

# Player coins
coins = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen
    screen.fill((0, 0, 0))

    if (
        pygame.time.get_ticks() % random.randint(1000, 8000) < 1
    ):  # Check if 5 seconds have passed (5000 ms)
        for _ in range(random.randint(1, 5)):
            if random.choice(
                [True, False]
            ):  # Randomly decide if the enemy spawns on the top/bottom or left/right
                enemy_x = random.choice([0, WIDTH])  # Left or right edge
                enemy_y = random.uniform(0, HIEGHT)  # Anywhere along the height
            else:
                enemy_x = random.uniform(0, WIDTH)  # Anywhere along the width
                enemy_y = random.choice([0, HIEGHT])  # Top or bottom edge
            enemies.append([enemy_x, enemy_y])

    for enemy in enemies:
        # Calculate the direction the enemy should move
        dx = WIDTH / 2 - enemy[0]
        dy = HIEGHT / 2 - enemy[1]

        # Normalize the direction (so enemies move at the same speed no matter the distance)
        distance = (
            dx**2 + dy**2
        ) ** 0.5  # Pythagoras theorem to calculate the distance
        dx /= distance
        dy /= distance

        # Move the enemy a little towards the center
        enemy[0] += dx * 1 / 100  # Move 2 pixels per frame in the x direction
        enemy[1] += dy * 1 / 100  # Move 2 pixels per frame in the y direction

    # Draw the base
    def draw_hexagon(surface, color, center, size, width=0):
        points = []
        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            x = center[0] + size * math.cos(rad)
            y = center[1] + size * math.sin(rad)
            points.append((x, y))
        pygame.draw.polygon(surface, color, points, width)

    for x in range(1, 25):  # less layers = cleaner
        glow_size = 30 + x * x/(x/2)
        fade = max(0, 255 - x * 50)  # reduce brightness
        color = (0, fade, 0)  # green glow
        draw_hexagon(screen, color, (base_x + 25, base_y + 30), glow_size, width=5)

    for x in range(1, 25):  # less layers = cleaner
        glow_size = 30 - x * x/(x/2)
        fade = max(0, 255 - x * 50)  # reduce brightness
        color = (0, fade, 0)  # green glow
        draw_hexagon(screen, color, (base_x + 25, base_y + 30), glow_size, width=5)

    draw_hexagon(screen, (0, 255, 0), (base_x + 25, base_y + 30), 30, width=5)

    # Draw enemies
    for enemy in enemies:
        for x in range(1, 5):
            glow_size = 10 + x * x/(x/2)
            fade = max(0, 255 - x * 50)  # reduce brightness
            color = (fade, 0, 0)  # red glow
            pygame.draw.circle(screen, color, (enemy[0], enemy[1]), glow_size, width=5)
        pygame.draw.circle(screen, ENEMY_COLOR, (enemy[0], enemy[1]), 10, 2)

    # Show the number of coins
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
