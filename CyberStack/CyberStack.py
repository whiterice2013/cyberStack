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


class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        for glow in range(1, 25):
            glow_size = 30 + glow * glow / (glow / 2)
            fade = max(0, 255 - glow * 50)
            color = (0, fade, 0)
            draw_hexagon(surface, color, (self.x, self.y), glow_size, width=5)
        for glow in range(1, 25):
            glow_size = 30 - glow * glow / (glow / 2)
            fade = max(0, 255 - glow * 50)
            color = (0, fade, 0)
            draw_hexagon(surface, color, (self.x, self.y), glow_size, width=5)
        draw_hexagon(surface, BASE_COLOR, (self.x, self.y), 30, width=5)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
        if dist > 35:
            self.x += dx
            self.y += dy

    def draw(self, surface):
        for glow in range(1, 5):
            glow_size = 10 + glow * glow / (glow / 2)
            fade = max(0, 255 - glow * 50)
            color = (fade, 0, 0)
            pygame.draw.circle(surface, color, (self.x, self.y), glow_size, width=5)
        pygame.draw.circle(surface, ENEMY_COLOR, (self.x, self.y), 10, 2)


class Laser:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def move(self, speed):
        self.x += self.dx * speed
        self.y += self.dy * speed

    def draw(self, surface):
        pygame.draw.circle(surface, LASER_COLOR, (int(self.x), int(self.y)), 5)


class Game:
    def __init__(self):
        self.base = Base(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.lasers = []
        self.coins = 0
        self.laser_timer = 0
        self.laser_shot_speed = 100
        self.laser_speed = 20
        self.wave = 1

    def spawn_enemies(self):
        for _ in range(random.randint(1, 3)):
            if random.choice([True, False]):
                x = random.choice([0, WIDTH])
                y = random.uniform(0, HEIGHT)
            else:
                x = random.uniform(0, WIDTH)
                y = random.choice([0, HEIGHT])
            self.enemies.append(Enemy(x, y))

    def fire_laser(self):
        if self.enemies:
            target = min(self.enemies, key=lambda e: math.hypot(e.x - self.base.x, e.y - self.base.y))
            dx = target.x - self.base.x
            dy = target.y - self.base.y
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx /= dist
                dy /= dist
            self.lasers.append(Laser(self.base.x, self.base.y, dx, dy))

    def update(self):
        # Spawn enemies
        if pygame.time.get_ticks() % random.randint(3000, 4000) / (self.wave / 3) < 20:
            self.spawn_enemies()

        # Increase difficulty
        if pygame.time.get_ticks() % 10000 < 20:
            self.wave += 1
            self.laser_speed += 2

        # Fire laser
        self.laser_timer += 1
        if self.laser_timer >= self.laser_shot_speed:
            self.laser_timer = 0
            self.fire_laser()

        # Update lasers
        for laser in self.lasers[:]:
            laser.move(self.laser_speed)
            for enemy in self.enemies:
                if math.hypot(enemy.x - laser.x, enemy.y - laser.y) < 10:
                    self.enemies.remove(enemy)
                    self.lasers.remove(laser)
                    self.coins += 1
                    break
            if not (0 <= laser.x <= WIDTH and 0 <= laser.y <= HEIGHT):
                self.lasers.remove(laser)

        # Move enemies
        for enemy in self.enemies:
            enemy.move_towards(self.base.x, self.base.y)

    def draw(self):
        screen.fill((0, 0, 0))
        self.base.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for laser in self.lasers:
            laser.draw(screen)
        text = font.render(f"Coins: {self.coins}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.update()


# Game loop
game = Game()
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    game.update()
    game.draw()

pygame.quit()
