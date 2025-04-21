import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberStack")

# Colors
BASE_COLOR = (167, 255, 153)
ENEMY_COLOR = (255, 153, 153)
LASER_COLOR = (153, 238, 255)
BUTTON_COLOR = (120, 120, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)

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

def fade_color(color, fade):
    return (max(0, color[0] - fade), max(0, color[1] - fade), max(0, color[2] - fade))

class Button:
    def __init__(self, rect, text, cost, level, effect, on_click):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.cost = cost
        self.level = level
        self.effect = effect
        self.on_click = on_click
        self.hover_time = 0
        self.hovered = False

    def update(self, mouse_pos, mouse_click, coins):
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.hover_time = time.time()
            self.hovered = True
            if mouse_click and coins >= self.cost:
                self.on_click()
        else:
            self.hovered = False
            self.hover_time = 0

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text = font.render(f"{self.text} Lv.{self.level}", True, (255, 255, 255))
        cost = font.render(f"Cost: {self.cost}", True, (255, 255, 0))
        effect = font.render(self.effect, True, (0, 255, 255))
        surface.blit(text, (self.rect.x + 5, self.rect.y + 5))
        surface.blit(cost, (self.rect.x + 5, self.rect.y + 35))
        surface.blit(effect, (self.rect.x + 5, self.rect.y + 65))
        if self.hovered and time.time() - self.hover_time > 1:
            tip = font.render("Click to upgrade!", True, (255, 255, 255))
            surface.blit(tip, (self.rect.x, self.rect.y - 30))

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        for glow in range(1, 25):
            glow_size = 30 + glow * glow / (glow / 2)
            color = fade_color(BASE_COLOR, glow * 50)
            draw_hexagon(surface, color, (self.x, self.y), glow_size, width=5)
        for glow in range(1, 25):
            glow_size = 30 - glow * glow / (glow / 2)
            color = fade_color(BASE_COLOR, glow * 50)
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
            color = fade_color(ENEMY_COLOR, glow * 50)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(glow_size), width=5)
        pygame.draw.circle(surface, ENEMY_COLOR, (int(self.x), int(self.y)), 10, 2)

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
        for i in range(1, 10):
            color = fade_color(LASER_COLOR, i * 25)
            pygame.draw.circle(surface, color, (int(self.x - self.dx * i * 5), int(self.y - self.dy * i * 5)), max(1, 5 - i // 2))
        pygame.draw.circle(surface, LASER_COLOR, (int(self.x), int(self.y)), 5)

class Game:
    def __init__(self):
        self.base = Base(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.lasers = []
        self.coins = 80
        self.laser_timer = 0
        self.laser_shot_speed = 50
        self.laser_speed = 20
        self.wave = 1
        self.pause_button_rect = pygame.Rect(WIDTH - 150, 20, 120, 40)
        self.paused = False
        self.buttons = [
            Button((10, 60, 200, 100), "Laser Speed", 10, 1, "+2 speed", self.upgrade_laser_speed),
            Button((10, 180, 200, 100), "Shot Rate", 15, 1, "-10 delay", self.upgrade_laser_rate)
        ]

    def upgrade_laser_speed(self):
        btn = self.buttons[0]
        if self.coins >= btn.cost:
            self.coins -= btn.cost
            self.laser_speed += 2
            btn.level += 1
            btn.cost += 10

    def upgrade_laser_rate(self):
        btn = self.buttons[1]
        if self.coins >= btn.cost:
            self.coins -= btn.cost
            self.laser_shot_speed = max(10, self.laser_shot_speed - 10)
            btn.level += 1
            btn.cost += 15

    def spawn_enemies(self):
        for _ in range(random.randint(1, 3)):
            x = random.choice([0, WIDTH]) if random.choice([True, False]) else random.uniform(0, WIDTH)
            y = random.choice([0, HEIGHT]) if not random.choice([True, False]) else random.uniform(0, HEIGHT)
            self.enemies.append(Enemy(x, y))

    def fire_laser(self):
        if self.enemies:
            target = min(self.enemies, key=lambda e: math.hypot(e.x - self.base.x, e.y - self.base.y))
            dx, dy = target.x - self.base.x, target.y - self.base.y
            dist = math.hypot(dx, dy)
            dx, dy = (dx / dist, dy / dist) if dist else (0, 0)
            self.lasers.append(Laser(self.base.x, self.base.y, dx, dy))

    def update(self):
        if pygame.time.get_ticks() % random.randint(3000, 4000) / (self.wave / 3) < 20:
            self.spawn_enemies()
        if pygame.time.get_ticks() % 10000 < 20:
            self.wave += 1
            self.laser_speed += 2
        self.laser_timer += 1
        if self.laser_timer >= self.laser_shot_speed:
            self.laser_timer = 0
            self.fire_laser()
        for laser in self.lasers[:]:
            laser.move(self.laser_speed)
            for enemy in self.enemies:
                if math.hypot(enemy.x - laser.x, enemy.y - laser.y) < 30:
                    self.enemies.remove(enemy)
                    self.lasers.remove(laser)
                    self.coins += 1
                    break
            if not (0 <= laser.x <= WIDTH and 0 <= laser.y <= HEIGHT):
                self.lasers.remove(laser)
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
        button_color = fade_color((100, 100, 100), 50 if self.paused else 0)
        pygame.draw.rect(screen, button_color, self.pause_button_rect)
        label = "Start" if self.paused else "Pause"
        btn_text = font.render(label, True, (255, 255, 255))
        screen.blit(btn_text, (self.pause_button_rect.x + 10, self.pause_button_rect.y + 5))
        if self.paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            pause_text = font.render("!Paused!", True, (255, 255, 0))
            screen.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 20))
        for btn in self.buttons:
            btn.draw(screen)
        pygame.display.update()

# Game loop
game = Game()
running = True
while running:
    clock.tick(60)
    mouse_click = False
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            if game.pause_button_rect.collidepoint(event.pos):
                game.paused = not game.paused
    for btn in game.buttons:
        btn.update(mouse_pos, mouse_click, game.coins)
    if not game.paused:
        game.update()
    game.draw()
pygame.quit()
