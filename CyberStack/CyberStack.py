import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberStack")

# Colors
BASE_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
LASER_COLOR = (0, 255, 255)

# Game objects
base_x, base_y = WIDTH // 2, HEIGHT // 2
enemies = []
lasers = []
coins = 0

# Timers
laser_timer = 0
laser_shot_speed = 100
laser_speed = 20

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_hexagon(surface, color, center, size, width=0):
    points = []
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = center[0] + size * math.cos(rad)
        y = center[1] + size * math.sin(rad)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)

def spawn_enemies():
    for _ in range(random.randint(1, 3)):
        if random.choice([True, False]):
            x = random.choice([0, WIDTH])
            y = random.uniform(0, HEIGHT)
        else:
            x = random.uniform(0, WIDTH)
            y = random.choice([0, HEIGHT])
        enemies.append([x, y])

wave = 1


# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn enemies
    if pygame.time.get_ticks() % random.randint(2000, 3000)/wave < 20:
        spawn_enemies()

    # Fire laser
    laser_timer += 1
    if laser_timer >= laser_shot_speed and enemies:
        laser_timer = 0
        target = min(enemies, key=lambda e: math.hypot(e[0] - base_x, e[1] - base_y))
        dx = target[0] - base_x
        dy = target[1] - base_y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        lasers.append({"x": base_x, "y": base_y, "dx": dx, "dy": dy})

    # Update lasers
    for laser in lasers[:]:
        laser["x"] += laser["dx"] * laser_speed
        laser["y"] += laser["dy"] * laser_speed

        for enemy in enemies:
            if math.hypot(enemy[0] - laser["x"], enemy[1] - laser["y"]) < 10:
                enemies.remove(enemy)
                lasers.remove(laser)
                coins += 1
                break

        if not (0 <= laser["x"] <= WIDTH and 0 <= laser["y"] <= HEIGHT):
            lasers.remove(laser)

    # Move enemies
    for enemy in enemies:
        dx = base_x - enemy[0]
        dy = base_y - enemy[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        enemy[0] += dx
        enemy[1] += dy

    # Draw base
    for x in range(1, 25):
        glow_size = 30 + x * x / (x / 2)
        fade = max(0, 255 - x * 50)
        color = (0, fade, 0)
        draw_hexagon(screen, color, (base_x, base_y), glow_size, width=5)
    for x in range(1, 25):
        glow_size = 30 - x * x / (x / 2)
        fade = max(0, 255 - x * 50)
        color = (0, fade, 0)
        draw_hexagon(screen, color, (base_x, base_y), glow_size, width=5)
    draw_hexagon(screen, BASE_COLOR, (base_x, base_y), 30, width=5)

    # Draw enemies
    for enemy in enemies:
        for x in range(1, 5):
            glow_size = 10 + x * x / (x / 2)
            fade = max(0, 255 - x * 50)
            color = (fade, 0, 0)
            pygame.draw.circle(screen, color, (enemy[0], enemy[1]), glow_size, width=5)
        pygame.draw.circle(screen, ENEMY_COLOR, (enemy[0], enemy[1]), 10, 2)

    # Draw short laser as dot
    for laser in lasers:
        pygame.draw.circle(screen, LASER_COLOR, (int(laser["x"]), int(laser["y"])), 5)

    # Draw coins
    text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()
