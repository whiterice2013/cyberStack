class Laser:
    def __init__(self, x, y, dx, dy, fade_color, LASER_COLOR, pygame):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fade_color = fade_color
        self.LASER_COLOR = LASER_COLOR
        self.pygame = pygame

    def move(self, speed):
        self.x += self.dx * speed
        self.y += self.dy * speed

    def draw(self, surface):
        for i in range(1, 10):
            color = self.fade_color(self.LASER_COLOR, i * 25)
            self.pygame.draw.circle(
                surface,
                color,
                (int(self.x - self.dx * i * 5), int(self.y - self.dy * i * 5)),
                max(1, 5 - i // 2),
            )
        self.pygame.draw.circle(
            surface, self.LASER_COLOR, (int(self.x), int(self.y)), 5
        )
