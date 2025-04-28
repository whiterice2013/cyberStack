from gui.button import Button
from game import Game
from entity.base import Base
from entity.enemy import Enemy
from entity.laser import Laser

from settings.game_settings import (
    BASE_COLOR,
    ENEMY_COLOR_PACK,
    LASER_COLOR,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    WIDTH,
    HEIGHT,
)

# CyberStack.py
import pygame
import random
import math
import time

pygame.init()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberStack")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)


def draw_hexagon(surface, color, center, size, width):
    points = []
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = center[0] + size * math.cos(rad)
        y = center[1] + size * math.sin(rad)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, width)


def fade_color(color, fade):
    return (max(0, color[0] - fade), max(0, color[1] - fade), max(0, color[2] - fade))


# Game loop

game = Game(
    Base(WIDTH // 2, HEIGHT // 2, fade_color, draw_hexagon, BASE_COLOR),
    pygame.Rect(WIDTH - 150, 20, 120, 40),
    pygame.Rect(WIDTH - 150, 70, 120, 40),
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    ENEMY_COLOR_PACK,
    LASER_COLOR,
    WIDTH,
    HEIGHT,
    font,
    screen,
    fade_color,
    Button,
    Enemy,
    Laser,
    random,
    pygame,
    time,
    math,
)


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
            elif game.shop_button_rect.collidepoint(event.pos):
                game.toggle_shop()

    for btn in game.buttons:
        btn.update(mouse_pos, mouse_click, game.coins)
    if not game.paused:
        game.update()
    game.draw()
pygame.quit()
