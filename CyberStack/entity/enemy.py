class Enemy:
    def __init__(self, x, y, enemy_type, fade_color, ENEMY_COLOR, pygame, math):
        self.x = x
        self.y = y
        self.fade_color = fade_color
        self.ENEMY_COLOR = ENEMY_COLOR
        self.pygame = pygame
        self.math = math
        self.type = enemy_type

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        speed = 0
        dist = self.math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        if dist > 35:
            if self.type == "fast":
                speed = 2
            elif self.type == "default":
                speed = 1
            if self.type == "curve":
                self.x += dx * 0.5
                self.y += dy * 3
            else:
                self.x += dx * speed
                self.y += dy * speed

    def draw(self, surface):
        for glow in range(1, 5):
            glow_size = 10 + glow * glow / (glow / 2)
            color = self.fade_color(self.ENEMY_COLOR, glow * 50)
            self.pygame.draw.circle(
                surface, color, (int(self.x), int(self.y)), int(glow_size), width=5
            )
        self.pygame.draw.circle(
            surface, self.ENEMY_COLOR, (int(self.x), int(self.y)), 10, 2
        )
